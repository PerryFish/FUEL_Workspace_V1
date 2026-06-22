#ifndef FUEL_ROS2_REAL_INTERFACE_FUEL_REAL_INTERFACE_ADAPTER_HPP_
#define FUEL_ROS2_REAL_INTERFACE_FUEL_REAL_INTERFACE_ADAPTER_HPP_

#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

namespace fuel_ros2
{

class FuelRealInterfaceAdapter
{
public:
  bool initializeFromRos2Params(const rclcpp::Node::SharedPtr & node);
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  void updateOdom(const nav_msgs::msg::Odometry & odom_msg);
  void updateMapCloud(const sensor_msgs::msg::PointCloud2 & cloud_msg);
  void updatePlannerOutputs(
    const geometry_msgs::msg::PoseStamped & waypoint,
    const nav_msgs::msg::Path & global_path,
    const nav_msgs::msg::Path & local_trajectory,
    const std::string & trajectory_contract);

  bool inputsHealthy() const;
  bool outputsHealthy() const;

  std::string inputStatusString() const;
  std::string outputStatusString() const;
  std_msgs::msg::String exportStatusMsg() const;
  std_msgs::msg::String exportInputStatusMsg() const;
  std_msgs::msg::String exportOutputStatusMsg() const;
  std_msgs::msg::String exportControlBridgeStatusMsg() const;
  std_msgs::msg::String exportModeManagerStatusMsg() const;
  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  bool enabled() const;
  bool controlBridgeEnabled() const;
  std::string robotMode() const;
  std::string odomTopic() const;
  std::string mapCloudTopic() const;

private:
  static double stampAgeSec(const builtin_interfaces::msg::Time & stamp);
  static double pathLength(const nav_msgs::msg::Path & path);
  double measuredHz(const rclcpp::Time & first, const rclcpp::Time & last, int count) const;
  bool frameAcceptable(const std::string & frame_id) const;

  bool enabled_{false};
  std::string global_frame_{"map"};
  std::string odom_frame_{"odom"};
  std::string base_frame_{"base_link"};
  std::string sensor_frame_{"sensor"};

  std::string odom_topic_{"/state_estimation"};
  std::string map_cloud_topic_{"/mapping/global_cloud"};
  std::string local_cloud_topic_{"/mapping/local_cloud"};
  std::string occupied_cloud_topic_{"/mapping/occupied_cloud"};
  std::string free_cloud_topic_{"/mapping/free_cloud"};

  bool control_bridge_enabled_{false};
  std::string preferred_control_interface_{"trajectory"};
  double control_publish_rate_{10.0};

  double min_odom_hz_{10.0};
  double min_map_hz_{1.0};
  double max_odom_age_sec_{0.3};
  double max_map_age_sec_{2.0};
  bool require_tf_map_to_base_{false};
  bool require_non_empty_map_{true};
  bool require_non_empty_path_{true};
  bool require_non_empty_trajectory_{true};

  std::string robot_mode_{"air"};
  bool allow_land_mode_{true};
  bool allow_air_mode_{true};
  double land_fixed_z_{0.6};
  double air_min_z_{0.8};
  double air_max_z_{2.5};

  bool have_odom_{false};
  bool have_map_{false};
  bool have_outputs_{false};
  nav_msgs::msg::Odometry last_odom_;
  sensor_msgs::msg::PointCloud2 last_map_;
  geometry_msgs::msg::PoseStamped last_waypoint_;
  nav_msgs::msg::Path last_global_path_;
  nav_msgs::msg::Path last_local_trajectory_;
  std::string last_contract_;
  rclcpp::Time first_odom_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_odom_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time first_map_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_map_time_{0, 0, RCL_ROS_TIME};
  int odom_count_{0};
  int map_count_{0};
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_REAL_INTERFACE_FUEL_REAL_INTERFACE_ADAPTER_HPP_
