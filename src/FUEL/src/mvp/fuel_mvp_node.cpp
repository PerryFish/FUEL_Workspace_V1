#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <memory>
#include <limits>
#include <optional>
#include <sstream>
#include <string>
#include <vector>

#include "geometry_msgs/msg/point.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "sensor_msgs/msg/point_field.hpp"
#include "std_msgs/msg/string.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_broadcaster.h"
#include "visualization_msgs/msg/marker.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

#include "fuel_ros2/bspline_traj/fuel_bspline_traj_adapter.hpp"
#include "fuel_ros2/exploration_fsm/fuel_exploration_fsm_adapter.hpp"
#include "fuel_ros2/frontier_fis/fuel_frontier_fis_adapter.hpp"
#include "fuel_ros2/path_searching/fuel_path_searching_adapter.hpp"
#include "fuel_ros2/plan_env/fuel_plan_env_adapter.hpp"
#include "fuel_ros2/plan_manager/fuel_plan_manager_adapter.hpp"
#include "fuel_ros2/real_interface/fuel_real_interface_adapter.hpp"

using namespace std::chrono_literals;

namespace fuel_ros2
{

struct Bounds
{
  double min_x{-8.0};
  double min_y{-6.0};
  double min_z{0.5};
  double max_x{8.0};
  double max_y{6.0};
  double max_z{4.0};
};

struct WorldObstacle
{
  std::string name;
  std::string type;
  Eigen::Vector3d center{0.0, 0.0, 0.0};
  Eigen::Vector3d size{0.0, 0.0, 0.0};
  double radius{0.0};
  double height{0.0};
};

struct CollisionResult
{
  bool collides{false};
  std::string obstacle{"none"};
  Eigen::Vector3d point{0.0, 0.0, 0.0};
};

struct PathQualityResult
{
  bool accepted{false};
  std::string reason{"unknown"};
  std::vector<Eigen::Vector3d> path;
  double length{0.0};
  double min_clearance{0.0};
};

struct ReachabilityResult
{
  bool reachable{false};
  std::string reason{"unknown"};
  Eigen::Vector3d start{0.0, 0.0, 0.0};
};

// Log contract tokens:
// PATH_QUALITY_REJECTED reason=too_short
// PATH_QUALITY_REJECTED reason=collision
// PATH_QUALITY_REJECTED reason=low_clearance
// PATH_QUALITY_REJECTED reason=endpoint_inside_obstacle
// PATH_QUALITY_REJECTED reason=no_progress
// GOAL_REACHABILITY_REJECTED reason=collision
// GOAL_REACHABILITY_REJECTED reason=low_clearance
// GOAL_REACHABILITY_REJECTED reason=no_grid_path
// GOAL_REACHABILITY_REJECTED reason=start_occupied
// START_OCCUPIED_ESCAPE original=
// START_OCCUPIED_ESCAPE_FAILED
// SAFE_DETOUR_GENERATED reason=low_clearance
// SAFE_DETOUR_FAILED reason=
// FALLBACK_SAFE_SWEEP_SELECTED
// FALLBACK_SAFE_SWEEP_PATH_READY points=
// NO_SAFE_SWEEP_AVAILABLE_HOLD
// FSM_TRANSITION from=EXECUTE_TRAJECTORY to=RESELECT_GOAL reason=EXECUTABLE_PATH_REJECTED

class FuelMvpNode final : public rclcpp::Node
{
public:
  FuelMvpNode() : Node("fuel_mvp_node")
  {
    frame_id_ = declare_parameter<std::string>("frame_id", "map");
    odom_frame_id_ = declare_parameter<std::string>("odom_frame_id", "odom");
    base_frame_id_ = declare_parameter<std::string>("base_frame_id", "base_link");
    bounds_.min_x = declare_parameter<double>("box_min_x", bounds_.min_x);
    bounds_.min_y = declare_parameter<double>("box_min_y", bounds_.min_y);
    bounds_.min_z = declare_parameter<double>("box_min_z", bounds_.min_z);
    bounds_.max_x = declare_parameter<double>("box_max_x", bounds_.max_x);
    bounds_.max_y = declare_parameter<double>("box_max_y", bounds_.max_y);
    bounds_.max_z = declare_parameter<double>("box_max_z", bounds_.max_z);
    default_z_ = declare_parameter<double>("default_z", 1.4);
    speed_mps_ = declare_parameter<double>("fake_controller_speed", 0.6);
    waypoint_accept_radius_ = declare_parameter<double>("waypoint_accept_radius", 0.25);
    replan_period_s_ = declare_parameter<double>("replan_period_s", 4.0);
    collision_clearance_ = declare_parameter<double>("path_quality.collision_clearance", 0.35);
    collision_resolution_ = declare_parameter<double>("path_quality.collision_resolution", 0.10);
    min_path_length_ = declare_parameter<double>("path_quality.min_path_length", 1.0);
    densify_step_ = declare_parameter<double>("path_quality.densify_step", 0.4);
    min_endpoint_progress_ = declare_parameter<double>("path_quality.min_endpoint_progress", 0.5);
    recent_goal_cooldown_sec_ = declare_parameter<double>("recent_goal_cooldown_sec", 20.0);
    recent_goal_radius_ = declare_parameter<double>("recent_goal_radius", 1.5);
    goal_revisit_penalty_ = declare_parameter<double>("goal_revisit_penalty", 0.7);
    minimum_goal_hold_sec_ = declare_parameter<double>("minimum_goal_hold_sec", 5.0);
    max_revisit_before_blacklist_ = declare_parameter<int>("max_revisit_before_blacklist", 3);
    blacklist_duration_sec_ = declare_parameter<double>("blacklist_duration_sec", 45.0);
    minimum_execution_time_before_replan_ =
      declare_parameter<double>("minimum_execution_time_before_replan", 5.0);
    goal_reached_radius_ = declare_parameter<double>("goal_reached_radius", 0.8);
    goal_progress_timeout_sec_ = declare_parameter<double>("goal_progress_timeout_sec", 20.0);
    minimum_progress_distance_ = declare_parameter<double>("minimum_progress_distance", 0.5);
    publish_tf_ = declare_parameter<bool>("publish_tf", true);
    planner_backend_ = declare_parameter<std::string>("planner_backend", "mvp");
    cloud_qos_mode_ = declare_parameter<std::string>("cloud_qos_mode", "rviz_compatible");
    if (planner_backend_ != "mvp" && planner_backend_ != "fuel_plan_env" &&
      planner_backend_ != "fuel_frontier_fis" && planner_backend_ != "fuel_exploration_fsm" &&
      planner_backend_ != "fuel_path_searching" && planner_backend_ != "fuel_bspline_traj" &&
      planner_backend_ != "fuel_plan_manager")
    {
      RCLCPP_ERROR(get_logger(), "Invalid planner_backend '%s', falling back to mvp", planner_backend_.c_str());
      planner_backend_ = "mvp";
    }
    plan_env_enabled_ = planner_backend_ == "fuel_plan_env" || planner_backend_ == "fuel_frontier_fis" ||
      planner_backend_ == "fuel_exploration_fsm" || planner_backend_ == "fuel_path_searching" ||
      planner_backend_ == "fuel_bspline_traj" || planner_backend_ == "fuel_plan_manager";
    frontier_fis_enabled_ = planner_backend_ == "fuel_frontier_fis" || planner_backend_ == "fuel_exploration_fsm" ||
      planner_backend_ == "fuel_path_searching" || planner_backend_ == "fuel_bspline_traj" ||
      planner_backend_ == "fuel_plan_manager";
    exploration_fsm_enabled_ = planner_backend_ == "fuel_exploration_fsm" ||
      planner_backend_ == "fuel_path_searching" || planner_backend_ == "fuel_bspline_traj" ||
      planner_backend_ == "fuel_plan_manager";
    path_searching_enabled_ = planner_backend_ == "fuel_path_searching" || planner_backend_ == "fuel_bspline_traj" ||
      planner_backend_ == "fuel_plan_manager";
    bspline_traj_enabled_ = planner_backend_ == "fuel_bspline_traj" || planner_backend_ == "fuel_plan_manager";
    plan_manager_enabled_ = planner_backend_ == "fuel_plan_manager";
    use_frontier_goal_source_ =
      declare_parameter<bool>("frontier_fis.use_frontier_goal_source", use_frontier_goal_source_);
    real_interface_enabled_ =
      declare_parameter<bool>("real_interface.enable_real_interface_mode", real_interface_enabled_);
    const char * gate_env = std::getenv("ONLINE_COLLISION_GATE_MODE");
    online_collision_gate_mode_ = declare_parameter<std::string>(
      "online_collision_gate_mode",
      gate_env && *gate_env ? std::string(gate_env) : std::string("warn"));
    if (online_collision_gate_mode_ != "off" && online_collision_gate_mode_ != "warn" &&
      online_collision_gate_mode_ != "enforce")
    {
      RCLCPP_WARN(
        get_logger(), "ONLINE_COLLISION_GATE_MODE_INVALID value=%s fallback=warn",
        online_collision_gate_mode_.c_str());
      online_collision_gate_mode_ = "warn";
    }

    default_z_ = clamp(default_z_, bounds_.min_z, bounds_.max_z);

    const auto cloud_qos = makeCloudQos();
    map_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>("/map_cloud", cloud_qos);
    global_cloud_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>("/global_cloud", cloud_qos);
    odom_pub_ = create_publisher<nav_msgs::msg::Odometry>("/odom", 20);
    waypoint_pub_ = create_publisher<geometry_msgs::msg::PoseStamped>("/fuel/waypoint", 10);
    path_pub_ = create_publisher<nav_msgs::msg::Path>("/fuel/global_path", 10);
    traj_pub_ = create_publisher<nav_msgs::msg::Path>("/fuel/local_trajectory", 10);
    safety_gate_safe_trajectory_clear_pub_ =
      create_publisher<nav_msgs::msg::Path>("/fuel/safety_gate/safe_trajectory", 10);
    debug_rejected_path_pub_ = create_publisher<nav_msgs::msg::Path>("/fuel/debug/rejected_path", 10);
    debug_collision_path_pub_ = create_publisher<nav_msgs::msg::Path>("/fuel/debug/collision_path", 10);
    debug_low_clearance_path_pub_ = create_publisher<nav_msgs::msg::Path>("/fuel/debug/low_clearance_path", 10);
    marker_pub_ = create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/frontiers", 10);
    state_pub_ = create_publisher<std_msgs::msg::String>("/fuel/exploration_state", 10);
    metrics_pub_ = create_publisher<std_msgs::msg::String>("/fuel/coverage_metrics", 10);
    demo_truth_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/visual/demo_truth_status", 10);
    demo_truth_marker_pub_ =
      create_publisher<visualization_msgs::msg::Marker>("/fuel/visual/demo_truth_status_marker", 10);
    if (plan_env_enabled_) {
      plan_env_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/plan_env/status", 10);
      plan_env_occupied_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>("/fuel/plan_env/occupied_cloud", 10);
      plan_env_inflated_pub_ = create_publisher<sensor_msgs::msg::PointCloud2>("/fuel/plan_env/inflated_cloud", 10);
      plan_env_frontier_pub_ = create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/plan_env/frontier_debug", 10);
      plan_env_debug_marker_pub_ = create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/plan_env/debug_markers", 10);
    }
    if (frontier_fis_enabled_) {
      fis_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/fis/status", 10);
      fis_frontier_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/fis/frontier_clusters", 10);
      fis_viewpoint_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/fis/viewpoints", 10);
      fis_best_viewpoint_pub_ =
        create_publisher<geometry_msgs::msg::PoseStamped>("/fuel/fis/best_viewpoint", 10);
      fis_debug_marker_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/fis/debug_markers", 10);
    }
    if (exploration_fsm_enabled_) {
      fsm_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/fsm/status", 10);
      fsm_state_pub_ = create_publisher<std_msgs::msg::String>("/fuel/fsm/state", 10);
      fsm_transition_pub_ = create_publisher<std_msgs::msg::String>("/fuel/fsm/transition", 10);
      fsm_current_goal_pub_ = create_publisher<geometry_msgs::msg::PoseStamped>("/fuel/fsm/current_goal", 10);
      fsm_debug_marker_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/fsm/debug_markers", 10);
      fsm_path_pub_ = create_publisher<nav_msgs::msg::Path>("/fuel/fsm/path", 10);
    }
    if (path_searching_enabled_) {
      path_searching_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/path_searching/status", 10);
      path_searching_path_pub_ = create_publisher<nav_msgs::msg::Path>("/fuel/path_searching/path", 10);
      path_searching_visited_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/path_searching/visited_nodes", 10);
      path_searching_debug_marker_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/path_searching/debug_markers", 10);
    }
    if (bspline_traj_enabled_) {
      bspline_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/bspline/status", 10);
      bspline_control_points_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/bspline/control_points", 10);
      bspline_sampled_trajectory_pub_ =
        create_publisher<nav_msgs::msg::Path>("/fuel/bspline/sampled_trajectory", 10);
      bspline_debug_marker_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/bspline/debug_markers", 10);
    }
    if (plan_manager_enabled_) {
      plan_manager_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/plan_manager/status", 10);
      plan_manager_contract_pub_ =
        create_publisher<std_msgs::msg::String>("/fuel/plan_manager/trajectory_contract", 10);
      plan_manager_managed_path_pub_ =
        create_publisher<nav_msgs::msg::Path>("/fuel/plan_manager/managed_path", 10);
      plan_manager_managed_trajectory_pub_ =
        create_publisher<nav_msgs::msg::Path>("/fuel/plan_manager/managed_trajectory", 10);
      plan_manager_debug_marker_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/plan_manager/debug_markers", 10);
    }
    if (real_interface_enabled_) {
      real_interface_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/real_interface/status", 10);
      real_interface_input_status_pub_ =
        create_publisher<std_msgs::msg::String>("/fuel/real_interface/input_status", 10);
      real_interface_output_status_pub_ =
        create_publisher<std_msgs::msg::String>("/fuel/real_interface/output_status", 10);
      real_interface_debug_marker_pub_ =
        create_publisher<visualization_msgs::msg::MarkerArray>("/fuel/real_interface/debug_markers", 10);
      control_bridge_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/control_bridge/status", 10);
      mode_manager_status_pub_ = create_publisher<std_msgs::msg::String>("/fuel/mode_manager/status", 10);
    }

    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);
    if (bounds_.min_x <= -14.0 && bounds_.max_x >= 14.0 && bounds_.min_y <= -14.0 && bounds_.max_y >= 14.0) {
      large_world_layout_ = true;
      buildExplorationWorldObstacles();
    }
    buildStaticObstacleMap();
    chooseNextWaypoint();
    if (plan_env_enabled_) {
      plan_env_adapter_ = std::make_unique<FuelPlanEnvAdapter>();
      plan_env_adapter_->initializeFromRos2Params(*this);
    }
    if (frontier_fis_enabled_) {
      frontier_fis_adapter_ = std::make_unique<FuelFrontierFisAdapter>();
      frontier_fis_adapter_->initializeFromRos2Params(*this);
    }
    if (exploration_fsm_enabled_) {
      exploration_fsm_adapter_ = std::make_unique<FuelExplorationFsmAdapter>();
      exploration_fsm_adapter_->initializeFromRos2Params(*this);
    }
    if (path_searching_enabled_) {
      path_searching_adapter_ = std::make_unique<FuelPathSearchingAdapter>();
      path_searching_adapter_->initializeFromRos2Params(*this);
      path_searching_adapter_->setPlanEnv(plan_env_adapter_.get());
    }
    if (bspline_traj_enabled_) {
      bspline_traj_adapter_ = std::make_unique<FuelBsplineTrajAdapter>();
      bspline_traj_adapter_->initializeFromRos2Params(*this);
      bspline_traj_adapter_->setPlanEnv(plan_env_adapter_.get());
    }
    if (plan_manager_enabled_) {
      plan_manager_adapter_ = std::make_unique<FuelPlanManagerAdapter>();
      plan_manager_adapter_->initializeFromRos2Params(*this);
    }
    if (real_interface_enabled_) {
      real_interface_adapter_ = std::make_unique<FuelRealInterfaceAdapter>();
      real_interface_adapter_->initializeFromRos2Params(*this);
      real_odom_sub_ = create_subscription<nav_msgs::msg::Odometry>(
        real_interface_adapter_->odomTopic(), 20,
        [this](const nav_msgs::msg::Odometry::SharedPtr msg) {
          if (real_interface_adapter_) {
            real_interface_adapter_->updateOdom(*msg);
          }
        });
      real_map_sub_ = create_subscription<sensor_msgs::msg::PointCloud2>(
        real_interface_adapter_->mapCloudTopic(), rclcpp::SensorDataQoS(),
        [this](const sensor_msgs::msg::PointCloud2::SharedPtr msg) {
          if (real_interface_adapter_) {
            real_interface_adapter_->updateMapCloud(*msg);
          }
        });
    }

    fast_timer_ = create_wall_timer(100ms, [this]() { publishFastLoop(); });
    slow_timer_ = create_wall_timer(1000ms, [this]() { publishSlowLoop(); });
    replan_timer_ = create_wall_timer(
      std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::duration<double>(replan_period_s_)),
      [this]() { chooseNextWaypoint(false); });

    RCLCPP_INFO(get_logger(), "FUEL ROS2 MVP node started with 3D bounds x[%.2f, %.2f] y[%.2f, %.2f] z[%.2f, %.2f]",
      bounds_.min_x, bounds_.max_x, bounds_.min_y, bounds_.max_y, bounds_.min_z, bounds_.max_z);
    RCLCPP_INFO(get_logger(), "planner_backend=%s", planner_backend_.c_str());
    RCLCPP_INFO(get_logger(), "MAP_CLOUD_QOS_PROFILE mode=%s reliability=%s durability=%s depth=1",
      cloud_qos_mode_.c_str(),
      cloud_qos_mode_ == "sensor_data" || cloud_qos_mode_ == "best_effort" ? "best_effort" : "reliable",
      cloud_qos_mode_ == "sensor_data" || cloud_qos_mode_ == "best_effort" ? "volatile" : "transient_local");
  }

private:
  static double clamp(double value, double lo, double hi)
  {
    return std::max(lo, std::min(value, hi));
  }

  rclcpp::QoS makeCloudQos() const
  {
    if (cloud_qos_mode_ == "sensor_data" || cloud_qos_mode_ == "best_effort") {
      return rclcpp::SensorDataQoS();
    }
    return rclcpp::QoS(rclcpp::KeepLast(1)).reliable().transient_local();
  }

  void buildStaticObstacleMap()
  {
    obstacle_points_.clear();
    const double resolution = 0.25;
    for (double x = bounds_.min_x; x <= bounds_.max_x; x += resolution) {
      for (double y = bounds_.min_y; y <= bounds_.max_y; y += resolution) {
        addPoint(x, y, bounds_.min_z);
        if (std::abs(y - bounds_.min_y) < 0.01 || std::abs(y - bounds_.max_y) < 0.01) {
          for (double z = bounds_.min_z; z <= bounds_.max_z; z += resolution) {
            addPoint(x, y, z);
          }
        }
      }
    }
    if (!world_obstacles_.empty()) {
      for (const auto & obstacle : world_obstacles_) {
        if (obstacle.type == "box") {
          const Eigen::Vector3d min = obstacle.center - obstacle.size * 0.5;
          const Eigen::Vector3d max = obstacle.center + obstacle.size * 0.5;
          addBox(min.x(), min.y(), min.z(), max.x(), max.y(), max.z(), resolution);
        } else if (obstacle.type == "cylinder") {
          addCylinder(
            obstacle.center.x(), obstacle.center.y(), obstacle.radius,
            obstacle.center.z() - obstacle.height * 0.5,
            obstacle.center.z() + obstacle.height * 0.5,
            resolution);
        }
      }
      return;
    }
    addBox(-2.5, -1.2, bounds_.min_z, -1.6, 1.5, 2.8, resolution);
    addBox(1.5, -3.5, bounds_.min_z, 2.2, -0.8, 2.4, resolution);
    addCylinder(4.0, 2.2, 0.55, bounds_.min_z, 3.6, resolution);
    addCylinder(-5.0, 3.2, 0.45, bounds_.min_z, 3.1, resolution);
  }

  void buildExplorationWorldObstacles()
  {
    world_obstacles_.clear();
    auto add_box = [this](const std::string & name, double cx, double cy, double cz,
        double sx, double sy, double sz) {
        WorldObstacle o;
        o.name = name;
        o.type = "box";
        o.center = Eigen::Vector3d(cx, cy, cz);
        o.size = Eigen::Vector3d(sx, sy, sz);
        world_obstacles_.push_back(o);
      };
    auto add_cylinder = [this](const std::string & name, double cx, double cy, double cz,
        double radius, double height) {
        WorldObstacle o;
        o.name = name;
        o.type = "cylinder";
        o.center = Eigen::Vector3d(cx, cy, cz);
        o.radius = radius;
        o.height = height;
        world_obstacles_.push_back(o);
      };
    add_box("south_corridor_left_wall", -4.2, -8.0, 1.5, 0.30, 12.0, 3.0);
    add_box("south_corridor_right_wall", 4.2, -8.0, 1.5, 0.30, 12.0, 3.0);
    add_box("west_room_outer_wall", -10.0, -1.0, 1.5, 0.30, 12.0, 3.0);
    add_box("east_room_outer_wall", 10.0, -1.0, 1.5, 0.30, 12.0, 3.0);
    add_box("north_back_wall", 0.0, 10.8, 1.5, 20.0, 0.30, 3.0);
    add_box("west_room_inner_wall", -6.8, 3.8, 1.5, 6.0, 0.30, 3.0);
    add_box("east_room_inner_wall", 6.8, 3.8, 1.5, 6.0, 0.30, 3.0);
    add_box("center_room_divider", 0.0, 4.6, 1.5, 0.30, 8.0, 3.0);
    add_box("west_dead_end_wall", -12.0, 6.0, 1.5, 4.0, 0.30, 3.0);
    add_box("east_dead_end_wall", 12.0, 6.0, 1.5, 4.0, 0.30, 3.0);
    add_box("box_obstacle_01", -2.0, -4.0, 0.75, 1.3, 1.0, 1.5);
    add_box("box_obstacle_02", 2.2, -1.5, 0.65, 1.1, 1.4, 1.3);
    add_box("box_obstacle_03", -7.4, -0.5, 0.8, 1.2, 1.2, 1.6);
    add_box("box_obstacle_04", 7.2, 2.4, 0.8, 1.4, 1.0, 1.6);
    add_cylinder("pillar_01", -1.5, 1.8, 1.4, 0.35, 2.8);
    add_cylinder("pillar_02", 3.0, 5.6, 1.4, 0.35, 2.8);
    add_cylinder("pillar_03", -4.8, 7.4, 1.4, 0.35, 2.8);
  }

  void addPoint(double x, double y, double z)
  {
    obstacle_points_.push_back({x, y, z});
  }

  void addBox(double min_x, double min_y, double min_z, double max_x, double max_y, double max_z, double resolution)
  {
    for (double x = min_x; x <= max_x; x += resolution) {
      for (double y = min_y; y <= max_y; y += resolution) {
        for (double z = min_z; z <= max_z; z += resolution) {
          const bool shell = x < min_x + resolution || x > max_x - resolution ||
            y < min_y + resolution || y > max_y - resolution || z < min_z + resolution || z > max_z - resolution;
          if (shell) {
            addPoint(x, y, z);
          }
        }
      }
    }
  }

  void addCylinder(double cx, double cy, double radius, double min_z, double max_z, double resolution)
  {
    for (double x = cx - radius; x <= cx + radius; x += resolution) {
      for (double y = cy - radius; y <= cy + radius; y += resolution) {
        if (std::hypot(x - cx, y - cy) <= radius) {
          for (double z = min_z; z <= max_z; z += resolution) {
            addPoint(x, y, z);
          }
        }
      }
    }
  }

  void chooseNextWaypoint(bool force)
  {
    const auto now = get_clock()->now();
    if (!force && last_goal_select_time_.nanoseconds() > 0 &&
      (now - last_goal_select_time_).seconds() < minimum_goal_hold_sec_)
    {
      return;
    }
    if (!force && accepted_path_active_ && last_execution_start_time_.nanoseconds() > 0 &&
      (now - last_execution_start_time_).seconds() < minimum_execution_time_before_replan_)
    {
      return;
    }
    const Eigen::Vector3d current(uav_position_.x, uav_position_.y, uav_position_.z);
    const Eigen::Vector3d goal_now(current_waypoint_.x, current_waypoint_.y, current_waypoint_.z);
    if ((goal_now - current).norm() <= goal_reached_radius_) {
      RCLCPP_INFO(get_logger(), "GOAL_REACHED");
      accepted_path_active_ = false;
    } else if (accepted_path_active_ && last_progress_check_time_.nanoseconds() > 0 &&
      (now - last_progress_check_time_).seconds() >= goal_progress_timeout_sec_)
    {
      const Eigen::Vector3d last(
        last_progress_position_.x, last_progress_position_.y, last_progress_position_.z);
      if ((current - last).norm() < minimum_progress_distance_) {
        RCLCPP_INFO(get_logger(), "GOAL_PROGRESS_TIMEOUT");
        RCLCPP_INFO(get_logger(), "REPLAN_DUE_TO_NO_PROGRESS");
        force = true;
        accepted_path_active_ = false;
      }
      last_progress_check_time_ = now;
      last_progress_position_ = uav_position_;
    }
    if (frontier_fis_enabled_ && use_frontier_goal_source_ && frontier_fis_adapter_ &&
      frontier_fis_adapter_->hasBestViewpoint())
    {
      const auto best = frontier_fis_adapter_->bestViewpoint();
      current_waypoint_.x = clamp(best.position.x(), bounds_.min_x + 0.4, bounds_.max_x - 0.4);
      current_waypoint_.y = clamp(best.position.y(), bounds_.min_y + 0.4, bounds_.max_y - 0.4);
      current_waypoint_.z = clamp(best.position.z(), bounds_.min_z + 0.2, bounds_.max_z - 0.2);
      recordSelectedGoal(Eigen::Vector3d(current_waypoint_.x, current_waypoint_.y, current_waypoint_.z), now);
      return;
    }
    static const std::vector<std::pair<double, double>> seeds{
      {-6.5, -4.2}, {-3.5, 3.9}, {0.0, -4.8}, {3.2, 4.4}, {6.5, -2.6}, {5.5, 3.2}, {-5.7, 1.0}};
    const double z_span = std::max(0.1, bounds_.max_z - bounds_.min_z);
    bool selected = false;
    geometry_msgs::msg::Point candidate{};
    for (std::size_t attempt = 0; attempt < seeds.size(); ++attempt) {
      const std::size_t idx = (waypoint_index_ + attempt) % seeds.size();
      const auto seed = seeds[idx];
      candidate.x = clamp(seed.first, bounds_.min_x + 0.4, bounds_.max_x - 0.4);
      candidate.y = clamp(seed.second, bounds_.min_y + 0.4, bounds_.max_y - 0.4);
      candidate.z = clamp(bounds_.min_z + 0.25 * z_span + 0.45 * z_span * std::abs(std::sin(0.75 * idx)),
        bounds_.min_z + 0.2, bounds_.max_z - 0.2);
      if (!isGoalBlacklisted(Eigen::Vector3d(candidate.x, candidate.y, candidate.z), now)) {
        waypoint_index_ = idx;
        selected = true;
        break;
      }
    }
    if (!selected) {
      RCLCPP_INFO(get_logger(), "GOAL_BLACKLIST_EXHAUSTED_FALLBACK");
      const auto seed = seeds[waypoint_index_ % seeds.size()];
      candidate.x = clamp(seed.first, bounds_.min_x + 0.4, bounds_.max_x - 0.4);
      candidate.y = clamp(seed.second, bounds_.min_y + 0.4, bounds_.max_y - 0.4);
      candidate.z = clamp(bounds_.min_z + 0.25 * z_span, bounds_.min_z + 0.2, bounds_.max_z - 0.2);
    }
    current_waypoint_ = candidate;
    recordSelectedGoal(Eigen::Vector3d(current_waypoint_.x, current_waypoint_.y, current_waypoint_.z), now);
  }

  void chooseNextWaypoint()
  {
    chooseNextWaypoint(true);
  }

  void publishFastLoop()
  {
    const auto now = now_msg();
    updateFakeController();
    publishOdom(now);
    publishWaypoint(now);
    publishPath(now);
    publishTrajectory(now);
    publishMarkers(now);
    publishStateAndMetrics();
    publishDemoTruthStatus(now);
    updateRealInterfacePlannerOutputs(now);
    publishRealInterfaceDebug(now);
    if (exploration_fsm_enabled_) {
      publishFsmDebug(now);
    }
  }

  void publishSlowLoop()
  {
    const auto now = now_msg();
    auto cloud = makeCloud(now);
    map_pub_->publish(cloud);
    global_cloud_pub_->publish(cloud);
    if (plan_env_enabled_ && plan_env_adapter_) {
      plan_env_adapter_->updateFromPointCloud(cloud);
      publishPlanEnvDebug(now);
      if (frontier_fis_enabled_ && frontier_fis_adapter_) {
        frontier_fis_adapter_->updateMapFromPlanEnv(*plan_env_adapter_);
        frontier_fis_adapter_->extractFrontierClusters();
        frontier_fis_adapter_->generateViewpoints();
        publishFisDebug(now);
        if (exploration_fsm_enabled_ && exploration_fsm_adapter_) {
          exploration_fsm_adapter_->updateFrontierFisStatus(frontier_fis_adapter_->exportStatusMsg().data);
          if (frontier_fis_adapter_->hasBestViewpoint()) {
            const rclcpp::Time rcl_stamp(now);
            exploration_fsm_adapter_->updateBestViewpoint(
              frontier_fis_adapter_->exportBestViewpointMsg(frame_id_, rcl_stamp));
          }
        }
      }
    }
  }

  builtin_interfaces::msg::Time now_msg()
  {
    return get_clock()->now();
  }

  sensor_msgs::msg::PointCloud2 makeCloud(const builtin_interfaces::msg::Time & stamp) const
  {
    sensor_msgs::msg::PointCloud2 cloud;
    cloud.header.stamp = stamp;
    cloud.header.frame_id = frame_id_;
    cloud.height = 1;
    cloud.width = static_cast<uint32_t>(obstacle_points_.size());
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
    for (size_t i = 0; i < obstacle_points_.size(); ++i) {
      for (size_t j = 0; j < 3; ++j) {
        const float value = static_cast<float>(obstacle_points_[i][j]);
        std::memcpy(&cloud.data[i * cloud.point_step + j * 4], &value, sizeof(float));
      }
    }
    return cloud;
  }

  void updateFakeController()
  {
    const double dt = 0.1;
    const double dx = current_waypoint_.x - uav_position_.x;
    const double dy = current_waypoint_.y - uav_position_.y;
    const double dz = current_waypoint_.z - uav_position_.z;
    const double distance = std::sqrt(dx * dx + dy * dy + dz * dz);
    if (distance < waypoint_accept_radius_) {
      chooseNextWaypoint(true);
      return;
    }
    const double step = std::min(distance, speed_mps_ * dt);
    uav_position_.x += dx / distance * step;
    uav_position_.y += dy / distance * step;
    uav_position_.z += dz / distance * step;
  }

  void publishOdom(const builtin_interfaces::msg::Time & stamp)
  {
    nav_msgs::msg::Odometry odom;
    odom.header.stamp = stamp;
    odom.header.frame_id = frame_id_;
    odom.child_frame_id = base_frame_id_;
    odom.pose.pose.position = uav_position_;
    tf2::Quaternion q;
    q.setRPY(0.0, 0.0, 0.0);
    odom.pose.pose.orientation.x = q.x();
    odom.pose.pose.orientation.y = q.y();
    odom.pose.pose.orientation.z = q.z();
    odom.pose.pose.orientation.w = q.w();
    odom_pub_->publish(odom);
    if (plan_env_enabled_ && plan_env_adapter_) {
      plan_env_adapter_->updateOdometry(odom);
    }
    if (frontier_fis_enabled_ && frontier_fis_adapter_) {
      frontier_fis_adapter_->updateOdometry(odom);
    }
    if (exploration_fsm_enabled_ && exploration_fsm_adapter_) {
      exploration_fsm_adapter_->updateOdometry(odom);
    }

    if (publish_tf_) {
      geometry_msgs::msg::TransformStamped tf;
      tf.header.stamp = stamp;
      tf.header.frame_id = frame_id_;
      tf.child_frame_id = base_frame_id_;
      tf.transform.translation.x = uav_position_.x;
      tf.transform.translation.y = uav_position_.y;
      tf.transform.translation.z = uav_position_.z;
      tf.transform.rotation = odom.pose.pose.orientation;
      tf_broadcaster_->sendTransform(tf);
    }
  }

  void publishWaypoint(const builtin_interfaces::msg::Time & stamp)
  {
    geometry_msgs::msg::PoseStamped waypoint;
    waypoint.header.stamp = stamp;
    waypoint.header.frame_id = frame_id_;
    waypoint.pose.position = current_waypoint_;
    waypoint.pose.orientation.w = 1.0;
    waypoint_pub_->publish(waypoint);
    last_waypoint_msg_ = waypoint;
  }

  void publishPath(const builtin_interfaces::msg::Time & stamp)
  {
    if (path_searching_enabled_ && path_searching_adapter_ &&
      !accepted_path_points_.empty())
    {
      last_global_path_msg_ = makePathMsg(accepted_path_points_, stamp);
      path_pub_->publish(last_global_path_msg_);
      return;
    }
    nav_msgs::msg::Path path;
    path.header.stamp = stamp;
    path.header.frame_id = frame_id_;
    appendPose(path, uav_position_, stamp);
    for (int i = 1; i <= 12; ++i) {
      geometry_msgs::msg::Point p;
      const double ratio = static_cast<double>(i) / 12.0;
      p.x = uav_position_.x + (current_waypoint_.x - uav_position_.x) * ratio;
      p.y = uav_position_.y + (current_waypoint_.y - uav_position_.y) * ratio;
      p.z = uav_position_.z + (current_waypoint_.z - uav_position_.z) * ratio +
        0.25 * std::sin(ratio * M_PI);
      p.z = clamp(p.z, bounds_.min_z, bounds_.max_z);
      appendPose(path, p, stamp);
    }
    path_pub_->publish(path);
    last_global_path_msg_ = path;
  }

  void publishTrajectory(const builtin_interfaces::msg::Time & stamp)
  {
    if (bspline_traj_enabled_ && bspline_traj_adapter_ &&
      bspline_traj_adapter_->useForStableOutput() &&
      bspline_traj_adapter_->status() == FuelBsplineTrajStatus::SUCCESS &&
      bspline_traj_adapter_->getSampledTrajectory().size() >= 2)
    {
      traj_pub_->publish(bspline_traj_adapter_->exportSampledTrajectoryMsg(frame_id_, rclcpp::Time(stamp)));
      last_local_trajectory_msg_ = bspline_traj_adapter_->exportSampledTrajectoryMsg(frame_id_, rclcpp::Time(stamp));
      logLocalTrajectorySource("bspline", bspline_traj_adapter_->getSampledTrajectory().size(), false);
      return;
    }
    if (plan_manager_enabled_ && plan_manager_adapter_ &&
      plan_manager_adapter_->useManagedOutput())
    {
      const auto contract = plan_manager_adapter_->currentContract();
      if (contract.safe_for_stable_output && contract.trajectory_points >= 2) {
        traj_pub_->publish(plan_manager_adapter_->exportManagedTrajectoryMsg(frame_id_, rclcpp::Time(stamp)));
        last_local_trajectory_msg_ =
          plan_manager_adapter_->exportManagedTrajectoryMsg(frame_id_, rclcpp::Time(stamp));
        logLocalTrajectorySource("managed_output", contract.trajectory_points, true);
        return;
      }
    }
    if (path_searching_enabled_ && path_searching_adapter_ &&
      accepted_path_points_.size() >= 3)
    {
      last_local_trajectory_msg_ = makePathMsg(accepted_path_points_, stamp);
      traj_pub_->publish(last_local_trajectory_msg_);
      logLocalTrajectorySource("path_searching", accepted_path_points_.size(), false);
      return;
    }
    nav_msgs::msg::Path traj;
    traj.header.stamp = stamp;
    traj.header.frame_id = frame_id_;
    if (!large_world_layout_) {
      for (int i = 0; i <= 8; ++i) {
        const double ratio = static_cast<double>(i) / 8.0;
        geometry_msgs::msg::Point p;
        p.x = uav_position_.x + (current_waypoint_.x - uav_position_.x) * ratio;
        p.y = uav_position_.y + (current_waypoint_.y - uav_position_.y) * ratio;
        p.z = clamp(uav_position_.z + (current_waypoint_.z - uav_position_.z) * ratio, bounds_.min_z, bounds_.max_z);
        appendPose(traj, p, stamp);
      }
      traj_pub_->publish(traj);
      last_local_trajectory_msg_ = traj;
      logLocalTrajectorySource("mvp", traj.poses.size(), false);
      return;
    }
    traj_pub_->publish(traj);
    last_local_trajectory_msg_ = traj;
    logLocalTrajectorySource("hold_empty_no_safe_path", traj.poses.size(), true);
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 2000,
      "NO_SAFE_FRONTIER_REGION_AVAILABLE executable_path_collision_free=false debug_only=false");
  }

  static void appendPose(nav_msgs::msg::Path & path, const geometry_msgs::msg::Point & point,
    const builtin_interfaces::msg::Time & stamp)
  {
    geometry_msgs::msg::PoseStamped pose;
    pose.header = path.header;
    pose.header.stamp = stamp;
    pose.pose.position = point;
    pose.pose.orientation.w = 1.0;
    path.poses.push_back(pose);
  }

  nav_msgs::msg::Path makePathMsg(
    const std::vector<Eigen::Vector3d> & points,
    const builtin_interfaces::msg::Time & stamp) const
  {
    nav_msgs::msg::Path path;
    path.header.frame_id = frame_id_;
    path.header.stamp = stamp;
    for (const auto & p : points) {
      geometry_msgs::msg::Point point;
      point.x = p.x();
      point.y = p.y();
      point.z = p.z();
      appendPose(path, point, stamp);
    }
    return path;
  }

  void publishMarkers(const builtin_interfaces::msg::Time & stamp)
  {
    visualization_msgs::msg::MarkerArray markers;
    visualization_msgs::msg::Marker frontier;
    frontier.header.frame_id = frame_id_;
    frontier.header.stamp = stamp;
    frontier.ns = "fuel_frontiers";
    frontier.id = 1;
    frontier.type = visualization_msgs::msg::Marker::SPHERE_LIST;
    frontier.action = visualization_msgs::msg::Marker::ADD;
    frontier.scale.x = 0.22;
    frontier.scale.y = 0.22;
    frontier.scale.z = 0.22;
    frontier.color.r = 0.1f;
    frontier.color.g = 0.8f;
    frontier.color.b = 1.0f;
    frontier.color.a = 0.9f;
    for (int i = 0; i < 18; ++i) {
      geometry_msgs::msg::Point p;
      p.x = clamp(bounds_.min_x + 0.7 + (i % 6) * 2.4, bounds_.min_x, bounds_.max_x);
      p.y = clamp(bounds_.min_y + 0.8 + (i / 6) * 2.7, bounds_.min_y, bounds_.max_y);
      p.z = clamp(default_z_ + 0.7 * std::sin(i * 0.9), bounds_.min_z, bounds_.max_z);
      frontier.points.push_back(p);
    }
    markers.markers.push_back(frontier);

    visualization_msgs::msg::Marker waypoint;
    waypoint.header.frame_id = frame_id_;
    waypoint.header.stamp = stamp;
    waypoint.ns = "fuel_waypoint";
    waypoint.id = 2;
    waypoint.type = visualization_msgs::msg::Marker::SPHERE;
    waypoint.action = visualization_msgs::msg::Marker::ADD;
    waypoint.pose.position = current_waypoint_;
    waypoint.pose.orientation.w = 1.0;
    waypoint.scale.x = 0.65;
    waypoint.scale.y = 0.65;
    waypoint.scale.z = 0.65;
    waypoint.color.r = 0.95f;
    waypoint.color.g = 0.05f;
    waypoint.color.b = 1.0f;
    waypoint.color.a = 1.0f;
    markers.markers.push_back(waypoint);
    marker_pub_->publish(markers);
  }

  void publishStateAndMetrics()
  {
    std_msgs::msg::String state;
    state.data = "EXPLORING";
    state_pub_->publish(state);

    std_msgs::msg::String metrics;
    const int total_voxels = 12000;
    const int observed = std::min(total_voxels, 1200 + static_cast<int>(replanning_count_ * 350));
    metrics.data = "observed_voxels=" + std::to_string(observed) +
      " total_voxels=" + std::to_string(total_voxels) +
      " frontier_count=18 replanning_count=" + std::to_string(replanning_count_) +
      " stuck_count=0";
    metrics_pub_->publish(metrics);
  }

  void publishDemoTruthStatus(const builtin_interfaces::msg::Time & stamp)
  {
    const std::size_t path_points = last_global_path_msg_.poses.size();
    const std::size_t traj_points = last_local_trajectory_msg_.poses.size();
    const bool path_too_short = path_points <= 2 || traj_points <= 2;
    const bool bspline_valid = bspline_traj_enabled_ && bspline_traj_adapter_ &&
      bspline_traj_adapter_->status() == FuelBsplineTrajStatus::SUCCESS;
    const bool plan_manager_safe = last_plan_manager_safe_;
    const bool active_goal = exploration_fsm_adapter_ && exploration_fsm_adapter_->hasActiveGoal();
    const bool used_fis = frontier_fis_adapter_ && frontier_fis_adapter_->hasBestViewpoint();
    const bool fallback_active = path_too_short || !bspline_valid || planner_backend_ == "fuel_plan_manager" ||
      !plan_manager_safe;
    const std::string fsm_state = exploration_fsm_adapter_ ?
      exploration_fsm_adapter_->currentStateString() : std::string("WRAPPER_MVP");
    const std::string reason = path_too_short ? "too_few_points_or_fallback" : "wrapper_visual_demo_partial_pipeline";
    std::string current_warning = "FUEL_ROS2_WRAPPER_VISUAL_DEMO";
    if (!plan_manager_safe) {
      current_warning += " PLAN_MANAGER_CANDIDATE_UNSAFE";
    }
    if (fallback_active) {
      current_warning += " FALLBACK_ACTIVE_VISUAL_DEMO_ONLY";
    }
    if (last_fsm_timeout_active_) {
      current_warning += " EXECUTION_TIMEOUT_RECOVERY_ACTIVE";
    }

    std_msgs::msg::String status;
    status.data =
      std::string("{\"demo_type\":\"FUEL_ROS2_WRAPPER_VISUAL_DEMO\",") +
      "\"wrapper_demo\":true," +
      "\"upstream_fuel_official_parity\":false," +
      "\"fallback_active\":" + (fallback_active ? "true" : "false") + "," +
      "\"fsm_state\":\"" + fsm_state + "\"," +
      "\"active_goal\":" + (active_goal ? "true" : "false") + "," +
      "\"used_fis\":" + (used_fis ? "true" : "false") + "," +
      "\"path_points\":" + std::to_string(path_points) + "," +
      "\"traj_points\":" + std::to_string(traj_points) + "," +
      "\"bspline_valid\":" + (bspline_valid ? "true" : "false") + "," +
      "\"plan_manager_source\":\"" + last_plan_manager_source_ + "\"," +
      "\"plan_manager_safe\":" + (plan_manager_safe ? "true" : "false") + "," +
      "\"execution_timeout_count\":" + std::to_string(execution_timeout_count_) + "," +
      "\"current_warning\":\"" + current_warning + "\"," +
      "\"exploration_complete\":false," +
      "\"reason\":\"" + reason + "\"," +
      "\"warning\":\"WRAPPER DEMO / FALLBACK PATH / NOT FULL UPSTREAM FUEL" +
      (path_too_short ? " PATH_TOO_SHORT_FOR_EXPLORATION_VISUALIZATION" : "") +
      " FSM_FINISH_DOES_NOT_MEAN_FULL_EXPLORATION\"}";
    demo_truth_status_pub_->publish(status);

    visualization_msgs::msg::Marker marker;
    marker.header.frame_id = frame_id_;
    marker.header.stamp = stamp;
    marker.ns = "fuel_demo_truth";
    marker.id = 0;
    marker.type = visualization_msgs::msg::Marker::TEXT_VIEW_FACING;
    marker.action = visualization_msgs::msg::Marker::ADD;
    marker.pose.position.x = -14.0;
    marker.pose.position.y = -14.0;
    marker.pose.position.z = 1.65;
    marker.pose.orientation.w = 1.0;
    marker.scale.z = 0.24;
    marker.color.r = 1.0f;
    marker.color.g = 0.30f;
    marker.color.b = 0.05f;
    marker.color.a = 1.0f;
    marker.text =
      "FUEL_ROS2 WRAPPER DEMO\n"
      "NOT UPSTREAM FUEL OFFICIAL\n"
      "fallback=" + std::string(fallback_active ? "true" : "false") +
      " safe=" + std::string(plan_manager_safe ? "true" : "false") + "\n" +
      "FSM state=" + fsm_state +
      " path_points=" + std::to_string(path_points) +
      " traj_points=" + std::to_string(traj_points) + "\n" +
      current_warning + "\n"
      "VISUAL DEMO ONLY";
    demo_truth_marker_pub_->publish(marker);
  }

  void publishPlanEnvDebug(const builtin_interfaces::msg::Time & stamp)
  {
    if (!plan_env_adapter_ || !plan_env_status_pub_ || !plan_env_occupied_pub_ || !plan_env_debug_marker_pub_) {
      return;
    }
    const rclcpp::Time rcl_stamp(stamp);
    plan_env_occupied_pub_->publish(plan_env_adapter_->exportOccupiedCloudMsg(frame_id_, rcl_stamp));
    plan_env_inflated_pub_->publish(plan_env_adapter_->exportInflatedCloudMsg(frame_id_, rcl_stamp));
    auto markers = plan_env_adapter_->exportDebugMarkers(frame_id_, rcl_stamp);
    plan_env_debug_marker_pub_->publish(markers);
    plan_env_frontier_pub_->publish(markers);

    std_msgs::msg::String status;
    status.data = "PLAN_ENV_BACKEND_PARTIAL occupied_voxels=" +
      std::to_string(plan_env_adapter_->occupiedVoxelCount()) +
      " inflated_voxels=" + std::to_string(plan_env_adapter_->inflatedVoxelCount()) +
      " frontier_count=" + std::to_string(plan_env_adapter_->extractSimpleFrontiers().size());
    plan_env_status_pub_->publish(status);
    if (exploration_fsm_enabled_ && exploration_fsm_adapter_) {
      exploration_fsm_adapter_->updatePlanEnvStatus(status.data);
    }
  }

  void publishFisDebug(const builtin_interfaces::msg::Time & stamp)
  {
    if (!frontier_fis_adapter_ || !fis_status_pub_ || !fis_frontier_pub_ || !fis_viewpoint_pub_ ||
      !fis_best_viewpoint_pub_ || !fis_debug_marker_pub_)
    {
      return;
    }
    const rclcpp::Time rcl_stamp(stamp);
    fis_status_pub_->publish(frontier_fis_adapter_->exportStatusMsg());
    fis_frontier_pub_->publish(frontier_fis_adapter_->exportFrontierMarkers(frame_id_, rcl_stamp));
    fis_viewpoint_pub_->publish(frontier_fis_adapter_->exportViewpointMarkers(frame_id_, rcl_stamp));
    fis_debug_marker_pub_->publish(frontier_fis_adapter_->exportDebugMarkers(frame_id_, rcl_stamp));
    if (frontier_fis_adapter_->hasBestViewpoint()) {
      fis_best_viewpoint_pub_->publish(frontier_fis_adapter_->exportBestViewpointMsg(frame_id_, rcl_stamp));
    }
  }

  void publishFsmDebug(const builtin_interfaces::msg::Time & stamp)
  {
    if (!exploration_fsm_adapter_ || !fsm_status_pub_ || !fsm_state_pub_ || !fsm_transition_pub_ ||
      !fsm_current_goal_pub_ || !fsm_path_pub_ || !fsm_debug_marker_pub_)
    {
      return;
    }
    geometry_msgs::msg::PoseStamped fallback;
    fallback.header.frame_id = frame_id_;
    fallback.header.stamp = stamp;
    fallback.pose.position = current_waypoint_;
    fallback.pose.orientation.w = 1.0;
    exploration_fsm_adapter_->setFallbackGoal(fallback);
    exploration_fsm_adapter_->tick(get_clock()->now());

    auto status = exploration_fsm_adapter_->exportStatusMsg();
    fsm_status_pub_->publish(status);
    std_msgs::msg::String state;
    state.data = exploration_fsm_adapter_->currentStateString();
    fsm_state_pub_->publish(state);
    std_msgs::msg::String transition;
    transition.data = exploration_fsm_adapter_->lastTransitionLog();
    fsm_transition_pub_->publish(transition);
    if (transition.data != last_logged_fsm_transition_) {
      last_logged_fsm_transition_ = transition.data;
      RCLCPP_INFO(get_logger(), "%s", transition.data.c_str());
    }
    const auto goal_log = exploration_fsm_adapter_->lastGoalLog();
    if (goal_log != last_logged_fsm_goal_) {
      last_logged_fsm_goal_ = goal_log;
      RCLCPP_INFO(get_logger(), "%s", goal_log.c_str());
    }
    const auto fallback_log = exploration_fsm_adapter_->lastFallbackLog();
    if (fallback_log != last_logged_fsm_fallback_) {
      last_logged_fsm_fallback_ = fallback_log;
      if (fallback_log.find("FSM_TIMEOUT") != std::string::npos) {
        ++execution_timeout_count_;
        last_fsm_timeout_active_ = true;
        RCLCPP_INFO(get_logger(), "EXECUTION_TIMEOUT_RECOVERY_ACTIVE count=%zu", execution_timeout_count_);
      }
      RCLCPP_INFO(get_logger(), "%s", fallback_log.c_str());
    }
    maybeRunPathSearching(stamp);
    maybeRunBsplineTrajectory(stamp);
    maybeRunPlanManager(stamp);
    const auto path_source_log = exploration_fsm_adapter_->lastPathSourceLog();
    if (path_source_log != last_logged_fsm_path_source_) {
      last_logged_fsm_path_source_ = path_source_log;
      RCLCPP_INFO(get_logger(), "%s", path_source_log.c_str());
    }
    if (exploration_fsm_adapter_->hasActiveGoal()) {
      fsm_current_goal_pub_->publish(exploration_fsm_adapter_->currentGoal());
    }
    const rclcpp::Time rcl_stamp(stamp);
    fsm_path_pub_->publish(exploration_fsm_adapter_->exportFsmPath(frame_id_, rcl_stamp));
    fsm_debug_marker_pub_->publish(exploration_fsm_adapter_->exportFsmDebugMarkers(frame_id_, rcl_stamp));
    publishPathSearchingDebug(stamp);
    publishBsplineDebug(stamp);
    publishPlanManagerDebug(stamp);
    RCLCPP_INFO_THROTTLE(get_logger(), *get_clock(), 1000, "%s", status.data.c_str());
  }

  void maybeRunPathSearching(const builtin_interfaces::msg::Time & stamp)
  {
    if (!path_searching_enabled_ || !path_searching_adapter_ || !exploration_fsm_adapter_ ||
      !exploration_fsm_adapter_->hasActiveGoal())
    {
      return;
    }
    const rclcpp::Time now(stamp);
    if ((now - last_path_search_time_).seconds() < 1.0) {
      return;
    }
    last_path_search_time_ = now;
    const auto goal_msg = exploration_fsm_adapter_->currentGoal();
    const Eigen::Vector3d raw_start(uav_position_.x, uav_position_.y, uav_position_.z);
    const Eigen::Vector3d goal(
      goal_msg.pose.position.x,
      goal_msg.pose.position.y,
      goal_msg.pose.position.z);
    ReachabilityResult reachability;
    reachability.reachable = true;
    reachability.reason = "not_enforced";
    reachability.start = raw_start;
    if (onlineCollisionGateEnforced()) {
      reachability = precheckGoalReachability(raw_start, goal);
      if (!reachability.reachable) {
        clearAcceptedPathAndBsplineCandidate();
        handleRejectedExecutablePath(reachability.reason, "goal_reachability");
        if (!generateFallbackSafeSweep(reachability.start, stamp)) {
          RCLCPP_INFO(get_logger(), "NO_SAFE_SWEEP_AVAILABLE_HOLD");
          ++no_safe_sweep_hold_count_;
        }
        return;
      }
    }
    const Eigen::Vector3d start = reachability.start;
    RCLCPP_INFO(
      get_logger(),
      "PATH_SEARCH_START start=(%.3f,%.3f,%.3f) goal=(%.3f,%.3f,%.3f) algorithm=grid_astar_3d resolution=%.3f",
      start.x(), start.y(), start.z(), goal.x(), goal.y(), goal.z(),
      path_searching_adapter_->gridResolution());
    const bool success = path_searching_adapter_->searchPath(start, goal);
    const auto status = path_searching_adapter_->status();
    const auto path = path_searching_adapter_->exportPathMsg(frame_id_, now);
    if (success) {
      const auto quality = filterPathQuality(path_searching_adapter_->getPath(), "path_searching");
      if (!quality.accepted) {
        if (onlineCollisionGateEnforced() && trySafeDetourOrSweep(start, goal, quality.reason, stamp)) {
          return;
        }
        clearAcceptedPathAndBsplineCandidate();
        handleRejectedExecutablePath(quality.reason, "path_searching");
        return;
      }
      acceptExecutablePath(quality.path, "path_searching", stamp);
      RCLCPP_INFO(
        get_logger(),
        "PATH_SEARCH_SUCCESS points=%zu visited=%zu length=%.3f duration_ms=%.3f path_collision_free=true min_obstacle_clearance=%.3f",
        accepted_path_points_.size(),
        path_searching_adapter_->getVisitedNodes().size(),
        quality.length,
        path_searching_adapter_->lastDurationMs(),
        quality.min_clearance);
    } else if (status == FuelPathSearchStatus::FALLBACK_STRAIGHT_LINE) {
      const auto quality = filterPathQuality(path_searching_adapter_->getPath(), "straight_line");
      if (quality.accepted) {
        acceptExecutablePath(quality.path, "straight_line", stamp);
      } else {
        if (!onlineCollisionGateEnforced() || !trySafeDetourOrSweep(start, goal, quality.reason, stamp)) {
          clearAcceptedPathAndBsplineCandidate();
          handleRejectedExecutablePath(quality.reason, "straight_line");
        }
      }
      RCLCPP_INFO(
        get_logger(),
        "PATH_SEARCH_FAIL reason=%s visited=%zu duration_ms=%.3f fallback=yes",
        path_searching_adapter_->lastFailureReason().c_str(),
        path_searching_adapter_->getVisitedNodes().size(),
        path_searching_adapter_->lastDurationMs());
      RCLCPP_INFO(
        get_logger(),
        "PATH_SEARCH_FALLBACK type=straight_line reason=%s",
        path_searching_adapter_->lastFailureReason().c_str());
    } else {
      RCLCPP_INFO(
        get_logger(),
        "PATH_SEARCH_FAIL reason=%s visited=%zu duration_ms=%.3f fallback=no",
        path_searching_adapter_->lastFailureReason().c_str(),
        path_searching_adapter_->getVisitedNodes().size(),
        path_searching_adapter_->lastDurationMs());
      if (onlineCollisionGateEnforced() && !generateFallbackSafeSweep(start, stamp)) {
        RCLCPP_INFO(get_logger(), "NO_SAFE_SWEEP_AVAILABLE_HOLD");
        ++no_safe_sweep_hold_count_;
      }
    }
  }

  void acceptExecutablePath(
    const std::vector<Eigen::Vector3d> & path,
    const std::string & source,
    const builtin_interfaces::msg::Time & stamp)
  {
    accepted_path_points_ = path;
    accepted_path_active_ = true;
    const rclcpp::Time now(stamp);
    last_execution_start_time_ = now;
    last_progress_check_time_ = now;
    last_progress_position_ = uav_position_;
    if (exploration_fsm_adapter_) {
      exploration_fsm_adapter_->setExternalPath(makePathMsg(accepted_path_points_, stamp), source);
    }
  }

  void clearAcceptedPathAndBsplineCandidate()
  {
    accepted_path_points_.clear();
    accepted_path_active_ = false;
    if (bspline_traj_adapter_) {
      bspline_traj_adapter_->reset();
    }
    publishEmptyExecutableTrajectories("empty_or_rejected");
  }

  void publishEmptyExecutableTrajectories(const std::string & reason)
  {
    nav_msgs::msg::Path empty;
    empty.header.frame_id = frame_id_;
    empty.header.stamp = get_clock()->now();
    if (traj_pub_) {
      traj_pub_->publish(empty);
    }
    if (plan_manager_managed_path_pub_) {
      plan_manager_managed_path_pub_->publish(empty);
    }
    if (plan_manager_managed_trajectory_pub_) {
      plan_manager_managed_trajectory_pub_->publish(empty);
    }
    if (path_searching_path_pub_) {
      path_searching_path_pub_->publish(empty);
    }
    if (safety_gate_safe_trajectory_clear_pub_) {
      safety_gate_safe_trajectory_clear_pub_->publish(empty);
    }
    last_local_trajectory_msg_ = empty;
    last_global_path_msg_ = empty;
    RCLCPP_INFO(
      get_logger(),
      "EXECUTABLE_TRAJECTORIES_CLEARED reason=%s path_points=0 traj_points=0 executable_path_collision_free=false debug_only=false",
      reason.c_str());
  }

  void publishPathSearchingDebug(const builtin_interfaces::msg::Time & stamp)
  {
    if (!path_searching_enabled_ || !path_searching_adapter_ || !path_searching_status_pub_ ||
      !path_searching_path_pub_ || !path_searching_visited_pub_ || !path_searching_debug_marker_pub_)
    {
      return;
    }
    const rclcpp::Time rcl_stamp(stamp);
    path_searching_status_pub_->publish(path_searching_adapter_->exportStatusMsg());
    if (!accepted_path_points_.empty()) {
      path_searching_path_pub_->publish(makePathMsg(accepted_path_points_, stamp));
    } else {
      nav_msgs::msg::Path empty;
      empty.header.frame_id = frame_id_;
      empty.header.stamp = stamp;
      path_searching_path_pub_->publish(empty);
    }
    path_searching_visited_pub_->publish(path_searching_adapter_->exportVisitedNodes(frame_id_, rcl_stamp));
    path_searching_debug_marker_pub_->publish(path_searching_adapter_->exportDebugMarkers(frame_id_, rcl_stamp));
  }

  void maybeRunBsplineTrajectory(const builtin_interfaces::msg::Time & stamp)
  {
    if (!bspline_traj_enabled_ || !bspline_traj_adapter_ || !path_searching_adapter_) {
      return;
    }
    if (accepted_path_points_.empty()) {
      bspline_traj_adapter_->reset();
      return;
    }
    const auto path_points = accepted_path_points_;
    const rclcpp::Time now(stamp);
    if ((now - last_bspline_generation_time_).seconds() < 1.0) {
      return;
    }
    last_bspline_generation_time_ = now;
    RCLCPP_INFO(
      get_logger(),
      "BSPLINE_TRAJ_START input_points=%zu algorithm=uniform_bspline_lite sample_dt=%.3f",
      path_points.size(), 0.1);
    const bool success = bspline_traj_adapter_->generateFromPath(path_points);
    if (success) {
      RCLCPP_INFO(
        get_logger(),
        "BSPLINE_TRAJ_SUCCESS control_points=%zu sampled_points=%zu length=%.3f duration_ms=%.3f",
        bspline_traj_adapter_->getControlPoints().size(),
        bspline_traj_adapter_->getSampledTrajectory().size(),
        bspline_traj_adapter_->lastTrajectoryLength(),
        bspline_traj_adapter_->lastDurationMs());
    } else if (bspline_traj_adapter_->status() == FuelBsplineTrajStatus::FALLBACK_PATH_AS_TRAJECTORY) {
      RCLCPP_INFO(
        get_logger(),
        "BSPLINE_TRAJ_FAIL reason=%s input_points=%zu duration_ms=%.3f fallback=yes",
        bspline_traj_adapter_->lastFailureReason().c_str(),
        path_points.size(),
        bspline_traj_adapter_->lastDurationMs());
      RCLCPP_INFO(
        get_logger(),
        "BSPLINE_TRAJ_FALLBACK type=path_as_trajectory reason=%s",
        bspline_traj_adapter_->lastFailureReason().c_str());
    } else {
      RCLCPP_INFO(
        get_logger(),
        "BSPLINE_TRAJ_FAIL reason=%s input_points=%zu duration_ms=%.3f fallback=no",
        bspline_traj_adapter_->lastFailureReason().c_str(),
        path_points.size(),
        bspline_traj_adapter_->lastDurationMs());
    }
  }

  void publishBsplineDebug(const builtin_interfaces::msg::Time & stamp)
  {
    if (!bspline_traj_enabled_ || !bspline_traj_adapter_ || !bspline_status_pub_ ||
      !bspline_control_points_pub_ || !bspline_sampled_trajectory_pub_ || !bspline_debug_marker_pub_)
    {
      return;
    }
    const rclcpp::Time rcl_stamp(stamp);
    bspline_status_pub_->publish(bspline_traj_adapter_->exportStatusMsg());
    bspline_control_points_pub_->publish(bspline_traj_adapter_->exportControlPointMarkers(frame_id_, rcl_stamp));
    bspline_sampled_trajectory_pub_->publish(
      bspline_traj_adapter_->exportSampledTrajectoryMsg(frame_id_, rcl_stamp));
    bspline_debug_marker_pub_->publish(bspline_traj_adapter_->exportDebugMarkers(frame_id_, rcl_stamp));
  }

  geometry_msgs::msg::PoseStamped currentGoalForManager(const builtin_interfaces::msg::Time & stamp) const
  {
    if (exploration_fsm_adapter_ && exploration_fsm_adapter_->hasActiveGoal()) {
      return exploration_fsm_adapter_->currentGoal();
    }
    geometry_msgs::msg::PoseStamped goal;
    goal.header.frame_id = frame_id_;
    goal.header.stamp = stamp;
    goal.pose.position = current_waypoint_;
    goal.pose.orientation.w = 1.0;
    return goal;
  }

  nav_msgs::msg::Odometry currentOdomForManager(const builtin_interfaces::msg::Time & stamp) const
  {
    nav_msgs::msg::Odometry odom;
    odom.header.stamp = stamp;
    odom.header.frame_id = frame_id_;
    odom.child_frame_id = base_frame_id_;
    odom.pose.pose.position = uav_position_;
    odom.pose.pose.orientation.w = 1.0;
    return odom;
  }

  void maybeRunPlanManager(const builtin_interfaces::msg::Time & stamp)
  {
    if (!plan_manager_enabled_ || !plan_manager_adapter_) {
      return;
    }
    const rclcpp::Time now(stamp);
    if ((now - last_plan_manager_eval_time_).seconds() < 1.0) {
      return;
    }
    last_plan_manager_eval_time_ = now;
    const auto goal = currentGoalForManager(stamp);
    const auto path_msg = path_searching_adapter_ ?
      makePathMsg(accepted_path_points_, stamp) : nav_msgs::msg::Path();
    const auto path_status = path_searching_adapter_ ?
      path_searching_adapter_->exportStatusMsg().data + " path_collision_free=" +
      (accepted_path_points_.empty() ? "false" : "true") : std::string("PATH_SEARCHING_UNAVAILABLE");
    const auto bspline_msg = bspline_traj_adapter_ ?
      bspline_traj_adapter_->exportSampledTrajectoryMsg(frame_id_, now) : nav_msgs::msg::Path();
    const auto bspline_status = bspline_traj_adapter_ ?
      bspline_traj_adapter_->exportStatusMsg().data : std::string("BSPLINE_TRAJ_UNAVAILABLE");

    RCLCPP_INFO(
      get_logger(),
      "PLAN_MANAGER_EVAL_START goal=(%.3f,%.3f,%.3f) path_points=%zu traj_points=%zu",
      goal.pose.position.x, goal.pose.position.y, goal.pose.position.z,
      path_msg.poses.size(), bspline_msg.poses.size());
    plan_manager_adapter_->updatePipelineInputs(currentOdomForManager(stamp), goal);
    plan_manager_adapter_->updatePathSearchingResult(path_msg, path_status);
    plan_manager_adapter_->updateBsplineCandidate(bspline_msg, bspline_status);
    plan_manager_adapter_->evaluateAndSelectFinalContract();

    const auto contract = plan_manager_adapter_->currentContract();
    last_plan_manager_source_ = contract.source;
    last_plan_manager_safe_ = contract.safe_for_stable_output && !accepted_path_points_.empty();
    const std::string selected = "PLAN_MANAGER_CONTRACT_SELECTED source=" + contract.source +
      " valid=" + std::string(contract.valid ? "true" : "false") +
      " safe=" + std::string(contract.safe_for_stable_output ? "true" : "false") +
      " path_points=" + std::to_string(contract.path_points) +
      " traj_points=" + std::to_string(contract.trajectory_points) +
      " length=" + std::to_string(contract.path_length);
    if (selected != last_logged_plan_manager_selected_) {
      last_logged_plan_manager_selected_ = selected;
      RCLCPP_INFO(get_logger(), "%s", selected.c_str());
    }
    if (!contract.fallback_reason.empty()) {
      const std::string fallback = "PLAN_MANAGER_FALLBACK from=advanced_pipeline to=" + contract.source +
        " reason=" + contract.fallback_reason;
      if (fallback != last_logged_plan_manager_fallback_) {
        last_logged_plan_manager_fallback_ = fallback;
        RCLCPP_INFO(get_logger(), "%s", fallback.c_str());
      }
    }
    if (!contract.safe_for_stable_output && contract.source != "mvp") {
      RCLCPP_INFO(
        get_logger(), "PLAN_MANAGER_CANDIDATE_UNSAFE source=%s path_points=%d traj_points=%d",
        contract.source.c_str(), contract.path_points, contract.trajectory_points);
      const std::string rejected = "PLAN_MANAGER_CONTRACT_REJECTED reason=guarded_stable_output_disabled source=" +
        contract.source;
      if (rejected != last_logged_plan_manager_rejected_) {
        last_logged_plan_manager_rejected_ = rejected;
        RCLCPP_INFO(get_logger(), "%s", rejected.c_str());
      }
    }
  }

  void publishPlanManagerDebug(const builtin_interfaces::msg::Time & stamp)
  {
    if (!plan_manager_enabled_ || !plan_manager_adapter_ || !plan_manager_status_pub_ ||
      !plan_manager_contract_pub_ || !plan_manager_managed_path_pub_ ||
      !plan_manager_managed_trajectory_pub_ || !plan_manager_debug_marker_pub_)
    {
      return;
    }
    const rclcpp::Time rcl_stamp(stamp);
    auto status_msg = plan_manager_adapter_->exportStatusMsg();
    status_msg.data += " path_collision_free=" + std::string(accepted_path_points_.empty() ? "false" : "true") +
      " collision_rejected_count=" + std::to_string(collision_rejected_count_) +
      " path_quality_rejected_count=" + std::to_string(path_quality_rejected_count_) +
      " last_collision_obstacle=" + last_collision_obstacle;
    plan_manager_status_pub_->publish(status_msg);
    auto contract_msg = plan_manager_adapter_->exportContractMsg();
    contract_msg.data += " path_collision_free=" + std::string(accepted_path_points_.empty() ? "false" : "true") +
      " collision_rejected_count=" + std::to_string(collision_rejected_count_) +
      " path_quality_rejected_count=" + std::to_string(path_quality_rejected_count_) +
      " last_collision_obstacle=" + last_collision_obstacle;
    plan_manager_contract_pub_->publish(contract_msg);
    last_trajectory_contract_ = contract_msg.data;
    if (!accepted_path_points_.empty()) {
      const auto safe_path = makePathMsg(accepted_path_points_, stamp);
      plan_manager_managed_path_pub_->publish(safe_path);
      plan_manager_managed_trajectory_pub_->publish(safe_path);
    } else {
      nav_msgs::msg::Path empty;
      empty.header.frame_id = frame_id_;
      empty.header.stamp = stamp;
      plan_manager_managed_path_pub_->publish(empty);
      plan_manager_managed_trajectory_pub_->publish(empty);
    }
    plan_manager_debug_marker_pub_->publish(plan_manager_adapter_->exportDebugMarkers(frame_id_, rcl_stamp));
  }

  bool pointInObstacle(const Eigen::Vector3d & p, double clearance, std::string * obstacle_name = nullptr) const
  {
    for (const auto & obstacle : world_obstacles_) {
      bool inside = false;
      if (obstacle.type == "box") {
        const Eigen::Vector3d d = (p - obstacle.center).cwiseAbs();
        inside = d.x() <= obstacle.size.x() * 0.5 + clearance &&
          d.y() <= obstacle.size.y() * 0.5 + clearance &&
          d.z() <= obstacle.size.z() * 0.5 + clearance;
      } else if (obstacle.type == "cylinder") {
        inside = std::hypot(p.x() - obstacle.center.x(), p.y() - obstacle.center.y()) <=
          obstacle.radius + clearance &&
          std::abs(p.z() - obstacle.center.z()) <= obstacle.height * 0.5 + clearance;
      }
      if (inside) {
        if (obstacle_name) {
          *obstacle_name = obstacle.name;
        }
        return true;
      }
    }
    return false;
  }

  double distanceToObstacleSurface(const Eigen::Vector3d & p) const
  {
    double best = std::numeric_limits<double>::infinity();
    for (const auto & obstacle : world_obstacles_) {
      double d = best;
      if (obstacle.type == "box") {
        const Eigen::Vector3d q = (p - obstacle.center).cwiseAbs() - obstacle.size * 0.5;
        const double outside = Eigen::Vector3d(std::max(q.x(), 0.0), std::max(q.y(), 0.0), std::max(q.z(), 0.0)).norm();
        const double inside = std::min(0.0, std::max(q.x(), std::max(q.y(), q.z())));
        d = outside + inside;
      } else if (obstacle.type == "cylinder") {
        const double radial = std::hypot(p.x() - obstacle.center.x(), p.y() - obstacle.center.y()) - obstacle.radius;
        const double vertical = std::abs(p.z() - obstacle.center.z()) - obstacle.height * 0.5;
        const double outside = std::hypot(std::max(radial, 0.0), std::max(vertical, 0.0));
        const double inside = std::min(0.0, std::max(radial, vertical));
        d = outside + inside;
      }
      best = std::min(best, d);
    }
    return best;
  }

  CollisionResult segmentCollides(
    const Eigen::Vector3d & a,
    const Eigen::Vector3d & b,
    double clearance,
    double resolution) const
  {
    const double length = (b - a).norm();
    const int steps = std::max(1, static_cast<int>(std::ceil(length / std::max(1e-6, resolution))));
    for (int i = 0; i <= steps; ++i) {
      const double r = static_cast<double>(i) / static_cast<double>(steps);
      const Eigen::Vector3d p = a + (b - a) * r;
      std::string obstacle;
      if (pointInObstacle(p, clearance, &obstacle)) {
        return CollisionResult{true, obstacle, p};
      }
    }
    return CollisionResult{};
  }

  CollisionResult pathCollides(
    const std::vector<Eigen::Vector3d> & path,
    double clearance,
    double resolution) const
  {
    for (const auto & p : path) {
      std::string obstacle;
      if (pointInObstacle(p, clearance, &obstacle)) {
        return CollisionResult{true, obstacle, p};
      }
    }
    for (std::size_t i = 1; i < path.size(); ++i) {
      const auto hit = segmentCollides(path[i - 1], path[i], clearance, resolution);
      if (hit.collides) {
        return hit;
      }
    }
    return CollisionResult{};
  }

  double pathLength(const std::vector<Eigen::Vector3d> & path) const
  {
    double length = 0.0;
    for (std::size_t i = 1; i < path.size(); ++i) {
      length += (path[i] - path[i - 1]).norm();
    }
    return length;
  }

  Eigen::Vector3d clampToBounds(const Eigen::Vector3d & p) const
  {
    return Eigen::Vector3d(
      clamp(p.x(), bounds_.min_x + 0.2, bounds_.max_x - 0.2),
      clamp(p.y(), bounds_.min_y + 0.2, bounds_.max_y - 0.2),
      clamp(p.z(), bounds_.min_z + 0.2, bounds_.max_z - 0.2));
  }

  bool pointHasSafeClearance(const Eigen::Vector3d & p) const
  {
    if (p.x() < bounds_.min_x || p.x() > bounds_.max_x ||
      p.y() < bounds_.min_y || p.y() > bounds_.max_y ||
      p.z() < bounds_.min_z || p.z() > bounds_.max_z)
    {
      return false;
    }
    return !pointInObstacle(p, collision_clearance_) &&
           distanceToObstacleSurface(p) >= collision_clearance_;
  }

  std::vector<Eigen::Vector3d> densifyPolyline(const std::vector<Eigen::Vector3d> & input) const
  {
    if (input.size() < 2) {
      return input;
    }
    std::vector<Eigen::Vector3d> output;
    output.push_back(input.front());
    for (std::size_t i = 1; i < input.size(); ++i) {
      const Eigen::Vector3d a = input[i - 1];
      const Eigen::Vector3d b = input[i];
      const double length = (b - a).norm();
      const int segments = std::max(1, static_cast<int>(std::ceil(length / std::max(0.1, densify_step_))));
      for (int j = 1; j <= segments; ++j) {
        const double r = static_cast<double>(j) / static_cast<double>(segments);
        output.push_back(a + (b - a) * r);
      }
    }
    return output;
  }

  PathQualityResult evaluatePathQualityNoSideEffects(const std::vector<Eigen::Vector3d> & input) const
  {
    PathQualityResult result;
    if (input.size() < 2) {
      result.reason = "too_short";
      return result;
    }
    if (pathLength(input) < min_path_length_) {
      result.reason = "too_short";
      return result;
    }
    auto path = densifyPolyline(input);
    if (path.size() < 3) {
      result.reason = "too_short";
      return result;
    }
    if ((path.back() - path.front()).norm() < min_endpoint_progress_) {
      result.reason = "no_progress";
      return result;
    }
    if (!pointHasSafeClearance(path.front()) || !pointHasSafeClearance(path.back())) {
      result.reason = "endpoint_inside_obstacle";
      return result;
    }
    const auto hit = pathCollides(path, collision_clearance_, collision_resolution_);
    if (hit.collides) {
      result.reason = "collision";
      return result;
    }
    double min_obstacle_clearance = std::numeric_limits<double>::infinity();
    for (const auto & p : path) {
      min_obstacle_clearance = std::min(min_obstacle_clearance, distanceToObstacleSurface(p));
    }
    if (!std::isfinite(min_obstacle_clearance) || min_obstacle_clearance < collision_clearance_) {
      result.reason = "low_clearance";
      return result;
    }
    result.accepted = true;
    result.reason = "accepted";
    result.path = path;
    result.length = pathLength(path);
    result.min_clearance = min_obstacle_clearance;
    return result;
  }

  std::optional<Eigen::Vector3d> projectStartIfOccupied(
    const Eigen::Vector3d & start,
    const Eigen::Vector3d & goal)
  {
    if (pointHasSafeClearance(start)) {
      return start;
    }
    const Eigen::Vector3d to_goal = goal - start;
    const double base_angle = std::atan2(to_goal.y(), to_goal.x());
    static const std::array<double, 9> angle_offsets{
      0.0, M_PI_4, -M_PI_4, M_PI_2, -M_PI_2, 3.0 * M_PI_4, -3.0 * M_PI_4, M_PI, -M_PI};
    static const std::array<double, 5> radii{0.2, 0.4, 0.6, 0.8, 1.0};
    for (const double radius : radii) {
      for (const double offset : angle_offsets) {
        Eigen::Vector3d candidate(
          start.x() + radius * std::cos(base_angle + offset),
          start.y() + radius * std::sin(base_angle + offset),
          start.z());
        candidate = clampToBounds(candidate);
        if (pointHasSafeClearance(candidate) &&
          !segmentCollides(start, candidate, 0.0, collision_resolution_).collides)
        {
          ++start_occupied_escape_count_;
          RCLCPP_INFO(
            get_logger(),
            "START_OCCUPIED_ESCAPE original=(%.3f,%.3f,%.3f) projected=(%.3f,%.3f,%.3f) radius=%.1f",
            start.x(), start.y(), start.z(),
            candidate.x(), candidate.y(), candidate.z(), radius);
          return candidate;
        }
      }
    }
    RCLCPP_INFO(get_logger(), "START_OCCUPIED_ESCAPE_FAILED");
    return std::nullopt;
  }

  std::optional<std::vector<Eigen::Vector3d>> findSafeDetourCandidate(
    const Eigen::Vector3d & start,
    const Eigen::Vector3d & goal) const
  {
    const Eigen::Vector3d delta = goal - start;
    const double xy_norm = std::hypot(delta.x(), delta.y());
    if (xy_norm < 1e-6) {
      return std::nullopt;
    }
    const Eigen::Vector3d perp(-delta.y() / xy_norm, delta.x() / xy_norm, 0.0);
    const Eigen::Vector3d mid = (start + goal) * 0.5;
    std::vector<std::vector<Eigen::Vector3d>> candidates;
    for (double offset : {0.8, 1.2, 1.8, 2.5, 3.5, 4.5}) {
      for (double side : {-1.0, 1.0}) {
        candidates.push_back({start, clampToBounds(mid + perp * offset * side), goal});
      }
    }
    candidates.push_back({start, clampToBounds(Eigen::Vector3d(start.x(), goal.y(), goal.z())), goal});
    candidates.push_back({start, clampToBounds(Eigen::Vector3d(goal.x(), start.y(), goal.z())), goal});
    for (const auto & candidate : candidates) {
      const auto quality = evaluatePathQualityNoSideEffects(candidate);
      if (quality.accepted && quality.path.size() >= 5) {
        return quality.path;
      }
    }
    return std::nullopt;
  }

  std::optional<std::vector<Eigen::Vector3d>> generateSafeDetour(
    const Eigen::Vector3d & start,
    const Eigen::Vector3d & goal,
    const std::string & reason)
  {
    const auto detour = findSafeDetourCandidate(start, goal);
    if (detour) {
      ++safe_detour_generated_count_;
      RCLCPP_INFO(
        get_logger(),
        "SAFE_DETOUR_GENERATED reason=%s points=%zu length=%.3f",
        reason.c_str(), detour->size(), pathLength(*detour));
      return detour;
    }
    ++safe_detour_failed_count_;
    RCLCPP_INFO(get_logger(), "SAFE_DETOUR_FAILED reason=%s", reason.c_str());
    return std::nullopt;
  }

  ReachabilityResult precheckGoalReachability(
    const Eigen::Vector3d & raw_start,
    const Eigen::Vector3d & goal)
  {
    ReachabilityResult result;
    result.start = raw_start;
    auto reject = [this, &result, &goal](const std::string & reason) {
        result.reachable = false;
        result.reason = reason;
        ++reachability_rejected_count_;
        RCLCPP_INFO(get_logger(), "GOAL_REACHABILITY_REJECTED reason=%s", reason.c_str());
        blacklistGoalRegion(goal, reason);
        return result;
      };
    std::string obstacle;
    if (pointInObstacle(goal, 0.0, &obstacle)) {
      last_collision_obstacle = obstacle;
      return reject("collision");
    }
    if (!pointHasSafeClearance(goal)) {
      return reject("low_clearance");
    }
    const auto projected = projectStartIfOccupied(raw_start, goal);
    if (!projected) {
      return reject("start_occupied");
    }
    result.start = *projected;
    const auto direct = evaluatePathQualityNoSideEffects({result.start, goal});
    if (!direct.accepted && !findSafeDetourCandidate(result.start, goal)) {
      return reject("no_grid_path");
    }
    result.reachable = true;
    result.reason = "reachable";
    return result;
  }

  void blacklistGoalRegion(const Eigen::Vector3d & goal, const std::string & reason)
  {
    const rclcpp::Time now = get_clock()->now();
    ++goal_blacklist_count_;
    goal_blacklist_.push_back({goal, now});
    RCLCPP_INFO(
      get_logger(),
      "GOAL_TEMP_BLACKLISTED reason=%s goal=(%.3f,%.3f,%.3f)",
      reason.c_str(), goal.x(), goal.y(), goal.z());
  }

  void handleRejectedExecutablePath(const std::string & reason, const std::string & source)
  {
    ++reselect_goal_count_;
    accepted_path_active_ = false;
    RCLCPP_INFO(
      get_logger(),
      "FSM_TRANSITION from=EXECUTE_TRAJECTORY to=RESELECT_GOAL reason=EXECUTABLE_PATH_REJECTED source=%s reject_reason=%s",
      source.c_str(), reason.c_str());
    chooseNextWaypoint(true);
  }

  bool trySafeDetourOrSweep(
    const Eigen::Vector3d & start,
    const Eigen::Vector3d & goal,
    const std::string & reason,
    const builtin_interfaces::msg::Time & stamp)
  {
    if (reason == "collision" || reason == "low_clearance" || reason == "no_grid_path") {
      const auto detour = generateSafeDetour(start, goal, reason);
      if (detour) {
        acceptExecutablePath(*detour, "safe_detour", stamp);
        return true;
      }
    }
    handleRejectedExecutablePath(reason, "path_quality");
    return generateFallbackSafeSweep(start, stamp);
  }

  bool generateFallbackSafeSweep(const Eigen::Vector3d & start, const builtin_interfaces::msg::Time & stamp)
  {
    const rclcpp::Time now(stamp);
    const Eigen::Vector3d safe_start = clampToBounds(start);
    const double z = clamp(safe_start.z(), bounds_.min_z + 0.2, bounds_.max_z - 0.2);
    for (double distance : {1.5, 2.0, 2.5, 3.0}) {
      for (int i = 0; i < 16; ++i) {
        const double angle = static_cast<double>(i) * 2.0 * M_PI / 16.0;
        Eigen::Vector3d goal(
          safe_start.x() + distance * std::cos(angle),
          safe_start.y() + distance * std::sin(angle),
          z);
        goal = clampToBounds(goal);
        if (isGoalBlacklisted(goal, now)) {
          continue;
        }
        const auto quality = evaluatePathQualityNoSideEffects({safe_start, goal});
        if (!quality.accepted) {
          continue;
        }
        current_waypoint_.x = goal.x();
        current_waypoint_.y = goal.y();
        current_waypoint_.z = goal.z();
        recordSelectedGoal(goal, now);
        ++fallback_safe_sweep_count_;
        RCLCPP_INFO(
          get_logger(),
          "FALLBACK_SAFE_SWEEP_SELECTED goal=(%.3f,%.3f,%.3f)",
          goal.x(), goal.y(), goal.z());
        RCLCPP_INFO(
          get_logger(),
          "FALLBACK_SAFE_SWEEP_PATH_READY points=%zu length=%.3f",
          quality.path.size(), quality.length);
        acceptExecutablePath(quality.path, "fallback_safe_sweep", stamp);
        return true;
      }
    }
    return false;
  }

  std::vector<Eigen::Vector3d> densifyPathForBspline(const std::vector<Eigen::Vector3d> & input)
  {
    const double length = pathLength(input);
    if (input.size() == 2 && length >= min_path_length_) {
      const int segments = std::max(4, static_cast<int>(std::ceil(length / std::max(0.1, densify_step_))));
      std::vector<Eigen::Vector3d> output;
      output.reserve(static_cast<std::size_t>(segments + 1));
      for (int i = 0; i <= segments; ++i) {
        const double r = static_cast<double>(i) / static_cast<double>(segments);
        output.push_back(input.front() + (input.back() - input.front()) * r);
      }
      RCLCPP_INFO(
        get_logger(),
        "PATH_DENSIFIED_FOR_BSPLINE original_points=2 densified_points=%zu length=%.3f",
        output.size(), length);
      ++path_densified_count_;
      return output;
    }
    return input;
  }

  PathQualityResult filterPathQuality(const std::vector<Eigen::Vector3d> & input, const std::string & source)
  {
    PathQualityResult result;
    auto warn_accept = [this, &result, &source, &input](const std::string & reason) {
        auto path = densifyPathForBspline(input);
        if (path.size() < 2) {
          result.accepted = false;
          result.reason = reason;
          return result;
        }
        result.accepted = true;
        result.reason = "warn_" + reason;
        result.path = path;
        result.length = pathLength(path);
        result.min_clearance = std::isfinite(distanceToObstacleSurface(path.front())) ?
          distanceToObstacleSurface(path.front()) : 0.0;
        ++collision_warning_count_;
        RCLCPP_INFO(
          get_logger(),
          "PATH_QUALITY_WARNING reason=%s source=%s online_collision_gate_mode=%s executable_not_blocked=true",
          reason.c_str(), source.c_str(), online_collision_gate_mode_.c_str());
        publishRejectedPathDebug(input, reason);
        return result;
      };
    auto reject = [this, &result, &source, &input, &warn_accept](const std::string & reason) {
        if (!onlineCollisionGateEnforced() &&
          (reason == "collision" || reason == "low_clearance" ||
          reason == "endpoint_inside_obstacle" || reason == "no_progress"))
        {
          return warn_accept(reason);
        }
        result.accepted = false;
        result.reason = reason;
        ++path_quality_rejected_count_;
        RCLCPP_INFO(get_logger(), "PATH_QUALITY_REJECTED reason=%s source=%s", reason.c_str(), source.c_str());
        publishRejectedPathDebug(input, reason);
        if (reason == "low_clearance") {
          invalidateCurrentGoalForLowClearance();
        }
        return result;
      };
    if (input.size() < 2) {
      return reject("too_short");
    }
    const double original_length = pathLength(input);
    if (original_length < min_path_length_) {
      RCLCPP_INFO(get_logger(), "PATH_TOO_SHORT_REJECTED_FOR_EXPLORATION length=%.3f", original_length);
      return reject("too_short");
    }
    auto path = densifyPathForBspline(input);
    if (path.size() < 3) {
      return reject("too_short");
    }
    if ((path.back() - path.front()).norm() < min_endpoint_progress_) {
      return reject("no_progress");
    }
    std::string endpoint_obstacle;
    if (pointInObstacle(path.front(), 0.0, &endpoint_obstacle) || pointInObstacle(path.back(), 0.0, &endpoint_obstacle)) {
      last_collision_obstacle = endpoint_obstacle;
      return reject("endpoint_inside_obstacle");
    }
    const auto hit = pathCollides(path, collision_clearance_, collision_resolution_);
    if (hit.collides) {
      ++collision_rejected_count_;
      ++path_collision_count_;
      last_collision_obstacle = hit.obstacle;
      RCLCPP_INFO(
        get_logger(),
        "PATH_COLLISION_REJECTED collision_obstacle=%s collision_point=(%.3f,%.3f,%.3f)",
        hit.obstacle.c_str(), hit.point.x(), hit.point.y(), hit.point.z());
      return reject("collision");
    }
    double min_obstacle_clearance = std::numeric_limits<double>::infinity();
    for (const auto & p : path) {
      min_obstacle_clearance = std::min(min_obstacle_clearance, distanceToObstacleSurface(p));
    }
    if (!std::isfinite(min_obstacle_clearance) || min_obstacle_clearance < collision_clearance_) {
      return reject("low_clearance");
    }
    result.accepted = true;
    result.reason = "accepted";
    result.path = path;
    result.length = pathLength(path);
    result.min_clearance = min_obstacle_clearance;
    return result;
  }

  bool onlineCollisionGateEnforced() const
  {
    return online_collision_gate_mode_ == "enforce";
  }

  void publishRejectedPathDebug(const std::vector<Eigen::Vector3d> & path, const std::string & reason)
  {
    const auto msg = makePathMsg(path, get_clock()->now());
    if (debug_rejected_path_pub_) {
      debug_rejected_path_pub_->publish(msg);
    }
    if (reason == "collision" && debug_collision_path_pub_) {
      debug_collision_path_pub_->publish(msg);
    }
    if (reason == "low_clearance" && debug_low_clearance_path_pub_) {
      debug_low_clearance_path_pub_->publish(msg);
    }
    RCLCPP_INFO(
      get_logger(),
      "DEBUG_PATH_PUBLISHED reason=%s debug_only=true executable_path_collision_free=false",
      reason.c_str());
  }

  void invalidateCurrentGoalForLowClearance()
  {
    const Eigen::Vector3d goal(current_waypoint_.x, current_waypoint_.y, current_waypoint_.z);
    const rclcpp::Time now = get_clock()->now();
    if (!last_low_clearance_goal_valid_ ||
      (goal - last_low_clearance_goal_).norm() > recent_goal_radius_)
    {
      last_low_clearance_goal_ = goal;
      last_low_clearance_goal_valid_ = true;
      consecutive_low_clearance_rejects_ = 0;
    }
    ++consecutive_low_clearance_rejects_;
    if (consecutive_low_clearance_rejects_ > 2) {
      blacklistGoalRegion(goal, "low_clearance");
      RCLCPP_INFO(
        get_logger(),
        "GOAL_INVALIDATED_BY_LOW_CLEARANCE goal=(%.3f,%.3f,%.3f) rejects=%d",
        goal.x(), goal.y(), goal.z(), consecutive_low_clearance_rejects_);
      RCLCPP_INFO(get_logger(), "GOAL_TEMP_BLACKLISTED reason=low_clearance");
      RCLCPP_INFO(get_logger(), "REPLAN_DUE_TO_LOW_CLEARANCE_GOAL_INVALID");
      RCLCPP_INFO(get_logger(), "FSM_RECOVERY_EXHAUSTED_SELECT_NEW_REGION");
      handleRejectedExecutablePath("low_clearance", "path_quality");
      chooseNextWaypoint();
      consecutive_low_clearance_rejects_ = 0;
      last_low_clearance_goal_valid_ = false;
    }
  }

  bool isGoalBlacklisted(const Eigen::Vector3d & goal, const rclcpp::Time & now) const
  {
    for (const auto & item : goal_blacklist_) {
      if ((now - item.second).seconds() <= blacklist_duration_sec_ &&
        (goal - item.first).norm() <= recent_goal_radius_)
      {
        return true;
      }
    }
    return false;
  }

  void recordSelectedGoal(const Eigen::Vector3d & goal, const rclcpp::Time & now)
  {
    int recent_hits = 0;
    for (const auto & item : recent_goals_) {
      if ((now - item.second).seconds() <= recent_goal_cooldown_sec_ &&
        (goal - item.first).norm() <= recent_goal_radius_)
      {
        ++recent_hits;
      }
    }
    if (recent_hits > 0) {
      ++goal_revisit_penalized_count_;
      RCLCPP_INFO(
        get_logger(), "GOAL_REVISIT_PENALIZED recent_hits=%d penalty=%.3f",
        recent_hits, goal_revisit_penalty_);
    }
    if (recent_hits + 1 >= max_revisit_before_blacklist_) {
      ++goal_blacklist_count_;
      goal_blacklist_.push_back({goal, now});
      RCLCPP_INFO(get_logger(), "GOAL_TEMP_BLACKLISTED");
    }
    recent_goals_.push_back({goal, now});
    while (recent_goals_.size() > 40) {
      recent_goals_.pop_front();
    }
    ++waypoint_index_;
    ++replanning_count_;
    last_goal_select_time_ = now;
  }

  void logLocalTrajectorySource(const std::string & source, std::size_t points, bool guarded)
  {
    const std::string log = "LOCAL_TRAJECTORY_SOURCE source=" + source +
      " guarded=" + std::string(guarded ? "true" : "false") +
      " points=" + std::to_string(points);
    if (log != last_logged_local_trajectory_source_) {
      last_logged_local_trajectory_source_ = log;
      RCLCPP_INFO(get_logger(), "%s", log.c_str());
    }
  }

  void updateRealInterfacePlannerOutputs(const builtin_interfaces::msg::Time &)
  {
    if (!real_interface_enabled_ || !real_interface_adapter_) {
      return;
    }
    real_interface_adapter_->updatePlannerOutputs(
      last_waypoint_msg_, last_global_path_msg_, last_local_trajectory_msg_, last_trajectory_contract_);
  }

  void publishRealInterfaceDebug(const builtin_interfaces::msg::Time & stamp)
  {
    if (!real_interface_enabled_ || !real_interface_adapter_ || !real_interface_status_pub_ ||
      !real_interface_input_status_pub_ || !real_interface_output_status_pub_ ||
      !real_interface_debug_marker_pub_ || !control_bridge_status_pub_ || !mode_manager_status_pub_)
    {
      return;
    }
    const rclcpp::Time rcl_stamp(stamp);
    real_interface_status_pub_->publish(real_interface_adapter_->exportStatusMsg());
    real_interface_input_status_pub_->publish(real_interface_adapter_->exportInputStatusMsg());
    real_interface_output_status_pub_->publish(real_interface_adapter_->exportOutputStatusMsg());
    real_interface_debug_marker_pub_->publish(real_interface_adapter_->exportDebugMarkers(frame_id_, rcl_stamp));
    control_bridge_status_pub_->publish(real_interface_adapter_->exportControlBridgeStatusMsg());
    mode_manager_status_pub_->publish(real_interface_adapter_->exportModeManagerStatusMsg());
    RCLCPP_INFO_THROTTLE(
      get_logger(), *get_clock(), 3000, "%s",
      real_interface_adapter_->exportStatusMsg().data.c_str());
  }

  std::string frame_id_;
  std::string odom_frame_id_;
  std::string base_frame_id_;
  Bounds bounds_;
  double default_z_{1.4};
  double speed_mps_{0.6};
  double waypoint_accept_radius_{0.25};
  double replan_period_s_{4.0};
  bool publish_tf_{true};
  std::string planner_backend_{"mvp"};
  std::string cloud_qos_mode_{"rviz_compatible"};
  double collision_clearance_{0.35};
  double collision_resolution_{0.10};
  double min_path_length_{1.0};
  double densify_step_{0.4};
  double min_endpoint_progress_{0.5};
  double recent_goal_cooldown_sec_{20.0};
  double recent_goal_radius_{1.5};
  double goal_revisit_penalty_{0.7};
  double minimum_goal_hold_sec_{5.0};
  int max_revisit_before_blacklist_{3};
  double blacklist_duration_sec_{45.0};
  double minimum_execution_time_before_replan_{5.0};
  double goal_reached_radius_{0.8};
  double goal_progress_timeout_sec_{20.0};
  double minimum_progress_distance_{0.5};
  bool plan_env_enabled_{false};
  bool frontier_fis_enabled_{false};
  bool exploration_fsm_enabled_{false};
  bool path_searching_enabled_{false};
  bool bspline_traj_enabled_{false};
  bool plan_manager_enabled_{false};
  bool real_interface_enabled_{false};
  bool use_frontier_goal_source_{false};
  std::string online_collision_gate_mode_{"warn"};
  bool large_world_layout_{false};
  size_t waypoint_index_{0};
  size_t replanning_count_{0};
  size_t collision_rejected_count_{0};
  size_t path_quality_rejected_count_{0};
  size_t goal_blacklist_count_{0};
  size_t goal_revisit_penalized_count_{0};
  size_t path_densified_count_{0};
  size_t path_collision_count_{0};
  size_t reachability_rejected_count_{0};
  size_t start_occupied_escape_count_{0};
  size_t safe_detour_generated_count_{0};
  size_t safe_detour_failed_count_{0};
  size_t fallback_safe_sweep_count_{0};
  size_t no_safe_sweep_hold_count_{0};
  size_t reselect_goal_count_{0};
  size_t collision_warning_count_{0};
  geometry_msgs::msg::Point uav_position_{};
  geometry_msgs::msg::Point current_waypoint_{};
  geometry_msgs::msg::Point last_progress_position_{};
  std::vector<std::array<double, 3>> obstacle_points_;
  std::vector<WorldObstacle> world_obstacles_;
  std::vector<Eigen::Vector3d> accepted_path_points_;
  bool accepted_path_active_{false};
  std::string last_collision_obstacle{"none"};
  std::deque<std::pair<Eigen::Vector3d, rclcpp::Time>> recent_goals_;
  std::deque<std::pair<Eigen::Vector3d, rclcpp::Time>> goal_blacklist_;
  Eigen::Vector3d last_low_clearance_goal_{0.0, 0.0, 0.0};
  bool last_low_clearance_goal_valid_{false};
  int consecutive_low_clearance_rejects_{0};

  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr map_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr global_cloud_pub_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr waypoint_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr traj_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr safety_gate_safe_trajectory_clear_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr debug_rejected_path_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr debug_collision_path_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr debug_low_clearance_path_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr state_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr metrics_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr demo_truth_status_pub_;
  rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr demo_truth_marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr plan_env_status_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr plan_env_occupied_pub_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr plan_env_inflated_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr plan_env_frontier_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr plan_env_debug_marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr fis_status_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr fis_frontier_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr fis_viewpoint_pub_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr fis_best_viewpoint_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr fis_debug_marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr fsm_status_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr fsm_state_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr fsm_transition_pub_;
  rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr fsm_current_goal_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr fsm_debug_marker_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr fsm_path_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr path_searching_status_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_searching_path_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr path_searching_visited_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr path_searching_debug_marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr bspline_status_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr bspline_control_points_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr bspline_sampled_trajectory_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr bspline_debug_marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr plan_manager_status_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr plan_manager_contract_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr plan_manager_managed_path_pub_;
  rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr plan_manager_managed_trajectory_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr plan_manager_debug_marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr real_interface_status_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr real_interface_input_status_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr real_interface_output_status_pub_;
  rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr real_interface_debug_marker_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr control_bridge_status_pub_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr mode_manager_status_pub_;
  std::unique_ptr<FuelPlanEnvAdapter> plan_env_adapter_;
  std::unique_ptr<FuelFrontierFisAdapter> frontier_fis_adapter_;
  std::unique_ptr<FuelExplorationFsmAdapter> exploration_fsm_adapter_;
  std::unique_ptr<FuelPathSearchingAdapter> path_searching_adapter_;
  std::unique_ptr<FuelBsplineTrajAdapter> bspline_traj_adapter_;
  std::unique_ptr<FuelPlanManagerAdapter> plan_manager_adapter_;
  std::unique_ptr<FuelRealInterfaceAdapter> real_interface_adapter_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr real_odom_sub_;
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr real_map_sub_;
  geometry_msgs::msg::PoseStamped last_waypoint_msg_;
  nav_msgs::msg::Path last_global_path_msg_;
  nav_msgs::msg::Path last_local_trajectory_msg_;
  std::string last_trajectory_contract_;
  std::string last_plan_manager_source_{"none"};
  bool last_plan_manager_safe_{false};
  bool last_fsm_timeout_active_{false};
  size_t execution_timeout_count_{0};
  std::string last_logged_fsm_transition_;
  std::string last_logged_fsm_goal_;
  std::string last_logged_fsm_fallback_;
  std::string last_logged_fsm_path_source_;
  std::string last_logged_local_trajectory_source_;
  std::string last_logged_plan_manager_selected_;
  std::string last_logged_plan_manager_fallback_;
  std::string last_logged_plan_manager_rejected_;
  rclcpp::Time last_path_search_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_bspline_generation_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_plan_manager_eval_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_goal_select_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_execution_start_time_{0, 0, RCL_ROS_TIME};
  rclcpp::Time last_progress_check_time_{0, 0, RCL_ROS_TIME};
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::TimerBase::SharedPtr fast_timer_;
  rclcpp::TimerBase::SharedPtr slow_timer_;
  rclcpp::TimerBase::SharedPtr replan_timer_;
};

}  // namespace fuel_ros2

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<fuel_ros2::FuelMvpNode>());
  rclcpp::shutdown();
  return 0;
}
