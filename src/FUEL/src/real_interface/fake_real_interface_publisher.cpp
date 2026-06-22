#include <chrono>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <vector>

#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "sensor_msgs/msg/point_field.hpp"
#include "tf2/LinearMath/Quaternion.h"

using namespace std::chrono_literals;

namespace fuel_ros2
{

class FakeRealInterfacePublisher final : public rclcpp::Node
{
public:
  FakeRealInterfacePublisher() : Node("fake_real_interface_publisher")
  {
    global_frame_ = declare_parameter<std::string>("global_frame", "map");
    base_frame_ = declare_parameter<std::string>("base_frame", "base_link");
    odom_topic_ = declare_parameter<std::string>("odom_topic", "/state_estimation");
    global_cloud_topic_ = declare_parameter<std::string>("global_cloud_topic", "/mapping/global_cloud");
    local_cloud_topic_ = declare_parameter<std::string>("local_cloud_topic", "/mapping/local_cloud");
    occupied_cloud_topic_ = declare_parameter<std::string>("occupied_cloud_topic", "/mapping/occupied_cloud");
    free_cloud_topic_ = declare_parameter<std::string>("free_cloud_topic", "/mapping/free_cloud");
    publish_optional_clouds_ = declare_parameter<bool>("publish_optional_clouds", true);
    odom_pub_ = create_publisher<nav_msgs::msg::Odometry>(odom_topic_, 20);
    global_cloud_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>(global_cloud_topic_, rclcpp::SensorDataQoS());
    local_cloud_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>(local_cloud_topic_, rclcpp::SensorDataQoS());
    occupied_cloud_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>(occupied_cloud_topic_, rclcpp::SensorDataQoS());
    free_cloud_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>(free_cloud_topic_, rclcpp::SensorDataQoS());
    buildCloudPoints();
    odom_timer_ = create_wall_timer(50ms, [this]() {publishOdom();});
    cloud_timer_ = create_wall_timer(500ms, [this]() {publishClouds();});
    RCLCPP_INFO(
      get_logger(),
      "FAKE_REAL_INTERFACE_PUBLISHER_RUNNING odom=%s global_cloud=%s no_real_sensor=true",
      odom_topic_.c_str(), global_cloud_topic_.c_str());
  }

private:
  void buildCloudPoints()
  {
    points_.clear();
    for (double x = -6.0; x <= 6.0; x += 0.5) {
      for (double y = -4.0; y <= 4.0; y += 0.5) {
        points_.push_back({x, y, 0.1});
      }
    }
    for (double z = 0.4; z <= 2.4; z += 0.35) {
      points_.push_back({-2.0, -1.0, z});
      points_.push_back({2.5, 1.6, z});
    }
  }

  void publishOdom()
  {
    const auto now = get_clock()->now();
    const double t = now.seconds();
    nav_msgs::msg::Odometry odom;
    odom.header.stamp = now;
    odom.header.frame_id = global_frame_;
    odom.child_frame_id = base_frame_;
    odom.pose.pose.position.x = 1.5 * std::sin(0.1 * t);
    odom.pose.pose.position.y = 1.0 * std::cos(0.1 * t);
    odom.pose.pose.position.z = 1.2 + 0.2 * std::sin(0.2 * t);
    tf2::Quaternion q;
    q.setRPY(0.0, 0.0, 0.0);
    odom.pose.pose.orientation.x = q.x();
    odom.pose.pose.orientation.y = q.y();
    odom.pose.pose.orientation.z = q.z();
    odom.pose.pose.orientation.w = q.w();
    odom_pub_->publish(odom);
  }

  sensor_msgs::msg::PointCloud2 makeCloud()
  {
    sensor_msgs::msg::PointCloud2 cloud;
    cloud.header.stamp = get_clock()->now();
    cloud.header.frame_id = global_frame_;
    cloud.height = 1;
    cloud.width = static_cast<uint32_t>(points_.size());
    cloud.is_bigendian = false;
    cloud.is_dense = true;
    cloud.point_step = 12;
    cloud.row_step = cloud.point_step * cloud.width;
    cloud.fields.resize(3);
    const char * names[3] = {"x", "y", "z"};
    for (size_t i = 0; i < 3; ++i) {
      cloud.fields[i].name = names[i];
      cloud.fields[i].offset = static_cast<uint32_t>(i * 4);
      cloud.fields[i].datatype = sensor_msgs::msg::PointField::FLOAT32;
      cloud.fields[i].count = 1;
    }
    cloud.data.resize(cloud.row_step);
    for (size_t i = 0; i < points_.size(); ++i) {
      for (size_t j = 0; j < 3; ++j) {
        const float value = static_cast<float>(points_[i][j]);
        std::memcpy(&cloud.data[i * cloud.point_step + j * 4], &value, sizeof(float));
      }
    }
    return cloud;
  }

  void publishClouds()
  {
    const auto cloud = makeCloud();
    global_cloud_pub_->publish(cloud);
    if (publish_optional_clouds_) {
      local_cloud_pub_->publish(cloud);
      occupied_cloud_pub_->publish(cloud);
      free_cloud_pub_->publish(cloud);
    }
  }

  std::string global_frame_{"map"};
  std::string base_frame_{"base_link"};
  std::string odom_topic_{"/state_estimation"};
  std::string global_cloud_topic_{"/mapping/global_cloud"};
  std::string local_cloud_topic_{"/mapping/local_cloud"};
  std::string occupied_cloud_topic_{"/mapping/occupied_cloud"};
  std::string free_cloud_topic_{"/mapping/free_cloud"};
  bool publish_optional_clouds_{true};
  std::vector<std::array<double, 3>> points_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr global_cloud_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr local_cloud_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr occupied_cloud_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr free_cloud_pub_;
  rclcpp::TimerBase::SharedPtr odom_timer_;
  rclcpp::TimerBase::SharedPtr cloud_timer_;
};

}  // namespace fuel_ros2

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<fuel_ros2::FakeRealInterfacePublisher>());
  rclcpp::shutdown();
  return 0;
}
