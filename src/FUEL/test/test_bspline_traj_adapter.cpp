#include <gtest/gtest.h>

#include <Eigen/Core>

#include "fuel_ros2/bspline_traj/fuel_bspline_traj_adapter.hpp"

namespace
{

using fuel_ros2::FuelBsplineTrajAdapter;
using fuel_ros2::FuelBsplineTrajStatus;

TEST(FuelBsplineTrajAdapterTest, GeneratesDenserSmoothTrajectoryFromPath)
{
  FuelBsplineTrajAdapter adapter;
  std::vector<Eigen::Vector3d> path{
    Eigen::Vector3d(0.0, 0.0, 1.0),
    Eigen::Vector3d(1.0, 0.5, 1.2),
    Eigen::Vector3d(2.0, 0.2, 1.5),
    Eigen::Vector3d(3.0, 1.0, 1.8)};

  ASSERT_TRUE(adapter.generateFromPath(path));
  EXPECT_EQ(adapter.status(), FuelBsplineTrajStatus::SUCCESS);
  EXPECT_GE(adapter.getControlPoints().size(), path.size());
  EXPECT_GT(adapter.getSampledTrajectory().size(), path.size());
  EXPECT_NEAR(adapter.getSampledTrajectory().front().x(), path.front().x(), 1e-6);
  EXPECT_NEAR(adapter.getSampledTrajectory().back().x(), path.back().x(), 1e-6);
}

TEST(FuelBsplineTrajAdapterTest, FallsBackForTooFewPointsWhenAllowed)
{
  FuelBsplineTrajAdapter adapter;
  ASSERT_FALSE(adapter.generateFromPath({Eigen::Vector3d(0.0, 0.0, 1.0), Eigen::Vector3d(1.0, 0.0, 1.0)}));
  EXPECT_EQ(adapter.status(), FuelBsplineTrajStatus::FALLBACK_PATH_AS_TRAJECTORY);
  EXPECT_EQ(adapter.getSampledTrajectory().size(), 2U);
}

}  // namespace
