#include <gtest/gtest.h>

#include <cstdlib>
#include <memory>
#include <string>

#include "fuel_ros2/onboard_preflight/fuel_onboard_preflight_adapter.hpp"

#include "rclcpp/rclcpp.hpp"

namespace
{

void ensureRclcpp()
{
  if (!rclcpp::ok()) {
    setenv("ROS_LOG_DIR", "/tmp/fuel_ros2_test_logs", 0);
    int argc = 0;
    char ** argv = nullptr;
    rclcpp::init(argc, argv);
  }
}

std::shared_ptr<rclcpp::Node> makeNode(const std::string & name)
{
  ensureRclcpp();
  auto node = std::make_shared<rclcpp::Node>(name);
  node->declare_parameter<bool>("onboard_preflight.enable_onboard_preflight", true);
  node->declare_parameter<bool>("onboard_preflight.dry_run_only", true);
  node->declare_parameter<bool>("onboard_preflight.allow_real_flight", false);
  node->declare_parameter<bool>("onboard_preflight.evidence_gate.require_real_bag", true);
  node->declare_parameter<bool>("onboard_preflight.evidence_gate.allow_fake_bag_for_dev", true);
  node->declare_parameter<bool>("onboard_preflight.evidence_gate.require_safety_gate_pass", true);
  node->declare_parameter<bool>("onboard_preflight.evidence_gate.require_closed_loop_fake_follower_pass", true);
  node->declare_parameter<bool>("onboard_preflight.evidence_gate.require_control_failsafe_pass", true);
  node->declare_parameter<bool>("onboard_preflight.hardware_interface.forbid_actuator_commands", true);
  node->declare_parameter<bool>("onboard_preflight.hardware_interface.allow_shadow_commands_only", true);
  return node;
}

}  // namespace

TEST(FuelOnboardPreflightAdapterTest, FakeBagCanOnlyProduceDevOnly)
{
  auto node = makeNode("preflight_fake_bag_test");
  fuel_ros2::FuelOnboardPreflightAdapter adapter;
  ASSERT_TRUE(adapter.initializeFromRos2Params(node));

  adapter.updateRealBagEvidence(false, false, true);
  adapter.updateLocalizationMappingHealth(true, true);
  adapter.updatePlannerHealth(true, true);
  adapter.updateSafetyGateHealth(true);
  adapter.updateClosedLoopHealth(true);
  adapter.updateControlFailsafeHealth(true);

  EXPECT_TRUE(adapter.evaluate());
  EXPECT_EQ(adapter.decision(), fuel_ros2::FuelPreflightDecision::DEV_ONLY);
  EXPECT_NE(adapter.checklist().decision_reason.find("FAKE_BAG_USED_NOT_REAL_EVIDENCE"), std::string::npos);
  EXPECT_FALSE(adapter.readyForRealOnboardFlight());
}

TEST(FuelOnboardPreflightAdapterTest, FailedControlFailsafeForcesNoGo)
{
  auto node = makeNode("preflight_failsafe_test");
  fuel_ros2::FuelOnboardPreflightAdapter adapter;
  ASSERT_TRUE(adapter.initializeFromRos2Params(node));

  adapter.updateRealBagEvidence(true, true, false);
  adapter.updateLocalizationMappingHealth(true, true);
  adapter.updatePlannerHealth(true, true);
  adapter.updateSafetyGateHealth(true);
  adapter.updateClosedLoopHealth(true);
  adapter.updateControlFailsafeHealth(false);

  EXPECT_FALSE(adapter.evaluate());
  EXPECT_EQ(adapter.decision(), fuel_ros2::FuelPreflightDecision::NO_GO);
  EXPECT_NE(adapter.checklist().decision_reason.find("CONTROL_FAILSAFE_NOT_PASSED"), std::string::npos);
}

TEST(FuelOnboardPreflightAdapterTest, RealEvidenceAndDryRunCanReachHardwareDryRunReady)
{
  auto node = makeNode("preflight_hardware_dry_run_test");
  fuel_ros2::FuelOnboardPreflightAdapter adapter;
  ASSERT_TRUE(adapter.initializeFromRos2Params(node));

  adapter.updateRealBagEvidence(true, true, false);
  adapter.updateLocalizationMappingHealth(true, true);
  adapter.updatePlannerHealth(true, true);
  adapter.updateSafetyGateHealth(true);
  adapter.updateClosedLoopHealth(true);
  adapter.updateControlFailsafeHealth(true);

  EXPECT_TRUE(adapter.evaluate());
  EXPECT_EQ(adapter.decision(), fuel_ros2::FuelPreflightDecision::HARDWARE_DRY_RUN_READY);
  EXPECT_FALSE(adapter.readyForRealOnboardFlight());
  EXPECT_NE(adapter.exportDecisionMsg().data.find("HARDWARE_DRY_RUN_READY"), std::string::npos);
}

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  testing::InitGoogleTest(&argc, argv);
  const int result = RUN_ALL_TESTS();
  rclcpp::shutdown();
  return result;
}
