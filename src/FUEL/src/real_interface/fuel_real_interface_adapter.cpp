#include "fuel_ros2/real_interface/fuel_real_interface_adapter.hpp"

#include <algorithm>
#include <cmath>
#include <sstream>

#include "geometry_msgs/msg/point.hpp"
#include "visualization_msgs/msg/marker.hpp"

namespace fuel_ros2
{

bool FuelRealInterfaceAdapter::initializeFromRos2Params(const rclcpp::Node::SharedPtr & node)
{
  return node ? initializeFromRos2Params(*node) : false;
}

bool FuelRealInterfaceAdapter::initializeFromRos2Params(rclcpp::Node & node)
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

  enabled_ = get_bool("real_interface.enable_real_interface_mode", enabled_);
  global_frame_ = get_string("real_interface.frames.global_frame", global_frame_);
  odom_frame_ = get_string("real_interface.frames.odom_frame", odom_frame_);
  base_frame_ = get_string("real_interface.frames.base_frame", base_frame_);
  sensor_frame_ = get_string("real_interface.frames.sensor_frame", sensor_frame_);
  odom_topic_ = get_string("real_interface.input_topics.odom", odom_topic_);
  map_cloud_topic_ = get_string("real_interface.input_topics.map_cloud", map_cloud_topic_);
  local_cloud_topic_ = get_string("real_interface.input_topics.local_cloud", local_cloud_topic_);
  occupied_cloud_topic_ = get_string("real_interface.input_topics.occupied_cloud", occupied_cloud_topic_);
  free_cloud_topic_ = get_string("real_interface.input_topics.free_cloud", free_cloud_topic_);
  control_bridge_enabled_ =
    get_bool("real_interface.control_bridge.enable_control_bridge", control_bridge_enabled_);
  preferred_control_interface_ =
    get_string("real_interface.control_bridge.preferred_control_interface", preferred_control_interface_);
  control_publish_rate_ =
    std::max(0.1, get_double("real_interface.control_bridge.publish_rate", control_publish_rate_));
  min_odom_hz_ = std::max(0.0, get_double("real_interface.validation.min_odom_hz", min_odom_hz_));
  min_map_hz_ = std::max(0.0, get_double("real_interface.validation.min_map_hz", min_map_hz_));
  max_odom_age_sec_ =
    std::max(0.0, get_double("real_interface.validation.max_odom_age_sec", max_odom_age_sec_));
  max_map_age_sec_ =
    std::max(0.0, get_double("real_interface.validation.max_map_age_sec", max_map_age_sec_));
  require_tf_map_to_base_ =
    get_bool("real_interface.validation.require_tf_map_to_base", require_tf_map_to_base_);
  require_non_empty_map_ =
    get_bool("real_interface.validation.require_non_empty_map", require_non_empty_map_);
  require_non_empty_path_ =
    get_bool("real_interface.validation.require_non_empty_path", require_non_empty_path_);
  require_non_empty_trajectory_ =
    get_bool("real_interface.validation.require_non_empty_trajectory", require_non_empty_trajectory_);
  robot_mode_ = get_string("real_interface.mode.robot_mode", robot_mode_);
  allow_land_mode_ = get_bool("real_interface.mode.allow_land_mode", allow_land_mode_);
  allow_air_mode_ = get_bool("real_interface.mode.allow_air_mode", allow_air_mode_);
  land_fixed_z_ = get_double("real_interface.mode.land_fixed_z", land_fixed_z_);
  air_min_z_ = get_double("real_interface.mode.air_min_z", air_min_z_);
  air_max_z_ = get_double("real_interface.mode.air_max_z", air_max_z_);
  if (robot_mode_ != "land" && robot_mode_ != "air") {
    robot_mode_ = "air";
  }
  if (robot_mode_ == "land" && !allow_land_mode_) {
    robot_mode_ = "air";
  }
  if (robot_mode_ == "air" && !allow_air_mode_) {
    robot_mode_ = "land";
  }
  reset();
  return enabled_;
}

void FuelRealInterfaceAdapter::reset()
{
  have_odom_ = false;
  have_map_ = false;
  have_outputs_ = false;
  odom_count_ = 0;
  map_count_ = 0;
  last_contract_.clear();
}

void FuelRealInterfaceAdapter::updateOdom(const nav_msgs::msg::Odometry & odom_msg)
{
  last_odom_ = odom_msg;
  have_odom_ = true;
  ++odom_count_;
  const rclcpp::Time stamp(odom_msg.header.stamp, RCL_SYSTEM_TIME);
  if (odom_count_ == 1) {
    first_odom_time_ = stamp;
  }
  last_odom_time_ = stamp;
}

void FuelRealInterfaceAdapter::updateMapCloud(const sensor_msgs::msg::PointCloud2 & cloud_msg)
{
  last_map_ = cloud_msg;
  have_map_ = true;
  ++map_count_;
  const rclcpp::Time stamp(cloud_msg.header.stamp, RCL_SYSTEM_TIME);
  if (map_count_ == 1) {
    first_map_time_ = stamp;
  }
  last_map_time_ = stamp;
}

void FuelRealInterfaceAdapter::updatePlannerOutputs(
  const geometry_msgs::msg::PoseStamped & waypoint,
  const nav_msgs::msg::Path & global_path,
  const nav_msgs::msg::Path & local_trajectory,
  const std::string & trajectory_contract)
{
  last_waypoint_ = waypoint;
  last_global_path_ = global_path;
  last_local_trajectory_ = local_trajectory;
  last_contract_ = trajectory_contract;
  have_outputs_ = true;
}

double FuelRealInterfaceAdapter::stampAgeSec(const builtin_interfaces::msg::Time & stamp)
{
  if (stamp.sec == 0 && stamp.nanosec == 0) {
    return 1.0e9;
  }
  rclcpp::Clock clock(RCL_SYSTEM_TIME);
  return std::max(0.0, (clock.now() - rclcpp::Time(stamp, RCL_SYSTEM_TIME)).seconds());
}

double FuelRealInterfaceAdapter::measuredHz(
  const rclcpp::Time & first, const rclcpp::Time & last, int count) const
{
  if (count < 2) {
    return 0.0;
  }
  const double duration = (last - first).seconds();
  if (duration <= 1.0e-6) {
    return 0.0;
  }
  return static_cast<double>(count - 1) / duration;
}

bool FuelRealInterfaceAdapter::frameAcceptable(const std::string & frame_id) const
{
  return frame_id == global_frame_ || frame_id == odom_frame_;
}

bool FuelRealInterfaceAdapter::inputsHealthy() const
{
  if (!enabled_) {
    return true;
  }
  if (!have_odom_ || !have_map_) {
    return false;
  }
  if (!frameAcceptable(last_odom_.header.frame_id) || !frameAcceptable(last_map_.header.frame_id)) {
    return false;
  }
  if (!last_odom_.child_frame_id.empty() && last_odom_.child_frame_id != base_frame_) {
    return false;
  }
  if (stampAgeSec(last_odom_.header.stamp) > max_odom_age_sec_) {
    return false;
  }
  if (stampAgeSec(last_map_.header.stamp) > max_map_age_sec_) {
    return false;
  }
  if (require_non_empty_map_ && last_map_.width * last_map_.height == 0) {
    return false;
  }
  if (odom_count_ >= 4 && measuredHz(first_odom_time_, last_odom_time_, odom_count_) < min_odom_hz_) {
    return false;
  }
  if (map_count_ >= 3 && measuredHz(first_map_time_, last_map_time_, map_count_) < min_map_hz_) {
    return false;
  }
  return true;
}

bool FuelRealInterfaceAdapter::outputsHealthy() const
{
  if (!enabled_) {
    return true;
  }
  if (!have_outputs_) {
    return false;
  }
  if (require_non_empty_path_ && last_global_path_.poses.empty()) {
    return false;
  }
  if (require_non_empty_trajectory_ && last_local_trajectory_.poses.empty()) {
    return false;
  }
  return true;
}

double FuelRealInterfaceAdapter::pathLength(const nav_msgs::msg::Path & path)
{
  double length = 0.0;
  for (std::size_t i = 1; i < path.poses.size(); ++i) {
    const auto & a = path.poses[i - 1].pose.position;
    const auto & b = path.poses[i].pose.position;
    length += std::hypot(std::hypot(b.x - a.x, b.y - a.y), b.z - a.z);
  }
  return length;
}

std::string FuelRealInterfaceAdapter::inputStatusString() const
{
  std::ostringstream out;
  out << "REAL_INTERFACE_INPUTS"
    << " enabled=" << (enabled_ ? "true" : "false")
    << " healthy=" << (inputsHealthy() ? "true" : "false")
    << " odom_received=" << (have_odom_ ? "true" : "false")
    << " map_received=" << (have_map_ ? "true" : "false")
    << " odom_topic=" << odom_topic_
    << " map_topic=" << map_cloud_topic_
    << " odom_frame=" << (have_odom_ ? last_odom_.header.frame_id : "NONE")
    << " map_frame=" << (have_map_ ? last_map_.header.frame_id : "NONE")
    << " odom_age_sec=" << (have_odom_ ? stampAgeSec(last_odom_.header.stamp) : -1.0)
    << " map_age_sec=" << (have_map_ ? stampAgeSec(last_map_.header.stamp) : -1.0)
    << " odom_hz=" << measuredHz(first_odom_time_, last_odom_time_, odom_count_)
    << " map_hz=" << measuredHz(first_map_time_, last_map_time_, map_count_)
    << " map_points=" << (have_map_ ? last_map_.width * last_map_.height : 0);
  if (require_tf_map_to_base_) {
    out << " tf_required=true tf_check=not_implemented_partial";
  }
  return out.str();
}

std::string FuelRealInterfaceAdapter::outputStatusString() const
{
  std::ostringstream out;
  out << "REAL_INTERFACE_OUTPUTS"
    << " enabled=" << (enabled_ ? "true" : "false")
    << " healthy=" << (outputsHealthy() ? "true" : "false")
    << " waypoint_received=" << (have_outputs_ ? "true" : "false")
    << " global_path_points=" << last_global_path_.poses.size()
    << " local_trajectory_points=" << last_local_trajectory_.poses.size()
    << " global_path_length=" << pathLength(last_global_path_)
    << " local_trajectory_length=" << pathLength(last_local_trajectory_)
    << " contract_available=" << (!last_contract_.empty() ? "true" : "false");
  return out.str();
}

std_msgs::msg::String FuelRealInterfaceAdapter::exportStatusMsg() const
{
  std_msgs::msg::String msg;
  msg.data = "REAL_INTERFACE_STATUS enabled=" + std::string(enabled_ ? "true" : "false") +
    " inputs_healthy=" + std::string(inputsHealthy() ? "true" : "false") +
    " outputs_healthy=" + std::string(outputsHealthy() ? "true" : "false") +
    " mode=" + robot_mode_ +
    " ready_for_onboard_flight=false";
  return msg;
}

std_msgs::msg::String FuelRealInterfaceAdapter::exportInputStatusMsg() const
{
  std_msgs::msg::String msg;
  msg.data = inputStatusString();
  return msg;
}

std_msgs::msg::String FuelRealInterfaceAdapter::exportOutputStatusMsg() const
{
  std_msgs::msg::String msg;
  msg.data = outputStatusString();
  return msg;
}

std_msgs::msg::String FuelRealInterfaceAdapter::exportControlBridgeStatusMsg() const
{
  std_msgs::msg::String msg;
  msg.data = "CONTROL_BRIDGE_CONFIG enabled=" + std::string(control_bridge_enabled_ ? "true" : "false") +
    " preferred_interface=" + preferred_control_interface_ +
    " publish_rate=" + std::to_string(control_publish_rate_) +
    " real_flight_command=false";
  return msg;
}

std_msgs::msg::String FuelRealInterfaceAdapter::exportModeManagerStatusMsg() const
{
  std_msgs::msg::String msg;
  msg.data = "MODE_MANAGER_STATUS mode=" + robot_mode_ +
    " allow_land=" + std::string(allow_land_mode_ ? "true" : "false") +
    " allow_air=" + std::string(allow_air_mode_ ? "true" : "false") +
    " land_fixed_z=" + std::to_string(land_fixed_z_) +
    " air_min_z=" + std::to_string(air_min_z_) +
    " air_max_z=" + std::to_string(air_max_z_) +
    " z_policy=" + (robot_mode_ == "land" ? std::string("land_fixed_z_constraint_partial") :
    std::string("air_3d_z_variation_allowed"));
  return msg;
}

visualization_msgs::msg::MarkerArray FuelRealInterfaceAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  visualization_msgs::msg::Marker marker;
  marker.header.frame_id = frame_id;
  marker.header.stamp = stamp;
  marker.ns = "fuel_real_interface";
  marker.id = 1;
  marker.type = visualization_msgs::msg::Marker::SPHERE;
  marker.action = visualization_msgs::msg::Marker::ADD;
  marker.pose.position = have_odom_ ? last_odom_.pose.pose.position : geometry_msgs::msg::Point{};
  marker.pose.orientation.w = 1.0;
  marker.scale.x = 0.25;
  marker.scale.y = 0.25;
  marker.scale.z = 0.25;
  marker.color.r = inputsHealthy() ? 0.0f : 1.0f;
  marker.color.g = inputsHealthy() ? 0.8f : 0.1f;
  marker.color.b = 0.2f;
  marker.color.a = 0.9f;
  array.markers.push_back(marker);
  return array;
}

bool FuelRealInterfaceAdapter::enabled() const {return enabled_;}
bool FuelRealInterfaceAdapter::controlBridgeEnabled() const {return control_bridge_enabled_;}
std::string FuelRealInterfaceAdapter::robotMode() const {return robot_mode_;}
std::string FuelRealInterfaceAdapter::odomTopic() const {return odom_topic_;}
std::string FuelRealInterfaceAdapter::mapCloudTopic() const {return map_cloud_topic_;}

}  // namespace fuel_ros2
