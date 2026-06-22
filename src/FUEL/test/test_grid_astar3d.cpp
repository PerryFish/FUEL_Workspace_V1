#include <gtest/gtest.h>

#include <Eigen/Core>

#include "fuel_ros2/path_searching/fuel_grid_astar3d.hpp"

namespace
{

using fuel_ros2::FuelGridAstar3D;

TEST(FuelGridAstar3DTest, FindsMultiPointPathAroundBlockedCell)
{
  FuelGridAstar3D astar;
  FuelGridAstar3D::Config config;
  config.resolution = 1.0;
  config.neighbor_mode = 6;
  config.max_search_nodes = 1000;
  config.min = Eigen::Vector3d(0.0, 0.0, 0.0);
  config.max = Eigen::Vector3d(4.0, 4.0, 2.0);
  astar.configure(config);

  const auto result = astar.search(
    Eigen::Vector3d(0.5, 0.5, 0.5),
    Eigen::Vector3d(3.5, 0.5, 0.5),
    [](const Eigen::Vector3d & p) {
      return !(p.x() > 1.0 && p.x() < 2.0 && p.y() < 1.0);
    });

  EXPECT_TRUE(result.success);
  EXPECT_GT(result.path.size(), 2U);
  EXPECT_GT(result.visited.size(), result.path.size());
}

TEST(FuelGridAstar3DTest, ReportsNoPathWhenGoalIsBlocked)
{
  FuelGridAstar3D astar;
  FuelGridAstar3D::Config config;
  config.resolution = 1.0;
  config.neighbor_mode = 26;
  config.max_search_nodes = 1000;
  config.min = Eigen::Vector3d(0.0, 0.0, 0.0);
  config.max = Eigen::Vector3d(4.0, 4.0, 2.0);
  astar.configure(config);

  const auto result = astar.search(
    Eigen::Vector3d(0.5, 0.5, 0.5),
    Eigen::Vector3d(3.5, 0.5, 0.5),
    [](const Eigen::Vector3d & p) {
      return p.x() < 3.0;
    });

  EXPECT_FALSE(result.success);
  EXPECT_EQ(result.reason, "goal_not_traversable");
  EXPECT_TRUE(result.path.empty());
}

}  // namespace
