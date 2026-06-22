#include <gtest/gtest.h>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/path.hpp"
#include "fuel_ros2/plan_manager/fuel_plan_manager_adapter.hpp"

namespace
{

nav_msgs::msg::Path makePath(std::size_t count)
{
  nav_msgs::msg::Path path;
  path.header.frame_id = "map";
  for (std::size_t i = 0; i < count; ++i) {
    geometry_msgs::msg::PoseStamped pose;
    pose.header = path.header;
    pose.pose.position.x = static_cast<double>(i);
    pose.pose.position.y = 0.2 * static_cast<double>(i);
    pose.pose.position.z = 1.0 + 0.1 * static_cast<double>(i);
    pose.pose.orientation.w = 1.0;
    path.poses.push_back(pose);
  }
  return path;
}

TEST(FuelPlanManagerAdapterTest, SelectsBsplineCandidateWhenValid)
{
  fuel_ros2::FuelPlanManagerAdapter adapter;
  adapter.updatePathSearchingResult(makePath(4), "PATH_SEARCHING_SUCCESS");
  adapter.updateBsplineCandidate(makePath(8), "BSPLINE_TRAJ_SUCCESS");

  ASSERT_TRUE(adapter.evaluateAndSelectFinalContract());
  const auto contract = adapter.currentContract();
  EXPECT_EQ(adapter.status(), fuel_ros2::FuelPlanManagerStatus::SUCCESS_BSPLINE_CANDIDATE);
  EXPECT_EQ(contract.source, "bspline_candidate");
  EXPECT_TRUE(contract.valid);
  EXPECT_TRUE(contract.dynamic_checked);
  EXPECT_FALSE(contract.safe_for_stable_output);
  EXPECT_EQ(contract.path_points, 4);
  EXPECT_EQ(contract.trajectory_points, 8);
}

TEST(FuelPlanManagerAdapterTest, FallsBackToPathSearchingWhenBsplineFallback)
{
  fuel_ros2::FuelPlanManagerAdapter adapter;
  adapter.updatePathSearchingResult(makePath(4), "PATH_SEARCHING_SUCCESS");
  adapter.updateBsplineCandidate(makePath(4), "BSPLINE_TRAJ_FAILED_FALLBACK_PATH");

  ASSERT_TRUE(adapter.evaluateAndSelectFinalContract());
  const auto contract = adapter.currentContract();
  EXPECT_EQ(adapter.status(), fuel_ros2::FuelPlanManagerStatus::FALLBACK_TO_PATH_SEARCHING);
  EXPECT_EQ(contract.source, "path_searching");
  EXPECT_TRUE(contract.valid);
  EXPECT_EQ(contract.fallback_reason, "bspline_candidate_unreliable");
}

TEST(FuelPlanManagerAdapterTest, FallsBackToMvpWithoutUsablePath)
{
  fuel_ros2::FuelPlanManagerAdapter adapter;
  adapter.updatePathSearchingResult(makePath(1), "FAILED_NO_PATH");
  adapter.updateBsplineCandidate(makePath(0), "FAILED_NO_PATH");

  ASSERT_TRUE(adapter.evaluateAndSelectFinalContract());
  const auto contract = adapter.currentContract();
  EXPECT_EQ(adapter.status(), fuel_ros2::FuelPlanManagerStatus::FALLBACK_TO_MVP);
  EXPECT_EQ(contract.source, "mvp");
  EXPECT_FALSE(contract.safe_for_stable_output);
}

}  // namespace
