#!/usr/bin/env python3
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path as FilesystemPath
from typing import Dict, List, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped, TransformStamped
from nav_msgs.msg import Odometry, Path
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy._rclpy_pybind11 import RCLError
from rclpy.node import Node
from std_msgs.msg import String
from tf2_ros import TransformBroadcaster
from visualization_msgs.msg import Marker

SCRIPT_DIR = FilesystemPath(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
try:
    from world_collision_checker import load_obstacles, path_collision
except Exception:  # pragma: no cover - startup logs explain disabled gate
    load_obstacles = None
    path_collision = None


SOURCE_PRIORITY = [
    ("/fuel/plan_manager/managed_trajectory", "plan_manager"),
    ("/fuel/bspline/sampled_trajectory", "bspline"),
    ("/fuel/safety_gate/safe_trajectory", "safety_gate"),
    ("/fuel/local_trajectory", "local_trajectory"),
    ("/fuel/path_searching/path", "path_searching"),
    ("/fuel/global_path", "global_path"),
]
SOURCE_RANK = {name: index for index, (_, name) in enumerate(SOURCE_PRIORITY)}
SOURCE_RANK["waypoint"] = len(SOURCE_PRIORITY)
SOURCE_RANK["none"] = len(SOURCE_PRIORITY) + 1


class GazeboUavTrajectoryFollower(Node):
    def __init__(self):
        super().__init__("gazebo_uav_trajectory_follower")
        self.frame_id = self.declare_parameter("frame_id", "map").value
        self.base_frame_id = self.declare_parameter("base_frame_id", "base_link").value
        self.gazebo_model_name = self.declare_parameter("gazebo_model_name", "fuel_simple_uav").value
        self.max_speed = max(0.05, float(self.declare_parameter("max_speed", 1.0).value))
        self.max_horizontal_accel = max(0.05, float(self.declare_parameter("max_horizontal_accel", 0.8).value))
        self.max_vertical_speed = min(0.25, max(0.02, float(self.declare_parameter("max_vertical_speed", 0.25).value)))
        self.max_vertical_accel = min(0.4, max(0.02, float(self.declare_parameter("max_vertical_accel", 0.4).value)))
        self.source_hold_sec = max(0.0, float(self.declare_parameter("source_hold_sec", 0.5).value))
        self.z_lowpass_alpha = min(1.0, max(0.05, float(self.declare_parameter("z_lowpass_alpha", 0.2).value)))
        self.update_rate = max(1.0, float(self.declare_parameter("update_rate", 20.0).value))
        env_marker_rate = self._env_float("VISUAL_DEMO_MARKER_RATE", 10.0)
        env_trail_max_points = self._env_float("VISUAL_DEMO_TRAIL_MAX_POINTS", 3000.0)
        self.visual_demo_frontier_points_max = int(
            max(0.0, self._env_float("VISUAL_DEMO_FRONTIER_POINTS_MAX", 1000.0))
        )
        self.visual_demo_cloud_stride = int(max(1.0, self._env_float("VISUAL_DEMO_CLOUD_STRIDE", 1.0)))
        self.marker_rate = min(
            10.0,
            max(1.0, self._numeric_parameter("visual_demo_marker_rate", env_marker_rate)),
        )
        self.trail_max_points = int(
            max(1.0, self._numeric_parameter("trail_max_points", env_trail_max_points))
        )
        self.loop_trajectory = bool(self.declare_parameter("loop_trajectory", False).value)
        self.max_demo_distance = max(1.0, float(self.declare_parameter("max_demo_distance", 80.0).value))
        self.hold_at_goal = bool(self.declare_parameter("hold_at_goal", True).value)
        self.trajectory_source = self.declare_parameter("trajectory_source", "auto").value
        self.visual_demo_allow_unsafe_candidate = bool(
            self.declare_parameter("visual_demo_allow_unsafe_candidate", True).value
        )
        self.visual_demo_preferred_sources = list(
            self.declare_parameter(
                "visual_demo_preferred_sources",
                ["plan_manager", "bspline", "safety_gate", "local_trajectory", "path_searching", "global_path"],
            ).value
        )
        self.min_executable_points = max(1, int(self.declare_parameter("min_executable_points", 3).value))
        self.min_executable_length = max(0.0, float(self.declare_parameter("min_executable_length", 0.5).value))
        self.candidate_age_reset_on_same_source_update = bool(
            self.declare_parameter("candidate_age_reset_on_same_source_update", False).value
        )
        self.execute_unsafe_with_warning = bool(self.declare_parameter("execute_unsafe_with_warning", True).value)
        env_gate_mode = os.environ.get("ONLINE_COLLISION_GATE_MODE", "warn").strip().lower()
        self.online_collision_gate_mode = str(
            self.declare_parameter("online_collision_gate_mode", env_gate_mode or "warn").value
        ).strip().lower()
        if self.online_collision_gate_mode not in {"off", "warn", "enforce"}:
            self.get_logger().warning(
                f"ONLINE_COLLISION_GATE_MODE_INVALID value={self.online_collision_gate_mode} fallback=warn"
            )
            self.online_collision_gate_mode = "warn"
        self.enable_collision_gate = bool(self.declare_parameter("enable_collision_gate", True).value)
        self.enable_collision_gate = self.enable_collision_gate and self.online_collision_gate_mode != "off"
        self.world_config = self.declare_parameter(
            "world_config",
            "/home/nuaa/ZHY/FUEL_PLANNER_V2/ros2_ws/src/fuel_ros2/config/fuel_visual_world_exploration.yaml",
        ).value
        self.collision_clearance = max(0.0, float(self.declare_parameter("collision_clearance", 0.35).value))
        self.collision_resolution = max(0.02, float(self.declare_parameter("collision_resolution", 0.1).value))
        self.enable_gazebo_pose_update = bool(self.declare_parameter("enable_gazebo_pose_update", True).value)
        self.gazebo_update_rate = max(0.5, float(self.declare_parameter("gazebo_update_rate", 5.0).value))
        self.position = [
            float(self.declare_parameter("initial_x", 0.0).value),
            float(self.declare_parameter("initial_y", -3.0).value),
            float(self.declare_parameter("initial_z", 1.0).value),
        ]
        self.paths: Dict[str, List[Tuple[float, float, float]]] = {}
        self.source_update_time: Dict[str, float] = {}
        self.source_first_seen_time: Dict[str, float] = {}
        self.waypoint: Optional[Tuple[float, float, float]] = None
        self.target_index = 0
        self.active_source = "none"
        self.previous_source = "none"
        self.active_points: List[Tuple[float, float, float]] = []
        self.velocity = [0.0, 0.0, 0.0]
        self.last_accel = [0.0, 0.0, 0.0]
        self.filtered_target_z = self.position[2]
        self.status_event = "NO_ACTIVE_TRAJECTORY_HOLD_POSITION"
        self.last_source_event = "none"
        self.candidate_source = "none"
        self.hold_reason = "no_executable_source"
        self.unsafe_visual_execution = False
        self._last_active_log_key = ""
        self.last_switch_time = 0.0
        self.trail: List[PoseStamped] = []
        self.odom_distance = 0.0
        self.last_position_for_distance = list(self.position)
        self.distance_anomaly_logged = False
        self.hold_at_goal_active = False
        self.last_gazebo_update = self.get_clock().now()
        self.gazebo_pose_update_ok = False
        self.gazebo_pose_update_reason = "not_attempted"
        self.gazebo_pose_before = "GAZEBO_POSE_READBACK_UNAVAILABLE"
        self.gazebo_pose_after = "GAZEBO_POSE_READBACK_UNAVAILABLE"
        self.gazebo_readback_z: Optional[float] = None
        self.gazebo_z_mismatch = 0.0
        self.gazebo_pose_reset = False
        self.gazebo_pose_reset_reason = "none"
        self.last_gazebo_mismatch_log = ""
        self.last_hold_log_time = 0.0
        self.last_marker_publish = self.get_clock().now()
        self.world_obstacles = []
        self.last_rejection_reason: Dict[str, str] = {}
        self.last_rejection_log_key = ""
        self.last_warning_log_key = ""
        self.collision_warning_count = 0
        self.collision_enforced_count = 0
        self.hold_due_to_collision_gate_count = 0
        self.holding_no_collision_free_logged = False
        if self.enable_collision_gate and load_obstacles is not None:
            try:
                self.world_obstacles = load_obstacles(FilesystemPath(str(self.world_config)))
            except Exception as exc:
                self.get_logger().error(
                    f"FOLLOWER_COLLISION_GATE_LOAD_FAILED world_config={self.world_config} exception={exc}"
                )
                self.enable_collision_gate = False
        elif self.enable_collision_gate:
            self.get_logger().error("FOLLOWER_COLLISION_GATE_IMPORT_FAILED")
            self.enable_collision_gate = False

        for topic, name in SOURCE_PRIORITY:
            self.create_subscription(Path, topic, lambda msg, n=name: self._path_cb(n, msg), 10)
        self.create_subscription(PoseStamped, "/fuel/waypoint", self._waypoint_cb, 10)

        self.odom_pub = self.create_publisher(Odometry, "/odom", 20)
        self.state_pub = self.create_publisher(Odometry, "/state_estimation", 20)
        self.pose_pub = self.create_publisher(PoseStamped, "/fuel/visual/uav_pose", 20)
        self.marker_pub = self.create_publisher(Marker, "/fuel/visual/uav_marker", 20)
        self.trail_pub = self.create_publisher(Path, "/fuel/visual/uav_trail", 10)
        self.status_pub = self.create_publisher(String, "/fuel/visual/uav_follower_status", 10)
        self.status_text_pub = self.create_publisher(Marker, "/fuel/visual/status_text", 10)
        self.warning_text_pub = self.create_publisher(Marker, "/fuel/visual/warning_text", 10)
        self.legend_pub = self.create_publisher(Marker, "/fuel/visual/legend_marker", 10)
        self.uav_label_pub = self.create_publisher(Marker, "/fuel/visual/uav_label", 10)
        self.goal_marker_pub = self.create_publisher(Marker, "/fuel/visual/current_goal", 10)
        self.goal_label_pub = self.create_publisher(Marker, "/fuel/visual/goal_label", 10)
        self.path_label_pub = self.create_publisher(Marker, "/fuel/visual/path_label", 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(1.0 / self.update_rate, self._step)
        self.get_logger().info(
            f"GAZEBO_UAV_TRAJECTORY_FOLLOWER_RUNNING max_speed={self.max_speed:.2f} "
            f"update_rate={self.update_rate:.2f} marker_rate={self.marker_rate:.2f} source={self.trajectory_source} "
            f"source_hold_sec={self.source_hold_sec:.2f} max_vertical_speed={self.max_vertical_speed:.2f} "
            f"max_vertical_accel={self.max_vertical_accel:.2f} max_horizontal_accel={self.max_horizontal_accel:.2f} "
            f"gazebo_pose_update={str(self.enable_gazebo_pose_update).lower()} real_flight_command=false "
            f"loop_trajectory={str(self.loop_trajectory).lower()} max_demo_distance={self.max_demo_distance:.2f} "
            f"hold_at_goal={str(self.hold_at_goal).lower()} "
            f"visual_demo_allow_unsafe_candidate={str(self.visual_demo_allow_unsafe_candidate).lower()} "
            f"execute_unsafe_with_warning={str(self.execute_unsafe_with_warning).lower()} "
            f"min_executable_points={self.min_executable_points} min_executable_length={self.min_executable_length:.2f} "
            f"ONLINE_COLLISION_GATE_MODE={self.online_collision_gate_mode} "
            f"enable_collision_gate={str(self.enable_collision_gate).lower()} "
            f"collision_clearance={self.collision_clearance:.2f} collision_resolution={self.collision_resolution:.2f} "
            f"world_config={self.world_config} obstacles={len(self.world_obstacles)} "
            f"visual_demo_preferred_sources={','.join(self.visual_demo_preferred_sources)} "
            f"VISUAL_DEMO_MARKER_RATE={self.marker_rate:.2f} "
            f"VISUAL_DEMO_TRAIL_MAX_POINTS={self.trail_max_points} "
            f"VISUAL_DEMO_FRONTIER_POINTS_MAX={self.visual_demo_frontier_points_max} "
            f"VISUAL_DEMO_CLOUD_STRIDE={self.visual_demo_cloud_stride}"
        )

    def _env_float(self, name: str, default: float) -> float:
        raw = os.environ.get(name)
        if raw is None or raw == "":
            return default
        try:
            return float(raw)
        except (TypeError, ValueError):
            self.get_logger().error(
                f"READABLE_DEMO_PARAMETER_PARSE_FAILED name={name} value={raw!r} default={default}"
            )
            return default

    def _numeric_parameter(self, name: str, default: float) -> float:
        descriptor = ParameterDescriptor(dynamic_typing=True)
        value = self.declare_parameter(name, default, descriptor=descriptor).value
        try:
            return float(value)
        except (TypeError, ValueError):
            self.get_logger().error(
                f"READABLE_DEMO_PARAMETER_PARSE_FAILED name={name} value={value!r} default={default}"
            )
            return float(default)

    def _path_cb(self, name: str, msg: Path):
        if msg.poses:
            self.paths[name] = [(p.pose.position.x, p.pose.position.y, p.pose.position.z) for p in msg.poses]
            now_sec = self._now_sec()
            self.source_update_time[name] = now_sec
            if self.candidate_age_reset_on_same_source_update or name not in self.source_first_seen_time:
                self.source_first_seen_time[name] = now_sec
            self.status_event = f"TRAJECTORY_SOURCE_UPDATED source={name} points={len(msg.poses)}"
            self.last_source_event = self.status_event
            self.get_logger().info(self.status_event)
            if self.active_source == name:
                self.target_index = self._project_target_index(self.paths[name], self.target_index)
        else:
            self.paths.pop(name, None)
            self.source_update_time.pop(name, None)
            self.source_first_seen_time.pop(name, None)
            self.last_rejection_reason.pop(name, None)
            self.status_event = f"TRAJECTORY_SOURCE_CLEARED source={name} reason=empty_or_rejected"
            self.last_source_event = self.status_event
            self.get_logger().info(self.status_event)
            self.get_logger().info(f"STALE_TRAJECTORY_CLEARED source={name}")
            if self.active_source == name:
                self.active_points = []
                self.active_source = "none"
                self.target_index = 0
                self.hold_reason = "no_collision_free_source"

    def _waypoint_cb(self, msg: PoseStamped):
        self.waypoint = (msg.pose.position.x, msg.pose.position.y, msg.pose.position.z)
        now_sec = self._now_sec()
        self.source_update_time["waypoint"] = now_sec
        self.source_first_seen_time.setdefault("waypoint", now_sec)

    def _select_source(self):
        previous = self.active_source
        self.previous_source = previous
        now_sec = self._now_sec()
        selected: List[Tuple[float, float, float]] = []
        selected_name = "none"
        self.candidate_source = "none"
        self.hold_reason = "no_executable_source"
        if self.trajectory_source != "auto":
            candidate = self.paths.get(self.trajectory_source, [])
            candidate_name = self.trajectory_source if candidate else "none"
        else:
            candidate = []
            candidate_name = "none"
            for name in self.visual_demo_preferred_sources:
                points = self.paths.get(name, [])
                if self._is_executable_path(name, points):
                    candidate = points
                    candidate_name = name
                    break
            if not candidate and self.waypoint and self._is_executable_path("waypoint", [self.waypoint]):
                candidate = [self.waypoint]
                candidate_name = "waypoint"
        self.candidate_source = candidate_name

        active_still_valid = previous != "none" and self._is_executable_path(previous, self.paths.get(previous, []))
        if previous == "waypoint" and self.waypoint:
            active_still_valid = self._is_executable_path("waypoint", [self.waypoint])

        if candidate_name == previous and active_still_valid:
            selected_name = previous
            selected = self.paths.get(previous, [self.waypoint] if self.waypoint else [])
            self.hold_reason = "active_source_retained"
            self._log_active_event(f"ACTIVE_SOURCE_RETAINED source={selected_name} points={len(selected)}")
        elif candidate_name != "none":
            age_time = self.source_update_time.get(candidate_name, now_sec)
            if not self.candidate_age_reset_on_same_source_update:
                age_time = self.source_first_seen_time.get(candidate_name, age_time)
            candidate_age = now_sec - age_time
            old_rank = SOURCE_RANK.get(previous, SOURCE_RANK["none"])
            new_rank = SOURCE_RANK.get(candidate_name, SOURCE_RANK["none"])
            switch_due_to_empty = not active_still_valid
            higher_priority_ready = new_rank < old_rank and candidate_age >= self.source_hold_sec
            lower_priority_ready = switch_due_to_empty and candidate_age >= self.source_hold_sec
            manual_ready = self.trajectory_source != "auto" and candidate_age >= self.source_hold_sec
            if higher_priority_ready or lower_priority_ready or manual_ready or previous == "none" and candidate_age >= self.source_hold_sec:
                selected_name = candidate_name
                selected = candidate
                projected = self._project_target_index(selected, self.target_index if previous == selected_name else 0)
                self.target_index = projected
                self.last_switch_time = now_sec
                event = f"TRAJECTORY_SOURCE_SWITCH from={previous} to={selected_name}"
                self.status_event = event
                self.get_logger().info(event)
                if previous == "none":
                    self._log_active_event(
                        f"ACTIVE_SOURCE_SELECTED source={selected_name} points={len(selected)} "
                        f"length={self._path_length(selected):.3f}"
                    )
                else:
                    self._log_active_event(f"ACTIVE_SOURCE_SWITCH from={previous} to={selected_name}")
                project_event = f"TARGET_INDEX_PROJECTED source={selected_name} index={projected}"
                self.last_source_event = project_event
                self.get_logger().info(project_event)
                self.hold_reason = "active_source_selected"
            elif active_still_valid:
                selected_name = previous
                selected = self.paths.get(previous, [self.waypoint] if self.waypoint else [])
                self.status_event = (
                    f"TRAJECTORY_SOURCE_HOLD active={previous} candidate={candidate_name} "
                    f"candidate_age={candidate_age:.2f} hold_sec={self.source_hold_sec:.2f}"
                )
                self.hold_reason = "source_hold_window"
                self._log_active_event(
                    f"ACTIVE_SOURCE_HOLD reason=source_hold_window active={previous} "
                    f"candidate={candidate_name} candidate_age={candidate_age:.2f}"
                )
            else:
                self.status_event = (
                    f"TRAJECTORY_SOURCE_HOLD active=none candidate={candidate_name} "
                    f"candidate_age={candidate_age:.2f} hold_sec={self.source_hold_sec:.2f}"
                )
                self.hold_reason = "candidate_hold_window"
                self._log_active_event(
                    f"ACTIVE_SOURCE_HOLD reason=candidate_hold_window candidate={candidate_name} "
                    f"candidate_age={candidate_age:.2f}"
                )
        elif active_still_valid:
            selected_name = previous
            selected = self.paths.get(previous, [self.waypoint] if self.waypoint else [])
            self.hold_reason = "active_source_retained_no_candidate"
        else:
            self.status_event = "HOLDING_NO_COLLISION_FREE_PATH NO_ACTIVE_TRAJECTORY_HOLD_POSITION"
            self.hold_reason = "no_collision_free_source"
            if self.online_collision_gate_mode == "enforce":
                self.hold_due_to_collision_gate_count += 1
            self._log_active_event("HOLDING_NO_COLLISION_FREE_PATH")
            self._log_active_event("FOLLOWER_HOLD_POSITION reason=no_collision_free_source")
        if selected_name != previous:
            self.previous_source = previous
        self.active_source = selected_name
        self.active_points = selected
        self.unsafe_visual_execution = self._is_unsafe_visual_execution()
        if self.unsafe_visual_execution:
            self._log_active_event(
                f"VISUAL_DEMO_EXECUTING_UNSAFE_CANDIDATE source={self.active_source} NOT_REAL_FLIGHT_COMMAND"
            )

    def _log_active_event(self, event: str):
        if event == self._last_active_log_key:
            return
        self._last_active_log_key = event
        self.get_logger().info(event)

    def _is_executable_path(self, name: str, points: List[Tuple[float, float, float]]) -> bool:
        if name == "waypoint":
            if not points:
                return False
            segment = [tuple(self.position), points[0]]
            safety = self._check_path_execution_safety(name, segment)
            if safety is not None:
                reason, hit = safety
                self.last_rejection_reason[name] = reason
                self._log_rejected_active_source(name, reason, hit)
                return False
            return True
        if len(points) < self.min_executable_points:
            return False
        if self._path_length(points) < self.min_executable_length:
            return False
        safety = self._check_path_execution_safety(name, points)
        if safety is not None:
            reason, hit = safety
            self.last_rejection_reason[name] = reason
            self._log_rejected_active_source(name, reason, hit)
            return False
        return True

    def _check_path_execution_safety(
        self, name: str, points: List[Tuple[float, float, float]]
    ) -> Optional[Tuple[str, object]]:
        if not self.enable_collision_gate or not self.world_obstacles or path_collision is None:
            return None
        hard_hit = path_collision(self.world_obstacles, points, 0.0, self.collision_resolution)
        if hard_hit.collides:
            if self.online_collision_gate_mode == "warn":
                self._log_collision_warning(name, "collision", hard_hit)
                return None
            return ("collision", hard_hit)
        clearance_hit = path_collision(
            self.world_obstacles, points, self.collision_clearance, self.collision_resolution
        )
        if clearance_hit.collides:
            if self.online_collision_gate_mode == "warn":
                self._log_collision_warning(name, "low_clearance", clearance_hit)
                return None
            return ("low_clearance", clearance_hit)
        return None

    def _log_collision_warning(self, name: str, reason: str, hit):
        point = getattr(hit, "point", (0.0, 0.0, 0.0))
        obstacle = getattr(hit, "obstacle", "unknown")
        event = (
            f"FOLLOWER_COLLISION_WARNING reason={reason} source={name} "
            f"obstacle={obstacle} collision_point=({point[0]:.3f},{point[1]:.3f},{point[2]:.3f}) "
            f"online_collision_gate_mode=warn executable_not_blocked=true"
        )
        if event == self.last_warning_log_key:
            return
        self.last_warning_log_key = event
        self.collision_warning_count += 1
        self.status_event = event
        self.last_source_event = event
        self.get_logger().info(event)

    def _log_rejected_active_source(self, name: str, reason: str, hit):
        point = getattr(hit, "point", (0.0, 0.0, 0.0))
        obstacle = getattr(hit, "obstacle", "unknown")
        event = (
            f"FOLLOWER_REJECTED_ACTIVE_SOURCE reason={reason} source={name} "
            f"obstacle={obstacle} collision_point=({point[0]:.3f},{point[1]:.3f},{point[2]:.3f})"
        )
        if event == self.last_rejection_log_key:
            return
        self.last_rejection_log_key = event
        self.collision_enforced_count += 1
        self.status_event = event
        self.last_source_event = event
        self.get_logger().info(event)

    def _path_length(self, points: List[Tuple[float, float, float]]) -> float:
        if len(points) < 2:
            return 0.0
        return sum(math.dist(points[i - 1], points[i]) for i in range(1, len(points)))

    def _is_unsafe_visual_execution(self) -> bool:
        if self.active_source == "none":
            return False
        if not self.visual_demo_allow_unsafe_candidate or not self.execute_unsafe_with_warning:
            return False
        return self.active_source in {
            "plan_manager",
            "bspline",
            "safety_gate",
            "local_trajectory",
            "path_searching",
            "global_path",
        }

    def _now_sec(self) -> float:
        return self.get_clock().now().nanoseconds * 1e-9

    def _project_target_index(self, points: List[Tuple[float, float, float]], previous_index: int) -> int:
        if not points:
            return 0
        nearest_index = min(
            range(len(points)),
            key=lambda i: (points[i][0] - self.position[0]) ** 2
            + (points[i][1] - self.position[1]) ** 2
            + (points[i][2] - self.position[2]) ** 2,
        )
        if previous_index > 0 and nearest_index + 1 < previous_index and previous_index < len(points):
            return previous_index
        return nearest_index

    def _step(self):
        if not rclpy.ok():
            return
        self._select_source()
        dt = 1.0 / self.update_rate
        self._accumulate_distance()
        if self.odom_distance > self.max_demo_distance:
            if not self.distance_anomaly_logged:
                event = f"MOTION_DISTANCE_ANOMALY odom_distance={self.odom_distance:.3f} limit={self.max_demo_distance:.3f}"
                self.status_event = event
                self.get_logger().info(event)
                self.distance_anomaly_logged = True
            self.active_points = []
            self.active_source = "none"
            self.velocity = self._limit_accel(self.velocity, [0.0, 0.0, 0.0], dt)
            self.position[0] += self.velocity[0] * dt
            self.position[1] += self.velocity[1] * dt
            self.position[2] += self.velocity[2] * dt
            self._publish_step(tuple(self.position))
            return

        target_pose: Optional[Tuple[float, float, float]] = None
        if self.active_points:
            while self.target_index < len(self.active_points):
                target = self.active_points[self.target_index]
                dx = target[0] - self.position[0]
                dy = target[1] - self.position[1]
                dz = target[2] - self.position[2]
                distance = math.sqrt(dx * dx + dy * dy + dz * dz)
                if distance > 0.06:
                    target_pose = target
                    self._integrate_toward_target(target, distance, dt)
                    break
                self.target_index += 1
            if target_pose is None and self.active_points:
                if self.loop_trajectory:
                    self.target_index = 0
                    target = self.active_points[0]
                    target_pose = target
                    self.status_event = "LOOP_TRAJECTORY_ENABLED"
                    self.get_logger().info("LOOP_TRAJECTORY_ENABLED")
                    self._integrate_toward_target(target, math.dist(tuple(self.position), target), dt)
                else:
                    if self.hold_at_goal and not self.hold_at_goal_active:
                        self.get_logger().info(
                            f"HOLD_AT_TRAJECTORY_END source={self.active_source} target_index={self.target_index} "
                            f"points={len(self.active_points)}"
                        )
                        self.get_logger().info(
                            f"TARGET_REACHED_HOLD source={self.active_source} target_index={self.target_index}"
                        )
                        self.get_logger().info("LOOP_TRAJECTORY_DISABLED")
                    self.status_event = "TARGET_REACHED_HOLD"
                    self.hold_at_goal_active = True
                self.velocity = self._limit_accel(self.velocity, [0.0, 0.0, 0.0], dt)
                self.position[0] += self.velocity[0] * dt
                self.position[1] += self.velocity[1] * dt
                self.position[2] += self.velocity[2] * dt
        else:
            now_sec = self._now_sec()
            if now_sec - self.last_hold_log_time > 1.0:
                self.status_event = (
                    "FOLLOWER_HOLD_POSITION reason=no_collision_free_source active_source=none "
                    "NO_ACTIVE_TRAJECTORY_HOLD_POSITION"
                )
                self.get_logger().info(self.status_event)
                self.last_hold_log_time = now_sec
            self.velocity = self._limit_accel(self.velocity, [0.0, 0.0, 0.0], dt)
            self.position[0] += self.velocity[0] * dt
            self.position[1] += self.velocity[1] * dt
            self.position[2] += self.velocity[2] * dt

        if target_pose is None:
            target_pose = tuple(self.position)
        self._publish_step(target_pose)

    def _publish_step(self, target_pose: Tuple[float, float, float]):
        self._accumulate_distance()

        stamp = self.get_clock().now().to_msg()
        yaw = self._estimate_yaw()
        qz = math.sin(yaw * 0.5)
        qw = math.cos(yaw * 0.5)
        pose = PoseStamped()
        pose.header.frame_id = self.frame_id
        pose.header.stamp = stamp
        pose.pose.position.x, pose.pose.position.y, pose.pose.position.z = self.position
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw

        odom = Odometry()
        odom.header = pose.header
        odom.child_frame_id = self.base_frame_id
        odom.pose.pose = pose.pose
        odom.twist.twist.linear.x = self.velocity[0]
        odom.twist.twist.linear.y = self.velocity[1]
        odom.twist.twist.linear.z = self.velocity[2]
        try:
            self.odom_pub.publish(odom)
            self.state_pub.publish(odom)
            self.pose_pub.publish(pose)
            self._publish_tf(stamp, qz, qw)
            self._maybe_update_gazebo_pose(yaw)
            self._publish_status(target_pose)
            if self._marker_publish_due():
                self.marker_pub.publish(self._make_uav_marker(stamp, qz, qw))
                self._publish_trail(pose)
                self.status_text_pub.publish(self._make_status_text_marker(stamp, target_pose))
                self.warning_text_pub.publish(self._make_warning_text_marker(stamp))
                self.legend_pub.publish(self._make_legend_marker(stamp))
                self.uav_label_pub.publish(self._make_text_label(stamp, "fuel_visual_uav_label", 0, "UAV", self.position, (1.0, 0.2, 0.05), 0.24, 0.7))
                self.goal_marker_pub.publish(self._make_goal_marker(stamp, target_pose))
                self.goal_label_pub.publish(self._make_text_label(stamp, "fuel_visual_goal_label", 0, "GOAL", target_pose, (1.0, 0.0, 1.0), 0.26, 0.9))
                if self.active_points:
                    label_pose = self.active_points[min(self.target_index, len(self.active_points) - 1)]
                else:
                    label_pose = target_pose
                self.path_label_pub.publish(self._make_text_label(stamp, "fuel_visual_path_label", 0, "FUTURE TRAJ", label_pose, (0.2, 0.8, 1.0), 0.24, 0.8))
        except RCLError:
            return

    def _marker_publish_due(self) -> bool:
        now = self.get_clock().now()
        if (now - self.last_marker_publish).nanoseconds < int(1e9 / self.marker_rate):
            return False
        self.last_marker_publish = now
        return True

    def _accumulate_distance(self):
        delta = math.dist(self.last_position_for_distance, self.position)
        if delta > 0.0:
            self.odom_distance += delta
        self.last_position_for_distance = list(self.position)

    def _integrate_toward_target(self, target: Tuple[float, float, float], distance: float, dt: float):
        raw_z = target[2]
        self.filtered_target_z = self.filtered_target_z * (1.0 - self.z_lowpass_alpha) + raw_z * self.z_lowpass_alpha
        filtered_target = (target[0], target[1], self.filtered_target_z)
        dx = filtered_target[0] - self.position[0]
        dy = filtered_target[1] - self.position[1]
        dz = filtered_target[2] - self.position[2]
        filtered_distance = max(1e-6, math.sqrt(dx * dx + dy * dy + dz * dz))
        desired = [
            dx / filtered_distance * self.max_speed,
            dy / filtered_distance * self.max_speed,
            max(-self.max_vertical_speed, min(self.max_vertical_speed, dz / max(dt, 1e-6))),
        ]
        horizontal_speed = math.hypot(desired[0], desired[1])
        if horizontal_speed > self.max_speed:
            scale = self.max_speed / horizontal_speed
            desired[0] *= scale
            desired[1] *= scale
        if abs(dz) > self.max_vertical_speed * dt * 1.5:
            event = (
                f"VERTICAL_JUMP_GUARD_ACTIVE target_z={raw_z:.3f} filtered_z={self.filtered_target_z:.3f} "
                f"current_z={self.position[2]:.3f} dz={dz:.3f}"
            )
            if self.status_event != event:
                self.status_event = event
                self.get_logger().info(event)
        self.velocity = self._limit_accel(self.velocity, desired, dt)
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.position[2] += self.velocity[2] * dt

    def _limit_accel(self, current: List[float], desired: List[float], dt: float) -> List[float]:
        dt = max(dt, 1e-6)
        next_velocity = list(current)
        dx = desired[0] - current[0]
        dy = desired[1] - current[1]
        horizontal_delta = math.hypot(dx, dy)
        horizontal_limit = self.max_horizontal_accel * dt
        if horizontal_delta > horizontal_limit > 0.0:
            scale = horizontal_limit / horizontal_delta
            dx *= scale
            dy *= scale
        next_velocity[0] = current[0] + dx
        next_velocity[1] = current[1] + dy
        delta_z = desired[2] - current[2]
        limit_z = self.max_vertical_accel * dt
        next_velocity[2] = current[2] + max(-limit_z, min(limit_z, delta_z))
        next_velocity[2] = max(-self.max_vertical_speed, min(self.max_vertical_speed, next_velocity[2]))
        self.last_accel = [
            (next_velocity[0] - current[0]) / dt,
            (next_velocity[1] - current[1]) / dt,
            (next_velocity[2] - current[2]) / dt,
        ]
        return next_velocity

    def _estimate_yaw(self) -> float:
        if self.active_points and self.target_index < len(self.active_points):
            target = self.active_points[self.target_index]
            return math.atan2(target[1] - self.position[1], target[0] - self.position[0])
        return 0.0

    def _make_uav_marker(self, stamp, qz: float, qw: float) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = "fuel_visual_uav"
        marker.id = 0
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        marker.pose.position.x, marker.pose.position.y, marker.pose.position.z = self.position
        marker.pose.orientation.z = qz
        marker.pose.orientation.w = qw
        marker.scale.x = 0.9
        marker.scale.y = 0.22
        marker.scale.z = 0.34
        marker.color.a = 0.95
        marker.color.r = 1.0
        marker.color.g = 0.18
        marker.color.b = 0.02
        return marker

    def _make_goal_marker(self, stamp, target_pose: Tuple[float, float, float]) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = "fuel_visual_current_goal"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x, marker.pose.position.y, marker.pose.position.z = target_pose
        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.9
        marker.scale.y = 0.9
        marker.scale.z = 0.9
        marker.color.a = 0.95
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        return marker

    def _make_text_label(
        self,
        stamp,
        namespace: str,
        marker_id: int,
        text: str,
        position: Tuple[float, float, float],
        color: Tuple[float, float, float],
        size: float,
        z_offset: float,
    ) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = namespace
        marker.id = marker_id
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.pose.position.x = float(position[0])
        marker.pose.position.y = float(position[1])
        marker.pose.position.z = float(position[2]) + z_offset
        marker.pose.orientation.w = 1.0
        marker.scale.z = size
        marker.color.a = 1.0
        marker.color.r, marker.color.g, marker.color.b = color
        marker.text = text
        return marker

    def _publish_trail(self, pose: PoseStamped):
        self.trail.append(pose)
        if len(self.trail) > self.trail_max_points:
            self.trail = self.trail[-self.trail_max_points :]
        trail = Path()
        trail.header = pose.header
        trail.poses = list(self.trail)
        self.trail_pub.publish(trail)

    def _publish_tf(self, stamp, qz: float, qw: float):
        transform = TransformStamped()
        transform.header.frame_id = self.frame_id
        transform.header.stamp = stamp
        transform.child_frame_id = self.base_frame_id
        transform.transform.translation.x, transform.transform.translation.y, transform.transform.translation.z = self.position
        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(transform)

    def _maybe_update_gazebo_pose(self, yaw: float):
        if not self.enable_gazebo_pose_update:
            self.gazebo_pose_update_reason = "disabled_by_parameter"
            return
        now = self.get_clock().now()
        if (now - self.last_gazebo_update).nanoseconds < int(1e9 / self.gazebo_update_rate):
            return
        self.last_gazebo_update = now
        if shutil.which("gz") is None:
            self.gazebo_pose_update_reason = "gz_command_not_found"
            self.gazebo_pose_before = "GAZEBO_POSE_READBACK_UNAVAILABLE"
            self.gazebo_pose_after = "GAZEBO_POSE_READBACK_UNAVAILABLE"
            self.gazebo_readback_z = None
            return
        readback = self._read_gazebo_pose()
        self.gazebo_pose_before = readback[0]
        self.gazebo_readback_z = readback[3]
        self.gazebo_pose_reset = False
        self.gazebo_pose_reset_reason = "none"
        if self.gazebo_readback_z is not None:
            self.gazebo_z_mismatch = self.gazebo_readback_z - self.position[2]
            if abs(self.gazebo_z_mismatch) > 0.4:
                event = (
                    f"GAZEBO_RVIZ_Z_MISMATCH follower_z={self.position[2]:.3f} "
                    f"gazebo_readback_z={self.gazebo_readback_z:.3f} "
                    f"z_mismatch={self.gazebo_z_mismatch:.3f}"
                )
                if event != self.last_gazebo_mismatch_log:
                    self.get_logger().info(event)
                    self.last_gazebo_mismatch_log = event
                self.gazebo_pose_reset = True
                self.gazebo_pose_reset_reason = "GAZEBO_POSE_SMOOTH_RESET"
                self.get_logger().info(
                    f"GAZEBO_POSE_SMOOTH_RESET model={self.gazebo_model_name} "
                    f"from_z={self.gazebo_readback_z:.3f} toward_z={self.position[2]:.3f}"
                )
        else:
            self.gazebo_z_mismatch = 0.0
        cmd = [
            "gz",
            "model",
            "-m",
            self.gazebo_model_name,
            "-x",
            f"{self.position[0]:.3f}",
            "-y",
            f"{self.position[1]:.3f}",
            "-z",
            f"{self.position[2]:.3f}",
            "-Y",
            f"{yaw:.3f}",
        ]
        try:
            proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, timeout=0.4)
            if proc.returncode == 0:
                self.gazebo_pose_update_ok = True
                self.gazebo_pose_update_reason = "gz_model_pose_updated"
                self.gazebo_pose_after = f"({self.position[0]:.3f},{self.position[1]:.3f},{self.position[2]:.3f},{yaw:.3f})"
                self.get_logger().info(
                    f"GAZEBO_SET_POSE_SMOOTHED model={self.gazebo_model_name} "
                    f"before={self.gazebo_pose_before} after={self.gazebo_pose_after} "
                    f"current_z={self.position[2]:.3f} gazebo_readback_z="
                    f"{self.gazebo_readback_z if self.gazebo_readback_z is not None else 'UNKNOWN'} "
                    f"yaw={yaw:.3f}"
                )
            else:
                self.gazebo_pose_update_ok = False
                self.gazebo_pose_update_reason = "gz_model_failed:" + proc.stderr.strip()[:120]
                self.gazebo_pose_after = "GAZEBO_POSE_READBACK_UNAVAILABLE"
        except Exception as exc:  # pragma: no cover
            self.gazebo_pose_update_ok = False
            self.gazebo_pose_update_reason = f"gz_model_exception:{exc}"
            self.gazebo_pose_after = "GAZEBO_POSE_READBACK_UNAVAILABLE"

    def _read_gazebo_pose(self) -> Tuple[str, Optional[float], Optional[float], Optional[float]]:
        try:
            proc = subprocess.run(
                ["gz", "model", "-m", self.gazebo_model_name, "-p"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=0.35,
            )
        except Exception as exc:  # pragma: no cover
            return (f"GAZEBO_POSE_READBACK_UNAVAILABLE exception={exc}", None, None, None)
        text = (proc.stdout + " " + proc.stderr).strip()
        if proc.returncode != 0 or not text:
            return ("GAZEBO_POSE_READBACK_UNAVAILABLE " + text[:120], None, None, None)
        import re

        nums = [float(x) for x in re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", text)]
        if len(nums) < 3:
            return ("GAZEBO_POSE_READBACK_PARTIAL " + text[:120], None, None, None)
        return (text, nums[0], nums[1], nums[2])

    def _publish_status(self, target_pose: Tuple[float, float, float]):
        msg = String()
        source_age = 0.0
        if self.active_source in self.source_update_time:
            source_age = max(0.0, self._now_sec() - self.source_update_time[self.active_source])
        z_error = target_pose[2] - self.position[2]
        acc_norm = math.sqrt(self.last_accel[0] ** 2 + self.last_accel[1] ** 2 + self.last_accel[2] ** 2)
        gazebo_readback_z = "UNKNOWN" if self.gazebo_readback_z is None else f"{self.gazebo_readback_z:.3f}"
        active_length = self._path_length(self.active_points)
        moving = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2 + self.velocity[2] ** 2) > 0.03
        unsafe_event = ""
        if self.unsafe_visual_execution:
            unsafe_event = (
                f"VISUAL_DEMO_EXECUTING_UNSAFE_CANDIDATE source={self.active_source} "
                f"NOT_REAL_FLIGHT_COMMAND "
            )
        msg.data = (
            f"event={self.status_event} {unsafe_event}last_source_event={self.last_source_event} "
            f"active_source={self.active_source} selected_source={self.active_source} previous_source={self.previous_source} "
            f"candidate_source={self.candidate_source} source={self.active_source} points={len(self.active_points)} "
            f"active_points={len(self.active_points)} active_length={active_length:.3f} "
            f"hold_reason={self.hold_reason} moving={str(moving).lower()} "
            f"visual_demo_allow_unsafe_candidate={str(self.visual_demo_allow_unsafe_candidate).lower()} "
            f"unsafe_visual_execution={str(self.unsafe_visual_execution).lower()} "
            f"blocked_real_flight_topics=true collision_gate={str(self.enable_collision_gate).lower()} "
            f"online_collision_gate_mode={self.online_collision_gate_mode} "
            f"collision_warning_count={self.collision_warning_count} "
            f"collision_enforced_count={self.collision_enforced_count} "
            f"hold_due_to_collision_gate_count={self.hold_due_to_collision_gate_count} "
            f"target_index={self.target_index} "
            f"current_pose=({self.position[0]:.3f},{self.position[1]:.3f},{self.position[2]:.3f}) "
            f"target_pose=({target_pose[0]:.3f},{target_pose[1]:.3f},{target_pose[2]:.3f}) "
            f"current_z={self.position[2]:.3f} target_z={target_pose[2]:.3f} "
            f"gazebo_readback_z={gazebo_readback_z} z_mismatch={self.gazebo_z_mismatch:.3f} "
            f"z_error={z_error:.3f} vx={self.velocity[0]:.3f} vy={self.velocity[1]:.3f} "
            f"vz={self.velocity[2]:.3f} az={self.last_accel[2]:.3f} acc_norm={acc_norm:.3f} "
            f"source_age_sec={source_age:.3f} source_age={source_age:.3f} "
            f"odom_distance={self.odom_distance:.3f} max_demo_distance={self.max_demo_distance:.3f} "
            f"trail_points={len(self.trail)} "
            f"pose_reset={str(self.gazebo_pose_reset).lower()} pose_reset_reason={self.gazebo_pose_reset_reason} "
            f"odom=true tf=true marker=true gazebo_pose_update={str(self.gazebo_pose_update_ok).lower()} "
            f"gazebo_set_pose_result={self.gazebo_pose_update_reason} gazebo_reason={self.gazebo_pose_update_reason} "
            f"gazebo_pose_before={self.gazebo_pose_before} gazebo_pose_after={self.gazebo_pose_after} "
            f"gazebo_pose_bridge=GAZEBO_POSE_BRIDGE_PARTIAL_RVIZ_TRAIL_AVAILABLE "
            f"real_flight_command=false"
        )
        self.status_pub.publish(msg)

    def _make_status_text_marker(self, stamp, target_pose: Tuple[float, float, float]) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = "fuel_visual_truth_status"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.pose.position.x = -14.0
        marker.pose.position.y = -14.0
        marker.pose.position.z = 3.2
        marker.pose.orientation.w = 1.0
        marker.scale.z = 0.22
        marker.color.a = 1.0
        marker.color.r = 0.20
        marker.color.g = 0.95
        marker.color.b = 1.0
        moving = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2 + self.velocity[2] ** 2) > 0.03
        safe = not self.unsafe_visual_execution
        fallback = self.active_source == "none"
        motion_line = (
            f"MOVING - ACTIVE SOURCE: {self.active_source}"
            if self.active_source != "none"
            else "HOLDING - NO ACTIVE SOURCE"
        )
        marker.text = (
            "FUEL_ROS2 WRAPPER DEMO\n"
            f"{motion_line}\n"
            f"active: {self.active_source} | moving: {str(moving).lower()}\n"
            f"path: {len(self.active_points)} pts | fallback: {str(fallback).lower()}\n"
            f"safe: {str(safe).lower()} | visual only\n"
            f"odom: {self.odom_distance:.1f}m | z: {self.position[2]:.2f}"
        )
        return marker

    def _make_warning_text_marker(self, stamp) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = "fuel_visual_warning_status"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.pose.position.x = -14.0
        marker.pose.position.y = -14.0
        marker.pose.position.z = 2.55
        marker.pose.orientation.w = 1.0
        marker.scale.z = 0.22
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.18
        marker.color.b = 0.05
        marker.text = (
            "WRAPPER VISUAL DEMO ONLY\n"
            "UNSAFE CANDIDATE / NOT REAL FLIGHT\n"
            "NOT UPSTREAM FUEL OFFICIAL"
        )
        return marker

    def _make_legend_marker(self, stamp) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = "fuel_visual_legend"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.pose.position.x = -9.5
        marker.pose.position.y = -10.5
        marker.pose.position.z = 3.6
        marker.pose.orientation.w = 1.0
        marker.scale.z = 0.26
        marker.color.a = 1.0
        marker.color.r = 0.95
        marker.color.g = 0.95
        marker.color.b = 0.95
        marker.text = (
            "RED ARROW = UAV\n"
            "YELLOW = HISTORY\n"
            "GREEN LINE = GLOBAL PATH\n"
            "CYAN/BLUE = FUTURE TRAJ\n"
            "MAGENTA = CURRENT GOAL"
        )
        return marker


def main():
    rclpy.init()
    try:
        node = GazeboUavTrajectoryFollower()
    except Exception as exc:
        print(f"GAZEBO_UAV_TRAJECTORY_FOLLOWER_STARTUP_FAILED reason={type(exc).__name__}: {exc}", flush=True)
        if rclpy.ok():
            rclpy.shutdown()
        raise
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException, RCLError):
        pass
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()
