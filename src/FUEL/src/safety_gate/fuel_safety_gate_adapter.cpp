#include "fuel_ros2/safety_gate/fuel_safety_gate_adapter.hpp"

#include <algorithm>
#include <cmath>
#include <sstream>

#include "visualization_msgs/msg/marker.hpp"

namespace fuel_ros2
{

bool FuelSafetyGateAdapter::initializeFromRos2Params(const rclcpp::Node::SharedPtr & node)
{
  return node ? initializeFromRos2Params(*node) : false;
}

bool FuelSafetyGateAdapter::initializeFromRos2Params(rclcpp::Node & node)
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
  auto get_string = [&node](const std::string & name, const std::string & fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<std::string>(name, fallback);
      }
      return node.get_parameter(name).as_string();
    };

  enabled_ = get_bool("safety_gate.enable_safety_gate", enabled_);
  output_filter_enabled_ = get_bool("safety_gate.enable_output_filter", output_filter_enabled_);
  input_trajectory_topic_ =
    get_string("safety_gate.input_trajectory_topic", input_trajectory_topic_);
  output_safe_trajectory_topic_ =
    get_string("safety_gate.output_safe_trajectory_topic", output_safe_trajectory_topic_);
  min_obstacle_distance_ =
    std::max(0.0, get_double("safety_gate.min_obstacle_distance", min_obstacle_distance_));
  min_z_ = get_double("safety_gate.min_z", min_z_);
  max_z_ = get_double("safety_gate.max_z", max_z_);
  if (max_z_ < min_z_) {
    std::swap(min_z_, max_z_);
  }
  max_speed_ = std::max(0.1, get_double("safety_gate.max_speed", max_speed_));
  max_acceleration_ =
    std::max(0.1, get_double("safety_gate.max_acceleration", max_acceleration_));
  max_trajectory_age_sec_ =
    std::max(0.0, get_double("safety_gate.max_trajectory_age_sec", max_trajectory_age_sec_));
  allow_hold_position_ =
    get_bool("safety_gate.allow_hold_position", allow_hold_position_);
  allow_emergency_stop_ =
    get_bool("safety_gate.allow_emergency_stop", allow_emergency_stop_);
  assumed_sample_dt_ = std::max(0.05, get_double("safety_gate.assumed_sample_dt", assumed_sample_dt_));
  reset();
  return enabled_;
}

void FuelSafetyGateAdapter::reset()
{
  have_trajectory_ = false;
  have_odom_ = false;
  input_trajectory_ = nav_msgs::msg::Path();
  safe_trajectory_ = nav_msgs::msg::Path();
  status_ = FuelSafetyGateStatus::IDLE;
  report_ = FuelTrajectorySafetyReport();
}

void FuelSafetyGateAdapter::updatePlanEnv(const FuelPlanEnvAdapter * plan_env)
{
  plan_env_ = plan_env;
}

void FuelSafetyGateAdapter::updateInputTrajectory(const nav_msgs::msg::Path & trajectory)
{
  input_trajectory_ = trajectory;
  have_trajectory_ = true;
}

void FuelSafetyGateAdapter::updateOdom(const nav_msgs::msg::Odometry & odom)
{
  last_odom_ = odom;
  have_odom_ = true;
}

double FuelSafetyGateAdapter::distance3d(
  const geometry_msgs::msg::Point & a,
  const geometry_msgs::msg::Point & b)
{
  return std::hypot(std::hypot(a.x - b.x, a.y - b.y), a.z - b.z);
}

double FuelSafetyGateAdapter::pathLength(const nav_msgs::msg::Path & path)
{
  double length = 0.0;
  for (std::size_t i = 1; i < path.poses.size(); ++i) {
    length += distance3d(path.poses[i - 1].pose.position, path.poses[i].pose.position);
  }
  return length;
}

double FuelSafetyGateAdapter::stampAgeSec(const builtin_interfaces::msg::Time & stamp)
{
  if (stamp.sec == 0 && stamp.nanosec == 0) {
    return 1.0e9;
  }
  rclcpp::Clock clock(RCL_SYSTEM_TIME);
  return std::max(0.0, (clock.now() - rclcpp::Time(stamp, RCL_SYSTEM_TIME)).seconds());
}

void FuelSafetyGateAdapter::setDecision(
  FuelSafetyGateStatus status,
  const std::string & decision,
  const std::string & reason)
{
  status_ = status;
  report_.decision = decision;
  report_.reason = reason;
}

bool FuelSafetyGateAdapter::estimateDynamics()
{
  report_.max_speed_estimate = 0.0;
  report_.max_acc_estimate = 0.0;
  if (input_trajectory_.poses.size() < 2) {
    report_.speed_limit_ok = true;
    report_.acceleration_limit_ok = true;
    return true;
  }

  double previous_speed = 0.0;
  bool have_previous_speed = false;
  for (std::size_t i = 1; i < input_trajectory_.poses.size(); ++i) {
    const double distance =
      distance3d(input_trajectory_.poses[i - 1].pose.position, input_trajectory_.poses[i].pose.position);
    const double speed = distance / assumed_sample_dt_;
    report_.max_speed_estimate = std::max(report_.max_speed_estimate, speed);
    if (have_previous_speed) {
      const double acceleration = std::abs(speed - previous_speed) / assumed_sample_dt_;
      report_.max_acc_estimate = std::max(report_.max_acc_estimate, acceleration);
    }
    previous_speed = speed;
    have_previous_speed = true;
  }

  report_.speed_limit_ok = report_.max_speed_estimate <= max_speed_;
  report_.acceleration_limit_ok = report_.max_acc_estimate <= max_acceleration_;
  return report_.speed_limit_ok && report_.acceleration_limit_ok;
}

bool FuelSafetyGateAdapter::evaluate()
{
  status_ = FuelSafetyGateStatus::CHECKING;
  report_ = FuelTrajectorySafetyReport();
  safe_trajectory_ = nav_msgs::msg::Path();
  report_.collision_free = true;
  report_.min_distance_ok = true;
  report_.within_map_bounds = true;
  report_.min_obstacle_distance = min_obstacle_distance_;

  if (!enabled_) {
    if (have_trajectory_) {
      safe_trajectory_ = input_trajectory_;
    }
    report_.valid = have_trajectory_ && !input_trajectory_.poses.empty();
    setDecision(FuelSafetyGateStatus::PASS, "PASS_DISABLED_DEBUG_ONLY", "safety_gate_disabled");
    return report_.valid;
  }
  if (!have_trajectory_ || input_trajectory_.poses.empty()) {
    safe_trajectory_ = nav_msgs::msg::Path();
    if (have_odom_ && allow_hold_position_) {
      setDecision(FuelSafetyGateStatus::HOLD_POSITION, "HOLD_POSITION", "empty_trajectory");
    } else if (allow_emergency_stop_) {
      setDecision(FuelSafetyGateStatus::EMERGENCY_STOP, "EMERGENCY_STOP", "empty_trajectory");
    } else {
      setDecision(FuelSafetyGateStatus::BLOCK_TRAJECTORY, "BLOCK_TRAJECTORY", "empty_trajectory");
    }
    return false;
  }

  report_.non_empty = true;
  report_.frame_ok = input_trajectory_.header.frame_id == "map" ||
    input_trajectory_.header.frame_id == "odom" ||
    input_trajectory_.header.frame_id.empty();
  report_.timestamp_ok = stampAgeSec(input_trajectory_.header.stamp) <= max_trajectory_age_sec_;
  if (!report_.frame_ok) {
    setDecision(FuelSafetyGateStatus::BLOCK_TRAJECTORY, "BLOCK_TRAJECTORY", "invalid_frame");
    return false;
  }
  if (!report_.timestamp_ok) {
    setDecision(FuelSafetyGateStatus::WARN, "WARN", "stale_trajectory");
  }

  report_.z_range_ok = true;
  for (const auto & pose : input_trajectory_.poses) {
    const double z = pose.pose.position.z;
    if (z < min_z_ || z > max_z_) {
      report_.z_range_ok = false;
      setDecision(FuelSafetyGateStatus::BLOCK_TRAJECTORY, "BLOCK_TRAJECTORY", "z_range_violation");
      return false;
    }
  }

  if (!estimateDynamics()) {
    setDecision(FuelSafetyGateStatus::WARN, "WARN", "dynamic_limit_violation");
    safe_trajectory_ = input_trajectory_;
    return false;
  }

  safe_trajectory_ = input_trajectory_;
  report_.valid = true;
  setDecision(
    report_.timestamp_ok ? FuelSafetyGateStatus::PASS : FuelSafetyGateStatus::WARN,
    report_.timestamp_ok ? "PASS" : "WARN",
    report_.timestamp_ok ? "trajectory_passed_debug_gate" : "stale_trajectory");
  (void)pathLength(input_trajectory_);
  (void)plan_env_;
  return report_.timestamp_ok;
}

FuelSafetyGateStatus FuelSafetyGateAdapter::status() const
{
  return status_;
}

std::string FuelSafetyGateAdapter::statusString() const
{
  switch (status_) {
    case FuelSafetyGateStatus::IDLE:
      return "IDLE";
    case FuelSafetyGateStatus::CHECKING:
      return "CHECKING";
    case FuelSafetyGateStatus::PASS:
      return "PASS";
    case FuelSafetyGateStatus::WARN:
      return "WARN";
    case FuelSafetyGateStatus::BLOCK_TRAJECTORY:
      return "BLOCK_TRAJECTORY";
    case FuelSafetyGateStatus::EMERGENCY_STOP:
      return "EMERGENCY_STOP";
    case FuelSafetyGateStatus::HOLD_POSITION:
      return "HOLD_POSITION";
    case FuelSafetyGateStatus::FALLBACK_TO_SAFE_OUTPUT:
      return "FALLBACK_TO_SAFE_OUTPUT";
  }
  return "UNKNOWN";
}

FuelTrajectorySafetyReport FuelSafetyGateAdapter::currentReport() const
{
  return report_;
}

nav_msgs::msg::Path FuelSafetyGateAdapter::exportSafeTrajectoryMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  auto path = safe_trajectory_;
  path.header.frame_id = frame_id;
  path.header.stamp = stamp;
  for (auto & pose : path.poses) {
    pose.header = path.header;
  }
  return path;
}

std_msgs::msg::String FuelSafetyGateAdapter::exportSafetyReportMsg() const
{
  std::ostringstream out;
  out << "{\"status\":\"" << statusString()
    << "\",\"valid\":" << (report_.valid ? "true" : "false")
    << ",\"non_empty\":" << (report_.non_empty ? "true" : "false")
    << ",\"frame_ok\":" << (report_.frame_ok ? "true" : "false")
    << ",\"timestamp_ok\":" << (report_.timestamp_ok ? "true" : "false")
    << ",\"z_range_ok\":" << (report_.z_range_ok ? "true" : "false")
    << ",\"speed_limit_ok\":" << (report_.speed_limit_ok ? "true" : "false")
    << ",\"acceleration_limit_ok\":" << (report_.acceleration_limit_ok ? "true" : "false")
    << ",\"max_speed_estimate\":" << report_.max_speed_estimate
    << ",\"max_acc_estimate\":" << report_.max_acc_estimate
    << ",\"decision\":\"" << report_.decision
    << "\",\"reason\":\"" << report_.reason
    << "\",\"real_flight_command\":false}";
  std_msgs::msg::String msg;
  msg.data = out.str();
  return msg;
}

std_msgs::msg::Bool FuelSafetyGateAdapter::exportEmergencyStopMsg() const
{
  std_msgs::msg::Bool msg;
  msg.data = status_ == FuelSafetyGateStatus::EMERGENCY_STOP;
  return msg;
}

geometry_msgs::msg::PoseStamped FuelSafetyGateAdapter::exportHoldPositionMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  geometry_msgs::msg::PoseStamped pose;
  pose.header.frame_id = frame_id;
  pose.header.stamp = stamp;
  pose.pose.orientation.w = 1.0;
  if (have_odom_) {
    pose.pose = last_odom_.pose.pose;
  }
  return pose;
}

visualization_msgs::msg::MarkerArray FuelSafetyGateAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray markers;
  visualization_msgs::msg::Marker marker;
  marker.header.frame_id = frame_id;
  marker.header.stamp = stamp;
  marker.ns = "fuel_safety_gate";
  marker.id = 1;
  marker.type = visualization_msgs::msg::Marker::SPHERE_LIST;
  marker.action = visualization_msgs::msg::Marker::ADD;
  marker.scale.x = 0.18;
  marker.scale.y = 0.18;
  marker.scale.z = 0.18;
  marker.color.a = 0.9f;
  marker.color.g = status_ == FuelSafetyGateStatus::PASS ? 1.0f : 0.2f;
  marker.color.r = status_ == FuelSafetyGateStatus::PASS ? 0.1f : 1.0f;
  marker.color.b = status_ == FuelSafetyGateStatus::WARN ? 0.8f : 0.1f;
  for (const auto & pose : safe_trajectory_.poses) {
    marker.points.push_back(pose.pose.position);
  }
  markers.markers.push_back(marker);
  return markers;
}

bool FuelSafetyGateAdapter::enabled() const
{
  return enabled_;
}

bool FuelSafetyGateAdapter::outputFilterEnabled() const
{
  return output_filter_enabled_;
}

std::string FuelSafetyGateAdapter::inputTrajectoryTopic() const
{
  return input_trajectory_topic_;
}

std::string FuelSafetyGateAdapter::outputSafeTrajectoryTopic() const
{
  return output_safe_trajectory_topic_;
}

}  // namespace fuel_ros2
