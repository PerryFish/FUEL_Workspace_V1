#pragma once

#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

namespace fuel_ros2
{

enum class FuelPreflightDecision {
  NO_GO,
  DEV_ONLY,
  SIM_ONLY,
  BAG_VALIDATED,
  HARDWARE_DRY_RUN_READY,
  READY_FOR_TETHERED_TEST
};

struct FuelPreflightChecklist {
  bool real_bag_present = false;
  bool real_bag_validated = false;
  bool fake_bag_used = false;
  bool localization_input_ok = false;
  bool mapping_input_ok = false;
  bool planner_output_ok = false;
  bool safety_gate_ok = false;
  bool closed_loop_fake_follower_ok = false;
  bool control_failsafe_ok = false;
  bool hardware_dry_run_only = true;
  bool actuator_commands_forbidden = true;
  bool stable_outputs_preserved = false;
  std::string decision_reason;
};

class FuelOnboardPreflightAdapter
{
public:
  bool initializeFromRos2Params(const rclcpp::Node::SharedPtr & node);
  bool initializeFromRos2Params(rclcpp::Node & node);
  void reset();

  void updateRealBagEvidence(bool present, bool validated, bool fake_used);
  void updateLocalizationMappingHealth(bool localization_ok, bool mapping_ok);
  void updatePlannerHealth(bool planner_output_ok, bool stable_outputs_ok);
  void updateSafetyGateHealth(bool safety_gate_ok);
  void updateClosedLoopHealth(bool fake_follower_ok);
  void updateControlFailsafeHealth(bool control_failsafe_ok);

  bool evaluate();

  FuelPreflightDecision decision() const;
  std::string decisionString() const;
  FuelPreflightChecklist checklist() const;
  bool readyForRealOnboardFlight() const;
  bool enabled() const;
  bool dryRunOnly() const;
  bool allowRealFlight() const;

  std_msgs::msg::String exportChecklistMsg() const;
  std_msgs::msg::String exportDecisionMsg() const;
  std_msgs::msg::String exportStatusMsg() const;
  visualization_msgs::msg::MarkerArray exportDebugMarkers(
    const std::string & frame_id,
    const rclcpp::Time & stamp) const;

private:
  template<typename T>
  T getOrDeclare(rclcpp::Node & node, const std::string & name, const T & default_value)
  {
    if (!node.has_parameter(name)) {
      node.declare_parameter<T>(name, default_value);
    }
    return node.get_parameter(name).get_value<T>();
  }

  bool enabled_{false};
  bool dry_run_only_{true};
  bool allow_real_flight_{false};
  bool require_real_bag_{true};
  bool allow_fake_bag_for_dev_{true};
  bool require_safety_gate_pass_{true};
  bool require_closed_loop_pass_{true};
  bool require_control_failsafe_pass_{true};
  bool forbid_actuator_commands_{true};
  bool allow_shadow_commands_only_{true};
  std::string default_decision_{"NO_GO"};

  FuelPreflightChecklist checklist_;
  FuelPreflightDecision decision_{FuelPreflightDecision::NO_GO};
};

}  // namespace fuel_ros2
