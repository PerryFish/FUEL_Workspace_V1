#ifndef FUEL_ROS2_FRONTIER_FIS_FUEL_FRONTIER_FIS_ADAPTER_HPP_
#define FUEL_ROS2_FRONTIER_FIS_FUEL_FRONTIER_FIS_ADAPTER_HPP_

#include <string>
#include <vector>

#include <Eigen/Core>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

#include "fuel_ros2/plan_env/fuel_plan_env_adapter.hpp"

namespace fuel_ros2
{

struct FuelFrontierCluster
{
  int id{-1};
  std::vector<Eigen::Vector3d> cells;
  Eigen::Vector3d center{Eigen::Vector3d::Zero()};
  double information_gain{0.0};
  double distance_cost{0.0};
  double utility{0.0};
};

struct FuelViewpointCandidate
{
  int cluster_id{-1};
  Eigen::Vector3d position{Eigen::Vector3d::Zero()};
  double yaw{0.0};
  double visible_unknown_count{0.0};
  double distance_cost{0.0};
  double utility{0.0};
  bool collision_safe{true};
};

class FuelFrontierFisAdapter
{
public:
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  bool updateMapFromPlanEnv(const FuelPlanEnvAdapter & plan_env);
  bool updateOdometry(const nav_msgs::msg::Odometry & odom_msg);
  bool extractFrontierClusters();
  bool generateViewpoints();

  std::vector<Eigen::Vector3d> getFrontierCenters() const;
  std::vector<Eigen::Vector3d> getBestViewpoints() const;
  bool hasBestViewpoint() const;
  FuelViewpointCandidate bestViewpoint() const;

  visualization_msgs::msg::MarkerArray exportFrontierMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;
  visualization_msgs::msg::MarkerArray exportViewpointMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;
  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;
  geometry_msgs::msg::PoseStamped exportBestViewpointMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;
  std_msgs::msg::String exportStatusMsg() const;

  std::size_t clusterCount() const;
  std::size_t viewpointCount() const;
  bool isPartial() const;

private:
  void clusterCandidates();
  double zPenalty(const Eigen::Vector3d & p) const;
  static double yawToTarget(const Eigen::Vector3d & from, const Eigen::Vector3d & to);

  bool enabled_{false};
  bool use_frontier_goal_source_{false};
  int min_frontier_cluster_size_{5};
  int max_frontier_cluster_size_{5000};
  double frontier_resolution_{0.2};
  double viewpoint_distance_{1.5};
  double viewpoint_z_min_{0.8};
  double viewpoint_z_max_{2.5};
  double information_gain_weight_{1.0};
  double distance_cost_weight_{0.3};
  double z_penalty_weight_{0.2};
  int max_frontier_markers_{200};

  Eigen::Vector3d odom_{0.0, 0.0, 1.0};
  bool has_odom_{false};
  std::vector<Eigen::Vector3d> frontier_candidates_;
  std::vector<FuelFrontierCluster> clusters_;
  std::vector<FuelViewpointCandidate> viewpoints_;
  std::string status_{"FIS_BACKEND_PARTIAL"};
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_FRONTIER_FIS_FUEL_FRONTIER_FIS_ADAPTER_HPP_
