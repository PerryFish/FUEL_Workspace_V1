#!/usr/bin/env python3
import math
from typing import List, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path as RosPath
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

try:
    from sensor_msgs_py import point_cloud2
except ImportError:  # pragma: no cover - runtime environment guard
    point_cloud2 = None


Point = Tuple[float, float, float]


class ExplorationManagerLite(Node):
    def __init__(self):
        super().__init__("exploration_manager_lite")
        self.minimum_goal_hold_sec = float(self.declare_parameter("minimum_goal_hold_sec", 15.0).value)
        self.min_goal_hold_sec = float(self.declare_parameter("min_goal_hold_sec", 18.0).value)
        self.min_progress_window_sec = float(self.declare_parameter("min_progress_window_sec", 20.0).value)
        self.min_coverage_gain_for_continue = float(self.declare_parameter("min_coverage_gain_for_continue", 0.01).value)
        self.min_goal_separation = float(self.declare_parameter("min_goal_separation", 1.0).value)
        self.min_switch_score_improvement = float(self.declare_parameter("min_switch_score_improvement", 1.5).value)
        self.oscillation_cooldown_sec = float(self.declare_parameter("oscillation_cooldown_sec", 20.0).value)
        self.goal_reached_radius = float(self.declare_parameter("goal_reached_radius", 0.8).value)
        self.goal_timeout_sec = float(self.declare_parameter("goal_timeout_sec", 25.0).value)
        self.min_goal_distance = float(self.declare_parameter("min_goal_distance", 1.0).value)
        self.min_new_goal_separation = float(self.declare_parameter("min_new_goal_separation", 1.0).value)
        self.min_switch_improvement_ratio = float(self.declare_parameter("min_switch_improvement_ratio", 1.35).value)
        self.spatial_hysteresis_radius = float(self.declare_parameter("spatial_hysteresis_radius", 2.0).value)
        self.max_goal_switch_rate = float(self.declare_parameter("max_goal_switch_rate", 45.0 / 300.0).value)
        self.min_region_hold_sec = float(self.declare_parameter("min_region_hold_sec", 45.0).value)
        self.region_stall_timeout_sec = float(self.declare_parameter("region_stall_timeout_sec", 60.0).value)
        self.region_switch_score_ratio = float(self.declare_parameter("region_switch_score_ratio", 1.8).value)
        self.goal_jitter_radius = float(self.declare_parameter("goal_jitter_radius", 2.0).value)
        self.max_goal_jump_without_region_switch = float(self.declare_parameter("max_goal_jump_without_region_switch", 5.0).value)
        self.goal_smoothing_alpha = float(self.declare_parameter("goal_smoothing_alpha", 0.3).value)
        self.recent_goal_memory_size = int(self.declare_parameter("recent_goal_memory_size", 10).value)
        self.recent_goal_quantization = float(self.declare_parameter("recent_goal_quantization", 0.5).value)
        self.recent_goal_ttl_sec = float(self.declare_parameter("recent_goal_ttl_sec", 120.0).value)
        self.escape_min_goal_separation = float(self.declare_parameter("escape_min_goal_separation", 2.0).value)
        self.escape_fallback_goal_separation = float(self.declare_parameter("escape_fallback_goal_separation", 1.2).value)
        self.too_close_retire_sec = float(self.declare_parameter("too_close_retire_sec", 3.0).value)
        self.progress_stall_window_sec = float(self.declare_parameter("progress_stall_window_sec", 30.0).value)
        self.progress_stall_min_motion = float(self.declare_parameter("progress_stall_min_motion", 0.5).value)
        self.progress_stall_min_coverage_gain = float(self.declare_parameter("progress_stall_min_coverage_gain", 0.01).value)
        self.no_progress_window_sec = float(self.declare_parameter("no_progress_window_sec", 20.0).value)
        self.no_progress_min_motion = float(self.declare_parameter("no_progress_min_motion", 0.3).value)
        self.escape_recent_penalty = float(self.declare_parameter("escape_recent_penalty", 0.5).value)
        self.escape_distance_bonus = float(self.declare_parameter("escape_distance_bonus", 0.3).value)
        self.max_escape_candidates = int(self.declare_parameter("max_escape_candidates", 250).value)
        self.escape_cooldown_sec = float(self.declare_parameter("escape_cooldown_sec", 15.0).value)
        self.enable_frontier_point_escape = bool(self.declare_parameter("enable_frontier_point_escape", True).value)
        self.goal_to_path_timeout_sec = float(self.declare_parameter("goal_to_path_timeout_sec", 15.0).value)
        self.goal_without_path_retire_sec = float(self.declare_parameter("goal_without_path_retire_sec", 15.0).value)
        self.no_path_blacklist_ttl_sec = float(self.declare_parameter("no_path_blacklist_ttl_sec", 90.0).value)
        self.no_path_region_radius = float(self.declare_parameter("no_path_region_radius", 2.0).value)
        self.active_goal: Optional[PoseStamped] = None
        self.pending_best: Optional[PoseStamped] = None
        self.pending_best_score = 0.0
        self.active_goal_score = 0.0
        self.goal_start_sec = 0.0
        self.first_switch_sec = 0.0
        self.goal_switch_count = 0
        self.switch_blocked_by_hysteresis_count = 0
        self.switch_blocked_by_score_count = 0
        self.switch_blocked_by_rate_count = 0
        self.odom: Optional[Odometry] = None
        self.reason = "waiting_for_best_viewpoint"
        self.last_switch_reason = "none"
        self.switch_reason = "none"
        self.goal_hold_active = False
        self.goal_start_distance: Optional[float] = None
        self.last_goal_distance: Optional[float] = None
        self.last_goal_distance_sample_sec = 0.0
        self.last_switch_sec = -999.0
        self.goal_progress_score = 0.0
        self.coverage_gain_since_goal = 0.0
        self.goal_switch_blocked_by_progress_count = 0
        self.goal_switch_blocked_by_similarity_count = 0
        self.goal_switch_blocked_by_low_gain_count = 0
        self.oscillation_cooldown_active = False
        self.active_region_id = "NONE"
        self.pending_region_id = "NONE"
        self.active_region_score = 0.0
        self.pending_region_score = 0.0
        self.active_region_start_sec = 0.0
        self.region_hold_active = False
        self.region_stall_detected = False
        self.region_switch_reason = "none"
        self.goal_jitter_suppressed_count = 0
        self.coverage_stall_detected = False
        self.coverage_stall_duration = 0.0
        self.recovery_region_id = "NONE"
        self.recovery_goal = "NONE"
        self.recovery_count = 0
        self.escape_goal_count = 0
        self.escape_fallback_count = 0
        self.escape_skip_recent_count = 0
        self.escape_candidate_count = 0
        self.goal_retire_event_count = 0
        self.goal_retire_reasons = {}
        self.true_repeated_goal_count = 0
        self.goal_republish_count = 0
        self.last_goal_event = "NONE"
        self.last_goal_event_reason = "NONE"
        self.last_goal_event_goal = "NONE"
        self.active_goal_key: Optional[Tuple[int, int, int]] = None
        self.retired_goal_keys: List[Tuple[Tuple[int, int, int], float]] = []
        self.recent_goals: List[Tuple[Tuple[int, int, int], float]] = []
        self.frontier_viewpoints: List[Point] = []
        self.frontier_viewpoint_count = 0
        self.frontier_candidate_count = 0
        self.explored_points = 0
        self.global_cloud_points = 0
        self.odom_history: List[Tuple[float, Point]] = []
        self.coverage_history: List[Tuple[float, float]] = []
        self.too_close_start_sec: Optional[float] = None
        self.no_progress_detected = False
        self.escape_active = False
        self.escape_reason = "none"
        self.last_escape_sec = -999.0
        self.path_feasible = True
        self.path_infeasible_start_sec: Optional[float] = None
        self.path_infeasible_count = 0
        self.path_infeasible_retire_count = 0
        self.path_status_reason = "none"
        self.path_status_goal_key = "UNKNOWN"
        self.path_endpoint_to_goal_distance = -1.0
        self.no_path_watchdog_enabled = True
        self.no_path_timeout_count = 0
        self.no_path_blacklist_count = 0
        self.goal_reselect_due_to_no_path_count = 0
        self.no_path_timeout_reported = False
        self.no_path_waiting_reported_sec = -999.0
        self.last_active_path_update_sec = -999.0
        self.last_travel_traj_update_sec = -999.0
        self.active_path_points = 0
        self.travel_traj_points = 0
        self.no_path_blacklisted_regions = {}
        self.goal_jump_reject_count = 0
        self.goal_smoothing_applied_count = 0
        self.goal_jump_count = 0
        self.goal_jitter_score = 0.0
        self._last_progress_sec = self._now()

        self.create_subscription(PoseStamped, "/fuel/p11_lite/best_viewpoint", self._best_cb, 10)
        self.create_subscription(String, "/fuel/p11_lite/frontier_status", self._frontier_status_cb, 10)
        self.create_subscription(String, "/fuel/p11_lite/goal_to_path_status", self._goal_to_path_status_cb, 10)
        self.create_subscription(RosPath, "/fuel/p10_lite/active_path", lambda msg: self._path_cb("active_path", msg), 10)
        self.create_subscription(RosPath, "/planning/travel_traj", lambda msg: self._path_cb("travel_traj", msg), 10)
        self.create_subscription(Odometry, "/odom", self._odom_cb, 20)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/frontier_viewpoints", self._frontier_viewpoints_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/frontier_candidates_raw", self._frontier_candidates_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/explored_grid", self._explored_grid_cb, 10)
        self.create_subscription(PointCloud2, "/map_generator/global_cloud", self._global_cloud_cb, 10)
        self.goal_pub = self.create_publisher(PoseStamped, "/fuel/p11_lite/exploration_goal", 10)
        self.status_pub = self.create_publisher(String, "/fuel/p11_lite/exploration_manager_status", 10)
        self.goal_lifecycle_pub = self.create_publisher(String, "/fuel/p11_lite/goal_lifecycle_status", 10)
        self.timer = self.create_timer(0.5, self._tick)
        self.get_logger().info("P11_LITE_EXPLORATION_MANAGER_READY REAL_FLIGHT_COMMAND=false")

    def _now(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    def _best_cb(self, msg: PoseStamped) -> None:
        self.pending_best = msg
        self.pending_best_score = self._extract_score(msg)

    @staticmethod
    def _field(data: str, key: str, default: str = "UNKNOWN") -> str:
        token = f"{key}="
        for part in data.split():
            if part.startswith(token):
                return part[len(token):]
        return default

    def _frontier_status_cb(self, msg: String) -> None:
        self.pending_region_id = self._field(msg.data, "active_region_id", self.pending_region_id)
        try:
            self.pending_region_score = float(self._field(msg.data, "selected_region_score", str(self.pending_region_score)))
        except ValueError:
            pass

    def _goal_to_path_status_cb(self, msg: String) -> None:
        now = self._now()
        path_feasible_text = self._field(msg.data, "path_feasible", "true")
        path_valid_text = self._field(msg.data, "path_valid", "true")
        request_reselect_text = self._field(msg.data, "request_reselect", "false")
        self.path_status_reason = self._field(msg.data, "reject_reason", self._field(msg.data, "reason", "none"))
        self.path_status_goal_key = self._field(msg.data, "goal_key", "UNKNOWN")
        try:
            self.path_endpoint_to_goal_distance = float(self._field(msg.data, "endpoint_to_goal_distance", str(self.path_endpoint_to_goal_distance)))
        except ValueError:
            pass
        infeasible = (
            path_feasible_text == "false"
            or path_valid_text == "false"
            or request_reselect_text == "true"
            or self.path_endpoint_to_goal_distance > 2.5
        )
        self.path_feasible = not infeasible
        if infeasible:
            if self.path_infeasible_start_sec is None:
                self.path_infeasible_start_sec = now
            self.path_infeasible_count += 1
        else:
            self.path_infeasible_start_sec = None

    def _path_cb(self, source: str, msg: RosPath) -> None:
        points = len(msg.poses)
        now = self._now()
        if source == "active_path":
            self.active_path_points = points
            if points > 0:
                self.last_active_path_update_sec = now
        elif source == "travel_traj":
            self.travel_traj_points = points
            if points > 0:
                self.last_travel_traj_update_sec = now

    @staticmethod
    def _extract_score(msg: PoseStamped) -> float:
        frame_id = msg.header.frame_id or ""
        marker = "score="
        if marker not in frame_id:
            return 0.0
        try:
            return float(frame_id.split(marker, 1)[1].split()[0])
        except (ValueError, IndexError):
            return 0.0

    def _odom_cb(self, msg: Odometry) -> None:
        self.odom = msg
        now = self._now()
        p = msg.pose.pose.position
        self.odom_history.append((now, (float(p.x), float(p.y), float(p.z))))
        self._trim_histories(now)

    def _frontier_viewpoints_cb(self, msg: PointCloud2) -> None:
        self.frontier_viewpoint_count = int(msg.width * msg.height)
        if point_cloud2 is None:
            return
        points: List[Point] = []
        try:
            for idx, p in enumerate(point_cloud2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)):
                if idx >= self.max_escape_candidates:
                    break
                x, y, z = float(p[0]), float(p[1]), float(p[2])
                if math.isfinite(x) and math.isfinite(y) and math.isfinite(z):
                    points.append((x, y, z))
        except Exception as exc:
            self.reason = f"frontier_viewpoint_parse_failed:{type(exc).__name__}"
            return
        self.frontier_viewpoints = points

    def _frontier_candidates_cb(self, msg: PointCloud2) -> None:
        self.frontier_candidate_count = int(msg.width * msg.height)

    def _explored_grid_cb(self, msg: PointCloud2) -> None:
        self.explored_points = int(msg.width * msg.height)
        self._record_coverage_sample()

    def _global_cloud_cb(self, msg: PointCloud2) -> None:
        self.global_cloud_points = max(self.global_cloud_points, int(msg.width * msg.height))
        self._record_coverage_sample()

    def _record_coverage_sample(self) -> None:
        now = self._now()
        self.coverage_history.append((now, self._coverage_proxy()))
        self._trim_histories(now)

    def _coverage_proxy(self) -> float:
        return float(self.explored_points) / float(max(self.global_cloud_points, 1))

    def _trim_histories(self, now: float) -> None:
        keep_after = now - max(self.recent_goal_ttl_sec, self.progress_stall_window_sec, self.no_progress_window_sec, 120.0)
        self.odom_history = [(t, p) for t, p in self.odom_history if t >= keep_after]
        self.coverage_history = [(t, c) for t, c in self.coverage_history if t >= keep_after]
        self.recent_goals = [(k, t) for k, t in self.recent_goals if now - t <= self.recent_goal_ttl_sec]
        self.retired_goal_keys = [(k, t) for k, t in self.retired_goal_keys if now - t <= self.recent_goal_ttl_sec]

    @staticmethod
    def _pose_point(msg: PoseStamped) -> Point:
        p = msg.pose.position
        return float(p.x), float(p.y), float(p.z)

    def _goal_key(self, point: Point) -> Tuple[int, int, int]:
        q = max(self.recent_goal_quantization, 1e-3)
        return tuple(int(round(v / q)) for v in point)

    def _remember_goal(self, goal: PoseStamped, now: float) -> None:
        key = self._goal_key(self._pose_point(goal))
        self.recent_goals.append((key, now))
        if len(self.recent_goals) > self.recent_goal_memory_size:
            self.recent_goals = self.recent_goals[-self.recent_goal_memory_size:]

    def _is_recent_goal(self, point: Point, now: Optional[float] = None) -> bool:
        now = self._now() if now is None else now
        key = self._goal_key(point)
        return any(k == key and now - t <= self.recent_goal_ttl_sec for k, t in self.recent_goals)

    def _retire_active_goal(self, reason: str, now: Optional[float] = None) -> None:
        if self.active_goal is None:
            return
        now = self._now() if now is None else now
        key = self._goal_key(self._pose_point(self.active_goal))
        self.retired_goal_keys.append((key, now))
        self.goal_retire_event_count += 1
        self.goal_retire_reasons[reason] = self.goal_retire_reasons.get(reason, 0) + 1
        self._publish_goal_event("RETIRE_GOAL", self.active_goal, reason)

    def _no_path_region_key(self, point: Point) -> Tuple[int, int]:
        res = max(0.5, self.no_path_region_radius)
        return int(math.floor(point[0] / res)), int(math.floor(point[1] / res))

    def _prune_no_path_blacklist(self, now: float) -> None:
        ttl = max(1.0, self.no_path_blacklist_ttl_sec)
        self.no_path_blacklisted_regions = {
            region: stamp for region, stamp in self.no_path_blacklisted_regions.items() if now - stamp <= ttl
        }

    def _is_no_path_blacklisted(self, point: Point, now: Optional[float] = None) -> bool:
        now = self._now() if now is None else now
        self._prune_no_path_blacklist(now)
        return self._no_path_region_key(point) in self.no_path_blacklisted_regions

    def _active_goal_without_active_path_duration(self, now: float) -> float:
        if self.active_goal is None:
            return 0.0
        return 0.0 if self.last_active_path_update_sec >= self.goal_start_sec else max(0.0, now - self.goal_start_sec)

    def _active_goal_without_travel_traj_duration(self, now: float) -> float:
        if self.active_goal is None:
            return 0.0
        return 0.0 if self.last_travel_traj_update_sec >= self.goal_start_sec else max(0.0, now - self.goal_start_sec)

    def _no_path_waiting(self, now: float) -> bool:
        if self.active_goal is None:
            return False
        return (
            self._active_goal_without_active_path_duration(now) >= self.goal_to_path_timeout_sec
            and self._active_goal_without_travel_traj_duration(now) >= self.goal_to_path_timeout_sec
        )

    def _handle_no_path_timeout(self, now: float) -> bool:
        if self.active_goal is None:
            return False
        active_missing = self._active_goal_without_active_path_duration(now)
        travel_missing = self._active_goal_without_travel_traj_duration(now)
        waiting = active_missing >= self.goal_to_path_timeout_sec and travel_missing >= self.goal_to_path_timeout_sec
        if waiting and not self.no_path_timeout_reported:
            self.no_path_timeout_count += 1
            self.no_path_timeout_reported = True
            self._publish_goal_event(
                "GOAL_TO_PATH_TIMEOUT",
                self.active_goal,
                "NO_PATH_TIMEOUT",
                f"wait_sec={max(active_missing, travel_missing):.3f}",
            )
        if waiting and now - self.no_path_waiting_reported_sec >= 2.0:
            self.no_path_waiting_reported_sec = now
            self._publish_goal_event(
                "ACTIVE_PATH_MISSING",
                self.active_goal,
                "NO_PATH_WAITING",
                f"duration_sec={active_missing:.3f} travel_traj_missing_sec={travel_missing:.3f}",
            )
        if active_missing < self.goal_without_path_retire_sec or travel_missing < self.goal_without_path_retire_sec:
            return False
        point = self._pose_point(self.active_goal)
        region = self._no_path_region_key(point)
        self.no_path_blacklisted_regions[region] = now
        self.no_path_blacklist_count += 1
        old_goal = self.active_goal
        self._publish_goal_event("GOAL_RETIRED", old_goal, "NO_PATH_TIMEOUT")
        self._publish_goal_event(
            "GOAL_BLACKLIST",
            old_goal,
            "NO_PATH_TIMEOUT",
            f"ttl={self.no_path_blacklist_ttl_sec:.1f} region={region}",
        )
        self._retire_active_goal("NO_PATH_TIMEOUT", now)
        if self._pending_is_usable():
            self.goal_reselect_due_to_no_path_count += 1
            self._publish_goal_event("GOAL_RESELECT", self.pending_best, "NO_PATH_TIMEOUT")
            self._switch_to_pending("NO_PATH_TIMEOUT")
        elif self._switch_to_escape_goal("NO_PATH_TIMEOUT"):
            self.goal_reselect_due_to_no_path_count += 1
            self._publish_goal_event("GOAL_RESELECT", self.active_goal, "NO_PATH_TIMEOUT")
        else:
            self.active_goal = None
            self.reason = "NO_PATH_TIMEOUT_waiting_for_new_viewpoint"
            self.switch_reason = self.reason
        return True

    def _recently_retired(self, point: Point, now: Optional[float] = None) -> bool:
        now = self._now() if now is None else now
        key = self._goal_key(point)
        return any(k == key and now - t <= self.recent_goal_ttl_sec for k, t in self.retired_goal_keys)

    def _publish_goal_event(self, event_type: str, goal: Optional[PoseStamped], reason: str, extra: str = "") -> None:
        self.last_goal_event = event_type
        self.last_goal_event_reason = reason
        if goal is not None:
            p = goal.pose.position
            self.last_goal_event_goal = f"({float(p.x):.2f},{float(p.y):.2f},{float(p.z):.2f})"
        else:
            self.last_goal_event_goal = "NONE"
        msg = String()
        if goal is None:
            xyz = "x=nan y=nan z=nan"
        else:
            p = goal.pose.position
            xyz = f"x={float(p.x):.3f} y={float(p.y):.3f} z={float(p.z):.3f}"
        msg.data = f"GOAL_EVENT type={event_type} {xyz} reason={reason} {extra}".strip()
        self.goal_lifecycle_pub.publish(msg)

    def _goal_reached(self) -> bool:
        distance = self._active_goal_distance()
        return distance is not None and distance <= self.goal_reached_radius

    def _active_goal_too_close(self) -> bool:
        distance = self._active_goal_distance()
        return distance is not None and distance <= self.min_goal_distance

    def _active_goal_distance(self) -> Optional[float]:
        if self.active_goal is None or self.odom is None:
            return None
        gp = self.active_goal.pose.position
        op = self.odom.pose.pose.position
        return math.dist((float(gp.x), float(gp.y), float(gp.z)), (float(op.x), float(op.y), float(op.z)))

    def _pending_goal_distance(self) -> Optional[float]:
        if self.pending_best is None or self.odom is None:
            return None
        pp = self.pending_best.pose.position
        op = self.odom.pose.pose.position
        return math.dist((float(pp.x), float(pp.y), float(pp.z)), (float(op.x), float(op.y), float(op.z)))

    def _smooth_pending_goal(self, region_switch: bool) -> Optional[PoseStamped]:
        if self.pending_best is None:
            return None
        if self.active_goal is None:
            return self.pending_best
        separation = self._pending_separation_from_active()
        if separation is None:
            return self.pending_best
        if separation <= self.max_goal_jump_without_region_switch or region_switch:
            if separation > self.max_goal_jump_without_region_switch:
                self.goal_jump_count += 1
                self.goal_jitter_score = max(self.goal_jitter_score, separation)
            return self.pending_best
        self.goal_jump_count += 1
        self.goal_jitter_score = max(self.goal_jitter_score, separation)
        alpha = max(0.0, min(1.0, self.goal_smoothing_alpha))
        ap = self.active_goal.pose.position
        pp = self.pending_best.pose.position
        smoothed = PoseStamped()
        smoothed.header = self.pending_best.header
        smoothed.pose.orientation = self.pending_best.pose.orientation
        smoothed.pose.position.x = (1.0 - alpha) * float(ap.x) + alpha * float(pp.x)
        smoothed.pose.position.y = (1.0 - alpha) * float(ap.y) + alpha * float(pp.y)
        smoothed.pose.position.z = (1.0 - alpha) * float(ap.z) + alpha * float(pp.z)
        if self.odom is not None:
            op = self.odom.pose.pose.position
            odom_xyz = (float(op.x), float(op.y), float(op.z))
            smoothed_xyz = (float(smoothed.pose.position.x), float(smoothed.pose.position.y), float(smoothed.pose.position.z))
            if math.dist(odom_xyz, smoothed_xyz) <= self.min_goal_distance:
                dx, dy, dz = float(pp.x) - odom_xyz[0], float(pp.y) - odom_xyz[1], float(pp.z) - odom_xyz[2]
                norm = math.sqrt(dx * dx + dy * dy + dz * dz)
                if norm <= self.min_goal_distance:
                    self.goal_jump_reject_count += 1
                    return None
                step = min(norm, self.min_goal_distance + 1.0)
                smoothed.pose.position.x = odom_xyz[0] + dx / norm * step
                smoothed.pose.position.y = odom_xyz[1] + dy / norm * step
                smoothed.pose.position.z = odom_xyz[2] + dz / norm * step
        self.goal_smoothing_applied_count += 1
        return smoothed

    def _switch_to_goal(self, goal: PoseStamped, score: float, reason: str, source: str) -> None:
        now = self._now()
        if self.active_goal is not None:
            self._retire_active_goal(reason, now)
        point = self._pose_point(goal)
        if self._recently_retired(point, now):
            self.true_repeated_goal_count += 1
        self.active_goal = goal
        self.active_goal.header.stamp = self.get_clock().now().to_msg()
        self.goal_start_sec = now
        self.last_switch_sec = self.goal_start_sec
        if self.goal_switch_count == 0:
            self.first_switch_sec = self.goal_start_sec
        self.goal_switch_count += 1
        self.active_goal_score = score
        self.goal_start_distance = self._active_goal_distance()
        self.last_goal_distance = self.goal_start_distance
        self.last_goal_distance_sample_sec = self.goal_start_sec
        self.goal_progress_score = 0.0
        self.coverage_gain_since_goal = 0.0
        self.too_close_start_sec = None
        self.no_progress_detected = False
        self.reason = reason
        self.last_switch_reason = reason
        self.switch_reason = reason
        self.active_goal_key = self._goal_key(point)
        self.no_path_timeout_reported = False
        self.no_path_waiting_reported_sec = -999.0
        self.last_active_path_update_sec = -999.0
        self.last_travel_traj_update_sec = -999.0
        self.active_path_points = 0
        self.travel_traj_points = 0
        self._remember_goal(goal, now)
        self._last_progress_sec = now
        self._publish_goal_event("GOAL_SELECTED", goal, reason, f"source={source} score={score:.3f}")
        self._publish_goal_event("GOAL_TO_PATH_REQUEST", goal, reason, f"goal_id={self.active_goal_key}")

    def _switch_to_pending(self, reason: str) -> None:
        if not self._pending_is_usable():
            self.reason = f"{reason}_waiting_for_distinct_viewpoint"
            self.switch_reason = self.reason
            return
        region_switch = self.pending_region_id not in ("NONE", self.active_region_id)
        next_goal = self._smooth_pending_goal(region_switch)
        if next_goal is None:
            self.reason = f"{reason}_goal_jump_rejected"
            self.switch_reason = "goal_jump_rejected"
            return
        self._switch_to_goal(next_goal, self.pending_best_score, reason, "best_viewpoint")
        if self.pending_region_id != "NONE":
            if self.pending_region_id != self.active_region_id:
                self.active_region_start_sec = self.goal_start_sec
            self.active_region_id = self.pending_region_id
            self.active_region_score = self.pending_region_score

    def _pending_is_usable(self) -> bool:
        if self.pending_best is None:
            return False
        pp = self.pending_best.pose.position
        pending_xyz = (float(pp.x), float(pp.y), float(pp.z))
        if self.active_goal is not None:
            ap = self.active_goal.pose.position
            active_xyz = (float(ap.x), float(ap.y), float(ap.z))
            if math.dist(active_xyz, pending_xyz) < self.min_new_goal_separation:
                return False
        if self.odom is not None:
            op = self.odom.pose.pose.position
            odom_xyz = (float(op.x), float(op.y), float(op.z))
            if math.dist(odom_xyz, pending_xyz) <= self.min_goal_distance:
                return False
        if self._recently_retired(pending_xyz):
            return False
        if self._is_no_path_blacklisted(pending_xyz):
            self.last_goal_event_reason = "NO_PATH_BLACKLIST"
            return False
        return True

    def _rate_limit_allows_switch(self, now: float) -> bool:
        if self.goal_switch_count <= 0 or self.first_switch_sec <= 0.0:
            return True
        elapsed = max(1.0, now - self.first_switch_sec)
        allowed = max(1.0, self.max_goal_switch_rate * elapsed + 1.0)
        return float(self.goal_switch_count) < allowed

    def _pending_separation_from_active(self) -> Optional[float]:
        if self.active_goal is None or self.pending_best is None:
            return None
        ap = self.active_goal.pose.position
        pp = self.pending_best.pose.position
        return math.dist((float(ap.x), float(ap.y), float(ap.z)), (float(pp.x), float(pp.y), float(pp.z)))

    def _pending_score_sufficient(self) -> bool:
        if self.active_goal_score <= 0.0:
            return True
        ratio_ok = self.pending_best_score >= self.active_goal_score * self.min_switch_improvement_ratio
        delta_ok = self.pending_best_score >= self.active_goal_score + self.min_switch_score_improvement
        return ratio_ok and delta_ok

    def _update_progress(self, now: float) -> None:
        distance = self._active_goal_distance()
        if distance is None:
            self.goal_progress_score = 0.0
            self.coverage_gain_since_goal = 0.0
            return
        if self.goal_start_distance is None:
            self.goal_start_distance = distance
        start = max(1e-3, self.goal_start_distance)
        self.goal_progress_score = max(0.0, min(1.0, (start - distance) / start))
        if self.last_goal_distance is not None:
            self.coverage_gain_since_goal = max(0.0, self.last_goal_distance - distance) / start
        if now - self.last_goal_distance_sample_sec >= self.min_progress_window_sec:
            self.last_goal_distance = distance
            self.last_goal_distance_sample_sec = now

    def _window_motion(self, window_sec: float) -> float:
        if len(self.odom_history) < 2:
            return 0.0
        now = self._now()
        recent = [(t, p) for t, p in self.odom_history if now - t <= window_sec]
        if len(recent) < 2:
            return 0.0
        return math.dist(recent[0][1], recent[-1][1])

    def _window_coverage_gain(self, window_sec: float) -> float:
        if len(self.coverage_history) < 2:
            return 0.0
        now = self._now()
        recent = [(t, c) for t, c in self.coverage_history if now - t <= window_sec]
        if len(recent) < 2:
            return 0.0
        return recent[-1][1] - recent[0][1]

    def _coverage_stall_escape_ready(self) -> bool:
        if self.active_goal is None or self.odom is None:
            return False
        if self._now() - self.last_switch_sec < self.escape_cooldown_sec:
            return False
        if self.frontier_candidate_count <= 0 and self.frontier_viewpoint_count <= 0:
            return False
        cov_gain = self._window_coverage_gain(self.progress_stall_window_sec)
        motion = self._window_motion(self.progress_stall_window_sec)
        ready = cov_gain < self.progress_stall_min_coverage_gain and motion < self.progress_stall_min_motion
        self.coverage_stall_detected = ready
        self.coverage_stall_duration = self.progress_stall_window_sec if ready else 0.0
        return ready

    def _no_progress_ready(self) -> bool:
        if self.active_goal is None:
            return False
        if self._now() - self.last_switch_sec < self.escape_cooldown_sec:
            return False
        cov_gain = self._window_coverage_gain(self.no_progress_window_sec)
        motion = self._window_motion(self.no_progress_window_sec)
        self.no_progress_detected = cov_gain < self.progress_stall_min_coverage_gain and motion < self.no_progress_min_motion
        return self.no_progress_detected

    def _make_goal(self, point: Point, score: float, frame: str = "map") -> PoseStamped:
        goal = PoseStamped()
        goal.header.frame_id = f"{frame} score={score:.3f} escape=true"
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = point[0]
        goal.pose.position.y = point[1]
        goal.pose.position.z = point[2]
        goal.pose.orientation.w = 1.0
        return goal

    def _select_escape_goal(self) -> Tuple[Optional[PoseStamped], str]:
        if self.odom is None:
            return None, "no_odom"
        op = self.odom.pose.pose.position
        odom_xyz = (float(op.x), float(op.y), float(op.z))
        active_xyz = self._pose_point(self.active_goal) if self.active_goal is not None else None
        now = self._now()
        if self.pending_best is not None:
            pending_point = self._pose_point(self.pending_best)
            pending_distance = math.dist(odom_xyz, pending_point)
            active_distance = math.dist(active_xyz, pending_point) if active_xyz is not None else 999.0
            if pending_distance >= self.escape_min_goal_separation and active_distance >= self.min_new_goal_separation:
                return self.pending_best, "pending_best_escape"
        if not self.enable_frontier_point_escape:
            return None, "frontier_point_escape_disabled"
        candidates: List[Tuple[float, Point, str]] = []
        fallback: List[Tuple[float, Point, str]] = []
        for point in self.frontier_viewpoints:
            distance = math.dist(odom_xyz, point)
            if distance < self.escape_fallback_goal_separation:
                continue
            recent = self._is_recent_goal(point, now)
            if recent:
                self.escape_skip_recent_count += 1
            active_penalty = 1.0 if active_xyz is not None and math.dist(active_xyz, point) < self.min_new_goal_separation else 0.0
            distance_bonus = min(distance, 8.0) / 8.0
            score = self.escape_distance_bonus * distance_bonus - (self.escape_recent_penalty if recent else 0.0) - active_penalty
            item = (score, point, "frontier_viewpoints")
            if distance >= self.escape_min_goal_separation and not recent and active_penalty <= 0.0:
                candidates.append(item)
            else:
                fallback.append(item)
        self.escape_candidate_count = len(candidates)
        source = "frontier_viewpoints"
        selected: Optional[Tuple[float, Point, str]] = None
        if candidates:
            selected = max(candidates, key=lambda item: item[0])
        elif fallback:
            selected = max(fallback, key=lambda item: item[0])
            source = "frontier_viewpoints_fallback"
            self.escape_fallback_count += 1
        elif self.pending_best is not None:
            pending_point = self._pose_point(self.pending_best)
            if math.dist(odom_xyz, pending_point) >= self.escape_fallback_goal_separation:
                selected = (self.pending_best_score, pending_point, "pending_best_fallback")
                source = "pending_best_fallback"
                self.escape_fallback_count += 1
        if selected is None:
            return None, "no_escape_candidate"
        score, point, source = selected
        return self._make_goal(point, score), source

    def _switch_to_escape_goal(self, reason: str) -> bool:
        bypass_rate_limit = reason in ("coverage_stall", "no_progress", "NO_PATH_TIMEOUT")
        if not bypass_rate_limit and not self._rate_limit_allows_switch(self._now()):
            self.switch_blocked_by_rate_count += 1
            self.reason = f"{reason}_rate_limited"
            self.switch_reason = "blocked_by_rate"
            return False
        goal, source = self._select_escape_goal()
        if goal is None:
            self.reason = f"{reason}_{source}"
            self.switch_reason = self.reason
            return False
        self.escape_goal_count += 1
        self.escape_active = True
        self.escape_reason = reason
        self.last_escape_sec = self._now()
        self.recovery_count += 1
        self.recovery_goal = self._pose_text(goal)
        self._switch_to_goal(goal, self._extract_score(goal), f"escape_goal_{reason}", source)
        self._publish_goal_event("ESCAPE_GOAL", goal, reason, f"source={source}")
        return True

    def _pose_text(self, goal: Optional[PoseStamped]) -> str:
        if goal is None:
            return "NONE"
        p = goal.pose.position
        return f"({float(p.x):.2f},{float(p.y):.2f},{float(p.z):.2f})"

    def _goal_progress_allows_switch(self, now: float) -> bool:
        self.oscillation_cooldown_active = now - self.last_switch_sec < self.oscillation_cooldown_sec and self.goal_switch_count > 0
        if self.oscillation_cooldown_active and self.goal_progress_score > 0.02:
            self.goal_switch_blocked_by_progress_count += 1
            self.reason = "hold_active_goal_oscillation_cooldown"
            self.switch_reason = "blocked_by_progress"
            return False
        goal_age = 0.0 if self.active_goal is None else now - self.goal_start_sec
        if goal_age < self.min_goal_hold_sec:
            self.goal_switch_blocked_by_progress_count += 1
            self.reason = "hold_active_goal_min_progress_hold"
            self.switch_reason = "blocked_by_progress"
            return False
        if self.goal_progress_score > 0.05 or self.coverage_gain_since_goal >= self.min_coverage_gain_for_continue:
            self._last_progress_sec = now
            self.goal_switch_blocked_by_progress_count += 1
            self.reason = "hold_active_goal_making_progress"
            self.switch_reason = "blocked_by_progress"
            return False
        return True

    def _region_allows_switch(self, now: float) -> bool:
        if self.active_region_id == "NONE" or self.pending_region_id in ("NONE", self.active_region_id):
            return True
        active_age = now - self.active_region_start_sec if self.active_region_start_sec > 0.0 else 0.0
        self.region_stall_detected = now - self._last_progress_sec >= self.region_stall_timeout_sec
        score_jump = self.active_region_score <= 0.0 or self.pending_region_score >= self.active_region_score * self.region_switch_score_ratio
        if active_age < self.min_region_hold_sec and not self.region_stall_detected and not score_jump:
            self.region_hold_active = True
            self.region_switch_reason = "hold_active_region"
            return False
        if self.region_stall_detected:
            self.coverage_stall_detected = True
            self.coverage_stall_duration = now - self._last_progress_sec
            self.recovery_region_id = self.pending_region_id
            if self.pending_best is not None:
                p = self.pending_best.pose.position
                self.recovery_goal = f"({float(p.x):.2f},{float(p.y):.2f},{float(p.z):.2f})"
            self.recovery_count += 1
            self.region_switch_reason = "coverage_stall_recovery"
            return True
        if score_jump:
            self.region_switch_reason = "higher_score_region"
            return True
        self.region_switch_reason = "region_switch_blocked"
        return False

    def _switch_allowed_after_hold(self, now: float) -> bool:
        separation = self._pending_separation_from_active()
        if separation is not None and separation < self.goal_jitter_radius:
            self.goal_jitter_suppressed_count += 1
            self.goal_switch_blocked_by_similarity_count += 1
            self.reason = "hold_active_goal_jitter_radius"
            self.switch_reason = "blocked_by_similarity"
            return False
        if not self._region_allows_switch(now):
            self.goal_switch_blocked_by_progress_count += 1
            self.reason = self.region_switch_reason
            self.switch_reason = "blocked_by_region_hold"
            return False
        if separation is not None and separation < max(self.spatial_hysteresis_radius, self.min_goal_separation):
            self.goal_switch_blocked_by_similarity_count += 1
            self.switch_blocked_by_hysteresis_count += 1
            self.reason = "hold_active_goal_hysteresis"
            self.switch_reason = "blocked_by_hysteresis"
            return False
        if not self._pending_score_sufficient():
            self.goal_switch_blocked_by_low_gain_count += 1
            self.switch_blocked_by_score_count += 1
            self.reason = "hold_active_goal_score"
            self.switch_reason = "blocked_by_score"
            return False
        if not self._goal_progress_allows_switch(now):
            return False
        if not self._rate_limit_allows_switch(now):
            self.switch_blocked_by_rate_count += 1
            self.reason = "hold_active_goal_rate_limit"
            self.switch_reason = "blocked_by_rate"
            return False
        return True

    def _tick(self) -> None:
        now = self._now()
        self._trim_histories(now)
        self._prune_no_path_blacklist(now)
        self._update_progress(now)
        goal_age = 0.0 if self.active_goal is None else now - self.goal_start_sec
        goal_distance = self._active_goal_distance()
        reached = self._goal_reached()
        too_close = self._active_goal_too_close()
        if too_close:
            if self.too_close_start_sec is None:
                self.too_close_start_sec = now
        else:
            self.too_close_start_sec = None
        too_close_expired = self.too_close_start_sec is not None and now - self.too_close_start_sec >= self.too_close_retire_sec
        timeout = (
            self.active_goal is not None
            and goal_age >= min(self.goal_timeout_sec, 25.0)
            and self._window_coverage_gain(self.min_progress_window_sec) < self.min_coverage_gain_for_continue
        )
        no_progress = self._no_progress_ready()
        escape_ready = self._coverage_stall_escape_ready()
        path_infeasible_duration = 0.0 if self.path_infeasible_start_sec is None else now - self.path_infeasible_start_sec
        path_infeasible_expired = self.active_goal is not None and path_infeasible_duration >= 3.0 and self.path_infeasible_count >= 3
        self.goal_hold_active = False
        self.region_hold_active = False
        self.region_stall_detected = now - self._last_progress_sec >= self.region_stall_timeout_sec
        no_path_handled = self._handle_no_path_timeout(now)
        if no_path_handled:
            self.goal_hold_active = True
        elif self.active_goal is None:
            self._switch_to_pending("new_best_viewpoint")
        elif path_infeasible_expired:
            self._retire_active_goal("path_infeasible", now)
            self.path_infeasible_retire_count += 1
            if self._pending_is_usable() and self._rate_limit_allows_switch(now):
                self._switch_to_pending("path_infeasible_reselect")
            else:
                self.active_goal = None
                self.reason = "path_infeasible_waiting_for_new_viewpoint"
                self.switch_reason = self.reason
                self.goal_hold_active = True
        elif reached:
            if self._pending_is_usable() and self._rate_limit_allows_switch(now):
                self._switch_to_pending("goal_reached_switch")
            elif self._pending_is_usable():
                self.switch_blocked_by_rate_count += 1
                self.reason = "goal_reached_rate_limited"
                self.switch_reason = "blocked_by_rate"
                self.goal_hold_active = True
            else:
                self.reason = "goal_reached_waiting_for_distinct_viewpoint"
                self.switch_reason = self.reason
                self.goal_hold_active = True
        elif escape_ready:
            if not self._switch_to_escape_goal("coverage_stall"):
                self.goal_hold_active = True
        elif no_progress:
            if self._pending_is_usable() and self._rate_limit_allows_switch(now):
                self._switch_to_pending("no_progress_switch")
            elif not self._switch_to_escape_goal("no_progress"):
                self.goal_hold_active = True
        elif too_close and too_close_expired:
            if self._pending_is_usable() and self._rate_limit_allows_switch(now):
                self._switch_to_pending("goal_too_close_switch")
            elif not self._switch_to_escape_goal("goal_too_close"):
                self.goal_hold_active = True
        elif too_close:
            if self._pending_is_usable() and self._rate_limit_allows_switch(now) and goal_age >= self.too_close_retire_sec:
                self._switch_to_pending("goal_too_close_switch")
            elif self._pending_is_usable():
                self.switch_blocked_by_rate_count += 1
                self.reason = "goal_too_close_rate_limited"
                self.switch_reason = "blocked_by_rate"
                self.goal_hold_active = True
            else:
                self.reason = "goal_too_close_waiting_for_distinct_viewpoint"
                self.switch_reason = self.reason
                self.goal_hold_active = True
        elif timeout:
            if self._rate_limit_allows_switch(now):
                self._switch_to_pending("goal_timeout")
            else:
                self.switch_blocked_by_rate_count += 1
                self.reason = "goal_timeout_rate_limited"
                self.switch_reason = "blocked_by_rate"
                self.goal_hold_active = True
        elif goal_age >= self.minimum_goal_hold_sec and self.pending_best is not None:
            if self._switch_allowed_after_hold(now):
                self._switch_to_pending("better_viewpoint_after_hold")
            else:
                self.goal_hold_active = True
        else:
            self.reason = "minimum_goal_hold"
            self.switch_reason = "minimum_goal_hold"
            self.goal_hold_active = True

        goal_distance = self._active_goal_distance()
        active_goal_valid = self.active_goal is not None and (goal_distance is None or goal_distance > self.min_goal_distance)
        if self.active_goal is not None and active_goal_valid:
            self.active_goal.header.stamp = self.get_clock().now().to_msg()
            self.goal_pub.publish(self.active_goal)
            self.goal_republish_count += 1
            if int(self.goal_republish_count) % 10 == 0:
                self._publish_goal_event("KEEP_GOAL", self.active_goal, self.reason, f"duration={goal_age:.3f}")

        status = String()
        goal_age = 0.0 if self.active_goal is None else now - self.goal_start_sec
        active_path_missing_sec = self._active_goal_without_active_path_duration(now)
        travel_traj_missing_sec = self._active_goal_without_travel_traj_duration(now)
        status.data = (
            "REAL_FLIGHT_COMMAND=false "
            f"active_goal={'true' if self.active_goal is not None else 'false'} "
            f"active_goal_valid={'true' if active_goal_valid else 'false'} "
            f"goal_age={goal_age:.3f} "
            f"active_goal_age={goal_age:.3f} "
            f"goal_distance={goal_distance if goal_distance is not None else -1.0:.3f} "
            f"goal_reached={'true' if reached else 'false'} "
            f"goal_timeout={'true' if timeout else 'false'} "
            f"too_close_expired={'true' if too_close_expired else 'false'} "
            f"no_progress_detected={'true' if no_progress else 'false'} "
            f"path_feasible={'true' if self.path_feasible else 'false'} "
            f"path_infeasible_duration={path_infeasible_duration:.3f} "
            f"path_infeasible_count={self.path_infeasible_count} "
            f"path_infeasible_retire_count={self.path_infeasible_retire_count} "
            f"path_status_reason={self.path_status_reason} "
            f"path_status_goal_key={self.path_status_goal_key} "
            f"path_endpoint_to_goal_distance={self.path_endpoint_to_goal_distance:.3f} "
            f"no_path_watchdog_enabled={'true' if self.no_path_watchdog_enabled else 'false'} "
            f"goal_to_path_timeout_sec={self.goal_to_path_timeout_sec:.3f} "
            f"goal_without_path_retire_sec={self.goal_without_path_retire_sec:.3f} "
            f"active_path_points={self.active_path_points} "
            f"travel_traj_points={self.travel_traj_points} "
            f"active_goal_without_active_path_duration={active_path_missing_sec:.3f} "
            f"active_goal_without_travel_traj_duration={travel_traj_missing_sec:.3f} "
            f"goal_to_path_timeout_count={self.no_path_timeout_count} "
            f"no_path_blacklist_count={self.no_path_blacklist_count} "
            f"no_path_blacklisted_region_count={len(self.no_path_blacklisted_regions)} "
            f"goal_reselect_due_to_no_path_count={self.goal_reselect_due_to_no_path_count} "
            f"goal_switch_count={self.goal_switch_count} "
            f"goal_retire_event_count={self.goal_retire_event_count} "
            f"goal_retire_reasons={self.goal_retire_reasons} "
            f"true_repeated_goal_count={self.true_repeated_goal_count} "
            f"goal_republish_count={self.goal_republish_count} "
            f"goal_hold_active={'true' if self.goal_hold_active else 'false'} "
            f"goal_progress_score={self.goal_progress_score:.3f} "
            f"coverage_gain_since_goal={self.coverage_gain_since_goal:.4f} "
            f"coverage_proxy={self._coverage_proxy():.6f} "
            f"window_coverage_gain_30s={self._window_coverage_gain(self.progress_stall_window_sec):.6f} "
            f"window_motion_30s={self._window_motion(self.progress_stall_window_sec):.3f} "
            f"goal_switch_blocked_by_progress_count={self.goal_switch_blocked_by_progress_count} "
            f"goal_switch_blocked_by_similarity_count={self.goal_switch_blocked_by_similarity_count} "
            f"goal_switch_blocked_by_low_gain_count={self.goal_switch_blocked_by_low_gain_count} "
            f"oscillation_cooldown_active={'true' if self.oscillation_cooldown_active else 'false'} "
            f"active_region_id={self.active_region_id} "
            f"pending_region_id={self.pending_region_id} "
            f"region_hold_active={'true' if self.region_hold_active else 'false'} "
            f"region_stall_detected={'true' if self.region_stall_detected else 'false'} "
            f"region_switch_reason={self.region_switch_reason} "
            f"goal_jitter_suppressed_count={self.goal_jitter_suppressed_count} "
            f"goal_jump_reject_count={self.goal_jump_reject_count} "
            f"goal_smoothing_applied_count={self.goal_smoothing_applied_count} "
            f"goal_jump_count={self.goal_jump_count} "
            f"goal_jitter_score={self.goal_jitter_score:.3f} "
            f"coverage_stall_detected={'true' if self.coverage_stall_detected else 'false'} "
            f"coverage_stall_duration={self.coverage_stall_duration:.3f} "
            f"recovery_region_id={self.recovery_region_id} "
            f"recovery_goal={self.recovery_goal} "
            f"recovery_count={self.recovery_count} "
            f"escape_goal_count={self.escape_goal_count} "
            f"escape_fallback_count={self.escape_fallback_count} "
            f"escape_skip_recent_count={self.escape_skip_recent_count} "
            f"escape_candidate_count={self.escape_candidate_count} "
            f"escape_active={'true' if self.escape_active else 'false'} "
            f"escape_reason={self.escape_reason} "
            f"frontier_candidate_count={self.frontier_candidate_count} "
            f"frontier_viewpoint_count={self.frontier_viewpoint_count} "
            f"last_goal_event={self.last_goal_event} "
            f"last_goal_event_reason={self.last_goal_event_reason} "
            f"last_goal_event_goal={self.last_goal_event_goal} "
            f"switch_blocked_by_hysteresis_count={self.switch_blocked_by_hysteresis_count} "
            f"switch_blocked_by_score_count={self.switch_blocked_by_score_count} "
            f"switch_blocked_by_rate_count={self.switch_blocked_by_rate_count} "
            f"switch_reason={self.switch_reason} "
            f"last_switch_reason={self.last_switch_reason} "
            f"min_goal_distance={self.min_goal_distance:.3f} "
            f"reason={self.reason}"
        )
        self.status_pub.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = ExplorationManagerLite()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
