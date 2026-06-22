#include "fuel_ros2/frontier_fis/fuel_frontier_fis_adapter.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <queue>
#include <string>

#include "geometry_msgs/msg/point.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "visualization_msgs/msg/marker.hpp"

namespace fuel_ros2
{

bool FuelFrontierFisAdapter::initializeFromRos2Params(rclcpp::Node & node)
{
  auto get_bool = [&node](const std::string & name, bool fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<bool>(name, fallback);
      }
      return node.get_parameter(name).as_bool();
    };
  auto get_int = [&node](const std::string & name, int fallback) -> int {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<int>(name, fallback);
      }
      return static_cast<int>(node.get_parameter(name).as_int());
    };
  auto get_double = [&node](const std::string & name, double fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<double>(name, fallback);
      }
      return node.get_parameter(name).as_double();
    };

  enabled_ = get_bool("frontier_fis.enable_frontier_fis", enabled_);
  std::string backend = "mvp";
  if (node.has_parameter("planner_backend")) {
    backend = node.get_parameter("planner_backend").as_string();
  }
  enabled_ = enabled_ || backend == "fuel_frontier_fis";
  use_frontier_goal_source_ = get_bool("frontier_fis.use_frontier_goal_source", use_frontier_goal_source_);
  min_frontier_cluster_size_ = get_int("frontier_fis.min_frontier_cluster_size", min_frontier_cluster_size_);
  max_frontier_cluster_size_ = get_int("frontier_fis.max_frontier_cluster_size", max_frontier_cluster_size_);
  frontier_resolution_ = get_double("frontier_fis.frontier_resolution", frontier_resolution_);
  viewpoint_distance_ = get_double("frontier_fis.viewpoint_distance", viewpoint_distance_);
  viewpoint_z_min_ = get_double("frontier_fis.viewpoint_z_min", viewpoint_z_min_);
  viewpoint_z_max_ = get_double("frontier_fis.viewpoint_z_max", viewpoint_z_max_);
  information_gain_weight_ = get_double("frontier_fis.information_gain_weight", information_gain_weight_);
  distance_cost_weight_ = get_double("frontier_fis.distance_cost_weight", distance_cost_weight_);
  z_penalty_weight_ = get_double("frontier_fis.z_penalty_weight", z_penalty_weight_);
  max_frontier_markers_ = get_int("frontier_fis.max_frontier_markers", max_frontier_markers_);

  min_frontier_cluster_size_ = std::max(1, min_frontier_cluster_size_);
  max_frontier_cluster_size_ = std::max(min_frontier_cluster_size_, max_frontier_cluster_size_);
  frontier_resolution_ = std::max(0.05, frontier_resolution_);
  viewpoint_distance_ = std::max(0.2, viewpoint_distance_);
  if (viewpoint_z_max_ < viewpoint_z_min_) {
    std::swap(viewpoint_z_min_, viewpoint_z_max_);
  }
  status_ = enabled_ ? "FIS_BACKEND_PARTIAL" : "FIS_DISABLED";
  return true;
}

void FuelFrontierFisAdapter::reset()
{
  frontier_candidates_.clear();
  clusters_.clear();
  viewpoints_.clear();
  status_ = enabled_ ? "FIS_BACKEND_PARTIAL" : "FIS_DISABLED";
}

bool FuelFrontierFisAdapter::updateMapFromPlanEnv(const FuelPlanEnvAdapter & plan_env)
{
  if (!enabled_) {
    status_ = "FIS_DISABLED";
    return false;
  }
  frontier_candidates_ = plan_env.extractSimpleFrontiers();
  if (frontier_candidates_.empty()) {
    clusters_.clear();
    viewpoints_.clear();
    status_ = "FIS_NO_FRONTIER_FALLBACK_MVP";
    return false;
  }
  return true;
}

bool FuelFrontierFisAdapter::updateOdometry(const nav_msgs::msg::Odometry & odom_msg)
{
  odom_.x() = odom_msg.pose.pose.position.x;
  odom_.y() = odom_msg.pose.pose.position.y;
  odom_.z() = odom_msg.pose.pose.position.z;
  has_odom_ = true;
  return true;
}

bool FuelFrontierFisAdapter::extractFrontierClusters()
{
  if (!enabled_) {
    status_ = "FIS_DISABLED";
    return false;
  }
  clusterCandidates();
  if (clusters_.empty()) {
    status_ = "FIS_NO_FRONTIER_FALLBACK_MVP";
    return false;
  }
  status_ = "FIS_BACKEND_PARTIAL";
  return true;
}

bool FuelFrontierFisAdapter::generateViewpoints()
{
  viewpoints_.clear();
  if (!enabled_ || clusters_.empty()) {
    status_ = enabled_ ? "FIS_NO_FRONTIER_FALLBACK_MVP" : "FIS_DISABLED";
    return false;
  }

  for (auto & cluster : clusters_) {
    const Eigen::Vector3d origin = has_odom_ ? odom_ : Eigen::Vector3d::Zero();
    Eigen::Vector3d away = cluster.center - origin;
    away.z() = 0.0;
    if (away.norm() < 1e-3) {
      away = Eigen::Vector3d(1.0, 0.0, 0.0);
    }
    away.normalize();

    FuelViewpointCandidate view;
    view.cluster_id = cluster.id;
    view.position = cluster.center - away * viewpoint_distance_;
    view.position.z() = std::min(viewpoint_z_max_, std::max(viewpoint_z_min_, cluster.center.z()));
    view.yaw = yawToTarget(view.position, cluster.center);
    view.visible_unknown_count = cluster.information_gain;
    view.distance_cost = (view.position - origin).norm();
    view.collision_safe = true;
    const double penalty = zPenalty(view.position);
    view.utility = information_gain_weight_ * view.visible_unknown_count -
      distance_cost_weight_ * view.distance_cost - z_penalty_weight_ * penalty;
    cluster.distance_cost = view.distance_cost;
    cluster.utility = view.utility;
    viewpoints_.push_back(view);
  }

  std::sort(viewpoints_.begin(), viewpoints_.end(), [](const auto & a, const auto & b) {
    return a.utility > b.utility;
  });
  status_ = viewpoints_.empty() ? "FIS_NO_FRONTIER_FALLBACK_MVP" : "FIS_BACKEND_PARTIAL";
  return !viewpoints_.empty();
}

std::vector<Eigen::Vector3d> FuelFrontierFisAdapter::getFrontierCenters() const
{
  std::vector<Eigen::Vector3d> centers;
  centers.reserve(clusters_.size());
  for (const auto & cluster : clusters_) {
    centers.push_back(cluster.center);
  }
  return centers;
}

std::vector<Eigen::Vector3d> FuelFrontierFisAdapter::getBestViewpoints() const
{
  std::vector<Eigen::Vector3d> points;
  points.reserve(viewpoints_.size());
  for (const auto & view : viewpoints_) {
    points.push_back(view.position);
  }
  return points;
}

bool FuelFrontierFisAdapter::hasBestViewpoint() const
{
  return !viewpoints_.empty();
}

FuelViewpointCandidate FuelFrontierFisAdapter::bestViewpoint() const
{
  if (viewpoints_.empty()) {
    return FuelViewpointCandidate{};
  }
  return viewpoints_.front();
}

visualization_msgs::msg::MarkerArray FuelFrontierFisAdapter::exportFrontierMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  visualization_msgs::msg::Marker cells;
  cells.header.frame_id = frame_id;
  cells.header.stamp = stamp;
  cells.ns = "fuel_fis_frontier_cells";
  cells.id = 1;
  cells.type = visualization_msgs::msg::Marker::SPHERE_LIST;
  cells.action = visualization_msgs::msg::Marker::ADD;
  cells.scale.x = frontier_resolution_;
  cells.scale.y = frontier_resolution_;
  cells.scale.z = frontier_resolution_;
  cells.color.r = 0.0f;
  cells.color.g = 0.9f;
  cells.color.b = 0.95f;
  cells.color.a = 0.9f;

  int count = 0;
  for (const auto & cluster : clusters_) {
    for (const auto & p : cluster.cells) {
      if (count++ >= max_frontier_markers_) {
        break;
      }
      geometry_msgs::msg::Point point;
      point.x = p.x();
      point.y = p.y();
      point.z = p.z();
      cells.points.push_back(point);
    }
    if (count >= max_frontier_markers_) {
      break;
    }
  }
  array.markers.push_back(cells);

  visualization_msgs::msg::Marker centers;
  centers.header = cells.header;
  centers.ns = "fuel_fis_frontier_centers";
  centers.id = 2;
  centers.type = visualization_msgs::msg::Marker::CUBE_LIST;
  centers.action = visualization_msgs::msg::Marker::ADD;
  centers.scale.x = 0.35;
  centers.scale.y = 0.35;
  centers.scale.z = 0.35;
  centers.color.r = 1.0f;
  centers.color.g = 0.45f;
  centers.color.b = 0.05f;
  centers.color.a = 1.0f;
  for (const auto & cluster : clusters_) {
    geometry_msgs::msg::Point point;
    point.x = cluster.center.x();
    point.y = cluster.center.y();
    point.z = cluster.center.z();
    centers.points.push_back(point);
  }
  array.markers.push_back(centers);
  return array;
}

visualization_msgs::msg::MarkerArray FuelFrontierFisAdapter::exportViewpointMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  visualization_msgs::msg::Marker views;
  views.header.frame_id = frame_id;
  views.header.stamp = stamp;
  views.ns = "fuel_fis_viewpoints";
  views.id = 1;
  views.type = visualization_msgs::msg::Marker::SPHERE_LIST;
  views.action = visualization_msgs::msg::Marker::ADD;
  views.scale.x = 0.28;
  views.scale.y = 0.28;
  views.scale.z = 0.28;
  views.color.r = 0.15f;
  views.color.g = 1.0f;
  views.color.b = 0.25f;
  views.color.a = 1.0f;
  for (const auto & view : viewpoints_) {
    geometry_msgs::msg::Point point;
    point.x = view.position.x();
    point.y = view.position.y();
    point.z = view.position.z();
    views.points.push_back(point);
  }
  array.markers.push_back(views);
  return array;
}

visualization_msgs::msg::MarkerArray FuelFrontierFisAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  auto array = exportFrontierMarkers(frame_id, stamp);
  auto viewpoints = exportViewpointMarkers(frame_id, stamp);
  array.markers.insert(array.markers.end(), viewpoints.markers.begin(), viewpoints.markers.end());
  return array;
}

geometry_msgs::msg::PoseStamped FuelFrontierFisAdapter::exportBestViewpointMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  geometry_msgs::msg::PoseStamped pose;
  pose.header.frame_id = frame_id;
  pose.header.stamp = stamp;
  const auto view = bestViewpoint();
  pose.pose.position.x = view.position.x();
  pose.pose.position.y = view.position.y();
  pose.pose.position.z = view.position.z();
  tf2::Quaternion q;
  q.setRPY(0.0, 0.0, view.yaw);
  pose.pose.orientation.x = q.x();
  pose.pose.orientation.y = q.y();
  pose.pose.orientation.z = q.z();
  pose.pose.orientation.w = q.w();
  return pose;
}

std_msgs::msg::String FuelFrontierFisAdapter::exportStatusMsg() const
{
  std_msgs::msg::String msg;
  msg.data = status_ + " clusters=" + std::to_string(clusters_.size()) +
    " viewpoints=" + std::to_string(viewpoints_.size()) +
    " candidates=" + std::to_string(frontier_candidates_.size());
  return msg;
}

std::size_t FuelFrontierFisAdapter::clusterCount() const
{
  return clusters_.size();
}

std::size_t FuelFrontierFisAdapter::viewpointCount() const
{
  return viewpoints_.size();
}

bool FuelFrontierFisAdapter::isPartial() const
{
  return true;
}

void FuelFrontierFisAdapter::clusterCandidates()
{
  clusters_.clear();
  if (frontier_candidates_.empty()) {
    return;
  }

  std::vector<char> visited(frontier_candidates_.size(), 0);
  int next_id = 0;
  const double neighbor_radius = frontier_resolution_ * 2.5;
  for (std::size_t i = 0; i < frontier_candidates_.size(); ++i) {
    if (visited[i]) {
      continue;
    }
    std::queue<std::size_t> queue;
    queue.push(i);
    visited[i] = 1;
    FuelFrontierCluster cluster;
    cluster.id = next_id++;

    while (!queue.empty()) {
      const auto idx = queue.front();
      queue.pop();
      cluster.cells.push_back(frontier_candidates_[idx]);
      if (static_cast<int>(cluster.cells.size()) >= max_frontier_cluster_size_) {
        continue;
      }
      for (std::size_t j = 0; j < frontier_candidates_.size(); ++j) {
        if (visited[j]) {
          continue;
        }
        if ((frontier_candidates_[idx] - frontier_candidates_[j]).norm() <= neighbor_radius) {
          visited[j] = 1;
          queue.push(j);
        }
      }
    }

    if (static_cast<int>(cluster.cells.size()) < min_frontier_cluster_size_) {
      continue;
    }
    cluster.center = Eigen::Vector3d::Zero();
    for (const auto & p : cluster.cells) {
      cluster.center += p;
    }
    cluster.center /= static_cast<double>(cluster.cells.size());
    cluster.information_gain = static_cast<double>(cluster.cells.size());
    cluster.distance_cost = has_odom_ ? (cluster.center - odom_).norm() : 0.0;
    cluster.utility = information_gain_weight_ * cluster.information_gain -
      distance_cost_weight_ * cluster.distance_cost;
    clusters_.push_back(cluster);
  }

  std::sort(clusters_.begin(), clusters_.end(), [](const auto & a, const auto & b) {
    return a.utility > b.utility;
  });
  for (std::size_t i = 0; i < clusters_.size(); ++i) {
    clusters_[i].id = static_cast<int>(i);
  }
}

double FuelFrontierFisAdapter::zPenalty(const Eigen::Vector3d & p) const
{
  if (p.z() < viewpoint_z_min_) {
    return viewpoint_z_min_ - p.z();
  }
  if (p.z() > viewpoint_z_max_) {
    return p.z() - viewpoint_z_max_;
  }
  return 0.0;
}

double FuelFrontierFisAdapter::yawToTarget(const Eigen::Vector3d & from, const Eigen::Vector3d & to)
{
  return std::atan2(to.y() - from.y(), to.x() - from.x());
}

}  // namespace fuel_ros2
