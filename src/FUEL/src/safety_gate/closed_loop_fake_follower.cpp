#include <algorithm>
#include <chrono>
#include <cmath>
#include <memory>
#include <string>

#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"

using namespace std::chrono_literals;

namespace fuel_ros2
{

class ClosedLoopFakeFollower final : public rclcpp::Node
{
public:
  ClosedLoopFakeFollower() : Node("closed_loop_fake_follower")
  {
    frame_id_ = declare_parameter<std::string>("frame_id", "map");
    base_frame_id_ = declare_parameter<std::string>("base_frame_id", "base_link");
    follow_rate_ = std::max(1.0, declare_parameter<double>("follow_rate", 20.0));
    max_speed_ = std::max(0.05, declare_parameter<double>("max_speed", 0.8));
    use_safety_gate_output_ = declare_parameter<bool>("use_safety_gate_output", true);
    stop_on_emergency_ = declare_parameter<bool>("stop_on_emergency", true);
    position_.x = declare_parameter<double>("initial_x", 0.0);
    position_.y = declare_parameter<double>("initial_y", 0.0);
    position_.z = declare_parameter<double>("initial_z", 1.2);

    const std::string trajectory_topic =
      use_safety_gate_output_ ? "/fuel/safety_gate/safe_trajectory" : "/fuel/local_trajectory";
    trajectory_sub_ = create_subscription<nav_msgs::msg::Path>(
      trajectory_topic, 10,
      [this](const nav_msgs::msg::Path::SharedPtr msg) {
        trajectory_ = *msg;
        target_index_ = 0;
        have_trajectory_ = !trajectory_.poses.empty();
      });
    emergency_sub_ = create_subscription<std_msgs::msg::Bool>(
      "/fuel/safety_gate/emergency_stop", 10,
      [this](const std_msgs::msg::Bool::SharedPtr msg) {
        emergency_stop_ = msg->data;
      });
    odom_pub_ = create_publisher<nav_msgs::msg::Odometry>("/state_estimation", 20);
    timer_ = create_wall_timer(
      std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::duration<double>(1.0 / follow_rate_)),
      [this]() { stepAndPublish(); });

    RCLCPP_INFO(
      get_logger(),
      "CLOSED_LOOP_FAKE_FOLLOWER_RUNNING topic=%s follow_rate=%.2f max_speed=%.2f real_flight_command=false",
      trajectory_topic.c_str(), follow_rate_, max_speed_);
  }

private:
  void stepAndPublish()
  {
    const double dt = 1.0 / follow_rate_;
    if (have_trajectory_ && (!emergency_stop_ || !stop_on_emergency_)) {
      while (target_index_ < trajectory_.poses.size()) {
        const auto & target = trajectory_.poses[target_index_].pose.position;
        const double dx = target.x - position_.x;
        const double dy = target.y - position_.y;
        const double dz = target.z - position_.z;
        const double distance = std::hypot(std::hypot(dx, dy), dz);
        if (distance > 0.08) {
          const double step = std::min(distance, max_speed_ * dt);
          position_.x += dx / distance * step;
          position_.y += dy / distance * step;
          position_.z += dz / distance * step;
          movement_distance_ += step;
          break;
        }
        ++target_index_;
      }
    }

    nav_msgs::msg::Odometry odom;
    odom.header.frame_id = frame_id_;
    odom.header.stamp = now();
    odom.child_frame_id = base_frame_id_;
    odom.pose.pose.position = position_;
    odom.pose.pose.orientation.w = 1.0;
    odom.twist.twist.linear.x = emergency_stop_ && stop_on_emergency_ ? 0.0 : max_speed_;
    odom_pub_->publish(odom);
    ++odom_count_;
    if (odom_count_ % static_cast<int>(std::max(1.0, follow_rate_)) == 0) {
      RCLCPP_INFO(
        get_logger(),
        "CLOSED_LOOP_FAKE_FOLLOWER_STATUS odom_count=%d movement_distance=%.3f emergency=%s real_flight_command=false",
        odom_count_, movement_distance_, emergency_stop_ ? "true" : "false");
    }
  }

  std::string frame_id_;
  std::string base_frame_id_;
  double follow_rate_{20.0};
  double max_speed_{0.8};
  bool use_safety_gate_output_{true};
  bool stop_on_emergency_{true};
  bool emergency_stop_{false};
  bool have_trajectory_{false};
  geometry_msgs::msg::Point position_;
  nav_msgs::msg::Path trajectory_;
  std::size_t target_index_{0};
  double movement_distance_{0.0};
  int odom_count_{0};
  rclcpp::Subscription<nav_msgs::msg::Path>::SharedPtr trajectory_sub_;
  rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr emergency_sub_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

}  // namespace fuel_ros2

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<fuel_ros2::ClosedLoopFakeFollower>());
  rclcpp::shutdown();
  return 0;
}
