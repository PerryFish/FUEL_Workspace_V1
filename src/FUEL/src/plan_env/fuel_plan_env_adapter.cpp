#include "fuel_ros2/plan_env/fuel_plan_env_adapter.hpp"

#include <algorithm>
#include <cmath>
#include <cstring>
#include <limits>

#include "geometry_msgs/msg/point.hpp"
#include "sensor_msgs/point_cloud2_iterator.hpp"
#include "sensor_msgs/msg/point_field.hpp"
#include "visualization_msgs/msg/marker.hpp"

namespace fuel_ros2
{

std::size_t FuelPlanEnvAdapter::GridIndexHash::operator()(const GridIndex & idx) const
{
  const std::size_t x = static_cast<std::size_t>(idx.x) * 73856093u;
  const std::size_t y = static_cast<std::size_t>(idx.y) * 19349663u;
  const std::size_t z = static_cast<std::size_t>(idx.z) * 83492791u;
  return x ^ y ^ z;
}

bool FuelPlanEnvAdapter::GridIndexEq::operator()(const GridIndex & a, const GridIndex & b) const
{
  return a.x == b.x && a.y == b.y && a.z == b.z;
}

bool FuelPlanEnvAdapter::initializeFromRos2Params(rclcpp::Node & node)
{
  frame_id_ = node.declare_parameter<std::string>("map.frame_id", frame_id_);
  resolution_ = node.declare_parameter<double>("map.resolution", resolution_);
  inflation_radius_ = node.declare_parameter<double>("map.inflation_radius", inflation_radius_);
  local_update_range_x_ = node.declare_parameter<double>("map.local_update_range_x", local_update_range_x_);
  local_update_range_y_ = node.declare_parameter<double>("map.local_update_range_y", local_update_range_y_);
  local_update_range_z_ = node.declare_parameter<double>("map.local_update_range_z", local_update_range_z_);
  min_.x() = node.declare_parameter<double>("map.min_x", min_.x());
  min_.y() = node.declare_parameter<double>("map.min_y", min_.y());
  min_.z() = node.declare_parameter<double>("map.min_z", min_.z());
  max_.x() = node.declare_parameter<double>("map.max_x", max_.x());
  max_.y() = node.declare_parameter<double>("map.max_y", max_.y());
  max_.z() = node.declare_parameter<double>("map.max_z", max_.z());
  enable_inflation_ = node.declare_parameter<bool>("plan_env.enable_inflation", enable_inflation_);
  enable_frontier_extraction_ =
    node.declare_parameter<bool>("plan_env.enable_frontier_extraction", enable_frontier_extraction_);

  if (resolution_ <= 0.0) {
    resolution_ = 0.2;
  }
  if (inflation_radius_ < 0.0) {
    inflation_radius_ = 0.0;
  }
  reset();
  return true;
}

void FuelPlanEnvAdapter::reset()
{
  occupied_.clear();
  inflated_.clear();
}

bool FuelPlanEnvAdapter::updateFromPointCloud(const sensor_msgs::msg::PointCloud2 & cloud_msg)
{
  if (cloud_msg.width == 0 || cloud_msg.point_step == 0) {
    return false;
  }

  std::unordered_set<GridIndex, GridIndexHash, GridIndexEq> next_occupied;
  sensor_msgs::PointCloud2ConstIterator<float> iter_x(cloud_msg, "x");
  sensor_msgs::PointCloud2ConstIterator<float> iter_y(cloud_msg, "y");
  sensor_msgs::PointCloud2ConstIterator<float> iter_z(cloud_msg, "z");
  for (; iter_x != iter_x.end(); ++iter_x, ++iter_y, ++iter_z) {
    const Eigen::Vector3d p(*iter_x, *iter_y, *iter_z);
    if (!isInsideMap(p)) {
      continue;
    }
    if (has_odom_) {
      const Eigen::Vector3d d = p - last_odom_;
      if (std::abs(d.x()) > local_update_range_x_ ||
        std::abs(d.y()) > local_update_range_y_ ||
        std::abs(d.z()) > local_update_range_z_)
      {
        continue;
      }
    }
    next_occupied.insert(pointToIndex(p));
  }
  occupied_.swap(next_occupied);
  rebuildInflation();
  return true;
}

bool FuelPlanEnvAdapter::updateOdometry(const nav_msgs::msg::Odometry & odom_msg)
{
  last_odom_.x() = odom_msg.pose.pose.position.x;
  last_odom_.y() = odom_msg.pose.pose.position.y;
  last_odom_.z() = odom_msg.pose.pose.position.z;
  has_odom_ = true;
  return true;
}

bool FuelPlanEnvAdapter::isInsideMap(const Eigen::Vector3d & p) const
{
  return p.x() >= min_.x() && p.y() >= min_.y() && p.z() >= min_.z() &&
    p.x() <= max_.x() && p.y() <= max_.y() && p.z() <= max_.z();
}

bool FuelPlanEnvAdapter::isOccupied(const Eigen::Vector3d & p) const
{
  if (!isInsideMap(p)) {
    return false;
  }
  return inflated_.find(pointToIndex(p)) != inflated_.end();
}

double FuelPlanEnvAdapter::getDistance(const Eigen::Vector3d & p) const
{
  if (!isInsideMap(p)) {
    return -1.0;
  }
  if (occupied_.empty()) {
    return std::numeric_limits<double>::infinity();
  }
  double best = std::numeric_limits<double>::infinity();
  for (const auto & idx : occupied_) {
    best = std::min(best, (indexToPoint(idx) - p).norm());
  }
  return best;
}

std::vector<Eigen::Vector3d> FuelPlanEnvAdapter::extractSimpleFrontiers() const
{
  std::vector<Eigen::Vector3d> frontiers;
  if (!enable_frontier_extraction_) {
    return frontiers;
  }
  frontiers.reserve(std::min<std::size_t>(occupied_.size(), 64));
  for (const auto & idx : occupied_) {
    GridIndex up{idx.x, idx.y, idx.z + 1};
    if (inflated_.find(up) == inflated_.end()) {
      frontiers.push_back(indexToPoint(up));
      if (frontiers.size() >= 64) {
        break;
      }
    }
  }
  return frontiers;
}

sensor_msgs::msg::PointCloud2 FuelPlanEnvAdapter::exportOccupiedCloudMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  return exportCloud(occupied_, frame_id, stamp);
}

sensor_msgs::msg::PointCloud2 FuelPlanEnvAdapter::exportInflatedCloudMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  return exportCloud(inflated_, frame_id, stamp);
}

visualization_msgs::msg::MarkerArray FuelPlanEnvAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  visualization_msgs::msg::Marker frontier;
  frontier.header.frame_id = frame_id;
  frontier.header.stamp = stamp;
  frontier.ns = "fuel_plan_env_frontiers";
  frontier.id = 1;
  frontier.type = visualization_msgs::msg::Marker::SPHERE_LIST;
  frontier.action = visualization_msgs::msg::Marker::ADD;
  frontier.scale.x = resolution_;
  frontier.scale.y = resolution_;
  frontier.scale.z = resolution_;
  frontier.color.r = 0.95f;
  frontier.color.g = 0.25f;
  frontier.color.b = 0.2f;
  frontier.color.a = 0.9f;
  for (const auto & p : extractSimpleFrontiers()) {
    geometry_msgs::msg::Point point;
    point.x = p.x();
    point.y = p.y();
    point.z = p.z();
    frontier.points.push_back(point);
  }
  array.markers.push_back(frontier);
  return array;
}

std::size_t FuelPlanEnvAdapter::occupiedVoxelCount() const
{
  return occupied_.size();
}

std::size_t FuelPlanEnvAdapter::inflatedVoxelCount() const
{
  return inflated_.size();
}

FuelPlanEnvAdapter::GridIndex FuelPlanEnvAdapter::pointToIndex(const Eigen::Vector3d & p) const
{
  return GridIndex{
    static_cast<int>(std::floor((p.x() - min_.x()) / resolution_)),
    static_cast<int>(std::floor((p.y() - min_.y()) / resolution_)),
    static_cast<int>(std::floor((p.z() - min_.z()) / resolution_))};
}

Eigen::Vector3d FuelPlanEnvAdapter::indexToPoint(const GridIndex & idx) const
{
  return Eigen::Vector3d(
    min_.x() + (static_cast<double>(idx.x) + 0.5) * resolution_,
    min_.y() + (static_cast<double>(idx.y) + 0.5) * resolution_,
    min_.z() + (static_cast<double>(idx.z) + 0.5) * resolution_);
}

void FuelPlanEnvAdapter::rebuildInflation()
{
  inflated_.clear();
  if (!enable_inflation_ || inflation_radius_ <= 0.0) {
    inflated_ = occupied_;
    return;
  }
  const int cells = static_cast<int>(std::ceil(inflation_radius_ / resolution_));
  for (const auto & idx : occupied_) {
    for (int dx = -cells; dx <= cells; ++dx) {
      for (int dy = -cells; dy <= cells; ++dy) {
        for (int dz = -cells; dz <= cells; ++dz) {
          GridIndex inflated_idx{idx.x + dx, idx.y + dy, idx.z + dz};
          const double dist = std::sqrt(dx * dx + dy * dy + dz * dz) * resolution_;
          if (dist <= inflation_radius_ && isInsideMap(indexToPoint(inflated_idx))) {
            inflated_.insert(inflated_idx);
          }
        }
      }
    }
  }
}

sensor_msgs::msg::PointCloud2 FuelPlanEnvAdapter::exportCloud(
  const std::unordered_set<GridIndex, GridIndexHash, GridIndexEq> & voxels,
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  sensor_msgs::msg::PointCloud2 cloud;
  cloud.header.frame_id = frame_id.empty() ? frame_id_ : frame_id;
  const int64_t ns = stamp.nanoseconds();
  cloud.header.stamp.sec = static_cast<int32_t>(ns / 1000000000LL);
  cloud.header.stamp.nanosec = static_cast<uint32_t>(ns % 1000000000LL);
  cloud.height = 1;
  cloud.width = static_cast<uint32_t>(voxels.size());
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
  size_t i = 0;
  for (const auto & idx : voxels) {
    const Eigen::Vector3d p = indexToPoint(idx);
    const float values[3] = {
      static_cast<float>(p.x()),
      static_cast<float>(p.y()),
      static_cast<float>(p.z())};
    std::memcpy(&cloud.data[i * cloud.point_step], &values[0], sizeof(float));
    std::memcpy(&cloud.data[i * cloud.point_step + 4], &values[1], sizeof(float));
    std::memcpy(&cloud.data[i * cloud.point_step + 8], &values[2], sizeof(float));
    ++i;
  }
  return cloud;
}

}  // namespace fuel_ros2
