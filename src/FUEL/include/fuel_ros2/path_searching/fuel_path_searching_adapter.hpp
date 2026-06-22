#ifndef FUEL_ROS2_PATH_SEARCHING_FUEL_PATH_SEARCHING_ADAPTER_HPP_
#define FUEL_ROS2_PATH_SEARCHING_FUEL_PATH_SEARCHING_ADAPTER_HPP_

#include <string>
#include <vector>

#include <Eigen/Core>

#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

#include "fuel_ros2/path_searching/fuel_grid_astar3d.hpp"

namespace fuel_ros2
{

class FuelPlanEnvAdapter;

enum class FuelPathSearchStatus {
  IDLE,
  SEARCHING,
  SUCCESS,
  FAILED_NO_MAP,
  FAILED_INVALID_START,
  FAILED_INVALID_GOAL,
  FAILED_OCCUPIED_START,
  FAILED_OCCUPIED_GOAL,
  FAILED_NO_PATH,
  FALLBACK_STRAIGHT_LINE
};

class FuelPathSearchingAdapter
{
public:
  bool initializeFromRos2Params(const rclcpp::Node::SharedPtr & node);
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  bool setPlanEnv(const FuelPlanEnvAdapter * plan_env);

  bool searchPath(
    const Eigen::Vector3d & start,
    const Eigen::Vector3d & goal);

  std::vector<Eigen::Vector3d> getPath() const;
  std::vector<Eigen::Vector3d> getVisitedNodes() const;

  FuelPathSearchStatus status() const;
  std::string statusString() const;
  std::string backendStatusString() const;
  std::string lastFailureReason() const;
  double lastDurationMs() const;
  double lastPathLength() const;
  double gridResolution() const;
  int searchCount() const;
  int successCount() const;
  int failureCount() const;
  int fallbackCount() const;

  nav_msgs::msg::Path exportPathMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  visualization_msgs::msg::MarkerArray exportVisitedNodes(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  std_msgs::msg::String exportStatusMsg() const;

private:
  bool isTraversable(const Eigen::Vector3d & p) const;
  bool makeStraightLineFallback(const Eigen::Vector3d & start, const Eigen::Vector3d & goal);
  static std::string statusToString(FuelPathSearchStatus status);

  const FuelPlanEnvAdapter * plan_env_{nullptr};
  FuelGridAstar3D astar_;
  FuelGridAstar3D::Config config_;
  bool enabled_{false};
  bool use_path_searching_in_fsm_{false};
  std::string algorithm_{"grid_astar_3d"};
  double safety_distance_{0.35};
  bool allow_unknown_{true};
  bool allow_straight_line_fallback_{true};

  FuelPathSearchStatus status_{FuelPathSearchStatus::IDLE};
  std::string last_failure_reason_{"none"};
  std::vector<Eigen::Vector3d> path_;
  std::vector<Eigen::Vector3d> visited_;
  double last_duration_ms_{0.0};
  double last_path_length_{0.0};
  int search_count_{0};
  int success_count_{0};
  int failure_count_{0};
  int fallback_count_{0};
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_PATH_SEARCHING_FUEL_PATH_SEARCHING_ADAPTER_HPP_
