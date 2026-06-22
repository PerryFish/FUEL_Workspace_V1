#include "fuel_ros2/plan_manager/fuel_plan_manager_adapter.hpp"

#include <algorithm>
#include <cmath>
#include <sstream>

#include "geometry_msgs/msg/point.hpp"
#include "visualization_msgs/msg/marker.hpp"

namespace fuel_ros2
{

bool FuelPlanManagerAdapter::initializeFromRos2Params(const rclcpp::Node::SharedPtr & node)
{
  return node ? initializeFromRos2Params(*node) : false;
}

bool FuelPlanManagerAdapter::initializeFromRos2Params(rclcpp::Node & node)
{
  auto get_bool = [&node](const std::string & name, bool fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<bool>(name, fallback);
      }
      return node.get_parameter(name).as_bool();
    };
  auto get_int = [&node](const std::string & name, int fallback) -> int {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<int>(name, fallback);
      }
      return static_cast<int>(node.get_parameter(name).as_int());
    };
  auto get_double = [&node](const std::string & name, double fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<double>(name, fallback);
      }
      return node.get_parameter(name).as_double();
    };
  auto get_string = [&node](const std::string & name, const std::string & fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<std::string>(name, fallback);
      }
      return node.get_parameter(name).as_string();
    };

  enabled_ = get_bool("plan_manager.enable_plan_manager", enabled_);
  if (node.has_parameter("planner_backend") &&
    node.get_parameter("planner_backend").as_string() == "fuel_plan_manager")
  {
    enabled_ = true;
  }
  use_managed_output_ = get_bool("plan_manager.use_managed_output", use_managed_output_);
  prefer_bspline_when_valid_ =
    get_bool("plan_manager.prefer_bspline_when_valid", prefer_bspline_when_valid_);
  require_collision_checked_ =
    get_bool("plan_manager.require_collision_checked", require_collision_checked_);
  require_dynamic_checked_ =
    get_bool("plan_manager.require_dynamic_checked", require_dynamic_checked_);
  min_path_points_ = std::max(2, get_int("plan_manager.min_path_points", min_path_points_));
  min_trajectory_points_ =
    std::max(2, get_int("plan_manager.min_trajectory_points", min_trajectory_points_));
  max_allowed_fallback_count_ =
    std::max(0, get_int("plan_manager.max_allowed_fallback_count", max_allowed_fallback_count_));
  publish_contract_debug_ =
    get_bool("plan_manager.publish_contract_debug", publish_contract_debug_);
  debug_publish_rate_ = std::max(0.1, get_double("plan_manager.debug_publish_rate", debug_publish_rate_));
  output_contract_topic_ =
    get_string("plan_manager.output_contract_topic", output_contract_topic_);
  reset();
  return enabled_;
}

void FuelPlanManagerAdapter::reset()
{
  status_ = FuelPlanManagerStatus::IDLE;
  contract_ = FuelTrajectoryContract{};
  path_searching_path_ = nav_msgs::msg::Path{};
  path_searching_status_.clear();
  bspline_candidate_ = nav_msgs::msg::Path{};
  bspline_status_.clear();
}

void FuelPlanManagerAdapter::updatePipelineInputs(
  const nav_msgs::msg::Odometry & odom,
  const geometry_msgs::msg::PoseStamped & current_goal)
{
  odom_ = odom;
  current_goal_ = current_goal;
  have_goal_ = current_goal.header.frame_id.size() > 0 ||
    std::isfinite(current_goal.pose.position.x);
}

void FuelPlanManagerAdapter::updatePathSearchingResult(
  const nav_msgs::msg::Path & path,
  const std::string & status)
{
  path_searching_path_ = path;
  path_searching_status_ = status;
}

void FuelPlanManagerAdapter::updateBsplineCandidate(
  const nav_msgs::msg::Path & sampled_traj,
  const std::string & status)
{
  bspline_candidate_ = sampled_traj;
  bspline_status_ = status;
}

bool FuelPlanManagerAdapter::evaluateAndSelectFinalContract()
{
  ++evaluation_count_;
  status_ = FuelPlanManagerStatus::RUNNING;
  contract_ = FuelTrajectoryContract{};

  const bool path_ok = isPathUsable(path_searching_path_) &&
    path_searching_status_.find("FAILED") == std::string::npos;
  const bool bspline_ok = isBsplineUsable();

  if (prefer_bspline_when_valid_ && bspline_ok) {
    contract_.source = use_managed_output_ ? "managed_output" : "bspline_candidate";
    contract_.valid = true;
    contract_.collision_checked = !require_collision_checked_ ||
      bspline_status_.find("SUCCESS") != std::string::npos;
    contract_.dynamic_checked = bspline_status_.find("SUCCESS") != std::string::npos;
    contract_.safe_for_stable_output = use_managed_output_ &&
      contract_.collision_checked &&
      (!require_dynamic_checked_ || contract_.dynamic_checked);
    contract_.path_msg = path_searching_path_;
    contract_.trajectory_msg = bspline_candidate_;
    contract_.path_points = static_cast<int>(path_searching_path_.poses.size());
    contract_.trajectory_points = static_cast<int>(bspline_candidate_.poses.size());
    contract_.path_length = pathLength(bspline_candidate_);
    contract_.estimated_duration = contract_.path_length / 1.0;
    status_ = use_managed_output_ ?
      FuelPlanManagerStatus::SUCCESS_MANAGED_OUTPUT :
      FuelPlanManagerStatus::SUCCESS_BSPLINE_CANDIDATE;
    return true;
  }

  if (path_ok) {
    contract_.source = "path_searching";
    contract_.valid = true;
    contract_.collision_checked = path_searching_status_.find("SUCCESS") != std::string::npos;
    contract_.dynamic_checked = false;
    contract_.safe_for_stable_output = false;
    contract_.path_msg = path_searching_path_;
    contract_.trajectory_msg = path_searching_path_;
    contract_.path_points = static_cast<int>(path_searching_path_.poses.size());
    contract_.trajectory_points = static_cast<int>(path_searching_path_.poses.size());
    contract_.path_length = pathLength(path_searching_path_);
    contract_.estimated_duration = contract_.path_length / 1.0;
    if (!bspline_candidate_.poses.empty() &&
      bspline_status_.find("SUCCESS") == std::string::npos)
    {
      contract_.fallback_reason = "bspline_candidate_unreliable";
      ++fallback_count_;
      status_ = FuelPlanManagerStatus::FALLBACK_TO_PATH_SEARCHING;
    } else {
      status_ = FuelPlanManagerStatus::SUCCESS_PATH_ONLY;
    }
    return true;
  }

  contract_.source = "mvp";
  contract_.valid = false;
  contract_.fallback_reason = "no_valid_path_or_trajectory";
  ++fallback_count_;
  status_ = FuelPlanManagerStatus::FALLBACK_TO_MVP;
  return true;
}

FuelPlanManagerStatus FuelPlanManagerAdapter::status() const {return status_;}
std::string FuelPlanManagerAdapter::statusString() const {return statusToString(status_);}
FuelTrajectoryContract FuelPlanManagerAdapter::currentContract() const {return contract_;}
bool FuelPlanManagerAdapter::useManagedOutput() const {return use_managed_output_;}
int FuelPlanManagerAdapter::evaluationCount() const {return evaluation_count_;}
int FuelPlanManagerAdapter::fallbackCount() const {return fallback_count_;}

std::string FuelPlanManagerAdapter::backendStatusString() const
{
  switch (status_) {
    case FuelPlanManagerStatus::SUCCESS_PATH_ONLY:
      return "PLAN_MANAGER_CONTRACT_PATH_ONLY";
    case FuelPlanManagerStatus::SUCCESS_BSPLINE_CANDIDATE:
      return "PLAN_MANAGER_CONTRACT_BSPLINE_CANDIDATE";
    case FuelPlanManagerStatus::SUCCESS_MANAGED_OUTPUT:
      return "PLAN_MANAGER_OUTPUT_GUARDED";
    case FuelPlanManagerStatus::FALLBACK_TO_PATH_SEARCHING:
      return "PLAN_MANAGER_FALLBACK_PATH_SEARCHING";
    case FuelPlanManagerStatus::FALLBACK_TO_MVP:
      return "PLAN_MANAGER_FALLBACK_MVP";
    case FuelPlanManagerStatus::RUNNING:
      return "PLAN_MANAGER_BACKEND_RUNNING";
    default:
      return enabled_ ? "PLAN_MANAGER_BACKEND_PARTIAL" : "PLAN_MANAGER_BACKEND_RUNNING";
  }
}

nav_msgs::msg::Path FuelPlanManagerAdapter::exportManagedPathMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  return stampedCopy(contract_.path_msg, frame_id, stamp);
}

nav_msgs::msg::Path FuelPlanManagerAdapter::exportManagedTrajectoryMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  return stampedCopy(contract_.trajectory_msg, frame_id, stamp);
}

visualization_msgs::msg::MarkerArray FuelPlanManagerAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  visualization_msgs::msg::Marker line;
  line.header.frame_id = frame_id;
  line.header.stamp = stamp;
  line.ns = "fuel_plan_manager_managed_trajectory";
  line.id = 0;
  line.type = visualization_msgs::msg::Marker::LINE_STRIP;
  line.action = visualization_msgs::msg::Marker::ADD;
  line.scale.x = 0.08;
  line.color.r = 0.1f;
  line.color.g = 0.45f;
  line.color.b = 1.0f;
  line.color.a = 1.0f;
  for (const auto & pose : contract_.trajectory_msg.poses) {
    geometry_msgs::msg::Point p;
    p.x = pose.pose.position.x;
    p.y = pose.pose.position.y;
    p.z = pose.pose.position.z;
    line.points.push_back(p);
  }
  array.markers.push_back(line);
  return array;
}

std_msgs::msg::String FuelPlanManagerAdapter::exportStatusMsg() const
{
  std_msgs::msg::String msg;
  std::ostringstream ss;
  ss << backendStatusString()
     << " status=" << statusString()
     << " source=" << contract_.source
     << " valid=" << (contract_.valid ? "true" : "false")
     << " safe=" << (contract_.safe_for_stable_output ? "true" : "false")
     << " path_points=" << contract_.path_points
     << " trajectory_points=" << contract_.trajectory_points
     << " length=" << contract_.path_length
     << " evaluations=" << evaluation_count_
     << " fallback=" << fallback_count_
     << " reason=" << contract_.fallback_reason;
  msg.data = ss.str();
  return msg;
}

std_msgs::msg::String FuelPlanManagerAdapter::exportContractMsg() const
{
  std_msgs::msg::String msg;
  std::ostringstream ss;
  ss << "{"
     << "\"source\":\"" << contract_.source << "\","
     << "\"valid\":" << (contract_.valid ? "true" : "false") << ","
     << "\"collision_checked\":" << (contract_.collision_checked ? "true" : "false") << ","
     << "\"dynamic_checked\":" << (contract_.dynamic_checked ? "true" : "false") << ","
     << "\"safe_for_stable_output\":" << (contract_.safe_for_stable_output ? "true" : "false") << ","
     << "\"path_points\":" << contract_.path_points << ","
     << "\"trajectory_points\":" << contract_.trajectory_points << ","
     << "\"path_length\":" << contract_.path_length << ","
     << "\"estimated_duration\":" << contract_.estimated_duration << ","
     << "\"fallback_reason\":\"" << contract_.fallback_reason << "\""
     << "}";
  msg.data = ss.str();
  return msg;
}

double FuelPlanManagerAdapter::pathLength(const nav_msgs::msg::Path & path)
{
  double length = 0.0;
  for (std::size_t i = 1; i < path.poses.size(); ++i) {
    const auto & a = path.poses[i - 1].pose.position;
    const auto & b = path.poses[i].pose.position;
    const double dx = b.x - a.x;
    const double dy = b.y - a.y;
    const double dz = b.z - a.z;
    length += std::sqrt(dx * dx + dy * dy + dz * dz);
  }
  return length;
}

bool FuelPlanManagerAdapter::hasZVariation(const nav_msgs::msg::Path & path)
{
  if (path.poses.size() < 2) {
    return false;
  }
  const double z0 = path.poses.front().pose.position.z;
  for (const auto & pose : path.poses) {
    if (std::abs(pose.pose.position.z - z0) > 1e-3) {
      return true;
    }
  }
  return false;
}

bool FuelPlanManagerAdapter::isPathUsable(const nav_msgs::msg::Path & path) const
{
  return static_cast<int>(path.poses.size()) >= min_path_points_ && pathLength(path) > 1e-6;
}

bool FuelPlanManagerAdapter::isBsplineUsable() const
{
  if (bspline_status_.find("SUCCESS") == std::string::npos) {
    return false;
  }
  if (static_cast<int>(bspline_candidate_.poses.size()) < min_trajectory_points_) {
    return false;
  }
  if (pathLength(bspline_candidate_) <= 1e-6) {
    return false;
  }
  return hasZVariation(bspline_candidate_);
}

nav_msgs::msg::Path FuelPlanManagerAdapter::stampedCopy(
  const nav_msgs::msg::Path & input,
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  nav_msgs::msg::Path out = input;
  out.header.frame_id = frame_id;
  out.header.stamp = stamp;
  for (auto & pose : out.poses) {
    pose.header = out.header;
  }
  return out;
}

std::string FuelPlanManagerAdapter::statusToString(FuelPlanManagerStatus status)
{
  switch (status) {
    case FuelPlanManagerStatus::IDLE: return "IDLE";
    case FuelPlanManagerStatus::RUNNING: return "RUNNING";
    case FuelPlanManagerStatus::SUCCESS_PATH_ONLY: return "SUCCESS_PATH_ONLY";
    case FuelPlanManagerStatus::SUCCESS_BSPLINE_CANDIDATE: return "SUCCESS_BSPLINE_CANDIDATE";
    case FuelPlanManagerStatus::SUCCESS_MANAGED_OUTPUT: return "SUCCESS_MANAGED_OUTPUT";
    case FuelPlanManagerStatus::FALLBACK_TO_PATH_SEARCHING: return "FALLBACK_TO_PATH_SEARCHING";
    case FuelPlanManagerStatus::FALLBACK_TO_MVP: return "FALLBACK_TO_MVP";
    case FuelPlanManagerStatus::FAILED_NO_GOAL: return "FAILED_NO_GOAL";
    case FuelPlanManagerStatus::FAILED_NO_PATH: return "FAILED_NO_PATH";
    case FuelPlanManagerStatus::FAILED_TRAJECTORY_INVALID: return "FAILED_TRAJECTORY_INVALID";
    case FuelPlanManagerStatus::ERROR_RECOVERY: return "ERROR_RECOVERY";
  }
  return "UNKNOWN";
}

}  // namespace fuel_ros2
