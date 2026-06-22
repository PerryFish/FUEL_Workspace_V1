#!/usr/bin/env python3
import math
from dataclasses import dataclass
from typing import Dict, Optional

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


@dataclass
class PathState:
    source: str
    msg: Path
    stamp_sec: float


class FuelRos2TrajServerLite(Node):
    def __init__(self):
        super().__init__("fuel_ros2_traj_server_lite")
        self.loop_trajectory = bool(self.declare_parameter("loop_trajectory", False).value)
        self.command_rate = max(0.5, float(self.declare_parameter("command_rate", 10.0).value))
        self.target_step_period = max(0.2, float(self.declare_parameter("target_step_period", 1.0).value))
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.initial_x = float(self.declare_parameter("initial_x", 0.0).value)
        self.initial_y = float(self.declare_parameter("initial_y", -12.0).value)
        self.initial_z = float(self.declare_parameter("initial_z", 1.2).value)
        self.execution_source_lock = self._normalize_source(
            str(self.declare_parameter("execution_source_lock", "").value)
        )
        priority_text = str(
            self.declare_parameter(
                "execution_source_priority",
                "managed_trajectory,local_trajectory,global_path",
            ).value
        )
        self.execution_source_priority = [
            self._normalize_source(item.strip())
            for item in priority_text.split(",")
            if item.strip()
        ]
        self.far_path_start_reject_distance = max(
            0.5, float(self.declare_parameter("far_path_start_reject_distance", 2.0).value)
        )
        self.min_path_update_period = max(0.1, float(self.declare_parameter("min_path_update_period", 1.0).value))

        self.paths: Dict[str, PathState] = {}
        self.active_source = "none"
        self.active_points = 0
        self.target_index = 0
        self.last_target_step_sec = self._now_sec()
        self.hold_position = True
        self.last_command = self._make_pose(self.initial_x, self.initial_y, self.initial_z)
        self.current_position = (self.initial_x, self.initial_y, self.initial_z)
        self.execution_source_switch_count = 0
        self.path_reset_count = 0
        self.rejected_far_path_start_count = 0
        self.stale_path_hold_count = 0
        self.debounced_path_update_count = 0
        self.path_direction_flip_count = 0
        self.last_active_path_update_sec = -999.0
        self.last_path_direction = None
        self.clear_reason = "none"
        self.empty_path_clear_count = 0
        self.terminal_hold_start_sec = -999.0
        self.terminal_hold_clear_sec = max(
            1.0, float(self.declare_parameter("terminal_hold_clear_sec", 3.0).value)
        )

        self.create_subscription(Odometry, "/odom", self._odom_cb, 20)
        self.create_subscription(
            Path,
            "/fuel/plan_manager/managed_trajectory",
            lambda msg: self._path_cb("managed_trajectory", msg),
            10,
        )
        self.create_subscription(Path, "/fuel/local_trajectory", lambda msg: self._path_cb("local_trajectory", msg), 10)
        self.create_subscription(Path, "/fuel/global_path", lambda msg: self._path_cb("global_path", msg), 10)

        self.position_pub = self.create_publisher(PoseStamped, "/fuel/p10_lite/position_cmd", 10)
        self.active_path_pub = self.create_publisher(Path, "/fuel/p10_lite/active_path", 10)
        self.status_pub = self.create_publisher(String, "/fuel/p10_lite/traj_server_status", 10)
        self.timer = self.create_timer(1.0 / self.command_rate, self._tick)
        self.get_logger().info(
            "P10_LITE_TRAJ_SERVER_RUNNING REAL_FLIGHT_COMMAND=false "
            f"execution_source_lock={self.execution_source_lock or 'NONE'} "
            f"execution_source_priority={','.join(self.execution_source_priority)} "
            f"far_path_start_reject_distance={self.far_path_start_reject_distance:.3f} "
            "blocked_real_flight_topics=true input_type=nav_msgs/Path output_type=geometry_msgs/PoseStamped"
        )

    def _now_sec(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    def _make_pose(self, x: float, y: float, z: float) -> PoseStamped:
        pose = PoseStamped()
        pose.header.frame_id = self.frame_id
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = float(z)
        pose.pose.orientation.w = 1.0
        return pose

    @staticmethod
    def _normalize_source(source: str) -> str:
        if source in ("plan_manager", "managed", "managed_path"):
            return "managed_trajectory"
        return source

    def _odom_cb(self, msg: Odometry) -> None:
        p = msg.pose.pose.position
        self.current_position = (float(p.x), float(p.y), float(p.z))

    def _nearest_index_to_current_position(self, msg: Path) -> int:
        if not msg.poses:
            return 0
        best_idx = 0
        best_dist = float("inf")
        for idx, pose in enumerate(msg.poses):
            p = pose.pose.position
            dist = (
                (float(p.x) - self.current_position[0]) ** 2
                + (float(p.y) - self.current_position[1]) ** 2
                + (float(p.z) - self.current_position[2]) ** 2
            )
            if dist < best_dist:
                best_idx = idx
                best_dist = dist
        return min(best_idx + 1, len(msg.poses) - 1)

    def _nearest_distance_to_current_position(self, msg: Path) -> float:
        if not msg.poses:
            return float("inf")
        best = float("inf")
        for pose in msg.poses:
            p = pose.pose.position
            dist = math.sqrt(
                (float(p.x) - self.current_position[0]) ** 2
                + (float(p.y) - self.current_position[1]) ** 2
                + (float(p.z) - self.current_position[2]) ** 2
            )
            best = min(best, dist)
        return best

    def _path_direction(self, msg: Path, index: int) -> Optional[tuple]:
        if len(msg.poses) < 2:
            return None
        i0 = min(max(0, index), len(msg.poses) - 2)
        p0 = msg.poses[i0].pose.position
        p1 = msg.poses[i0 + 1].pose.position
        vec = (float(p1.x - p0.x), float(p1.y - p0.y), float(p1.z - p0.z))
        norm = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
        if norm < 1e-6:
            return None
        return (vec[0] / norm, vec[1] / norm, vec[2] / norm)

    def _path_cb(self, source: str, msg: Path) -> None:
        source = self._normalize_source(source)
        now = self._now_sec()
        if len(msg.poses) == 0:
            self.paths.pop(source, None)
            self.empty_path_clear_count += 1
            self.clear_reason = f"empty_path_from_{source}"
            if source == self.active_source or self.active_source == "none":
                self.active_source = "none"
                self.active_points = 0
                self.target_index = 0
                self.hold_position = True
                self.last_path_direction = None
                self.terminal_hold_start_sec = -999.0
            self.last_active_path_update_sec = now
            self.get_logger().warn(
                f"P10_LITE_TRAJECTORY_CLEARED source={source} clear_reason={self.clear_reason} "
                f"empty_path_clear_count={self.empty_path_clear_count} REAL_FLIGHT_COMMAND=false"
            )
            return
        if self.execution_source_lock and source != self.execution_source_lock:
            self.paths[source] = PathState(source=source, msg=msg, stamp_sec=now)
            self.get_logger().info(
                f"P10_LITE_TRAJECTORY_SOURCE_IGNORED_BY_LOCK source={source} points={len(msg.poses)} "
                f"execution_source_lock={self.execution_source_lock} REAL_FLIGHT_COMMAND=false"
            )
            return
        if source == self.active_source and now - self.last_active_path_update_sec < self.min_path_update_period:
            self.debounced_path_update_count += 1
            self.get_logger().info(
                f"P10_LITE_TRAJECTORY_UPDATE_DEBOUNCED source={source} points={len(msg.poses)} "
                f"debounced_path_update_count={self.debounced_path_update_count} REAL_FLIGHT_COMMAND=false"
            )
            return
        nearest_distance = self._nearest_distance_to_current_position(msg)
        if msg.poses and nearest_distance > self.far_path_start_reject_distance:
            self.rejected_far_path_start_count += 1
            self.stale_path_hold_count += 1
            self.get_logger().warn(
                f"PATH_REJECTED_FAR_START source={source} nearest_distance={nearest_distance:.3f} "
                f"threshold={self.far_path_start_reject_distance:.3f} "
                f"rejected_far_path_start_count={self.rejected_far_path_start_count} REAL_FLIGHT_COMMAND=false"
            )
            return
        self.paths[source] = PathState(source=source, msg=msg, stamp_sec=self._now_sec())
        selected = self._select_source()
        if selected and selected.source != self.active_source:
            self.target_index = self._nearest_index_to_current_position(selected.msg)
            self.last_target_step_sec = self._now_sec()
        elif selected and selected.source == self.active_source and source == self.active_source:
            previous_direction = self.last_path_direction
            projected_index = self._nearest_index_to_current_position(selected.msg)
            if projected_index > self.target_index + 2 or self.target_index >= len(selected.msg.poses):
                self.target_index = projected_index
                self.path_reset_count += 1
            new_direction = self._path_direction(selected.msg, self.target_index)
            if previous_direction and new_direction:
                dot = sum(previous_direction[i] * new_direction[i] for i in range(3))
                if dot < -0.35:
                    self.path_direction_flip_count += 1
            self.last_target_step_sec = self._now_sec()
            self.last_path_direction = self._path_direction(selected.msg, self.target_index) or self.last_path_direction
        self.last_active_path_update_sec = now
        self.get_logger().info(
            f"P10_LITE_TRAJECTORY_SOURCE_UPDATED source={source} points={len(msg.poses)} "
            "REAL_FLIGHT_COMMAND=false"
        )

    def _select_source(self) -> Optional[PathState]:
        if self.execution_source_lock:
            locked = self.paths.get(self.execution_source_lock)
            if locked and len(locked.msg.poses) > 0:
                return locked
            return None
        for source in self.execution_source_priority:
            state = self.paths.get(source)
            min_points = 3 if source == "managed_trajectory" else 1
            if state and len(state.msg.poses) >= min_points:
                return state
        return None

    def _tick(self) -> None:
        now = self._now_sec()
        selected = self._select_source()
        if selected is None:
            if self.active_source != "none" and self.last_command is not None:
                self.stale_path_hold_count += 1
            self.active_source = "none"
            self.active_points = 0
            self.hold_position = True
            self.clear_reason = self.clear_reason if self.clear_reason != "none" else "no_selected_path"
            self.terminal_hold_start_sec = -999.0
            self._publish_command(self.last_command)
            self._publish_status()
            return

        if selected.source != self.active_source:
            previous_source = self.active_source
            self.active_source = selected.source
            if previous_source not in ("none", ""):
                self.execution_source_switch_count += 1
            self.target_index = self._nearest_index_to_current_position(selected.msg)
            if previous_source not in ("none", ""):
                self.path_reset_count += 1
            self.last_target_step_sec = now

        self.active_points = len(selected.msg.poses)
        if self.active_points == 0:
            self.hold_position = True
            self._publish_command(self.last_command)
            self._publish_status()
            return

        if now - self.last_target_step_sec >= self.target_step_period:
            if self.target_index + 1 < self.active_points:
                self.target_index += 1
                self.last_target_step_sec = now
            elif self.loop_trajectory:
                self.target_index = 0
                self.last_target_step_sec = now

        self.target_index = min(self.target_index, self.active_points - 1)
        self.hold_position = self.target_index >= self.active_points - 1 and not self.loop_trajectory
        if self.hold_position:
            if self.terminal_hold_start_sec < 0.0:
                self.terminal_hold_start_sec = now
            elif now - self.terminal_hold_start_sec >= self.terminal_hold_clear_sec:
                stale_source = self.active_source
                if stale_source in self.paths:
                    self.paths.pop(stale_source, None)
                self.active_source = "none"
                self.active_points = 0
                self.target_index = 0
                self.clear_reason = f"terminal_hold_timeout_from_{stale_source}"
                self.stale_path_hold_count += 1
                self.terminal_hold_start_sec = -999.0
                self._publish_command(self.last_command)
                self._publish_status()
                return
        else:
            self.terminal_hold_start_sec = -999.0
        if not self.hold_position:
            self.clear_reason = "none"
        command = selected.msg.poses[self.target_index]
        if not command.header.frame_id:
            command.header.frame_id = selected.msg.header.frame_id or self.frame_id
        self.last_command = command
        self.last_path_direction = self._path_direction(selected.msg, self.target_index) or self.last_path_direction
        self._publish_active_path(selected.msg)
        self._publish_command(command)
        self._publish_status()

    def _publish_command(self, command: PoseStamped) -> None:
        command.header.stamp = self.get_clock().now().to_msg()
        if not command.header.frame_id:
            command.header.frame_id = self.frame_id
        self.position_pub.publish(command)

    def _publish_active_path(self, path: Path) -> None:
        active = Path()
        active.header = path.header
        active.header.stamp = self.get_clock().now().to_msg()
        if not active.header.frame_id:
            active.header.frame_id = self.frame_id
        active.poses = list(path.poses[self.target_index :])
        if not active.poses and path.poses:
            active.poses = [path.poses[-1]]
        self.active_path_pub.publish(active)

    def _publish_status(self) -> None:
        msg = String()
        msg.data = (
            "REAL_FLIGHT_COMMAND=false "
            f"active_source={self.active_source} "
            f"execution_source_lock={self.execution_source_lock or 'NONE'} "
            f"active_points={self.active_points} "
            f"target_index={self.target_index} "
            f"hold_position={str(self.hold_position).lower()} "
            f"execution_source_switch_count={self.execution_source_switch_count} "
            f"path_reset_count={self.path_reset_count} "
            f"rejected_far_path_start_count={self.rejected_far_path_start_count} "
            f"stale_path_hold_count={self.stale_path_hold_count} "
            f"debounced_path_update_count={self.debounced_path_update_count} "
            f"empty_path_clear_count={self.empty_path_clear_count} "
            f"clear_reason={self.clear_reason} "
            f"terminal_hold_duration={0.0 if self.terminal_hold_start_sec < 0.0 else self._now_sec() - self.terminal_hold_start_sec:.3f} "
            f"stale_path={'true' if self.clear_reason.startswith('terminal_hold_timeout') else 'false'} "
            f"path_direction_flip_count={self.path_direction_flip_count} "
            "blocked_real_flight_topics=true"
        )
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FuelRos2TrajServerLite()
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
