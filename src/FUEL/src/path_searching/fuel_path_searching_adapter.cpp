#include "fuel_ros2/path_searching/fuel_path_searching_adapter.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <limits>
#include <sstream>

#include "geometry_msgs/msg/point.hpp"
#include "visualization_msgs/msg/marker.hpp"

#include "fuel_ros2/plan_env/fuel_plan_env_adapter.hpp"

namespace fuel_ros2
{

bool FuelPathSearchingAdapter::initializeFromRos2Params(const rclcpp::Node::SharedPtr & node)
{
  return node ? initializeFromRos2Params(*node) : false;
}

bool FuelPathSearchingAdapter::initializeFromRos2Params(rclcpp::Node & node)
{
  auto get_bool = [&node](const std::string & name, bool fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<bool>(name, fallback);
      }
      return node.get_parameter(name).as_bool();
    };
  auto get_double = [&node](const std::string & name, double fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<double>(name, fallback);
      }
      return node.get_parameter(name).as_double();
    };
  auto get_int = [&node](const std::string & name, int fallback) -> int {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<int>(name, fallback);
      }
      return static_cast<int>(node.get_parameter(name).as_int());
    };
  auto get_string = [&node](const std::string & name, const std::string & fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<std::string>(name, fallback);
      }
      return node.get_parameter(name).as_string();
    };

  enabled_ = get_bool("path_searching.enable_path_searching", enabled_);
  if (node.has_parameter("planner_backend") &&
    node.get_parameter("planner_backend").as_string() == "fuel_path_searching")
  {
    enabled_ = true;
  }
  use_path_searching_in_fsm_ =
    get_bool("path_searching.use_path_searching_in_fsm", use_path_searching_in_fsm_);
  algorithm_ = get_string("path_searching.algorithm", algorithm_);
  config_.resolution = get_double("path_searching.grid_resolution", config_.resolution);
  config_.neighbor_mode = get_int("path_searching.neighbor_mode", config_.neighbor_mode);
  config_.max_search_nodes = get_int("path_searching.max_search_nodes", config_.max_search_nodes);
  safety_distance_ = get_double("path_searching.safety_distance", safety_distance_);
  allow_unknown_ = get_bool("path_searching.allow_unknown", allow_unknown_);
  allow_straight_line_fallback_ =
    get_bool("path_searching.allow_straight_line_fallback", allow_straight_line_fallback_);
  config_.simplify_path = get_bool("path_searching.simplify_path", config_.simplify_path);
  config_.simplify_line_of_sight =
    get_bool("path_searching.simplify_line_of_sight", config_.simplify_line_of_sight);
  config_.min.x() = get_double("map.min_x", config_.min.x());
  config_.min.y() = get_double("map.min_y", config_.min.y());
  config_.min.z() = get_double("map.min_z", config_.min.z());
  config_.max.x() = get_double("map.max_x", config_.max.x());
  config_.max.y() = get_double("map.max_y", config_.max.y());
  config_.max.z() = get_double("map.max_z", config_.max.z());

  if (algorithm_ != "grid_astar_3d") {
    algorithm_ = "grid_astar_3d";
  }
  if (safety_distance_ < 0.0) {
    safety_distance_ = 0.0;
  }
  astar_.configure(config_);
  reset();
  return enabled_;
}

void FuelPathSearchingAdapter::reset()
{
  status_ = FuelPathSearchStatus::IDLE;
  last_failure_reason_ = "none";
  path_.clear();
  visited_.clear();
  last_duration_ms_ = 0.0;
  last_path_length_ = 0.0;
}

bool FuelPathSearchingAdapter::setPlanEnv(const FuelPlanEnvAdapter * plan_env)
{
  plan_env_ = plan_env;
  return plan_env_ != nullptr;
}

bool FuelPathSearchingAdapter::searchPath(
  const Eigen::Vector3d & start,
  const Eigen::Vector3d & goal)
{
  ++search_count_;
  path_.clear();
  visited_.clear();
  last_path_length_ = 0.0;
  status_ = FuelPathSearchStatus::SEARCHING;

  const auto start_time = std::chrono::steady_clock::now();
  auto finish_timing = [this, &start_time]() {
      const auto end_time = std::chrono::steady_clock::now();
      last_duration_ms_ =
        std::chrono::duration<double, std::milli>(end_time - start_time).count();
    };

  if (!plan_env_) {
    status_ = FuelPathSearchStatus::FAILED_NO_MAP;
    last_failure_reason_ = "no_plan_env";
    ++failure_count_;
    finish_timing();
    return false;
  }
  if (!plan_env_->isInsideMap(start)) {
    status_ = FuelPathSearchStatus::FAILED_INVALID_START;
    last_failure_reason_ = "start_outside_map";
    ++failure_count_;
    finish_timing();
    return false;
  }
  if (!plan_env_->isInsideMap(goal)) {
    status_ = FuelPathSearchStatus::FAILED_INVALID_GOAL;
    last_failure_reason_ = "goal_outside_map";
    ++failure_count_;
    finish_timing();
    return false;
  }
  if (plan_env_->isOccupied(start)) {
    status_ = FuelPathSearchStatus::FAILED_OCCUPIED_START;
    last_failure_reason_ = "start_occupied";
    ++failure_count_;
    finish_timing();
    return false;
  }
  if (plan_env_->isOccupied(goal)) {
    status_ = FuelPathSearchStatus::FAILED_OCCUPIED_GOAL;
    last_failure_reason_ = "goal_occupied";
    ++failure_count_;
    finish_timing();
    return false;
  }

  const auto result = astar_.search(start, goal, [this](const Eigen::Vector3d & p) {
      return isTraversable(p);
    });
  visited_ = result.visited;
  finish_timing();

  if (result.success) {
    status_ = FuelPathSearchStatus::SUCCESS;
    path_ = result.path;
    last_path_length_ = result.path_length;
    last_failure_reason_ = "none";
    ++success_count_;
    return true;
  }

  status_ = FuelPathSearchStatus::FAILED_NO_PATH;
  last_failure_reason_ = result.reason;
  ++failure_count_;
  if (allow_straight_line_fallback_ && makeStraightLineFallback(start, goal)) {
    status_ = FuelPathSearchStatus::FALLBACK_STRAIGHT_LINE;
    ++fallback_count_;
    return false;
  }
  return false;
}

std::vector<Eigen::Vector3d> FuelPathSearchingAdapter::getPath() const
{
  return path_;
}

std::vector<Eigen::Vector3d> FuelPathSearchingAdapter::getVisitedNodes() const
{
  return visited_;
}

FuelPathSearchStatus FuelPathSearchingAdapter::status() const
{
  return status_;
}

std::string FuelPathSearchingAdapter::statusString() const
{
  return statusToString(status_);
}

std::string FuelPathSearchingAdapter::backendStatusString() const
{
  if (status_ == FuelPathSearchStatus::SUCCESS) {
    return "PATH_SEARCHING_SUCCESS";
  }
  if (status_ == FuelPathSearchStatus::FALLBACK_STRAIGHT_LINE) {
    return "PATH_SEARCHING_FAILED_STRAIGHT_LINE";
  }
  if (status_ == FuelPathSearchStatus::FAILED_NO_PATH ||
    status_ == FuelPathSearchStatus::FAILED_NO_MAP ||
    status_ == FuelPathSearchStatus::FAILED_INVALID_START ||
    status_ == FuelPathSearchStatus::FAILED_INVALID_GOAL ||
    status_ == FuelPathSearchStatus::FAILED_OCCUPIED_START ||
    status_ == FuelPathSearchStatus::FAILED_OCCUPIED_GOAL)
  {
    return "PATH_SEARCHING_FAILED_FALLBACK_MVP";
  }
  return "PATH_SEARCHING_BACKEND_PARTIAL";
}

std::string FuelPathSearchingAdapter::lastFailureReason() const {return last_failure_reason_;}
double FuelPathSearchingAdapter::lastDurationMs() const {return last_duration_ms_;}
double FuelPathSearchingAdapter::lastPathLength() const {return last_path_length_;}
double FuelPathSearchingAdapter::gridResolution() const {return config_.resolution;}
int FuelPathSearchingAdapter::searchCount() const {return search_count_;}
int FuelPathSearchingAdapter::successCount() const {return success_count_;}
int FuelPathSearchingAdapter::failureCount() const {return failure_count_;}
int FuelPathSearchingAdapter::fallbackCount() const {return fallback_count_;}

nav_msgs::msg::Path FuelPathSearchingAdapter::exportPathMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  nav_msgs::msg::Path msg;
  msg.header.frame_id = frame_id;
  msg.header.stamp = stamp;
  for (const auto & p : path_) {
    geometry_msgs::msg::PoseStamped pose;
    pose.header = msg.header;
    pose.pose.position.x = p.x();
    pose.pose.position.y = p.y();
    pose.pose.position.z = p.z();
    pose.pose.orientation.w = 1.0;
    msg.poses.push_back(pose);
  }
  return msg;
}

visualization_msgs::msg::MarkerArray FuelPathSearchingAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array = exportVisitedNodes(frame_id, stamp);
  visualization_msgs::msg::Marker line;
  line.header.frame_id = frame_id;
  line.header.stamp = stamp;
  line.ns = "fuel_path_searching_path";
  line.id = 1;
  line.type = visualization_msgs::msg::Marker::LINE_STRIP;
  line.action = visualization_msgs::msg::Marker::ADD;
  line.scale.x = 0.08;
  line.color.r = status_ == FuelPathSearchStatus::SUCCESS ? 0.0f : 1.0f;
  line.color.g = status_ == FuelPathSearchStatus::SUCCESS ? 0.9f : 0.45f;
  line.color.b = 0.2f;
  line.color.a = 1.0f;
  for (const auto & p : path_) {
    geometry_msgs::msg::Point point;
    point.x = p.x();
    point.y = p.y();
    point.z = p.z();
    line.points.push_back(point);
  }
  array.markers.push_back(line);
  return array;
}

visualization_msgs::msg::MarkerArray FuelPathSearchingAdapter::exportVisitedNodes(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  visualization_msgs::msg::Marker visited;
  visited.header.frame_id = frame_id;
  visited.header.stamp = stamp;
  visited.ns = "fuel_path_searching_visited";
  visited.id = 0;
  visited.type = visualization_msgs::msg::Marker::CUBE_LIST;
  visited.action = visualization_msgs::msg::Marker::ADD;
  visited.scale.x = config_.resolution;
  visited.scale.y = config_.resolution;
  visited.scale.z = config_.resolution;
  visited.color.r = 0.1f;
  visited.color.g = 0.35f;
  visited.color.b = 1.0f;
  visited.color.a = 0.25f;
  const std::size_t max_points = std::min<std::size_t>(visited_.size(), 2000);
  for (std::size_t i = 0; i < max_points; ++i) {
    geometry_msgs::msg::Point point;
    point.x = visited_[i].x();
    point.y = visited_[i].y();
    point.z = visited_[i].z();
    visited.points.push_back(point);
  }
  array.markers.push_back(visited);
  return array;
}

std_msgs::msg::String FuelPathSearchingAdapter::exportStatusMsg() const
{
  std_msgs::msg::String msg;
  std::ostringstream ss;
  ss << backendStatusString()
     << " status=" << statusString()
     << " algorithm=" << algorithm_
     << " searches=" << search_count_
     << " success=" << success_count_
     << " failures=" << failure_count_
     << " fallback=" << fallback_count_
     << " points=" << path_.size()
     << " visited=" << visited_.size()
     << " length=" << last_path_length_
     << " duration_ms=" << last_duration_ms_
     << " reason=" << last_failure_reason_;
  msg.data = ss.str();
  return msg;
}

bool FuelPathSearchingAdapter::isTraversable(const Eigen::Vector3d & p) const
{
  if (!plan_env_ || !plan_env_->isInsideMap(p)) {
    return false;
  }
  if (plan_env_->isOccupied(p)) {
    return false;
  }
  const double distance = plan_env_->getDistance(p);
  if (!std::isfinite(distance)) {
    return allow_unknown_;
  }
  return distance >= safety_distance_;
}

bool FuelPathSearchingAdapter::makeStraightLineFallback(
  const Eigen::Vector3d & start,
  const Eigen::Vector3d & goal)
{
  path_.clear();
  constexpr int kSegments = 10;
  for (int i = 0; i <= kSegments; ++i) {
    const double r = static_cast<double>(i) / static_cast<double>(kSegments);
    path_.push_back(start + (goal - start) * r);
  }
  last_path_length_ = (goal - start).norm();
  return true;
}

std::string FuelPathSearchingAdapter::statusToString(FuelPathSearchStatus status)
{
  switch (status) {
    case FuelPathSearchStatus::IDLE: return "IDLE";
    case FuelPathSearchStatus::SEARCHING: return "SEARCHING";
    case FuelPathSearchStatus::SUCCESS: return "SUCCESS";
    case FuelPathSearchStatus::FAILED_NO_MAP: return "FAILED_NO_MAP";
    case FuelPathSearchStatus::FAILED_INVALID_START: return "FAILED_INVALID_START";
    case FuelPathSearchStatus::FAILED_INVALID_GOAL: return "FAILED_INVALID_GOAL";
    case FuelPathSearchStatus::FAILED_OCCUPIED_START: return "FAILED_OCCUPIED_START";
    case FuelPathSearchStatus::FAILED_OCCUPIED_GOAL: return "FAILED_OCCUPIED_GOAL";
    case FuelPathSearchStatus::FAILED_NO_PATH: return "FAILED_NO_PATH";
    case FuelPathSearchStatus::FALLBACK_STRAIGHT_LINE: return "FALLBACK_STRAIGHT_LINE";
  }
  return "UNKNOWN";
}

}  // namespace fuel_ros2
