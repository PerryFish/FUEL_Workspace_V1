#include <chrono>
#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

namespace fuel_ros2
{

class FuelControlBridgeNode final : public rclcpp::Node
{
public:
  FuelControlBridgeNode() : Node("fuel_control_bridge_node")
  {
    enable_control_bridge_ = declare_parameter<bool>("enable_control_bridge", true);
    preferred_control_interface_ = declare_parameter<std::string>("preferred_control_interface", "trajectory");
    publish_rate_ = std::max(0.1, declare_parameter<double>("publish_rate", 10.0));
    waypoint_pub_ = create_publisher<geometry_msgs::msg::PoseStamped>("/planner/waypoint_cmd", 10);
    path_pub_ = create_publisher<nav_msgs::msg::Path>("/planner/path_cmd", 10);
    trajectory_pub_ = create_publisher<nav_msgs::msg::Path>("/planner/trajectory_cmd", 10);
    status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/control_bridge/status", 10);
    waypoint_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>(
      "/fuel/waypoint", 10, [this](const geometry_msgs::msg::PoseStamped::SharedPtr msg) {
        last_waypoint_ = *msg;
        have_waypoint_ = true;
      });
    path_sub_ = create_subscription<nav_msgs::msg::Path>(
      "/fuel/global_path", 10, [this](const nav_msgs::msg::Path::SharedPtr msg) {
        last_path_ = *msg;
        have_path_ = true;
      });
    trajectory_sub_ = create_subscription<nav_msgs::msg::Path>(
      "/fuel/local_trajectory", 10, [this](const nav_msgs::msg::Path::SharedPtr msg) {
        last_trajectory_ = *msg;
        have_trajectory_ = true;
      });
    contract_sub_ = create_subscription<std_msgs::msg::String>(
      "/fuel/plan_manager/trajectory_contract", 10, [this](const std_msgs::msg::String::SharedPtr msg) {
        last_contract_ = msg->data;
      });
    timer_ = create_wall_timer(
      std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::duration<double>(1.0 / publish_rate_)),
      [this]() {publishBridgeOutputs();});
    RCLCPP_INFO(
      get_logger(),
      "CONTROL_BRIDGE_DEMO_RUNNING enabled=%s preferred=%s real_flight_command=false",
      enable_control_bridge_ ? "true" : "false", preferred_control_interface_.c_str());
  }

private:
  void publishBridgeOutputs()
  {
    if (enable_control_bridge_) {
      if (have_waypoint_) {
        waypoint_pub_->publish(last_waypoint_);
      }
      if (have_path_) {
        path_pub_->publish(last_path_);
      }
      if (have_trajectory_) {
        trajectory_pub_->publish(last_trajectory_);
      }
    }
    std_msgs::msg::String status;
    status.data = "CONTROL_BRIDGE_DEMO_STATUS enabled=" + std::string(enable_control_bridge_ ? "true" : "false") +
      " preferred_interface=" + preferred_control_interface_ +
      " waypoint_ready=" + std::string(have_waypoint_ ? "true" : "false") +
      " path_ready=" + std::string(have_path_ ? "true" : "false") +
      " trajectory_ready=" + std::string(have_trajectory_ ? "true" : "false") +
      " contract_ready=" + std::string(last_contract_.empty() ? "false" : "true") +
      " real_flight_command=false";
    status_pub_->publish(status);
  }

  bool enable_control_bridge_{true};
  std::string preferred_control_interface_{"trajectory"};
  double publish_rate_{10.0};
  bool have_waypoint_{false};
  bool have_path_{false};
  bool have_trajectory_{false};
  geometry_msgs::msg::PoseStamped last_waypoint_;
  nav_msgs::msg::Path last_path_;
  nav_msgs::msg::Path last_trajectory_;
  std::string last_contract_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr waypoint_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr trajectory_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_pub_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr waypoint_sub_;
  rclcpp::Subscription<nav_msgs::msg::Path>::SharedPtr path_sub_;
  rclcpp::Subscription<nav_msgs::msg::Path>::SharedPtr trajectory_sub_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr contract_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

}  // namespace fuel_ros2

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<fuel_ros2::FuelControlBridgeNode>());
  rclcpp::shutdown();
  return 0;
}
