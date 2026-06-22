#!/usr/bin/env python3
import math
from typing import Optional

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

from p11_lite_collision_utils import OccupancyGrid2D, astar_detour_path
from p11_lite_utils import astar_path, densify, make_path, path_collision_free, world_config_path
from p11_lite_utils import parse_bounds, read_cloud
from world_collision_checker import load_obstacles


class P11LiteGoalToPathBridge(Node):
    def __init__(self):
        super().__init__("p11_lite_goal_to_path_bridge")
        self.world_config = world_config_path(str(self.declare_parameter("world_config", "").value))
        self.environment_mode = str(self.declare_parameter("environment_mode", "simple").value)
        self.grid_resolution = float(self.declare_parameter("grid_resolution", 0.5).value)
        self.complex_grid_resolution = float(self.declare_parameter("complex_grid_resolution", 0.25).value)
        self.clearance = float(self.declare_parameter("clearance", 0.35).value)
        self.inflation_radius = float(self.declare_parameter("inflation_radius", 0.45).value)
        self.min_path_goal_distance = float(self.declare_parameter("min_path_goal_distance", 1.0).value)
        self.anti_backtrack_angle_deg = float(self.declare_parameter("anti_backtrack_angle_deg", 140.0).value)
        self.recent_path_memory_sec = float(self.declare_parameter("recent_path_memory_sec", 30.0).value)
        self.short_low_gain_path_length = float(self.declare_parameter("short_low_gain_path_length", 2.5).value)
        self.low_expected_gain_threshold = float(self.declare_parameter("low_expected_gain_threshold", 0.25).value)
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.obstacles = load_obstacles(self.world_config)
        self.bounds = parse_bounds(self.world_config)
        self.complex_occupied_points = []
        self.complex_grid = OccupancyGrid2D(self.bounds, self.complex_grid_resolution, self.inflation_radius)
        self.complex_env_received = False
        self.odom: Optional[Odometry] = None
        self.goal: Optional[PoseStamped] = None
        self.last_goal_key = None
        self.goal_received_sec = -999.0
        self.goal_request_count = 0
        self.goal_to_path_timeout_sec = float(self.declare_parameter("goal_to_path_timeout_sec", 15.0).value)
        self.last_rejected_goal_key = None
        self.path_publish_count = 0
        self.path_fail_count = 0
        self.last_reason = "waiting"
        self.last_path_points = 0
        self.last_path_valid = False
        self.last_valid_path_points = 0
        self.last_valid_goal_key = None
        self.last_empty_path_publish_sec = -999.0
        self.empty_path_publish_count = 0
        self.endpoint_to_goal_distance = -1.0
        self.path_feasible = False
        self.last_success_planner_mode = "waiting"
        self.last_close_reject_key = None
        self.last_close_reject_sec = -999.0
        self.close_goal_ignore_sec = float(self.declare_parameter("close_goal_ignore_sec", 5.0).value)
        self.path_planner_mode = "waiting"
        self.straight_path_collision = False
        self.astar_used = False
        self.astar_success = False
        self.fallback_used = False
        self.fallback_success = False
        self.final_path_collision_free = False
        self.path_collision_free = False
        self.min_clearance = -1.0
        self.first_collision_point = "NONE"
        self.collision_segment_index = -1
        self.odom_trail = []
        self.last_motion_direction = None
        self.backtrack_reject_count = 0
        self.short_low_gain_path_reject_count = 0
        self.path_direction_flip_count = 0
        self.path_expected_gain = 0.0
        self.latest_goal_information_gain = 1.0
        self.latest_goal_boundary_distance = 999.0
        self.boundary_path_reject_count = 0
        self.boundary_follow_reject_count = 0
        self.boundary_follow_ratio = 0.0
        self.boundary_goal_count = 0
        self.selected_goal_boundary_distance = 999.0
        self.boundary_penalty = 0.0

        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self._goal_cb, 10)
        self.create_subscription(Odometry, "/odom", self._odom_cb, 20)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/complex_env/occupied_points", self._complex_occupied_cb, 10)
        self.create_subscription(String, "/fuel/p11_lite/frontier_status", self._frontier_status_cb, 10)
        self.managed_pub = self.create_publisher(Path, "/fuel/plan_manager/managed_trajectory", 10)
        self.local_pub = self.create_publisher(Path, "/fuel/local_trajectory", 10)
        self.global_pub = self.create_publisher(Path, "/fuel/global_path", 10)
        self.status_pub = self.create_publisher(String, "/fuel/p11_lite/goal_to_path_status", 10)
        self.timer = self.create_timer(1.0, self._tick)
        self.get_logger().info("P11_LITE_GOAL_TO_PATH_BRIDGE_READY REAL_FLIGHT_COMMAND=false")

    def _publish_empty_paths(self, reason: str) -> None:
        now = self.get_clock().now().nanoseconds / 1e9
        if now - self.last_empty_path_publish_sec < 0.5:
            return
        empty = Path()
        empty.header.frame_id = self.frame_id
        empty.header.stamp = self.get_clock().now().to_msg()
        self.global_pub.publish(empty)
        self.local_pub.publish(empty)
        self.managed_pub.publish(empty)
        self.last_empty_path_publish_sec = now
        self.empty_path_publish_count += 1
        self.get_logger().info(
            f"P11_LITE_EMPTY_PATH_PUBLISHED reason={reason} empty_path_publish_count={self.empty_path_publish_count} "
            "REAL_FLIGHT_COMMAND=false"
        )

    def _odom_cb(self, msg: Odometry) -> None:
        if self.odom is not None:
            prev = self.odom.pose.pose.position
            cur = msg.pose.pose.position
            dx, dy = float(cur.x) - float(prev.x), float(cur.y) - float(prev.y)
            norm = math.hypot(dx, dy)
            if norm > 0.05:
                new_dir = (dx / norm, dy / norm)
                if self.last_motion_direction is not None:
                    dot = max(-1.0, min(1.0, new_dir[0] * self.last_motion_direction[0] + new_dir[1] * self.last_motion_direction[1]))
                    if math.degrees(math.acos(dot)) > self.anti_backtrack_angle_deg:
                        self.path_direction_flip_count += 1
                self.last_motion_direction = new_dir
        self.odom = msg
        p = msg.pose.pose.position
        now = self.get_clock().now().nanoseconds / 1e9
        if not self.odom_trail or math.dist(self.odom_trail[-1][:3], (float(p.x), float(p.y), float(p.z))) > 0.2:
            self.odom_trail.append((float(p.x), float(p.y), float(p.z), now))
            self.odom_trail = [q for q in self.odom_trail if now - q[3] <= self.recent_path_memory_sec][-120:]

    def _complex_occupied_cb(self, msg: PointCloud2) -> None:
        self.complex_occupied_points = read_cloud(msg)
        self.complex_grid = OccupancyGrid2D(self.bounds, self.complex_grid_resolution, self.inflation_radius)
        self.complex_grid.update_from_points(self.complex_occupied_points)
        self.complex_env_received = True

    @staticmethod
    def _field(data: str, key: str, default: str = "UNKNOWN") -> str:
        token = f"{key}="
        for part in data.split():
            if part.startswith(token):
                return part[len(token):]
        return default

    def _frontier_status_cb(self, msg: String) -> None:
        value = self._field(msg.data, "selected_goal_information_gain", self._field(msg.data, "information_gain", "1.0"))
        try:
            self.latest_goal_information_gain = float(value)
        except ValueError:
            self.latest_goal_information_gain = 1.0
        try:
            self.latest_goal_boundary_distance = float(self._field(msg.data, "selected_goal_boundary_distance", str(self.latest_goal_boundary_distance)))
        except ValueError:
            pass
        try:
            self.boundary_follow_ratio = float(self._field(msg.data, "boundary_follow_ratio", str(self.boundary_follow_ratio)))
        except ValueError:
            pass
        try:
            self.boundary_goal_count = int(float(self._field(msg.data, "boundary_goal_count", str(self.boundary_goal_count))))
        except ValueError:
            pass
        try:
            self.boundary_penalty = float(self._field(msg.data, "boundary_penalty", str(self.boundary_penalty)))
        except ValueError:
            pass

    def _path_length(self, points) -> float:
        if len(points) < 2:
            return 0.0
        return sum(math.dist(a, b) for a, b in zip(points, points[1:]))

    def _anti_backtrack_reject(self, points) -> Optional[str]:
        if len(points) < 2 or self.last_motion_direction is None:
            return None
        start, nxt = points[0], points[1]
        dx, dy = nxt[0] - start[0], nxt[1] - start[1]
        norm = math.hypot(dx, dy)
        if norm <= 1e-6:
            return None
        path_dir = (dx / norm, dy / norm)
        dot = max(-1.0, min(1.0, path_dir[0] * self.last_motion_direction[0] + path_dir[1] * self.last_motion_direction[1]))
        angle = math.degrees(math.acos(dot))
        path_len = self._path_length(points)
        self.path_expected_gain = self.latest_goal_information_gain
        low_gain = self.path_expected_gain < self.low_expected_gain_threshold
        self.selected_goal_boundary_distance = self.latest_goal_boundary_distance
        if self.latest_goal_boundary_distance < 1.0 and low_gain and path_len > 4.0:
            self.boundary_path_reject_count += 1
            self.boundary_follow_reject_count += 1
            return "boundary_follow_low_gain_path"
        if angle > self.anti_backtrack_angle_deg and low_gain:
            self.backtrack_reject_count += 1
            return "anti_backtrack_low_gain"
        if path_len < self.short_low_gain_path_length and low_gain:
            self.short_low_gain_path_reject_count += 1
            return "short_low_gain_path"
        if low_gain and self.odom_trail:
            near_recent = sum(1 for px, py, _pz, _t in self.odom_trail if any(math.hypot(px - q[0], py - q[1]) < 1.0 for q in points[: min(4, len(points))]))
            if near_recent >= 3:
                self.backtrack_reject_count += 1
                return "recent_trail_low_gain"
        return None

    def _goal_cb(self, msg: PoseStamped) -> None:
        new_goal_key = None
        if self.odom is not None:
            op = self.odom.pose.pose.position
            gp = msg.pose.position
            goal_key = (round(float(gp.x), 1), round(float(gp.y), 1), round(float(gp.z), 1))
            new_goal_key = goal_key
            now = self.get_clock().now().nanoseconds / 1e9
            if (
                goal_key == self.last_close_reject_key
                and now - self.last_close_reject_sec < self.close_goal_ignore_sec
                and math.dist((float(op.x), float(op.y), float(op.z)), (float(gp.x), float(gp.y), float(gp.z))) < self.min_path_goal_distance
            ):
                return
        if new_goal_key is None:
            gp = msg.pose.position
            new_goal_key = (round(float(gp.x), 1), round(float(gp.y), 1), round(float(gp.z), 1))
        if self.last_goal_key is not None and new_goal_key != self.last_goal_key:
            self._publish_empty_paths("goal_changed_clear_previous_path")
            self.last_valid_goal_key = None
            self.last_valid_path_points = 0
        if new_goal_key != self.last_goal_key:
            self.goal_received_sec = self.get_clock().now().nanoseconds / 1e9
            self.goal_request_count += 1
        self.last_goal_key = new_goal_key
        self.goal = msg

    def _goal_key(self):
        if self.goal is None:
            return None
        p = self.goal.pose.position
        return (round(float(p.x), 1), round(float(p.y), 1), round(float(p.z), 1))

    def _tick(self) -> None:
        points = []
        executable = False
        reject_reason = "none"
        request_reselect = False
        clear_close_goal_after_status = False
        goal_distance = -1.0
        self.path_planner_mode = "waiting"
        self.straight_path_collision = False
        self.astar_used = False
        self.astar_success = False
        self.fallback_used = False
        self.fallback_success = False
        self.final_path_collision_free = False
        self.path_collision_free = False
        self.min_clearance = -1.0
        self.first_collision_point = "NONE"
        self.collision_segment_index = -1
        self.path_expected_gain = self.latest_goal_information_gain
        self.endpoint_to_goal_distance = -1.0
        self.path_feasible = False
        if self.odom is None or self.goal is None:
            self.last_reason = "waiting_for_odom_or_goal"
            reject_reason = self.last_reason
        else:
            op = self.odom.pose.pose.position
            gp = self.goal.pose.position
            start = (float(op.x), float(op.y), float(op.z))
            goal = (float(gp.x), float(gp.y), float(gp.z))
            goal_key = self._goal_key()
            goal_distance = math.dist(start, goal)
            if goal_distance < self.min_path_goal_distance:
                request_reselect = True
                now = self.get_clock().now().nanoseconds / 1e9
                if goal_key != self.last_close_reject_key:
                    self.last_reason = "goal_too_close"
                    if not executable:
                        reject_reason = self.last_reason
                    self.last_close_reject_key = goal_key
                    self.last_close_reject_sec = now
                    clear_close_goal_after_status = True
                else:
                    self.last_reason = "waiting_for_reselect"
                    if not executable:
                        reject_reason = "waiting_for_reselect"
                    clear_close_goal_after_status = True
            else:
                straight = densify([start, goal], max(0.15, min(0.5, math.dist(start, goal) / 4.0)))
                if self.environment_mode == "complex" and self.complex_env_received:
                    straight_result = self.complex_grid.check_path(straight)
                    self.straight_path_collision = not straight_result.collision_free
                    self.min_clearance = straight_result.min_clearance
                    self.first_collision_point = (
                        "NONE"
                        if straight_result.first_collision_point is None
                        else f"({straight_result.first_collision_point[0]:.3f},{straight_result.first_collision_point[1]:.3f},{straight_result.first_collision_point[2]:.3f})"
                    )
                    self.collision_segment_index = straight_result.collision_segment_index
                    if len(straight) >= 5 and straight_result.collision_free:
                        points = straight
                        self.path_planner_mode = "straight"
                        self.last_reason = "STRAIGHT_PATH_READY"
                    else:
                        self.astar_used = True
                        points = astar_detour_path(start, goal, self.complex_grid) or []
                        self.astar_success = len(points) >= 5 and self.complex_grid.check_path(points).collision_free
                        self.path_planner_mode = "astar" if self.astar_success else "failed"
                        self.last_reason = "ASTAR_PATH_READY" if self.astar_success else "no_collision_free_grid_path"
                    if points:
                        final_result = self.complex_grid.check_path(points)
                        self.path_collision_free = final_result.collision_free
                        self.min_clearance = final_result.min_clearance
                        self.collision_segment_index = final_result.collision_segment_index
                        self.first_collision_point = (
                            "NONE"
                            if final_result.first_collision_point is None
                            else f"({final_result.first_collision_point[0]:.3f},{final_result.first_collision_point[1]:.3f},{final_result.first_collision_point[2]:.3f})"
                        )
                elif len(straight) >= 5 and path_collision_free(straight, self.obstacles, self.clearance):
                    points = straight
                    self.path_planner_mode = "straight"
                    self.path_collision_free = True
                    self.last_reason = "STRAIGHT_PATH_READY"
                else:
                    points = astar_path(start, goal, self.world_config, self.grid_resolution, self.clearance) or []
                    self.astar_used = True
                    self.astar_success = bool(points)
                    self.path_planner_mode = "astar" if points else "failed"
                    self.path_collision_free = bool(points)
                    self.last_reason = "ASTAR_PATH_READY" if points else "no_collision_free_grid_path"
                anti_reason = self._anti_backtrack_reject(points) if points else None
                if anti_reason is not None:
                    request_reselect = True
                    points = []
                    self.path_collision_free = False
                    self.path_planner_mode = "failed"
                    self.last_reason = anti_reason
                executable = len(points) >= 5 and (self.path_collision_free or self.environment_mode != "complex")
                if executable:
                    if points:
                        self.endpoint_to_goal_distance = math.dist(points[-1], goal)
                        self.path_feasible = self.endpoint_to_goal_distance <= 1.5
                        if not self.path_feasible:
                            request_reselect = True
                            executable = False
                            self.path_collision_free = False
                            self.final_path_collision_free = False
                            self.path_planner_mode = "failed"
                            self.last_reason = "path_endpoint_far_from_goal"
                            reject_reason = self.last_reason
                    if executable and points:
                        path = make_path(points, self.frame_id)
                        path.header.stamp = self.get_clock().now().to_msg()
                        self.global_pub.publish(path)
                        self.local_pub.publish(path)
                        self.managed_pub.publish(path)
                        self.path_publish_count += 1
                        self.last_rejected_goal_key = None
                        self.last_valid_path_points = len(points)
                        self.last_valid_goal_key = goal_key
                        self.last_success_planner_mode = self.path_planner_mode
                        self.final_path_collision_free = self.path_collision_free
                else:
                    reject_reason = self.last_reason
                    if goal_key != self.last_rejected_goal_key:
                        self.path_fail_count += 1
                        self.last_rejected_goal_key = goal_key
        if not executable and request_reselect:
            self._publish_empty_paths(reject_reason)
        self.last_path_points = len(points)
        self.last_path_valid = executable
        now = self.get_clock().now().nanoseconds / 1e9
        wait_sec = 0.0 if self.goal_received_sec < 0.0 else max(0.0, now - self.goal_received_sec)
        goal_key_text = self._goal_key()
        goal_id = self.goal_request_count
        if self.goal is None:
            status_event = "GOAL_TO_PATH_WAITING"
        elif executable:
            status_event = "GOAL_TO_PATH_SUCCESS"
        elif wait_sec >= self.goal_to_path_timeout_sec:
            status_event = "GOAL_TO_PATH_TIMEOUT"
        elif request_reselect:
            status_event = "GOAL_TO_PATH_FAIL"
        else:
            status_event = "GOAL_TO_PATH_WAITING"
        status = String()
        status.data = (
            "REAL_FLIGHT_COMMAND=false "
            f"status_event={status_event} "
            f"goal_id={goal_id} "
            f"wait_sec={wait_sec:.3f} "
            f"GOAL_TO_PATH_REQUEST goal_id={goal_id} goal_key={goal_key_text} "
            f"{status_event} goal_id={goal_id} path_len={self._path_length(points):.3f} endpoint_dist={self.endpoint_to_goal_distance:.3f} reason={reject_reason if not executable else 'none'} "
            f"environment_mode={self.environment_mode} "
            f"path_planner_mode={self.path_planner_mode} "
            f"straight_path_collision={'true' if self.straight_path_collision else 'false'} "
            f"astar_used={'true' if self.astar_used else 'false'} "
            f"astar_success={'true' if self.astar_success else 'false'} "
            f"fallback_used={'true' if self.fallback_used else 'false'} "
            f"fallback_success={'true' if self.fallback_success else 'false'} "
            f"final_path_collision_free={'true' if self.final_path_collision_free or self.path_collision_free else 'false'} "
            f"path_collision_free={'true' if self.path_collision_free else 'false'} "
            f"min_clearance={self.min_clearance:.3f} "
            f"first_collision_point={self.first_collision_point} "
            f"collision_segment_index={self.collision_segment_index} "
            f"backtrack_reject_count={self.backtrack_reject_count} "
            f"short_low_gain_path_reject_count={self.short_low_gain_path_reject_count} "
            f"path_direction_flip_count={self.path_direction_flip_count} "
            f"path_expected_gain={self.path_expected_gain:.3f} "
            f"boundary_path_reject_count={self.boundary_path_reject_count} "
            f"boundary_follow_reject_count={self.boundary_follow_reject_count} "
            f"boundary_follow_ratio={self.boundary_follow_ratio:.3f} "
            f"boundary_goal_count={self.boundary_goal_count} "
            f"selected_goal_boundary_distance={self.selected_goal_boundary_distance:.3f} "
            f"boundary_penalty={self.boundary_penalty:.3f} "
            f"inflation_radius={self.inflation_radius:.3f} "
            f"grid_resolution={self.complex_grid_resolution if self.environment_mode == 'complex' else self.grid_resolution:.3f} "
            f"goal_key={goal_key_text} "
            f"goal_distance={goal_distance:.3f} "
            f"endpoint_to_goal_distance={self.endpoint_to_goal_distance:.3f} "
            f"path_feasible={'true' if self.path_feasible else 'false'} "
            f"managed_path_points={len(points)} "
            f"last_valid_path_points={self.last_valid_path_points} "
            f"last_valid_goal_key={self.last_valid_goal_key} "
            f"empty_path_publish_count={self.empty_path_publish_count} "
            f"clear_stale_path={'true' if (not executable and request_reselect) else 'false'} "
            f"path_valid={'true' if executable else 'false'} "
            f"reject_reason={reject_reason if not executable else 'none'} "
            f"request_reselect={'true' if request_reselect else 'false'} "
            f"executable_path_collision_free={'true' if executable else 'false'} "
            f"path_publish_count={self.path_publish_count} "
            f"path_fail_count={self.path_fail_count} "
            f"reason={self.last_reason}"
        )
        self.status_pub.publish(status)
        if clear_close_goal_after_status:
            self.goal = None


def main(args=None):
    rclpy.init(args=args)
    node = P11LiteGoalToPathBridge()
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
