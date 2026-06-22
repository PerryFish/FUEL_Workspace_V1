#ifndef FUEL_ROS2_SAFETY_GATE_FUEL_SAFETY_GATE_ADAPTER_HPP_
#define FUEL_ROS2_SAFETY_GATE_FUEL_SAFETY_GATE_ADAPTER_HPP_

#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

namespace fuel_ros2
{

class FuelPlanEnvAdapter;

enum class FuelSafetyGateStatus
{
  IDLE,
  CHECKING,
  PASS,
  WARN,
  BLOCK_TRAJECTORY,
  EMERGENCY_STOP,
  HOLD_POSITION,
  FALLBACK_TO_SAFE_OUTPUT
};

struct FuelTrajectorySafetyReport
{
  bool valid{false};
  bool non_empty{false};
  bool frame_ok{false};
  bool timestamp_ok{false};
  bool within_map_bounds{false};
  bool collision_free{false};
  bool min_distance_ok{false};
  bool z_range_ok{false};
  bool speed_limit_ok{false};
  bool acceleration_limit_ok{false};
  double min_obstacle_distance{-1.0};
  double max_speed_estimate{-1.0};
  double max_acc_estimate{-1.0};
  std::string decision{"IDLE"};
  std::string reason{"not_evaluated"};
};

class FuelSafetyGateAdapter
{
public:
  bool initializeFromRos2Params(const rclcpp::Node::SharedPtr & node);
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  void updatePlanEnv(const FuelPlanEnvAdapter * plan_env);
  void updateInputTrajectory(const nav_msgs::msg::Path & trajectory);
  void updateOdom(const nav_msgs::msg::Odometry & odom);

  bool evaluate();

  FuelSafetyGateStatus status() const;
  std::string statusString() const;
  FuelTrajectorySafetyReport currentReport() const;

  nav_msgs::msg::Path exportSafeTrajectoryMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  std_msgs::msg::String exportSafetyReportMsg() const;
  std_msgs::msg::Bool exportEmergencyStopMsg() const;
  geometry_msgs::msg::PoseStamped exportHoldPositionMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  bool enabled() const;
  bool outputFilterEnabled() const;
  std::string inputTrajectoryTopic() const;
  std::string outputSafeTrajectoryTopic() const;

private:
  static double pathLength(const nav_msgs::msg::Path & path);
  static double stampAgeSec(const builtin_interfaces::msg::Time & stamp);
  static double distance3d(
    const geometry_msgs::msg::Point & a,
    const geometry_msgs::msg::Point & b);
  void setDecision(FuelSafetyGateStatus status, const std::string & decision, const std::string & reason);
  bool estimateDynamics();

  bool enabled_{false};
  bool output_filter_enabled_{false};
  std::string input_trajectory_topic_{"/fuel/local_trajectory"};
  std::string output_safe_trajectory_topic_{"/fuel/safety_gate/safe_trajectory"};
  double min_obstacle_distance_{0.5};
  double min_z_{0.6};
  double max_z_{3.0};
  double max_speed_{3.0};
  double max_acceleration_{2.0};
  double max_trajectory_age_sec_{1.0};
  bool allow_hold_position_{true};
  bool allow_emergency_stop_{true};
  double assumed_sample_dt_{0.2};

  const FuelPlanEnvAdapter * plan_env_{nullptr};
  bool have_trajectory_{false};
  bool have_odom_{false};
  nav_msgs::msg::Path input_trajectory_;
  nav_msgs::msg::Path safe_trajectory_;
  nav_msgs::msg::Odometry last_odom_;
  FuelSafetyGateStatus status_{FuelSafetyGateStatus::IDLE};
  FuelTrajectorySafetyReport report_;
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_SAFETY_GATE_FUEL_SAFETY_GATE_ADAPTER_HPP_
