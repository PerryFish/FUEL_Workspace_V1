#include "fuel_ros2/bspline_traj/fuel_bspline_traj_adapter.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <sstream>

#include "geometry_msgs/msg/point.hpp"
#include "visualization_msgs/msg/marker.hpp"

#include "fuel_ros2/plan_env/fuel_plan_env_adapter.hpp"

namespace fuel_ros2
{

bool FuelBsplineTrajAdapter::initializeFromRos2Params(const rclcpp::Node::SharedPtr & node)
{
  return node ? initializeFromRos2Params(*node) : false;
}

bool FuelBsplineTrajAdapter::initializeFromRos2Params(rclcpp::Node & node)
{
  auto get_bool = [&node](const std::string & name, bool fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<bool>(name, fallback);
      }
      return node.get_parameter(name).as_bool();
    };
  auto get_double = [&node](const std::string & name, double fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<double>(name, fallback);
      }
      return node.get_parameter(name).as_double();
    };
  auto get_int = [&node](const std::string & name, int fallback) -> int {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<int>(name, fallback);
      }
      return static_cast<int>(node.get_parameter(name).as_int());
    };
  auto get_string = [&node](const std::string & name, const std::string & fallback) {
      if (!node.has_parameter(name)) {
        return node.declare_parameter<std::string>(name, fallback);
      }
      return node.get_parameter(name).as_string();
    };

  enabled_ = get_bool("bspline_traj.enable_bspline_traj", enabled_);
  if (node.has_parameter("planner_backend") &&
    node.get_parameter("planner_backend").as_string() == "fuel_bspline_traj")
  {
    enabled_ = true;
  }
  use_bspline_for_stable_output_ =
    get_bool("bspline_traj.use_bspline_for_stable_output", use_bspline_for_stable_output_);
  input_path_topic_ = get_string("bspline_traj.input_path_topic", input_path_topic_);
  algorithm_ = get_string("bspline_traj.algorithm", algorithm_);
  spline_order_ = get_int("bspline_traj.spline_order", spline_order_);
  sample_dt_ = get_double("bspline_traj.sample_dt", sample_dt_);
  control_point_spacing_ = get_double("bspline_traj.control_point_spacing", control_point_spacing_);
  max_velocity_ = get_double("bspline_traj.max_velocity", max_velocity_);
  max_acceleration_ = get_double("bspline_traj.max_acceleration", max_acceleration_);
  safety_distance_ = get_double("bspline_traj.safety_distance", safety_distance_);
  collision_check_resolution_ =
    get_double("bspline_traj.collision_check_resolution", collision_check_resolution_);
  allow_path_as_trajectory_fallback_ =
    get_bool("bspline_traj.allow_path_as_trajectory_fallback", allow_path_as_trajectory_fallback_);

  if (algorithm_ != "uniform_bspline_lite") {
    algorithm_ = "uniform_bspline_lite";
  }
  if (spline_order_ < 3) {
    spline_order_ = 3;
  }
  if (sample_dt_ <= 0.0) {
    sample_dt_ = 0.1;
  }
  if (control_point_spacing_ <= 0.0) {
    control_point_spacing_ = 0.5;
  }
  if (max_velocity_ <= 0.0) {
    max_velocity_ = 3.0;
  }
  if (max_acceleration_ <= 0.0) {
    max_acceleration_ = 2.0;
  }
  safety_distance_ = std::max(0.0, safety_distance_);
  collision_check_resolution_ = std::max(0.02, collision_check_resolution_);
  reset();
  return enabled_;
}

void FuelBsplineTrajAdapter::reset()
{
  status_ = FuelBsplineTrajStatus::IDLE;
  last_failure_reason_ = "none";
  control_points_.clear();
  sampled_trajectory_.clear();
  last_duration_ms_ = 0.0;
  last_trajectory_length_ = 0.0;
}

bool FuelBsplineTrajAdapter::setPlanEnv(const FuelPlanEnvAdapter * plan_env)
{
  plan_env_ = plan_env;
  return plan_env_ != nullptr;
}

bool FuelBsplineTrajAdapter::generateFromPath(const std::vector<Eigen::Vector3d> & path_points)
{
  ++generation_count_;
  status_ = FuelBsplineTrajStatus::GENERATING;
  last_failure_reason_ = "none";
  control_points_.clear();
  sampled_trajectory_.clear();
  last_trajectory_length_ = 0.0;
  const auto start_time = std::chrono::steady_clock::now();
  auto finish_timing = [this, &start_time]() {
      const auto end_time = std::chrono::steady_clock::now();
      last_duration_ms_ =
        std::chrono::duration<double, std::milli>(end_time - start_time).count();
    };

  if (path_points.empty()) {
    status_ = FuelBsplineTrajStatus::FAILED_NO_PATH;
    last_failure_reason_ = "no_path";
    ++failure_count_;
    finish_timing();
    return false;
  }
  if (path_points.size() < 3) {
    status_ = FuelBsplineTrajStatus::FAILED_TOO_FEW_POINTS;
    last_failure_reason_ = "too_few_points";
    ++failure_count_;
    const bool fallback = allow_path_as_trajectory_fallback_ && makePathFallback(path_points);
    finish_timing();
    return fallback ? false : false;
  }

  control_points_ = buildControlPoints(path_points);
  sampled_trajectory_ = sampleCatmullRom(control_points_);
  if (sampled_trajectory_.size() < 2) {
    status_ = FuelBsplineTrajStatus::FAILED_TOO_FEW_POINTS;
    last_failure_reason_ = "too_few_sampled_points";
    ++failure_count_;
    const bool fallback = allow_path_as_trajectory_fallback_ && makePathFallback(path_points);
    finish_timing();
    return fallback ? false : false;
  }
  last_trajectory_length_ = pathLength(sampled_trajectory_);
  if (!validateSampledTrajectory()) {
    ++failure_count_;
    const bool fallback = allow_path_as_trajectory_fallback_ && makePathFallback(path_points);
    finish_timing();
    return fallback ? false : false;
  }

  status_ = FuelBsplineTrajStatus::SUCCESS;
  ++success_count_;
  finish_timing();
  return true;
}

std::vector<Eigen::Vector3d> FuelBsplineTrajAdapter::getControlPoints() const
{
  return control_points_;
}

std::vector<Eigen::Vector3d> FuelBsplineTrajAdapter::getSampledTrajectory() const
{
  return sampled_trajectory_;
}

FuelBsplineTrajStatus FuelBsplineTrajAdapter::status() const
{
  return status_;
}

std::string FuelBsplineTrajAdapter::statusString() const
{
  return statusToString(status_);
}

std::string FuelBsplineTrajAdapter::backendStatusString() const
{
  if (status_ == FuelBsplineTrajStatus::SUCCESS) {
    return "BSPLINE_TRAJ_SUCCESS";
  }
  if (status_ == FuelBsplineTrajStatus::FALLBACK_PATH_AS_TRAJECTORY) {
    return "BSPLINE_TRAJ_FAILED_FALLBACK_PATH";
  }
  if (status_ == FuelBsplineTrajStatus::FAILED_NO_PATH ||
    status_ == FuelBsplineTrajStatus::FAILED_TOO_FEW_POINTS ||
    status_ == FuelBsplineTrajStatus::FAILED_COLLISION_RISK ||
    status_ == FuelBsplineTrajStatus::FAILED_DYNAMIC_LIMIT)
  {
    return "BSPLINE_TRAJ_FAILED_FALLBACK_MVP";
  }
  return enabled_ ? "BSPLINE_TRAJ_BACKEND_PARTIAL" : "BSPLINE_TRAJ_BACKEND_RUNNING";
}

std::string FuelBsplineTrajAdapter::lastFailureReason() const {return last_failure_reason_;}
double FuelBsplineTrajAdapter::lastDurationMs() const {return last_duration_ms_;}
double FuelBsplineTrajAdapter::lastTrajectoryLength() const {return last_trajectory_length_;}
bool FuelBsplineTrajAdapter::useForStableOutput() const {return use_bspline_for_stable_output_;}
int FuelBsplineTrajAdapter::generationCount() const {return generation_count_;}
int FuelBsplineTrajAdapter::successCount() const {return success_count_;}
int FuelBsplineTrajAdapter::failureCount() const {return failure_count_;}
int FuelBsplineTrajAdapter::fallbackCount() const {return fallback_count_;}

nav_msgs::msg::Path FuelBsplineTrajAdapter::exportSampledTrajectoryMsg(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  nav_msgs::msg::Path msg;
  msg.header.frame_id = frame_id;
  msg.header.stamp = stamp;
  for (const auto & p : sampled_trajectory_) {
    geometry_msgs::msg::PoseStamped pose;
    pose.header = msg.header;
    pose.pose.position.x = p.x();
    pose.pose.position.y = p.y();
    pose.pose.position.z = p.z();
    pose.pose.orientation.w = 1.0;
    msg.poses.push_back(pose);
  }
  return msg;
}

visualization_msgs::msg::MarkerArray FuelBsplineTrajAdapter::exportControlPointMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  visualization_msgs::msg::MarkerArray array;
  visualization_msgs::msg::Marker points;
  points.header.frame_id = frame_id;
  points.header.stamp = stamp;
  points.ns = "fuel_bspline_control_points";
  points.id = 0;
  points.type = visualization_msgs::msg::Marker::SPHERE_LIST;
  points.action = visualization_msgs::msg::Marker::ADD;
  points.scale.x = 0.18;
  points.scale.y = 0.18;
  points.scale.z = 0.18;
  points.color.r = 1.0f;
  points.color.g = 0.8f;
  points.color.b = 0.05f;
  points.color.a = 1.0f;
  for (const auto & p : control_points_) {
    geometry_msgs::msg::Point point;
    point.x = p.x();
    point.y = p.y();
    point.z = p.z();
    points.points.push_back(point);
  }
  array.markers.push_back(points);
  return array;
}

visualization_msgs::msg::MarkerArray FuelBsplineTrajAdapter::exportDebugMarkers(
  const std::string & frame_id,
  const rclcpp::Time & stamp) const
{
  auto array = exportControlPointMarkers(frame_id, stamp);
  visualization_msgs::msg::Marker line;
  line.header.frame_id = frame_id;
  line.header.stamp = stamp;
  line.ns = "fuel_bspline_sampled_trajectory";
  line.id = 1;
  line.type = visualization_msgs::msg::Marker::LINE_STRIP;
  line.action = visualization_msgs::msg::Marker::ADD;
  line.scale.x = 0.07;
  line.color.r = 0.0f;
  line.color.g = 0.9f;
  line.color.b = 0.65f;
  line.color.a = 1.0f;
  for (const auto & p : sampled_trajectory_) {
    geometry_msgs::msg::Point point;
    point.x = p.x();
    point.y = p.y();
    point.z = p.z();
    line.points.push_back(point);
  }
  array.markers.push_back(line);
  return array;
}

std_msgs::msg::String FuelBsplineTrajAdapter::exportStatusMsg() const
{
  std_msgs::msg::String msg;
  std::ostringstream ss;
  ss << backendStatusString()
     << " status=" << statusString()
     << " algorithm=" << algorithm_
     << " generations=" << generation_count_
     << " success=" << success_count_
     << " failures=" << failure_count_
     << " fallback=" << fallback_count_
     << " control_points=" << control_points_.size()
     << " sampled_points=" << sampled_trajectory_.size()
     << " length=" << last_trajectory_length_
     << " duration_ms=" << last_duration_ms_
     << " stable_output=" << (use_bspline_for_stable_output_ ? "enabled" : "disabled")
     << " reason=" << last_failure_reason_;
  msg.data = ss.str();
  return msg;
}

std::vector<Eigen::Vector3d> FuelBsplineTrajAdapter::buildControlPoints(
  const std::vector<Eigen::Vector3d> & path_points) const
{
  std::vector<Eigen::Vector3d> out;
  out.reserve(path_points.size() + 2);
  out.push_back(path_points.front());
  for (const auto & p : path_points) {
    if (out.empty() || (p - out.back()).norm() >= 1e-6) {
      out.push_back(p);
    }
  }
  if ((out.back() - path_points.back()).norm() > 1e-6) {
    out.push_back(path_points.back());
  }
  return out;
}

std::vector<Eigen::Vector3d> FuelBsplineTrajAdapter::sampleCatmullRom(
  const std::vector<Eigen::Vector3d> & control_points) const
{
  std::vector<Eigen::Vector3d> out;
  if (control_points.size() < 3) {
    return out;
  }
  out.push_back(control_points.front());
  for (std::size_t i = 0; i + 1 < control_points.size(); ++i) {
    const Eigen::Vector3d & p0 = i == 0 ? control_points[i] : control_points[i - 1];
    const Eigen::Vector3d & p1 = control_points[i];
    const Eigen::Vector3d & p2 = control_points[i + 1];
    const Eigen::Vector3d & p3 =
      (i + 2 < control_points.size()) ? control_points[i + 2] : control_points[i + 1];
    const double segment_length = std::max(1e-6, (p2 - p1).norm());
    const double dynamic_spacing = std::max(0.02, max_velocity_ * sample_dt_ * 0.8);
    const double sample_spacing = std::min(control_point_spacing_, dynamic_spacing);
    const int samples = std::max(2, static_cast<int>(std::ceil(segment_length / sample_spacing)));
    for (int j = 1; j <= samples; ++j) {
      const double t = static_cast<double>(j) / static_cast<double>(samples);
      out.push_back(catmullRom(p0, p1, p2, p3, t));
    }
  }
  out.front() = control_points.front();
  out.back() = control_points.back();
  return out;
}

bool FuelBsplineTrajAdapter::validateSampledTrajectory()
{
  if (sampled_trajectory_.empty()) {
    status_ = FuelBsplineTrajStatus::FAILED_NO_PATH;
    last_failure_reason_ = "empty_sampled_trajectory";
    return false;
  }
  if (plan_env_) {
    for (const auto & p : sampled_trajectory_) {
      if (!plan_env_->isInsideMap(p) || plan_env_->isOccupied(p)) {
        status_ = FuelBsplineTrajStatus::FAILED_COLLISION_RISK;
        last_failure_reason_ = "sample_collision_or_outside_map";
        return false;
      }
      const double distance = plan_env_->getDistance(p);
      if (std::isfinite(distance) && distance < safety_distance_) {
        status_ = FuelBsplineTrajStatus::FAILED_COLLISION_RISK;
        last_failure_reason_ = "sample_below_safety_distance";
        return false;
      }
    }
  }
  for (std::size_t i = 1; i < sampled_trajectory_.size(); ++i) {
    const double v = (sampled_trajectory_[i] - sampled_trajectory_[i - 1]).norm() / sample_dt_;
    if (v > max_velocity_ * 1.5) {
      status_ = FuelBsplineTrajStatus::FAILED_DYNAMIC_LIMIT;
      last_failure_reason_ = "velocity_limit";
      return false;
    }
  }
  for (std::size_t i = 2; i < sampled_trajectory_.size(); ++i) {
    const Eigen::Vector3d v0 = (sampled_trajectory_[i - 1] - sampled_trajectory_[i - 2]) / sample_dt_;
    const Eigen::Vector3d v1 = (sampled_trajectory_[i] - sampled_trajectory_[i - 1]) / sample_dt_;
    const double a = (v1 - v0).norm() / sample_dt_;
    if (a > max_acceleration_ * 6.0) {
      status_ = FuelBsplineTrajStatus::FAILED_DYNAMIC_LIMIT;
      last_failure_reason_ = "acceleration_limit";
      return false;
    }
  }
  return true;
}

bool FuelBsplineTrajAdapter::makePathFallback(const std::vector<Eigen::Vector3d> & path_points)
{
  control_points_ = path_points;
  sampled_trajectory_ = path_points;
  last_trajectory_length_ = pathLength(sampled_trajectory_);
  status_ = FuelBsplineTrajStatus::FALLBACK_PATH_AS_TRAJECTORY;
  ++fallback_count_;
  return true;
}

Eigen::Vector3d FuelBsplineTrajAdapter::catmullRom(
  const Eigen::Vector3d & p0,
  const Eigen::Vector3d & p1,
  const Eigen::Vector3d & p2,
  const Eigen::Vector3d & p3,
  double t)
{
  const double t2 = t * t;
  const double t3 = t2 * t;
  return 0.5 * ((2.0 * p1) + (-p0 + p2) * t +
         (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 +
         (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3);
}

double FuelBsplineTrajAdapter::pathLength(const std::vector<Eigen::Vector3d> & points)
{
  double length = 0.0;
  for (std::size_t i = 1; i < points.size(); ++i) {
    length += (points[i] - points[i - 1]).norm();
  }
  return length;
}

std::string FuelBsplineTrajAdapter::statusToString(FuelBsplineTrajStatus status)
{
  switch (status) {
    case FuelBsplineTrajStatus::IDLE: return "IDLE";
    case FuelBsplineTrajStatus::GENERATING: return "GENERATING";
    case FuelBsplineTrajStatus::SUCCESS: return "SUCCESS";
    case FuelBsplineTrajStatus::FAILED_NO_PATH: return "FAILED_NO_PATH";
    case FuelBsplineTrajStatus::FAILED_TOO_FEW_POINTS: return "FAILED_TOO_FEW_POINTS";
    case FuelBsplineTrajStatus::FAILED_COLLISION_RISK: return "FAILED_COLLISION_RISK";
    case FuelBsplineTrajStatus::FAILED_DYNAMIC_LIMIT: return "FAILED_DYNAMIC_LIMIT";
    case FuelBsplineTrajStatus::FALLBACK_PATH_AS_TRAJECTORY: return "FALLBACK_PATH_AS_TRAJECTORY";
  }
  return "UNKNOWN";
}

}  // namespace fuel_ros2
