#include <chrono>
#include <memory>
#include <string>

#include "fuel_ros2/onboard_preflight/fuel_onboard_preflight_adapter.hpp"

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

using namespace std::chrono_literals;

namespace fuel_ros2
{

class FuelOnboardPreflightNode final : public rclcpp::Node
{
public:
  FuelOnboardPreflightNode() : Node("fuel_onboard_preflight_node")
  {
    frame_id_ = declare_parameter<std::string>("frame_id", "map");
    real_bag_present_ = declare_parameter<bool>("preflight_inputs.real_bag_present", false);
    real_bag_validated_ = declare_parameter<bool>("preflight_inputs.real_bag_validated", false);
    fake_bag_used_ = declare_parameter<bool>("preflight_inputs.fake_bag_used", true);
    localization_ok_ = declare_parameter<bool>("preflight_inputs.localization_input_ok", true);
    mapping_ok_ = declare_parameter<bool>("preflight_inputs.mapping_input_ok", true);
    planner_output_ok_ = declare_parameter<bool>("preflight_inputs.planner_output_ok", true);
    stable_outputs_ok_ = declare_parameter<bool>("preflight_inputs.stable_outputs_preserved", true);
    safety_gate_ok_ = declare_parameter<bool>("preflight_inputs.safety_gate_ok", true);
    closed_loop_ok_ = declare_parameter<bool>("preflight_inputs.closed_loop_fake_follower_ok", true);
    control_failsafe_ok_ = declare_parameter<bool>("preflight_inputs.control_failsafe_ok", true);

    adapter_ = std::make_unique<FuelOnboardPreflightAdapter>();
    adapter_->initializeFromRos2Params(*this);
    updateAdapterInputs();

    status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/onboard_preflight/status", 10);
    checklist_pub_ = create_publisher<std_msgs::msg::String>("/fuel/onboard_preflight/checklist", 10);
    go_no_go_pub_ = create_publisher<std_msgs::msg::String>("/fuel/onboard_preflight/go_no_go", 10);
    debug_pub_ = create_publisher<visualization_msgs::msg::MarkerArray>(
      "/fuel/onboard_preflight/debug_markers", 10);
    timer_ = create_wall_timer(500ms, [this]() { publishPreflight(); });

    RCLCPP_INFO(
      get_logger(),
      "ONBOARD_PREFLIGHT_NODE_RUNNING enabled=%s dry_run_only=%s allow_real_flight=%s real_flight_command=false",
      adapter_->enabled() ? "true" : "false",
      adapter_->dryRunOnly() ? "true" : "false",
      adapter_->allowRealFlight() ? "true" : "false");
  }

private:
  void updateAdapterInputs()
  {
    adapter_->updateRealBagEvidence(real_bag_present_, real_bag_validated_, fake_bag_used_);
    adapter_->updateLocalizationMappingHealth(localization_ok_, mapping_ok_);
    adapter_->updatePlannerHealth(planner_output_ok_, stable_outputs_ok_);
    adapter_->updateSafetyGateHealth(safety_gate_ok_);
    adapter_->updateClosedLoopHealth(closed_loop_ok_);
    adapter_->updateControlFailsafeHealth(control_failsafe_ok_);
    adapter_->evaluate();
  }

  void publishPreflight()
  {
    updateAdapterInputs();
    status_pub_->publish(adapter_->exportStatusMsg());
    checklist_pub_->publish(adapter_->exportChecklistMsg());
    go_no_go_pub_->publish(adapter_->exportDecisionMsg());
    debug_pub_->publish(adapter_->exportDebugMarkers(frame_id_, now()));
  }

  std::string frame_id_;
  bool real_bag_present_{false};
  bool real_bag_validated_{false};
  bool fake_bag_used_{true};
  bool localization_ok_{true};
  bool mapping_ok_{true};
  bool planner_output_ok_{true};
  bool stable_outputs_ok_{true};
  bool safety_gate_ok_{true};
  bool closed_loop_ok_{true};
  bool control_failsafe_ok_{true};
  std::unique_ptr<FuelOnboardPreflightAdapter> adapter_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr checklist_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr go_no_go_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr debug_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

}  // namespace fuel_ros2

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<fuel_ros2::FuelOnboardPreflightNode>());
  rclcpp::shutdown();
  return 0;
}
