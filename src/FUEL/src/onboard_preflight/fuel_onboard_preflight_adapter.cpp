#include "fuel_ros2/onboard_preflight/fuel_onboard_preflight_adapter.hpp"

#include <sstream>

#include "visualization_msgs/msg/marker.hpp"

namespace fuel_ros2
{

bool FuelOnboardPreflightAdapter::initializeFromRos2Params(const rclcpp::Node::SharedPtr & node)
{
  return node && initializeFromRos2Params(*node);
}

bool FuelOnboardPreflightAdapter::initializeFromRos2Params(rclcpp::Node & node)
{
  enabled_ = getOrDeclare<bool>(node, "onboard_preflight.enable_onboard_preflight", false);
  dry_run_only_ = getOrDeclare<bool>(node, "onboard_preflight.dry_run_only", true);
  allow_real_flight_ = getOrDeclare<bool>(node, "onboard_preflight.allow_real_flight", false);
  require_real_bag_ =
    getOrDeclare<bool>(node, "onboard_preflight.evidence_gate.require_real_bag", true);
  allow_fake_bag_for_dev_ =
    getOrDeclare<bool>(node, "onboard_preflight.evidence_gate.allow_fake_bag_for_dev", true);
  require_safety_gate_pass_ =
    getOrDeclare<bool>(node, "onboard_preflight.evidence_gate.require_safety_gate_pass", true);
  require_closed_loop_pass_ = getOrDeclare<bool>(
    node, "onboard_preflight.evidence_gate.require_closed_loop_fake_follower_pass", true);
  require_control_failsafe_pass_ = getOrDeclare<bool>(
    node, "onboard_preflight.evidence_gate.require_control_failsafe_pass", true);
  forbid_actuator_commands_ =
    getOrDeclare<bool>(node, "onboard_preflight.hardware_interface.forbid_actuator_commands", true);
  allow_shadow_commands_only_ = getOrDeclare<bool>(
    node, "onboard_preflight.hardware_interface.allow_shadow_commands_only", true);
  default_decision_ =
    getOrDeclare<std::string>(node, "onboard_preflight.go_no_go.default_decision", "NO_GO");

  checklist_.hardware_dry_run_only = dry_run_only_;
  checklist_.actuator_commands_forbidden = forbid_actuator_commands_;
  evaluate();
  return true;
}

void FuelOnboardPreflightAdapter::reset()
{
  checklist_ = FuelPreflightChecklist{};
  checklist_.hardware_dry_run_only = dry_run_only_;
  checklist_.actuator_commands_forbidden = forbid_actuator_commands_;
  decision_ = FuelPreflightDecision::NO_GO;
}

void FuelOnboardPreflightAdapter::updateRealBagEvidence(
  bool present, bool validated, bool fake_used)
{
  checklist_.real_bag_present = present;
  checklist_.real_bag_validated = validated;
  checklist_.fake_bag_used = fake_used;
}

void FuelOnboardPreflightAdapter::updateLocalizationMappingHealth(
  bool localization_ok, bool mapping_ok)
{
  checklist_.localization_input_ok = localization_ok;
  checklist_.mapping_input_ok = mapping_ok;
}

void FuelOnboardPreflightAdapter::updatePlannerHealth(
  bool planner_output_ok, bool stable_outputs_ok)
{
  checklist_.planner_output_ok = planner_output_ok;
  checklist_.stable_outputs_preserved = stable_outputs_ok;
}

void FuelOnboardPreflightAdapter::updateSafetyGateHealth(bool safety_gate_ok)
{
  checklist_.safety_gate_ok = safety_gate_ok;
}

void FuelOnboardPreflightAdapter::updateClosedLoopHealth(bool fake_follower_ok)
{
  checklist_.closed_loop_fake_follower_ok = fake_follower_ok;
}

void FuelOnboardPreflightAdapter::updateControlFailsafeHealth(bool control_failsafe_ok)
{
  checklist_.control_failsafe_ok = control_failsafe_ok;
}

bool FuelOnboardPreflightAdapter::evaluate()
{
  checklist_.hardware_dry_run_only = dry_run_only_;
  checklist_.actuator_commands_forbidden = forbid_actuator_commands_;

  auto reject = [this](const std::string & reason) {
    decision_ = FuelPreflightDecision::NO_GO;
    checklist_.decision_reason = reason;
    return false;
  };

  if (allow_real_flight_) {
    return reject("ALLOW_REAL_FLIGHT_MUST_REMAIN_FALSE_IN_P9");
  }
  if (!dry_run_only_) {
    return reject("DRY_RUN_ONLY_REQUIRED");
  }
  if (!forbid_actuator_commands_) {
    return reject("ACTUATOR_COMMANDS_NOT_FORBIDDEN");
  }
  if (!allow_shadow_commands_only_) {
    return reject("SHADOW_COMMANDS_ONLY_NOT_ENABLED");
  }
  if (require_control_failsafe_pass_ && !checklist_.control_failsafe_ok) {
    return reject("CONTROL_FAILSAFE_NOT_PASSED");
  }
  if (require_safety_gate_pass_ && !checklist_.safety_gate_ok) {
    return reject("SAFETY_GATE_NOT_PASSED");
  }
  if (require_closed_loop_pass_ && !checklist_.closed_loop_fake_follower_ok) {
    return reject("CLOSED_LOOP_FAKE_FOLLOWER_NOT_PASSED");
  }
  if (!checklist_.planner_output_ok || !checklist_.stable_outputs_preserved) {
    return reject("PLANNER_OUTPUT_OR_STABLE_TOPICS_NOT_OK");
  }
  if (!checklist_.localization_input_ok || !checklist_.mapping_input_ok) {
    return reject("LOCALIZATION_OR_MAPPING_INPUT_NOT_OK");
  }

  if (checklist_.fake_bag_used) {
    decision_ = FuelPreflightDecision::DEV_ONLY;
    checklist_.decision_reason = "FAKE_BAG_USED_NOT_REAL_EVIDENCE";
    return true;
  }

  if (require_real_bag_ && (!checklist_.real_bag_present || !checklist_.real_bag_validated)) {
    if (allow_fake_bag_for_dev_) {
      decision_ = FuelPreflightDecision::DEV_ONLY;
      checklist_.decision_reason = "REAL_BAG_REQUIRED_NOT_PRESENT_DEV_ONLY";
      return true;
    }
    return reject("REAL_BAG_REQUIRED_NOT_VALIDATED");
  }

  if (checklist_.real_bag_validated && dry_run_only_) {
    decision_ = FuelPreflightDecision::HARDWARE_DRY_RUN_READY;
    checklist_.decision_reason = "REAL_BAG_AND_DRY_RUN_EVIDENCE_READY_REAL_FLIGHT_STILL_DISABLED";
    return true;
  }

  decision_ = FuelPreflightDecision::BAG_VALIDATED;
  checklist_.decision_reason = "REAL_BAG_VALIDATED_HARDWARE_DRY_RUN_PENDING";
  return true;
}

FuelPreflightDecision FuelOnboardPreflightAdapter::decision() const
{
  return decision_;
}

std::string FuelOnboardPreflightAdapter::decisionString() const
{
  switch (decision_) {
    case FuelPreflightDecision::NO_GO:
      return "NO_GO";
    case FuelPreflightDecision::DEV_ONLY:
      return "DEV_ONLY";
    case FuelPreflightDecision::SIM_ONLY:
      return "SIM_ONLY";
    case FuelPreflightDecision::BAG_VALIDATED:
      return "BAG_VALIDATED";
    case FuelPreflightDecision::HARDWARE_DRY_RUN_READY:
      return "HARDWARE_DRY_RUN_READY";
    case FuelPreflightDecision::READY_FOR_TETHERED_TEST:
      return "READY_FOR_TETHERED_TEST";
  }
  return "NO_GO";
}

FuelPreflightChecklist FuelOnboardPreflightAdapter::checklist() const
{
  return checklist_;
}

bool FuelOnboardPreflightAdapter::readyForRealOnboardFlight() const
{
  return false;
}

bool FuelOnboardPreflightAdapter::enabled() const
{
  return enabled_;
}

bool FuelOnboardPreflightAdapter::dryRunOnly() const
{
  return dry_run_only_;
}

bool FuelOnboardPreflightAdapter::allowRealFlight() const
{
  return allow_real_flight_;
}

std_msgs::msg::String FuelOnboardPreflightAdapter::exportChecklistMsg() const
{
  std_msgs::msg::String msg;
  std::ostringstream out;
  out << "{"
      << "\"real_bag_present\":" << (checklist_.real_bag_present ? "true" : "false") << ","
      << "\"real_bag_validated\":" << (checklist_.real_bag_validated ? "true" : "false") << ","
      << "\"fake_bag_used\":" << (checklist_.fake_bag_used ? "true" : "false") << ","
      << "\"localization_input_ok\":" << (checklist_.localization_input_ok ? "true" : "false") << ","
      << "\"mapping_input_ok\":" << (checklist_.mapping_input_ok ? "true" : "false") << ","
      << "\"planner_output_ok\":" << (checklist_.planner_output_ok ? "true" : "false") << ","
      << "\"safety_gate_ok\":" << (checklist_.safety_gate_ok ? "true" : "false") << ","
      << "\"closed_loop_fake_follower_ok\":"
      << (checklist_.closed_loop_fake_follower_ok ? "true" : "false") << ","
      << "\"control_failsafe_ok\":" << (checklist_.control_failsafe_ok ? "true" : "false") << ","
      << "\"hardware_dry_run_only\":" << (checklist_.hardware_dry_run_only ? "true" : "false") << ","
      << "\"actuator_commands_forbidden\":"
      << (checklist_.actuator_commands_forbidden ? "true" : "false") << ","
      << "\"stable_outputs_preserved\":"
      << (checklist_.stable_outputs_preserved ? "true" : "false") << ","
      << "\"decision\":\"" << decisionString() << "\","
      << "\"reason\":\"" << checklist_.decision_reason << "\""
      << "}";
  msg.data = out.str();
  return msg;
}

std_msgs::msg::String FuelOnboardPreflightAdapter::exportDecisionMsg() const
{
  std_msgs::msg::String msg;
  msg.data = "ONBOARD_PREFLIGHT_GO_NO_GO decision=" + decisionString() +
    " reason=" + checklist_.decision_reason +
    " ready_for_real_onboard_flight=false dry_run_only=" +
    std::string(dry_run_only_ ? "true" : "false") +
    " allow_real_flight=" + std::string(allow_real_flight_ ? "true" : "false");
  return msg;
}

std_msgs::msg::String FuelOnboardPreflightAdapter::exportStatusMsg() const
{
  std_msgs::msg::String msg;
  msg.data = "ONBOARD_PREFLIGHT_STATUS enabled=" + std::string(enabled_ ? "true" : "false") +
    " decision=" + decisionString() +
    " real_bag_present=" + std::string(checklist_.real_bag_present ? "true" : "false") +
    " fake_bag_used=" + std::string(checklist_.fake_bag_used ? "true" : "false") +
    " actuator_commands_forbidden=" +
    std::string(checklist_.actuator_commands_forbidden ? "true" : "false") +
    " shadow_commands_only=" + std::string(allow_shadow_commands_only_ ? "true" : "false") +
    " ready_for_real_onboard_flight=false";
  return msg;
}

visualization_msgs::msg::MarkerArray FuelOnboardPreflightAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray markers;
  visualization_msgs::msg::Marker marker;
  marker.header.frame_id = frame_id;
  marker.header.stamp = stamp;
  marker.ns = "fuel_onboard_preflight";
  marker.id = 1;
  marker.type = visualization_msgs::msg::Marker::TEXT_VIEW_FACING;
  marker.action = visualization_msgs::msg::Marker::ADD;
  marker.pose.position.z = 1.5;
  marker.pose.orientation.w = 1.0;
  marker.scale.z = 0.25;
  marker.color.a = 1.0;
  marker.color.r = decision_ == FuelPreflightDecision::NO_GO ? 1.0 : 0.1;
  marker.color.g = decision_ == FuelPreflightDecision::NO_GO ? 0.1 : 0.8;
  marker.color.b = 0.1;
  marker.text = "P9 " + decisionString();
  markers.markers.push_back(marker);
  return markers;
}

}  // namespace fuel_ros2
