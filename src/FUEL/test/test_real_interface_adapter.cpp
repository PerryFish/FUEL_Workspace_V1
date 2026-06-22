#include <gtest/gtest.h>

#include <cstdlib>

#include "fuel_ros2/real_interface/fuel_real_interface_adapter.hpp"

namespace
{

void ensureRclcpp()
{
  if (!rclcpp::ok()) {
    setenv("ROS_LOG_DIR", "/tmp/fuel_ros2_test_logs", 0);
    int argc = 0;
    char ** argv = nullptr;
    rclcpp::init(argc, argv);
  }
}

builtin_interfaces::msg::Time nowStamp()
{
  return rclcpp::Clock(RCL_SYSTEM_TIME).now();
}

nav_msgs::msg::Path makePath(std::size_t count)
{
  nav_msgs::msg::Path path;
  path.header.frame_id = "map";
  path.header.stamp = nowStamp();
  for (std::size_t i = 0; i < count; ++i) {
    geometry_msgs::msg::PoseStamped pose;
    pose.header = path.header;
    pose.pose.position.x = static_cast<double>(i);
    pose.pose.position.z = 1.0;
    pose.pose.orientation.w = 1.0;
    path.poses.push_back(pose);
  }
  return path;
}

TEST(FuelRealInterfaceAdapterTest, DefaultsAreHealthyWhenDisabled)
{
  fuel_ros2::FuelRealInterfaceAdapter adapter;
  EXPECT_TRUE(adapter.inputsHealthy());
  EXPECT_TRUE(adapter.outputsHealthy());
  EXPECT_FALSE(adapter.enabled());
}

TEST(FuelRealInterfaceAdapterTest, HealthyWithRecentInputsAndOutputs)
{
  ensureRclcpp();
  fuel_ros2::FuelRealInterfaceAdapter adapter;
  auto node = std::make_shared<rclcpp::Node>("real_interface_adapter_test_node");
  node->declare_parameter<bool>("real_interface.enable_real_interface_mode", true);
  ASSERT_TRUE(adapter.initializeFromRos2Params(node));

  nav_msgs::msg::Odometry odom;
  odom.header.frame_id = "map";
  odom.header.stamp = nowStamp();
  odom.child_frame_id = "base_link";
  adapter.updateOdom(odom);

  sensor_msgs::msg::PointCloud2 cloud;
  cloud.header.frame_id = "map";
  cloud.header.stamp = nowStamp();
  cloud.width = 8;
  cloud.height = 1;
  adapter.updateMapCloud(cloud);

  geometry_msgs::msg::PoseStamped waypoint;
  waypoint.header.frame_id = "map";
  waypoint.header.stamp = nowStamp();
  adapter.updatePlannerOutputs(waypoint, makePath(4), makePath(6), "{\"source\":\"path_searching\"}");

  EXPECT_TRUE(adapter.inputsHealthy());
  EXPECT_TRUE(adapter.outputsHealthy());
  EXPECT_NE(adapter.inputStatusString().find("healthy=true"), std::string::npos);
  EXPECT_NE(adapter.outputStatusString().find("local_trajectory_points=6"), std::string::npos);
}

TEST(FuelRealInterfaceAdapterTest, RejectsMissingMapWhenEnabled)
{
  ensureRclcpp();
  fuel_ros2::FuelRealInterfaceAdapter adapter;
  auto node = std::make_shared<rclcpp::Node>("real_interface_adapter_missing_map_test_node");
  node->declare_parameter<bool>("real_interface.enable_real_interface_mode", true);
  ASSERT_TRUE(adapter.initializeFromRos2Params(node));

  nav_msgs::msg::Odometry odom;
  odom.header.frame_id = "map";
  odom.header.stamp = nowStamp();
  odom.child_frame_id = "base_link";
  adapter.updateOdom(odom);

  EXPECT_FALSE(adapter.inputsHealthy());
}

}  // namespace
