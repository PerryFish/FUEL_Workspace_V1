#ifndef FUEL_ROS2_PLAN_MANAGER_FUEL_PLAN_MANAGER_ADAPTER_HPP_
#define FUEL_ROS2_PLAN_MANAGER_FUEL_PLAN_MANAGER_ADAPTER_HPP_

#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

namespace fuel_ros2
{

enum class FuelPlanManagerStatus {
  IDLE,
  RUNNING,
  SUCCESS_PATH_ONLY,
  SUCCESS_BSPLINE_CANDIDATE,
  SUCCESS_MANAGED_OUTPUT,
  FALLBACK_TO_PATH_SEARCHING,
  FALLBACK_TO_MVP,
  FAILED_NO_GOAL,
  FAILED_NO_PATH,
  FAILED_TRAJECTORY_INVALID,
  ERROR_RECOVERY
};

struct FuelTrajectoryContract
{
  std::string source{"mvp"};
  bool valid{false};
  bool collision_checked{false};
  bool dynamic_checked{false};
  bool safe_for_stable_output{false};
  double path_length{0.0};
  double estimated_duration{0.0};
  int path_points{0};
  int trajectory_points{0};
  std::string fallback_reason;
  nav_msgs::msg::Path path_msg;
  nav_msgs::msg::Path trajectory_msg;
};

class FuelPlanManagerAdapter
{
public:
  bool initializeFromRos2Params(const rclcpp::Node::SharedPtr & node);
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  void updatePipelineInputs(
    const nav_msgs::msg::Odometry & odom,
    const geometry_msgs::msg::PoseStamped & current_goal);

  void updatePathSearchingResult(
    const nav_msgs::msg::Path & path,
    const std::string & status);

  void updateBsplineCandidate(
    const nav_msgs::msg::Path & sampled_traj,
    const std::string & status);

  bool evaluateAndSelectFinalContract();

  FuelPlanManagerStatus status() const;
  std::string statusString() const;
  std::string backendStatusString() const;
  FuelTrajectoryContract currentContract() const;

  nav_msgs::msg::Path exportManagedPathMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  nav_msgs::msg::Path exportManagedTrajectoryMsg(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  std_msgs::msg::String exportStatusMsg() const;
  std_msgs::msg::String exportContractMsg() const;

  bool useManagedOutput() const;
  int evaluationCount() const;
  int fallbackCount() const;

private:
  static double pathLength(const nav_msgs::msg::Path & path);
  static bool hasZVariation(const nav_msgs::msg::Path & path);
  static std::string statusToString(FuelPlanManagerStatus status);
  bool isPathUsable(const nav_msgs::msg::Path & path) const;
  bool isBsplineUsable() const;
  nav_msgs::msg::Path stampedCopy(
    const nav_msgs::msg::Path & input,
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

  bool enabled_{false};
  bool use_managed_output_{false};
  bool prefer_bspline_when_valid_{true};
  bool require_collision_checked_{true};
  bool require_dynamic_checked_{false};
  int min_path_points_{3};
  int min_trajectory_points_{5};
  int max_allowed_fallback_count_{10};
  bool publish_contract_debug_{true};
  double debug_publish_rate_{2.0};
  std::string output_contract_topic_{"/fuel/plan_manager/trajectory_contract"};

  FuelPlanManagerStatus status_{FuelPlanManagerStatus::IDLE};
  FuelTrajectoryContract contract_;
  nav_msgs::msg::Odometry odom_;
  geometry_msgs::msg::PoseStamped current_goal_;
  bool have_goal_{false};
  nav_msgs::msg::Path path_searching_path_;
  std::string path_searching_status_;
  nav_msgs::msg::Path bspline_candidate_;
  std::string bspline_status_;
  int evaluation_count_{0};
  int fallback_count_{0};
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_PLAN_MANAGER_FUEL_PLAN_MANAGER_ADAPTER_HPP_
