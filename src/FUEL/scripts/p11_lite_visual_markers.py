#!/usr/bin/env python3
import math
import re
from typing import Dict, List, Optional, Sequence, Set, Tuple

import rclpy
from geometry_msgs.msg import Point, PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
from visualization_msgs.msg import Marker, MarkerArray

from p11_lite_utils import parse_bounds, read_cloud, world_config_path


Point3 = Tuple[float, float, float]


class P11LiteVisualMarkers(Node):
    def __init__(self):
        super().__init__("p11_lite_visual_markers")
        self.world_config = world_config_path(str(self.declare_parameter("world_config", "").value))
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.environment_mode = str(self.declare_parameter("environment_mode", "simple").value)
        self.visual_profile = str(self.declare_parameter("visual_profile", "acceptance").value).lower()
        self.clean_profile = self.visual_profile == "clean"
        self.bounds = parse_bounds(self.world_config)
        self.odom: Optional[Odometry] = None
        self.global_path: Optional[Path] = None
        self.local_trajectory: Optional[Path] = None
        self.managed_trajectory: Optional[Path] = None
        self.active_execution_path: Optional[Path] = None
        self.best_viewpoint: Optional[PoseStamped] = None
        self.exploration_goal: Optional[PoseStamped] = None
        self.frontiers: List[Point3] = []
        self.occupied: List[Point3] = []
        self.free: List[Point3] = []
        self.complex_occupied: List[Point3] = []
        self.complex_status = ""
        self.complex_wall_markers = MarkerArray()
        self.complex_map_boundary: Optional[Marker] = None
        self.trail: List[Point3] = []
        self.goal_history: List[Point3] = []
        self.explored_keys: Set[Tuple[int, int]] = set()
        self.unknown_grid = self._build_unknown_grid()
        self.total_unknown_cells = max(1, len(self.unknown_grid))
        self.uav_distance = 0.0
        self.goal_switch_count = 0
        self.path_valid = False
        self.reject_reason = "none"
        self.wall_crossing_risk = "NO"
        self.active_path_source = "unknown"
        self.planned_path_points = 0
        self.average_tracking_error = -1.0
        self.max_tracking_error = -1.0
        self.tracking_consistency = "UNKNOWN"
        self.marker_deleteall_used = False
        self.stable_marker_ids = True
        self.static_marker_publish_rate_hz = 0.5
        self.dynamic_marker_publish_rate_hz = 2.0
        self.large_overlay_disabled = self.clean_profile
        self.active_path_only = self.clean_profile
        self.executed_trail_line_only = True
        self.sensor_fan_disabled = self.clean_profile
        self.clean_profile_overlay_namespaces_disabled = [
            "unknown_area",
            "explored_area",
            "frontier_candidates",
            "occupied_obstacles",
            "complex_obstacle_points",
            "free_space",
            "goal_history",
            "sensor_fan",
            "sensor_frustum",
            "coverage_overlay",
            "explored_overlay",
            "large_overlay",
        ]
        self.clean_status_tokens = (
            "large_overlay_disabled=true active_path_only=true "
            "executed_trail_line_only=true sensor_fan_disabled=true "
            "large_orange_overlay_present=NO"
        )
        self.last_goal_time = self.get_clock().now()

        self.create_subscription(Odometry, "/odom", self._odom_cb, 20)
        self.create_subscription(Path, "/fuel/global_path", lambda msg: setattr(self, "global_path", msg), 10)
        self.create_subscription(Path, "/fuel/local_trajectory", lambda msg: setattr(self, "local_trajectory", msg), 10)
        self.create_subscription(Path, "/fuel/plan_manager/managed_trajectory", lambda msg: setattr(self, "managed_trajectory", msg), 10)
        self.create_subscription(Path, "/fuel/p10_lite/active_path", lambda msg: setattr(self, "active_execution_path", msg), 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/best_viewpoint", lambda msg: setattr(self, "best_viewpoint", msg), 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self._goal_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/frontier_candidates_raw", self._frontier_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/local_occupied_points", self._occupied_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/local_free_points", self._free_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/complex_env/occupied_points", self._complex_occupied_cb, 10)
        self.create_subscription(MarkerArray, "/fuel/p11_lite/complex_env/wall_markers", self._complex_wall_cb, 10)
        self.create_subscription(Marker, "/fuel/p11_lite/complex_env/map_boundary", self._complex_boundary_cb, 10)
        self.create_subscription(String, "/fuel/p11_lite/complex_env/status", lambda msg: setattr(self, "complex_status", msg.data), 10)
        self.create_subscription(String, "/fuel/p11_lite/goal_to_path_status", self._goal_to_path_status_cb, 10)
        self.create_subscription(String, "/fuel/p11_lite/exploration_manager_status", self._exploration_status_cb, 10)
        self.create_subscription(String, "/fuel/p10_lite/traj_server_status", self._traj_status_cb, 10)

        self.uav_pub = self.create_publisher(Marker, "/fuel/p11_lite/visual/uav_marker", 10)
        self.trail_pub = self.create_publisher(Marker, "/fuel/p11_lite/visual/uav_trail", 10)
        self.goal_pub = self.create_publisher(Marker, "/fuel/p11_lite/visual/current_goal_marker", 10)
        self.best_pub = self.create_publisher(Marker, "/fuel/p11_lite/visual/best_viewpoint_marker", 10)
        self.frontier_pub = self.create_publisher(MarkerArray, "/fuel/p11_lite/visual/frontier_markers", 10)
        self.path_pub = self.create_publisher(MarkerArray, "/fuel/p11_lite/visual/path_markers", 10)
        self.boundary_pub = self.create_publisher(Marker, "/fuel/p11_lite/visual/map_boundary_marker", 10)
        self.legend_pub = self.create_publisher(MarkerArray, "/fuel/p11_lite/visual/legend_markers", 10)
        self.all_pub = self.create_publisher(MarkerArray, "/fuel/p11_lite/visual/all_markers", 10)
        self.timer = self.create_timer(0.5, self._publish)
        self.get_logger().info(
            f"P11_LITE_VISUAL_MARKERS_READY visual_profile={self.visual_profile} "
            f"large_overlay_disabled={str(self.large_overlay_disabled).lower()} "
            f"sensor_fan_disabled={str(self.sensor_fan_disabled).lower()} "
            "REAL_FLIGHT_COMMAND=false"
        )

    def _odom_cb(self, msg: Odometry) -> None:
        self.odom = msg
        p = msg.pose.pose.position
        point = (float(p.x), float(p.y), float(p.z))
        if not self.trail or math.dist(self.trail[-1], point) > 0.08:
            if self.trail:
                self.uav_distance += math.dist(self.trail[-1], point)
            self.trail.append(point)
            self.trail = self.trail[-1000:]
            self._mark_explored_disc(point, 1.8)

    def _goal_cb(self, msg: PoseStamped) -> None:
        self.exploration_goal = msg
        p = msg.pose.position
        point = (float(p.x), float(p.y), float(p.z))
        if not self.goal_history or math.dist(self.goal_history[-1], point) > 0.6:
            self.goal_history.append(point)
            self.goal_history = self.goal_history[-30:]
            self.goal_switch_count += 1
            self.last_goal_time = self.get_clock().now()

    def _frontier_cb(self, msg: PointCloud2) -> None:
        self.frontiers = read_cloud(msg)

    def _occupied_cb(self, msg: PointCloud2) -> None:
        self.occupied = read_cloud(msg)
        self._mark_explored_points(self.occupied)

    def _free_cb(self, msg: PointCloud2) -> None:
        self.free = read_cloud(msg)
        self._mark_explored_points(self.free)

    def _complex_occupied_cb(self, msg: PointCloud2) -> None:
        self.complex_occupied = read_cloud(msg)

    def _complex_wall_cb(self, msg: MarkerArray) -> None:
        self.complex_wall_markers = msg

    def _complex_boundary_cb(self, msg: Marker) -> None:
        self.complex_map_boundary = msg

    def _goal_to_path_status_cb(self, msg: String) -> None:
        self.path_valid = self._extract_value(msg.data, "path_valid", "false").lower() == "true"
        self.reject_reason = self._extract_value(msg.data, "reject_reason", self.reject_reason)
        self.wall_crossing_risk = self._extract_value(msg.data, "wall_crossing_risk", self.wall_crossing_risk)

    def _exploration_status_cb(self, msg: String) -> None:
        value = self._extract_value(msg.data, "goal_switch_count", "")
        if value.isdigit():
            self.goal_switch_count = max(self.goal_switch_count, int(value))

    def _traj_status_cb(self, msg: String) -> None:
        self.active_path_source = self._normalize_source(self._extract_value(msg.data, "active_source", self.active_path_source))

    @staticmethod
    def _normalize_source(source: str) -> str:
        if source == "plan_manager":
            return "managed_trajectory"
        return source

    @staticmethod
    def _extract_value(text: str, key: str, default: str) -> str:
        match = re.search(rf"{re.escape(key)}[:=]([A-Za-z0-9_.+-]+)", text)
        return match.group(1) if match else default

    def _grid_key(self, point: Point3, resolution: float = 0.75) -> Tuple[int, int]:
        return (int(round((point[0] - self.bounds["min_x"]) / resolution)), int(round((point[1] - self.bounds["min_y"]) / resolution)))

    def _grid_center(self, key: Tuple[int, int], resolution: float = 0.75, z: float = 0.04) -> Point3:
        return (self.bounds["min_x"] + key[0] * resolution, self.bounds["min_y"] + key[1] * resolution, z)

    def _mark_explored_points(self, points: Sequence[Point3]) -> None:
        for point in points[:4000]:
            self.explored_keys.add(self._grid_key(point))

    def _mark_explored_disc(self, point: Point3, radius: float) -> None:
        resolution = 0.75
        cells = int(math.ceil(radius / resolution))
        center = self._grid_key(point, resolution)
        for ix in range(center[0] - cells, center[0] + cells + 1):
            for iy in range(center[1] - cells, center[1] + cells + 1):
                candidate = self._grid_center((ix, iy), resolution, point[2])
                if math.hypot(candidate[0] - point[0], candidate[1] - point[1]) <= radius:
                    self.explored_keys.add((ix, iy))

    def _build_unknown_grid(self) -> List[Point3]:
        points: List[Point3] = []
        step = 1.5
        x = self.bounds["min_x"]
        while x <= self.bounds["max_x"]:
            y = self.bounds["min_y"]
            while y <= self.bounds["max_y"]:
                points.append((x, y, 0.03))
                y += step
            x += step
        return points

    def _marker(self, ns: str, mid: int, marker_type: int) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = ns
        marker.id = mid
        marker.type = marker_type
        marker.action = Marker.ADD
        marker.lifetime.sec = 3
        marker.lifetime.nanosec = 0
        marker.pose.orientation.w = 1.0
        return marker

    @staticmethod
    def _color(marker: Marker, r: float, g: float, b: float, a: float = 1.0) -> Marker:
        marker.color.r = r
        marker.color.g = g
        marker.color.b = b
        marker.color.a = a
        return marker

    @staticmethod
    def _point(x: float, y: float, z: float) -> Point:
        p = Point()
        p.x = float(x)
        p.y = float(y)
        p.z = float(z)
        return p

    def _text(self, ns: str, mid: int, text: str, xyz: Point3, size: float = 0.55) -> Marker:
        marker = self._marker(ns, mid, Marker.TEXT_VIEW_FACING)
        marker.text = text
        marker.pose.position = self._point(xyz[0], xyz[1], xyz[2])
        marker.scale.z = size
        return self._color(marker, 1.0, 1.0, 1.0, 1.0)

    def _sphere(self, ns: str, mid: int, xyz: Point3, scale: float, color: Tuple[float, float, float, float]) -> Marker:
        marker = self._marker(ns, mid, Marker.SPHERE)
        marker.pose.position = self._point(*xyz)
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        return self._color(marker, *color)

    def _arrow(self, ns: str, mid: int, start: Point3, end: Point3, color: Tuple[float, float, float, float]) -> Marker:
        marker = self._marker(ns, mid, Marker.ARROW)
        marker.points = [self._point(*start), self._point(*end)]
        marker.scale.x = 0.18
        marker.scale.y = 0.38
        marker.scale.z = 0.45
        return self._color(marker, *color)

    def _line(self, ns: str, mid: int, points: Sequence[Point3], width: float, color: Tuple[float, float, float, float]) -> Marker:
        marker = self._marker(ns, mid, Marker.LINE_STRIP)
        marker.scale.x = width
        marker.points = [self._point(*p) for p in points]
        return self._color(marker, *color)

    def _points(self, ns: str, mid: int, points: Sequence[Point3], size: float, color: Tuple[float, float, float, float]) -> Marker:
        marker = self._marker(ns, mid, Marker.POINTS)
        marker.scale.x = size
        marker.scale.y = size
        marker.points = [self._point(*p) for p in points[:2500]]
        return self._color(marker, *color)

    def _cube_list(self, ns: str, mid: int, points: Sequence[Point3], scale: float, color: Tuple[float, float, float, float]) -> Marker:
        marker = self._marker(ns, mid, Marker.CUBE_LIST)
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = 0.04
        marker.points = [self._point(*p) for p in points[:3000]]
        return self._color(marker, *color)

    @staticmethod
    def _path_points(path: Optional[Path]) -> List[Point3]:
        if path is None:
            return []
        return [(float(p.pose.position.x), float(p.pose.position.y), float(p.pose.position.z)) for p in path.poses]

    @staticmethod
    def _pose_xyz(pose: Optional[PoseStamped]) -> Optional[Point3]:
        if pose is None:
            return None
        p = pose.pose.position
        return (float(p.x), float(p.y), float(p.z))

    def _boundary(self) -> Marker:
        z = 0.05
        min_x, max_x = self.bounds["min_x"], self.bounds["max_x"]
        min_y, max_y = self.bounds["min_y"], self.bounds["max_y"]
        points = [(min_x, min_y, z), (max_x, min_y, z), (max_x, max_y, z), (min_x, max_y, z), (min_x, min_y, z)]
        return self._line("map_boundary", 1, points, 0.16, (1.0, 1.0, 1.0, 0.95))

    def _legend(self) -> MarkerArray:
        array = MarkerArray()
        x = self.bounds["min_x"] + 1.0
        y = self.bounds["max_y"] - 1.0
        z = 2.2
        if self.clean_profile:
            labels = [
                "Clean Acceptance",
                "Yellow = Active Executed Path",
                "Orange line = Executed Trail",
                "Purple = Goal",
                "Cyan = Best View",
                "Yellow dots = Frontier",
            ]
        else:
            labels = [
            "Unknown = dark gray/purple",
            "Explored = translucent green/blue",
            "Frontier Boundary = bright yellow",
            "UAV = orange",
            "Trail = orange/red",
            "Goal = purple",
            "Best View = cyan",
            "Global Path = green",
            "Local Traj = blue",
            "Managed Traj = yellow",
            "Obstacle = red",
            "Frontier = yellow",
            "Free = light blue",
            ]
        for i, label in enumerate(labels):
            array.markers.append(self._text("legend", 100 + i, label, (x, y, z - i * 0.7), 0.58))
        return array

    def _unknown_area_marker(self) -> Marker:
        unknown = [p for p in self.unknown_grid if self._grid_key(p) not in self.explored_keys]
        return self._cube_list("unknown_area", 200, unknown, 0.38, (0.18, 0.16, 0.26, 0.22))

    def _explored_area_marker(self) -> Marker:
        explored = [self._grid_center(key, 0.75, 0.06) for key in sorted(self.explored_keys)]
        return self._cube_list("explored_area", 201, explored, 0.34, (0.35, 0.95, 0.78, 0.34))

    def _goal_history_markers(self) -> MarkerArray:
        array = MarkerArray()
        if self.goal_history:
            array.markers.append(self._points("goal_history", 220, self.goal_history, 0.25, (0.72, 0.0, 1.0, 0.58)))
            recent = list(reversed(self.goal_history[-3:]))
            for i, point in enumerate(recent, 1):
                array.markers.append(self._text("goal_history", 220 + i, f"G-{i}", (point[0], point[1], point[2] + 0.75), 0.48))
        return array

    def _status_panel(self) -> MarkerArray:
        array = MarkerArray()
        x = self.bounds["max_x"] - 7.5
        y = self.bounds["max_y"] - 1.0
        z = 3.2
        coverage = min(1.0, len(self.explored_keys) / float(self.total_unknown_cells))
        goal_age = (self.get_clock().now() - self.last_goal_time).nanoseconds / 1e9
        tracking_line = f"Tracking: {self.tracking_consistency}"
        if self.tracking_consistency == "BAD":
            tracking_line = "TRACKING BAD: UAV not following displayed path"
        if self.clean_profile:
            lines = [
                "P11-lite Clean Acceptance",
                f"ENV: {self.environment_mode}",
                f"Active path source: {self.active_path_source}",
                f"Planned points: {self.planned_path_points}",
                f"Tracking avg/max: {self.average_tracking_error:.2f}/{self.max_tracking_error:.2f} m",
                tracking_line,
                f"Trail: {self.uav_distance:.2f} m",
                f"Path valid: {str(self.path_valid).lower()}",
                f"Wall risk: {self.wall_crossing_risk}",
                "Real flight command: false",
            ]
        else:
            lines = [
                "P11-lite Exploration Demo",
            f"ENV: {self.environment_mode}",
            f"Active execution source: {self.active_path_source}",
            f"Planned path points: {self.planned_path_points}",
            f"Executed trail length: {self.uav_distance:.2f} m",
            f"Tracking error: {self.average_tracking_error:.2f} m",
            tracking_line,
            f"Coverage: {coverage:.3f}",
            f"Distance: {self.uav_distance:.2f} m",
            f"Goal switches: {self.goal_switch_count}",
            f"Goal age: {goal_age:.1f} s",
            f"Frontiers: {len(self.frontiers)}",
            f"Path valid: {str(self.path_valid).lower()}",
            f"Reject reason: {self.reject_reason}",
            f"Wall risk: {self.wall_crossing_risk}",
            "Real flight command: false",
            ]
        for i, line in enumerate(lines):
            array.markers.append(self._text("exploration_status_panel", 300 + i, line, (x, y, z - i * 0.48), 0.38 if i else 0.52))
        return array

    def _direction_arrows(self, points: Sequence[Point3]) -> MarkerArray:
        array = MarkerArray()
        if len(points) < 2:
            return array
        step = max(1, len(points) // 4)
        marker_id = 330
        for idx in range(0, len(points) - 1, step):
            start = points[idx]
            end = points[min(idx + 1, len(points) - 1)]
            if math.dist(start, end) < 0.05:
                continue
            array.markers.append(self._arrow("managed_path_direction_arrows", marker_id, start, end, (1.0, 0.9, 0.0, 1.0)))
            marker_id += 1
        return array

    def _active_path(self) -> Tuple[str, List[Point3]]:
        source = self._normalize_source(self.active_path_source)
        active = self._path_points(self.active_execution_path)
        if active:
            return source if source != "unknown" else "managed_trajectory", active
        if source == "managed_trajectory":
            return source, self._path_points(self.managed_trajectory)
        if source == "local_trajectory":
            return source, self._path_points(self.local_trajectory)
        if source == "global_path":
            return source, self._path_points(self.global_path)
        managed = self._path_points(self.managed_trajectory)
        if managed:
            return "managed_trajectory", managed
        local = self._path_points(self.local_trajectory)
        if local:
            return "local_trajectory", local
        return "global_path", self._path_points(self.global_path)

    def _update_tracking_view(self, path: Sequence[Point3]) -> None:
        self.planned_path_points = len(path)
        if self.odom is None or len(path) < 2:
            self.average_tracking_error = -1.0
            self.max_tracking_error = -1.0
            self.tracking_consistency = "UNKNOWN"
            return
        op = self.odom.pose.pose.position
        odom_xyz = (float(op.x), float(op.y), float(op.z))
        distances = [math.dist(odom_xyz, p) for p in path]
        self.average_tracking_error = min(distances) if distances else -1.0
        self.max_tracking_error = max(distances) if distances else -1.0
        if self.average_tracking_error < 0.0:
            self.tracking_consistency = "UNKNOWN"
        elif self.average_tracking_error <= 1.0 and self.max_tracking_error <= 3.0:
            self.tracking_consistency = "GOOD"
        elif self.average_tracking_error <= 3.0:
            self.tracking_consistency = "PARTIAL"
        else:
            self.tracking_consistency = "BAD"

    def _publish(self) -> None:
        all_markers = MarkerArray()
        path_markers = MarkerArray()
        frontier_markers = MarkerArray()
        if not self.clean_profile:
            semantic_markers = [
                self._unknown_area_marker(),
                self._explored_area_marker(),
            ]
            all_markers.markers.extend(semantic_markers)

        if self.odom is not None:
            p = self.odom.pose.pose.position
            uav_xyz = (float(p.x), float(p.y), float(p.z))
            heading = self.odom.pose.pose.orientation
            yaw = math.atan2(
                2.0 * (heading.w * heading.z + heading.x * heading.y),
                1.0 - 2.0 * (heading.y * heading.y + heading.z * heading.z),
            )
            arrow_end = (uav_xyz[0] + math.cos(yaw) * 1.5, uav_xyz[1] + math.sin(yaw) * 1.5, uav_xyz[2])
            uav = self._sphere("uav_body", 1, uav_xyz, 1.1, (1.0, 0.12, 0.0, 1.0))
            uav_arrow = self._arrow("uav_body", 2, uav_xyz, arrow_end, (1.0, 0.35, 0.0, 1.0))
            label = self._text("uav_label", 3, "UAV", (uav_xyz[0], uav_xyz[1], uav_xyz[2] + 1.25), 0.9)
            trail_width = 0.10 if self.clean_profile else 0.24
            trail = self._line("uav_trail", 4, self.trail, trail_width, (1.0, 0.22, 0.0, 0.95))
            self.uav_pub.publish(uav)
            self.trail_pub.publish(trail)
            all_markers.markers.extend([uav, uav_arrow, label, trail])

        goal_xyz = self._pose_xyz(self.exploration_goal)
        if goal_xyz is not None:
            goal = self._sphere("current_goal", 10, goal_xyz, 1.05, (0.75, 0.0, 1.0, 1.0))
            goal_label = self._text("current_goal_label", 11, "GOAL", (goal_xyz[0], goal_xyz[1], goal_xyz[2] + 1.15), 0.82)
            self.goal_pub.publish(goal)
            all_markers.markers.extend([goal, goal_label])
            if self.odom is not None:
                p = self.odom.pose.pose.position
                uav_xyz = (float(p.x), float(p.y), float(p.z))
                line = self._line("uav_to_goal_line", 12, [uav_xyz, goal_xyz], 0.12, (0.78, 0.0, 1.0, 0.92))
                line_label = self._text("uav_to_goal_line", 13, "Selected Goal Direction", ((uav_xyz[0] + goal_xyz[0]) * 0.5, (uav_xyz[1] + goal_xyz[1]) * 0.5, max(uav_xyz[2], goal_xyz[2]) + 0.65), 0.46)
                all_markers.markers.extend([line, line_label])

        best_xyz = self._pose_xyz(self.best_viewpoint)
        if best_xyz is not None:
            best = self._sphere("best_viewpoint", 20, best_xyz, 0.75, (0.0, 1.0, 1.0, 1.0))
            best_arrow = self._arrow("best_viewpoint", 21, (best_xyz[0], best_xyz[1], best_xyz[2] + 0.2), (best_xyz[0], best_xyz[1], best_xyz[2] + 1.4), (0.0, 1.0, 1.0, 1.0))
            best_label = self._text("best_viewpoint_label", 22, "BEST VIEW", (best_xyz[0], best_xyz[1], best_xyz[2] + 1.55), 0.68)
            self.best_pub.publish(best)
            all_markers.markers.extend([best, best_arrow, best_label])

        if self.clean_profile:
            active_source, active_path = self._active_path()
            path_specs = [("active_executed_path", 32, active_path, 0.22, (1.0, 0.85, 0.0, 1.0))]
            self.active_path_source = active_source
        else:
            path_specs = [
                ("global_path", 30, self._path_points(self.global_path), 0.18, (0.0, 1.0, 0.18, 1.0)),
                ("local_trajectory", 31, self._path_points(self.local_trajectory), 0.22, (0.05, 0.35, 1.0, 1.0)),
                ("planned_path_managed_trajectory", 32, self._path_points(self.managed_trajectory), 0.30, (1.0, 0.85, 0.0, 1.0)),
            ]
        for ns, mid, path, width, color in path_specs:
            if len(path) >= 2:
                if ns in ("planned_path_managed_trajectory", "active_executed_path"):
                    self._update_tracking_view(path)
                marker = self._line(ns, mid, path, width, color)
                path_markers.markers.append(marker)
                all_markers.markers.append(marker)
                if ns in ("planned_path_managed_trajectory", "active_executed_path"):
                    arrows = self._direction_arrows(path)
                    path_markers.markers.extend(arrows.markers)
                    all_markers.markers.extend(arrows.markers)
        self.path_pub.publish(path_markers)

        if self.frontiers:
            frontier_points = self.frontiers[:350] if self.clean_profile else self.frontiers
            frontier = self._points("frontier_candidates", 40, frontier_points, 0.34, (1.0, 1.0, 0.0, 0.55 if self.clean_profile else 1.0))
            frontier_boundary = self._points("frontier_boundary", 43, frontier_points, 0.28 if self.clean_profile else 0.46, (1.0, 0.95, 0.0, 0.70))
            if not self.clean_profile:
                frontier_markers.markers.append(frontier)
            frontier_markers.markers.append(frontier_boundary)
            all_markers.markers.append(frontier_boundary)
            if not self.clean_profile:
                all_markers.markers.append(frontier)
            if self.frontiers:
                fx, fy, fz = self.frontiers[0]
                all_markers.markers.append(self._text("frontier_boundary", 44, "FRONTIER", (fx, fy, fz + 0.75), 0.5))
        if self.occupied and not self.clean_profile:
            all_markers.markers.append(self._points("occupied_obstacles", 41, self.occupied, 0.28, (1.0, 0.0, 0.0, 0.95)))
        if self.complex_occupied and not self.clean_profile:
            all_markers.markers.append(self._points("complex_obstacle_points", 45, self.complex_occupied, 0.18, (0.92, 0.08, 0.04, 0.72)))
        if self.complex_wall_markers.markers:
            all_markers.markers.extend(self.complex_wall_markers.markers[:120])
        if self.complex_map_boundary is not None:
            self.complex_map_boundary.header.stamp = self.get_clock().now().to_msg()
            all_markers.markers.append(self.complex_map_boundary)
        if self.free and not self.clean_profile:
            all_markers.markers.append(self._points("free_space", 42, self.free, 0.14, (0.45, 0.82, 1.0, 0.55)))
        self.frontier_pub.publish(frontier_markers)

        boundary = self._boundary()
        legend = self._legend()
        goal_history = MarkerArray() if self.clean_profile else self._goal_history_markers()
        status_panel = self._status_panel()
        self.boundary_pub.publish(boundary)
        self.legend_pub.publish(legend)
        all_markers.markers.extend(goal_history.markers)
        all_markers.markers.append(boundary)
        all_markers.markers.extend(legend.markers)
        all_markers.markers.extend(status_panel.markers)
        self.all_pub.publish(all_markers)
        self.get_logger().info(
            "P11_LITE_VISUAL_MARKER_STATUS "
            f"visual_profile={self.visual_profile} large_overlay_disabled={str(self.large_overlay_disabled).lower()} "
            f"active_path_only={str(self.active_path_only).lower()} executed_trail_line_only=true "
            f"sensor_fan_disabled={str(self.sensor_fan_disabled).lower()} large_orange_overlay_present=NO "
            "clean_profile_overlay_namespaces_disabled="
            f"{','.join(self.clean_profile_overlay_namespaces_disabled)} "
            "marker_deleteall_used=false stable_marker_ids=true "
            f"static_marker_publish_rate_hz={self.static_marker_publish_rate_hz:.1f} "
            f"dynamic_marker_publish_rate_hz={self.dynamic_marker_publish_rate_hz:.1f} "
            "REAL_FLIGHT_COMMAND=false",
            throttle_duration_sec=5.0,
        )


def main(args=None):
    rclpy.init(args=args)
    node = P11LiteVisualMarkers()
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
