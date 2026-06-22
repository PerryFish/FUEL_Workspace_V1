#include <chrono>
#include <memory>
#include <string>

#include "fuel_ros2/safety_gate/fuel_safety_gate_adapter.hpp"

#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"
#include "std_msgs/msg/string.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

using namespace std::chrono_literals;

namespace fuel_ros2
{

class FuelSafetyGateNode final : public rclcpp::Node
{
public:
  FuelSafetyGateNode() : Node("fuel_safety_gate_node")
  {
    frame_id_ = declare_parameter<std::string>("frame_id", "map");
    adapter_ = std::make_unique<FuelSafetyGateAdapter>();
    adapter_->initializeFromRos2Params(*this);

    status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/safety_gate/status", 10);
    report_pub_ = create_publisher<std_msgs::msg::String>("/fuel/safety_gate/report", 10);
    safe_traj_pub_ =
      create_publisher<nav_msgs::msg::Path>(adapter_->outputSafeTrajectoryTopic(), 10);
    debug_pub_ =
      create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/safety_gate/debug_markers", 10);
    emergency_stop_pub_ =
      create_publisher<std_msgs::msg::Bool>("/fuel/safety_gate/emergency_stop", 10);
    hold_position_pub_ =
      create_publisher<geometry_msgs::msg::PoseStamped>("/fuel/safety_gate/hold_position", 10);

    trajectory_sub_ = create_subscription<nav_msgs::msg::Path>(
      adapter_->inputTrajectoryTopic(), 10,
      [this](const nav_msgs::msg::Path::SharedPtr msg) {
        adapter_->updateInputTrajectory(*msg);
      });
    odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(
      "/state_estimation", 20,
      [this](const nav_msgs::msg::Odometry::SharedPtr msg) {
        adapter_->updateOdom(*msg);
      });
    fallback_odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(
      "/odom", 20,
      [this](const nav_msgs::msg::Odometry::SharedPtr msg) {
        adapter_->updateOdom(*msg);
      });

    timer_ = create_wall_timer(500ms, [this]() { publishGate(); });
    RCLCPP_INFO(
      get_logger(),
      "SAFETY_GATE_NODE_RUNNING enabled=%s filter=%s input=%s output=%s real_flight_command=false",
      adapter_->enabled() ? "true" : "false",
      adapter_->outputFilterEnabled() ? "true" : "false",
      adapter_->inputTrajectoryTopic().c_str(),
      adapter_->outputSafeTrajectoryTopic().c_str());
  }

private:
  void publishGate()
  {
    const auto stamp = now();
    const bool pass = adapter_->evaluate();
    std_msgs::msg::String status;
    status.data = "SAFETY_GATE_STATUS status=" + adapter_->statusString() +
      " enabled=" + std::string(adapter_->enabled() ? "true" : "false") +
      " output_filter=" + std::string(adapter_->outputFilterEnabled() ? "true" : "false") +
      " decision=" + adapter_->currentReport().decision +
      " reason=" + adapter_->currentReport().reason +
      " pass=" + std::string(pass ? "true" : "false") +
      " real_flight_command=false";
    status_pub_->publish(status);
    report_pub_->publish(adapter_->exportSafetyReportMsg());
    safe_traj_pub_->publish(adapter_->exportSafeTrajectoryMsg(frame_id_, stamp));
    debug_pub_->publish(adapter_->exportDebugMarkers(frame_id_, stamp));
    emergency_stop_pub_->publish(adapter_->exportEmergencyStopMsg());
    hold_position_pub_->publish(adapter_->exportHoldPositionMsg(frame_id_, stamp));
  }

  std::string frame_id_;
  std::unique_ptr<FuelSafetyGateAdapter> adapter_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr report_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr safe_traj_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr debug_pub_;
  rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr emergency_stop_pub_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr hold_position_pub_;
  rclcpp::Subscription<nav_msgs::msg::Path>::SharedPtr trajectory_sub_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr fallback_odom_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

}  // namespace fuel_ros2

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<fuel_ros2::FuelSafetyGateNode>());
  rclcpp::shutdown();
  return 0;
}
