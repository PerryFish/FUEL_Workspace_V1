#ifndef FUEL_ROS2_PLAN_ENV_FUEL_PLAN_ENV_ADAPTER_HPP_
#define FUEL_ROS2_PLAN_ENV_FUEL_PLAN_ENV_ADAPTER_HPP_

#include <cstddef>
#include <string>
#include <unordered_set>
#include <vector>

#include <Eigen/Core>

#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

namespace fuel_ros2
{

class FuelPlanEnvAdapter
{
public:
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  bool updateFromPointCloud(const sensor_msgs::msg::PointCloud2 & cloud_msg);
  bool updateOdometry(const nav_msgs::msg::Odometry & odom_msg);

  bool isInsideMap(const Eigen::Vector3d & p) const;
  bool isOccupied(const Eigen::Vector3d & p) const;
  double getDistance(const Eigen::Vector3d & p) const;

  std::vector<Eigen::Vector3d> extractSimpleFrontiers() const;

  sensor_msgs::msg::PointCloud2 exportOccupiedCloudMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  sensor_msgs::msg::PointCloud2 exportInflatedCloudMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  std::size_t occupiedVoxelCount() const;
  std::size_t inflatedVoxelCount() const;

private:
  struct GridIndex
  {
    int x{0};
    int y{0};
    int z{0};
  };

  struct GridIndexHash
  {
    std::size_t operator()(const GridIndex & idx) const;
  };

  struct GridIndexEq
  {
    bool operator()(const GridIndex & a, const GridIndex & b) const;
  };

  GridIndex pointToIndex(const Eigen::Vector3d & p) const;
  Eigen::Vector3d indexToPoint(const GridIndex & idx) const;
  void rebuildInflation();
  sensor_msgs::msg::PointCloud2 exportCloud(
    const std::unordered_set<GridIndex, GridIndexHash, GridIndexEq> & voxels,
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  std::string frame_id_{"map"};
  double resolution_{0.2};
  double inflation_radius_{0.4};
  double local_update_range_x_{8.0};
  double local_update_range_y_{8.0};
  double local_update_range_z_{3.0};
  Eigen::Vector3d min_{-10.0, -10.0, 0.5};
  Eigen::Vector3d max_{10.0, 10.0, 3.0};
  Eigen::Vector3d last_odom_{0.0, 0.0, 1.0};
  bool has_odom_{false};
  bool enable_inflation_{true};
  bool enable_frontier_extraction_{true};

  std::unordered_set<GridIndex, GridIndexHash, GridIndexEq> occupied_;
  std::unordered_set<GridIndex, GridIndexHash, GridIndexEq> inflated_;
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_PLAN_ENV_FUEL_PLAN_ENV_ADAPTER_HPP_
