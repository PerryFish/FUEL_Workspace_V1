#include <memory>

#include "fuel_ros2/safety_gate/fuel_safety_gate_adapter.hpp"

#include "gtest/gtest.h"
#include "rclcpp/rclcpp.hpp"

namespace
{

nav_msgs::msg::Path makePath(double z, int points = 4)
{
  nav_msgs::msg::Path path;
  path.header.frame_id = "map";
  path.header.stamp = rclcpp::Clock(RCL_SYSTEM_TIME).now();
  for (int i = 0; i < points; ++i) {
    geometry_msgs::msg::PoseStamped pose;
    pose.header = path.header;
    pose.pose.position.x = static_cast<double>(i) * 0.4;
    pose.pose.position.y = 0.1 * static_cast<double>(i);
    pose.pose.position.z = z;
    pose.pose.orientation.w = 1.0;
    path.poses.push_back(pose);
  }
  return path;
}

nav_msgs::msg::Odometry makeOdom()
{
  nav_msgs::msg::Odometry odom;
  odom.header.frame_id = "map";
  odom.header.stamp = rclcpp::Clock(RCL_SYSTEM_TIME).now();
  odom.child_frame_id = "base_link";
  odom.pose.pose.position.z = 1.0;
  odom.pose.pose.orientation.w = 1.0;
  return odom;
}

}  // namespace

TEST(FuelSafetyGateAdapterTest, ValidNonEmptyTrajectoryPasses)
{
  auto node = std::make_shared<rclcpp::Node>("safety_gate_valid_test");
  node->declare_parameter("safety_gate.enable_safety_gate", true);
  node->declare_parameter("safety_gate.min_z", 0.6);
  node->declare_parameter("safety_gate.max_z", 3.0);
  node->declare_parameter("safety_gate.max_speed", 10.0);
  node->declare_parameter("safety_gate.max_acceleration", 20.0);

  fuel_ros2::FuelSafetyGateAdapter adapter;
  EXPECT_TRUE(adapter.initializeFromRos2Params(node));
  adapter.updateOdom(makeOdom());
  adapter.updateInputTrajectory(makePath(1.2));

  EXPECT_TRUE(adapter.evaluate());
  EXPECT_EQ(adapter.status(), fuel_ros2::FuelSafetyGateStatus::PASS);
  EXPECT_TRUE(adapter.currentReport().valid);
  EXPECT_TRUE(adapter.currentReport().non_empty);
  EXPECT_EQ(adapter.exportSafeTrajectoryMsg("map", node->now()).poses.size(), 4U);
}

TEST(FuelSafetyGateAdapterTest, EmptyTrajectoryBlocksOrHolds)
{
  auto node = std::make_shared<rclcpp::Node>("safety_gate_empty_test");
  node->declare_parameter("safety_gate.enable_safety_gate", true);

  fuel_ros2::FuelSafetyGateAdapter adapter;
  EXPECT_TRUE(adapter.initializeFromRos2Params(node));
  adapter.updateOdom(makeOdom());
  nav_msgs::msg::Path empty;
  empty.header.frame_id = "map";
  empty.header.stamp = node->now();
  adapter.updateInputTrajectory(empty);

  EXPECT_FALSE(adapter.evaluate());
  EXPECT_EQ(adapter.status(), fuel_ros2::FuelSafetyGateStatus::HOLD_POSITION);
  EXPECT_FALSE(adapter.currentReport().valid);
  EXPECT_EQ(adapter.currentReport().reason, "empty_trajectory");
  EXPECT_TRUE(adapter.exportEmergencyStopMsg().data == false);
}

TEST(FuelSafetyGateAdapterTest, ZRangeViolationBlocks)
{
  auto node = std::make_shared<rclcpp::Node>("safety_gate_z_test");
  node->declare_parameter("safety_gate.enable_safety_gate", true);
  node->declare_parameter("safety_gate.min_z", 0.6);
  node->declare_parameter("safety_gate.max_z", 2.0);

  fuel_ros2::FuelSafetyGateAdapter adapter;
  EXPECT_TRUE(adapter.initializeFromRos2Params(node));
  adapter.updateOdom(makeOdom());
  adapter.updateInputTrajectory(makePath(3.4));

  EXPECT_FALSE(adapter.evaluate());
  EXPECT_EQ(adapter.status(), fuel_ros2::FuelSafetyGateStatus::BLOCK_TRAJECTORY);
  EXPECT_FALSE(adapter.currentReport().z_range_ok);
  EXPECT_EQ(adapter.currentReport().reason, "z_range_violation");
}

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  testing::InitGoogleTest(&argc, argv);
  const int result = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return result;
}
