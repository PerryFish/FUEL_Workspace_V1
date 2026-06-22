#ifndef FUEL_ROS2_EXPLORATION_FSM_FUEL_EXPLORATION_FSM_ADAPTER_HPP_
#define FUEL_ROS2_EXPLORATION_FSM_FUEL_EXPLORATION_FSM_ADAPTER_HPP_

#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

namespace fuel_ros2
{

enum class FuelExplorationState {
  INIT,
  WAIT_TRIGGER,
  UPDATE_MAP,
  FIND_FRONTIER,
  SELECT_VIEWPOINT,
  PLAN_PATH,
  PUBLISH_TRAJECTORY,
  EXECUTE_TRAJECTORY,
  FINISH,
  ERROR_RECOVERY
};

enum class FuelExplorationEvent {
  ODOM_READY,
  MAP_READY,
  FRONTIER_READY,
  VIEWPOINT_READY,
  PLAN_READY,
  TRAJECTORY_PUBLISHED,
  EXECUTION_TIMEOUT,
  NO_FRONTIER,
  ERROR
};

class FuelExplorationFsmAdapter
{
public:
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  void updateOdometry(const nav_msgs::msg::Odometry & odom_msg);
  void updatePlanEnvStatus(const std::string & status);
  void updateFrontierFisStatus(const std::string & status);
  void updateBestViewpoint(const geometry_msgs::msg::PoseStamped & viewpoint);
  void setFallbackGoal(const geometry_msgs::msg::PoseStamped & goal);

  void tick(const rclcpp::Time & now);

  FuelExplorationState currentState() const;
  std::string currentStateString() const;
  std::string lastTransitionReason() const;
  std::string lastTransitionLog() const;
  std::string lastGoalLog() const;
  std::string lastFallbackLog() const;
  std::string lastPathSourceLog() const;

  bool hasActiveGoal() const;
  geometry_msgs::msg::PoseStamped currentGoal() const;
  bool usedFisBestViewpoint() const;
  bool usedFallback() const;
  void setExternalPath(const nav_msgs::msg::Path & path, const std::string & source);

  nav_msgs::msg::Path exportFsmPath(const std::string & frame_id, const rclcpp::Time & stamp) const;
  visualization_msgs::msg::MarkerArray exportFsmDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;
  std_msgs::msg::String exportStatusMsg() const;

private:
  static std::string stateToString(FuelExplorationState state);
  void transit(FuelExplorationState next, const std::string & reason, const rclcpp::Time & now);
  bool planSimplePath(const rclcpp::Time & now);
  bool goalReached() const;
  double stateDuration(const rclcpp::Time & now) const;

  bool enabled_{false};
  bool auto_start_{true};
  bool use_fis_best_viewpoint_{true};
  bool fallback_to_mvp_goal_{true};
  double goal_reached_distance_{0.5};
  double execution_timeout_sec_{15.0};
  double no_frontier_timeout_sec_{5.0};
  int max_error_recovery_count_{5};
  bool publish_debug_markers_{true};

  FuelExplorationState state_{FuelExplorationState::INIT};
  rclcpp::Time state_enter_time_{0, 0, RCL_ROS_TIME};
  std::string last_transition_reason_{"init"};
  std::string last_transition_log_{"FSM_TRANSITION from=INIT to=INIT reason=init time=0"};
  std::string last_goal_log_{"FSM_GOAL_SELECTED source=none x=0 y=0 z=0 yaw=0 utility=0"};
  std::string last_fallback_log_{"FSM_FALLBACK reason=none fallback_backend=none"};
  std::string last_path_source_log_{"FSM_PATH_SOURCE source=none points=0"};
  std::string plan_env_status_;
  std::string fis_status_;
  bool have_odom_{false};
  bool have_plan_env_{false};
  bool have_frontier_{false};
  bool have_best_viewpoint_{false};
  bool have_plan_{false};
  bool active_goal_{false};
  bool used_fis_best_viewpoint_{false};
  bool used_fallback_{false};
  int error_recovery_count_{0};

  nav_msgs::msg::Odometry last_odom_;
  geometry_msgs::msg::PoseStamped best_viewpoint_;
  geometry_msgs::msg::PoseStamped fallback_goal_;
  geometry_msgs::msg::PoseStamped active_goal_msg_;
  nav_msgs::msg::Path path_;
};

}  // namespace fuel_ros2

#endif  // FUEL_ROS2_EXPLORATION_FSM_FUEL_EXPLORATION_FSM_ADAPTER_HPP_
