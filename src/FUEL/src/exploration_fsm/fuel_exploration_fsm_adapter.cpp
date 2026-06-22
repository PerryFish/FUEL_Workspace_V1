#include "fuel_ros2/exploration_fsm/fuel_exploration_fsm_adapter.hpp"

#include <cmath>
#include <sstream>

#include "geometry_msgs/msg/point.hpp"
#include "visualization_msgs/msg/marker.hpp"

namespace fuel_ros2
{

bool FuelExplorationFsmAdapter::initializeFromRos2Params(rclcpp::Node & node)
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

  enabled_ = get_bool("exploration_fsm.enable_exploration_fsm", enabled_);
  if (node.has_parameter("planner_backend") &&
    node.get_parameter("planner_backend").as_string() == "fuel_exploration_fsm")
  {
    enabled_ = true;
  }
  auto_start_ = get_bool("exploration_fsm.auto_start", auto_start_);
  use_fis_best_viewpoint_ = get_bool("exploration_fsm.use_fis_best_viewpoint", use_fis_best_viewpoint_);
  fallback_to_mvp_goal_ = get_bool("exploration_fsm.fallback_to_mvp_goal", fallback_to_mvp_goal_);
  goal_reached_distance_ = get_double("exploration_fsm.goal_reached_distance", goal_reached_distance_);
  execution_timeout_sec_ = get_double("exploration_fsm.execution_timeout_sec", execution_timeout_sec_);
  no_frontier_timeout_sec_ = get_double("exploration_fsm.no_frontier_timeout_sec", no_frontier_timeout_sec_);
  max_error_recovery_count_ = get_int("exploration_fsm.max_error_recovery_count", max_error_recovery_count_);
  publish_debug_markers_ = get_bool("exploration_fsm.publish_debug_markers", publish_debug_markers_);
  reset();
  return enabled_;
}

void FuelExplorationFsmAdapter::reset()
{
  state_ = FuelExplorationState::INIT;
  last_transition_reason_ = "reset";
  have_odom_ = false;
  have_plan_env_ = false;
  have_frontier_ = false;
  have_best_viewpoint_ = false;
  have_plan_ = false;
  active_goal_ = false;
  used_fis_best_viewpoint_ = false;
  used_fallback_ = false;
  error_recovery_count_ = 0;
  path_.poses.clear();
}

void FuelExplorationFsmAdapter::updateOdometry(const nav_msgs::msg::Odometry & odom_msg)
{
  last_odom_ = odom_msg;
  have_odom_ = true;
}

void FuelExplorationFsmAdapter::updatePlanEnvStatus(const std::string & status)
{
  plan_env_status_ = status;
  have_plan_env_ = status.find("PLAN_ENV") != std::string::npos;
}

void FuelExplorationFsmAdapter::updateFrontierFisStatus(const std::string & status)
{
  fis_status_ = status;
  have_frontier_ = status.find("FIS_BACKEND_PARTIAL") != std::string::npos ||
    status.find("FIS_BACKEND_RUNNING") != std::string::npos;
}

void FuelExplorationFsmAdapter::updateBestViewpoint(const geometry_msgs::msg::PoseStamped & viewpoint)
{
  best_viewpoint_ = viewpoint;
  have_best_viewpoint_ = true;
}

void FuelExplorationFsmAdapter::setFallbackGoal(const geometry_msgs::msg::PoseStamped & goal)
{
  fallback_goal_ = goal;
}

void FuelExplorationFsmAdapter::tick(const rclcpp::Time & now)
{
  if (state_enter_time_.nanoseconds() == 0) {
    state_enter_time_ = now;
  }

  switch (state_) {
    case FuelExplorationState::INIT:
      if (have_odom_) {
        transit(FuelExplorationState::WAIT_TRIGGER, "ODOM_READY", now);
      }
      break;
    case FuelExplorationState::WAIT_TRIGGER:
      if (auto_start_) {
        transit(FuelExplorationState::UPDATE_MAP, "auto_start", now);
      }
      break;
    case FuelExplorationState::UPDATE_MAP:
      if (have_plan_env_) {
        transit(FuelExplorationState::FIND_FRONTIER, "MAP_READY", now);
      }
      break;
    case FuelExplorationState::FIND_FRONTIER:
      if (have_frontier_) {
        transit(FuelExplorationState::SELECT_VIEWPOINT, "FRONTIER_READY", now);
      } else if (stateDuration(now) > no_frontier_timeout_sec_) {
        transit(FuelExplorationState::ERROR_RECOVERY, "NO_FRONTIER", now);
      }
      break;
    case FuelExplorationState::SELECT_VIEWPOINT:
      if (use_fis_best_viewpoint_ && have_best_viewpoint_) {
        active_goal_msg_ = best_viewpoint_;
        active_goal_ = true;
        have_plan_ = false;
        used_fis_best_viewpoint_ = true;
        std::ostringstream ss;
        ss << "FSM_GOAL_SELECTED source=fis x=" << active_goal_msg_.pose.position.x
           << " y=" << active_goal_msg_.pose.position.y
           << " z=" << active_goal_msg_.pose.position.z
           << " yaw=0 utility=partial";
        last_goal_log_ = ss.str();
        transit(FuelExplorationState::PLAN_PATH, "VIEWPOINT_READY", now);
      } else if (fallback_to_mvp_goal_) {
        active_goal_msg_ = fallback_goal_;
        active_goal_ = true;
        have_plan_ = false;
        used_fallback_ = true;
        last_fallback_log_ = "FSM_FALLBACK reason=no_fis_viewpoint fallback_backend=mvp";
        std::ostringstream ss;
        ss << "FSM_GOAL_SELECTED source=fallback x=" << active_goal_msg_.pose.position.x
           << " y=" << active_goal_msg_.pose.position.y
           << " z=" << active_goal_msg_.pose.position.z
           << " yaw=0 utility=0";
        last_goal_log_ = ss.str();
        transit(FuelExplorationState::PLAN_PATH, "FIS_NO_FRONTIER_FALLBACK_MVP", now);
      } else {
        transit(FuelExplorationState::ERROR_RECOVERY, "ERROR", now);
      }
      break;
    case FuelExplorationState::PLAN_PATH:
      if ((have_plan_ && !path_.poses.empty()) || planSimplePath(now)) {
        transit(FuelExplorationState::PUBLISH_TRAJECTORY, "PLAN_READY", now);
      } else {
        transit(FuelExplorationState::ERROR_RECOVERY, "plan_failed", now);
      }
      break;
    case FuelExplorationState::PUBLISH_TRAJECTORY:
      transit(FuelExplorationState::EXECUTE_TRAJECTORY, "TRAJECTORY_PUBLISHED", now);
      break;
    case FuelExplorationState::EXECUTE_TRAJECTORY:
      if (goalReached()) {
        transit(FuelExplorationState::UPDATE_MAP, "goal_reached", now);
      } else if (stateDuration(now) > execution_timeout_sec_) {
        last_fallback_log_ = "FSM_TIMEOUT state=EXECUTE_TRAJECTORY duration=" +
          std::to_string(stateDuration(now)) + " action=ERROR_RECOVERY";
        transit(FuelExplorationState::ERROR_RECOVERY, "EXECUTION_TIMEOUT", now);
      }
      break;
    case FuelExplorationState::ERROR_RECOVERY:
      ++error_recovery_count_;
      used_fallback_ = true;
      last_fallback_log_ = "FSM_FALLBACK reason=ERROR_RECOVERY fallback_backend=mvp";
      if (error_recovery_count_ > max_error_recovery_count_) {
        transit(FuelExplorationState::FINISH, "max_recovery", now);
      } else {
        active_goal_msg_ = fallback_goal_;
        active_goal_ = true;
        have_plan_ = false;
        transit(FuelExplorationState::PLAN_PATH, "FSM_ERROR_FALLBACK_MVP", now);
      }
      break;
    case FuelExplorationState::FINISH:
      break;
  }
}

FuelExplorationState FuelExplorationFsmAdapter::currentState() const {return state_;}
std::string FuelExplorationFsmAdapter::currentStateString() const {return stateToString(state_);}
std::string FuelExplorationFsmAdapter::lastTransitionReason() const {return last_transition_reason_;}
std::string FuelExplorationFsmAdapter::lastTransitionLog() const {return last_transition_log_;}
std::string FuelExplorationFsmAdapter::lastGoalLog() const {return last_goal_log_;}
std::string FuelExplorationFsmAdapter::lastFallbackLog() const {return last_fallback_log_;}
std::string FuelExplorationFsmAdapter::lastPathSourceLog() const {return last_path_source_log_;}
bool FuelExplorationFsmAdapter::hasActiveGoal() const {return active_goal_;}
geometry_msgs::msg::PoseStamped FuelExplorationFsmAdapter::currentGoal() const {return active_goal_msg_;}
bool FuelExplorationFsmAdapter::usedFisBestViewpoint() const {return used_fis_best_viewpoint_;}
bool FuelExplorationFsmAdapter::usedFallback() const {return used_fallback_;}

void FuelExplorationFsmAdapter::setExternalPath(const nav_msgs::msg::Path & path, const std::string & source)
{
  if (path.poses.empty()) {
    return;
  }
  path_ = path;
  have_plan_ = true;
  last_path_source_log_ = "FSM_PATH_SOURCE source=" + source + " points=" +
    std::to_string(path_.poses.size());
}

nav_msgs::msg::Path FuelExplorationFsmAdapter::exportFsmPath(
  const std::string & frame_id, const rclcpp::Time & stamp) const
{
  nav_msgs::msg::Path path = path_;
  path.header.frame_id = frame_id;
  path.header.stamp = stamp;
  return path;
}

visualization_msgs::msg::MarkerArray FuelExplorationFsmAdapter::exportFsmDebugMarkers(
  const std::string & frame_id, const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  if (!publish_debug_markers_) {
    return array;
  }
  visualization_msgs::msg::Marker goal;
  goal.header.frame_id = frame_id;
  goal.header.stamp = stamp;
  goal.ns = "fuel_fsm_goal";
  goal.id = 1;
  goal.type = visualization_msgs::msg::Marker::SPHERE;
  goal.action = visualization_msgs::msg::Marker::ADD;
  goal.pose = active_goal_msg_.pose;
  goal.scale.x = 0.65;
  goal.scale.y = 0.65;
  goal.scale.z = 0.65;
  goal.color.r = 1.0f;
  goal.color.g = 0.1f;
  goal.color.b = 0.8f;
  goal.color.a = active_goal_ ? 1.0f : 0.2f;
  array.markers.push_back(goal);
  return array;
}

std_msgs::msg::String FuelExplorationFsmAdapter::exportStatusMsg() const
{
  std_msgs::msg::String msg;
    msg.data = "FSM_BACKEND_PARTIAL state=" + currentStateString() +
    " active_goal=" + std::string(active_goal_ ? "true" : "false") +
    " used_fis=" + std::string(used_fis_best_viewpoint_ ? "true" : "false") +
    " fallback=" + std::string(used_fallback_ ? "true" : "false") +
    " transition=\"" + last_transition_log_ + "\"" +
    " goal=\"" + last_goal_log_ + "\"" +
    " fallback_log=\"" + last_fallback_log_ + "\"";
  return msg;
}

std::string FuelExplorationFsmAdapter::stateToString(FuelExplorationState state)
{
  switch (state) {
    case FuelExplorationState::INIT: return "INIT";
    case FuelExplorationState::WAIT_TRIGGER: return "WAIT_TRIGGER";
    case FuelExplorationState::UPDATE_MAP: return "UPDATE_MAP";
    case FuelExplorationState::FIND_FRONTIER: return "FIND_FRONTIER";
    case FuelExplorationState::SELECT_VIEWPOINT: return "SELECT_VIEWPOINT";
    case FuelExplorationState::PLAN_PATH: return "PLAN_PATH";
    case FuelExplorationState::PUBLISH_TRAJECTORY: return "PUBLISH_TRAJECTORY";
    case FuelExplorationState::EXECUTE_TRAJECTORY: return "EXECUTE_TRAJECTORY";
    case FuelExplorationState::FINISH: return "FINISH";
    case FuelExplorationState::ERROR_RECOVERY: return "ERROR_RECOVERY";
  }
  return "UNKNOWN";
}

void FuelExplorationFsmAdapter::transit(
  FuelExplorationState next, const std::string & reason, const rclcpp::Time & now)
{
  if (state_ == next) {
    return;
  }
  const auto old = state_;
  state_ = next;
  state_enter_time_ = now;
  last_transition_reason_ = reason;
  last_transition_log_ = "FSM_TRANSITION from=" + stateToString(old) +
    " to=" + stateToString(next) + " reason=" + reason +
    " time=" + std::to_string(now.seconds());
}

bool FuelExplorationFsmAdapter::planSimplePath(const rclcpp::Time & now)
{
  if (!have_odom_ || !active_goal_) {
    return false;
  }
  path_.header = active_goal_msg_.header;
  path_.header.stamp = now;
  path_.poses.clear();
  geometry_msgs::msg::PoseStamped start;
  start.header = path_.header;
  start.pose = last_odom_.pose.pose;
  path_.poses.push_back(start);
  for (int i = 1; i <= 10; ++i) {
    const double r = static_cast<double>(i) / 10.0;
    geometry_msgs::msg::PoseStamped pose;
    pose.header = path_.header;
    pose.pose.position.x = start.pose.position.x + (active_goal_msg_.pose.position.x - start.pose.position.x) * r;
    pose.pose.position.y = start.pose.position.y + (active_goal_msg_.pose.position.y - start.pose.position.y) * r;
    pose.pose.position.z = start.pose.position.z + (active_goal_msg_.pose.position.z - start.pose.position.z) * r;
    pose.pose.orientation = active_goal_msg_.pose.orientation;
    path_.poses.push_back(pose);
  }
  have_plan_ = true;
  last_path_source_log_ = "FSM_PATH_SOURCE source=straight_line points=" + std::to_string(path_.poses.size());
  return true;
}

bool FuelExplorationFsmAdapter::goalReached() const
{
  if (!have_odom_ || !active_goal_) {
    return false;
  }
  const auto & p = last_odom_.pose.pose.position;
  const auto & g = active_goal_msg_.pose.position;
  const double dx = p.x - g.x;
  const double dy = p.y - g.y;
  const double dz = p.z - g.z;
  return std::sqrt(dx * dx + dy * dy + dz * dz) < goal_reached_distance_;
}

double FuelExplorationFsmAdapter::stateDuration(const rclcpp::Time & now) const
{
  return (now - state_enter_time_).seconds();
}

}  // namespace fuel_ros2
