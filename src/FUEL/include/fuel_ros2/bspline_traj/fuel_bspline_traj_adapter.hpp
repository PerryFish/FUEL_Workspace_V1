#ifndef FUEL_ROS2_BSPLINE_TRAJ_FUEL_BSPLINE_TRAJ_ADAPTER_HPP_
#define FUEL_ROS2_BSPLINE_TRAJ_FUEL_BSPLINE_TRAJ_ADAPTER_HPP_

#include <string>
#include <vector>

#include <Eigen/Core>

#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

namespace fuel_ros2
{

class FuelPlanEnvAdapter;

enum class FuelBsplineTrajStatus {
  IDLE,
  GENERATING,
  SUCCESS,
  FAILED_NO_PATH,
  FAILED_TOO_FEW_POINTS,
  FAILED_COLLISION_RISK,
  FAILED_DYNAMIC_LIMIT,
  FALLBACK_PATH_AS_TRAJECTORY
};

class FuelBsplineTrajAdapter
{
public:
  bool initializeFromRos2Params(const rclcpp::Node::SharedPtr & node);
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  bool setPlanEnv(const FuelPlanEnvAdapter * plan_env);

  bool generateFromPath(const std::vector<Eigen::Vector3d> & path_points);

  std::vector<Eigen::Vector3d> getControlPoints() const;
  std::vector<Eigen::Vector3d> getSampledTrajectory() const;

  FuelBsplineTrajStatus status() const;
  std::string statusString() const;
  std::string backendStatusString() const;
  std::string lastFailureReason() const;
  double lastDurationMs() const;
  double lastTrajectoryLength() const;
  bool useForStableOutput() const;
  int generationCount() const;
  int successCount() const;
  int failureCount() const;
  int fallbackCount() const;

  nav_msgs::msg::Path exportSampledTrajectoryMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  visualization_msgs::msg::MarkerArray exportControlPointMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  std_msgs::msg::String exportStatusMsg() const;

private:
  std::vector<Eigen::Vector3d> buildControlPoints(
    const std::vector<Eigen::Vector3d> & path_points) const;
  std::vector<Eigen::Vector3d> sampleCatmullRom(
    const std::vector<Eigen::Vector3d> & control_points) const;
  bool validateSampledTrajectory();
  bool makePathFallback(const std::vector<Eigen::Vector3d> & path_points);
  static Eigen::Vector3d catmullRom(
    const Eigen::Vector3d & p0,
    const Eigen::Vector3d & p1,
    const Eigen::Vector3d & p2,
    const Eigen::Vector3d & p3,
    double t);
  static double pathLength(const std::vector<Eigen::Vector3d> & points);
  static std::string statusToString(FuelBsplineTrajStatus status);

  const FuelPlanEnvAdapter * plan_env_{nullptr};
  bool enabled_{false};
  bool use_bspline_for_stable_output_{false};
  std::string input_path_topic_{"/fuel/path_searching/path"};
  std::string algorithm_{"uniform_bspline_lite"};
  int spline_order_{3};
  double sample_dt_{0.1};
  double control_point_spacing_{0.5};
  double max_velocity_{3.0};
  double max_acceleration_{2.0};
  double safety_distance_{0.35};
  double collision_check_resolution_{0.1};
  bool allow_path_as_trajectory_fallback_{true};

  FuelBsplineTrajStatus status_{FuelBsplineTrajStatus::IDLE};
  std::string last_failure_reason_{"none"};
  std::vector<Eigen::Vector3d> control_points_;
  std::vector<Eigen::Vector3d> sampled_trajectory_;
  double last_duration_ms_{0.0};
  double last_trajectory_length_{0.0};
  int generation_count_{0};
  int success_count_{0};
  int failure_count_{0};
  int fallback_count_{0};
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_BSPLINE_TRAJ_FUEL_BSPLINE_TRAJ_ADAPTER_HPP_
