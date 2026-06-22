#!/usr/bin/env python3
import math

import rclpy
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

from p11_lite_utils import make_cloud, parse_bounds, sample_circle, world_config_path
from world_collision_checker import load_obstacles, point_collision


class LocalSensingLite(Node):
    def __init__(self):
        super().__init__("local_sensing_lite")
        self.world_config = world_config_path(str(self.declare_parameter("world_config", "").value))
        self.environment_mode = str(self.declare_parameter("environment_mode", "simple").value)
        self.sensing_radius = float(self.declare_parameter("sensing_radius", 4.0).value)
        self.local_window_radius = float(self.declare_parameter("local_window_radius", self.sensing_radius).value)
        self.z_min = float(self.declare_parameter("z_min", float("nan")).value)
        self.z_max = float(self.declare_parameter("z_max", float("nan")).value)
        self.grid_step = float(self.declare_parameter("grid_step", 0.5).value)
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.bounds = parse_bounds(self.world_config)
        self.obstacles = load_obstacles(self.world_config)
        self.complex_occupied_points = []
        self.complex_env_received = False
        self.odom = None
        self.odom_received = False

        self.create_subscription(Odometry, "/odom", self._odom_cb, 20)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/complex_env/occupied_points", self._complex_occupied_cb, 10)
        self.occupied_pub = self.create_publisher(PointCloud2, "/fuel/p11_lite/local_occupied_points", 10)
        self.free_pub = self.create_publisher(PointCloud2, "/fuel/p11_lite/local_free_points", 10)
        self.status_pub = self.create_publisher(String, "/fuel/p11_lite/sensing_status", 10)
        self.timer = self.create_timer(0.5, self._tick)
        self.get_logger().info("P11_LITE_LOCAL_SENSING_READY REAL_FLIGHT_COMMAND=false")

    def _odom_cb(self, msg: Odometry) -> None:
        self.odom = msg
        self.odom_received = True

    def _complex_occupied_cb(self, msg: PointCloud2) -> None:
        from p11_lite_utils import read_cloud

        self.complex_occupied_points = read_cloud(msg)
        self.complex_env_received = True

    def _tick(self) -> None:
        occupied = []
        free = []
        if self.odom is not None:
            p = self.odom.pose.pose.position
            min_z = self.bounds["min_z"] if math.isnan(self.z_min) else self.z_min
            max_z = self.bounds["max_z"] if math.isnan(self.z_max) else self.z_max
            z_base = max(min_z + 0.25, min(max_z - 0.25, float(p.z)))
            z_values = sorted({round(max(self.bounds["min_z"] + 0.25, min(self.bounds["max_z"] - 0.25, z)), 2) for z in (z_base, 0.75, 1.5, 2.5)})
            occupied_xy_keys = set()
            if self.environment_mode == "complex" and self.complex_env_received:
                for pt in self.complex_occupied_points:
                    x, y, z = pt
                    if z < min_z or z > max_z:
                        continue
                    if math.hypot(x - float(p.x), y - float(p.y)) <= self.local_window_radius:
                        occupied.append(pt)
                        occupied_xy_keys.add((round(x / self.grid_step), round(y / self.grid_step)))
            elif self.environment_mode == "complex" and not self.complex_env_received:
                self.get_logger().warn("complex environment requested but occupied_points topic not received; using simple world fallback", throttle_duration_sec=5.0)

            for pt in sample_circle((float(p.x), float(p.y), z_base), self.sensing_radius, self.grid_step, z_values):
                x, y, z = pt
                if x < self.bounds["min_x"] or x > self.bounds["max_x"] or y < self.bounds["min_y"] or y > self.bounds["max_y"]:
                    continue
                if self.environment_mode == "complex" and self.complex_env_received:
                    if (round(x / self.grid_step), round(y / self.grid_step)) in occupied_xy_keys:
                        continue
                    if abs(z - z_base) < 1e-3:
                        free.append(pt)
                elif point_collision(self.obstacles, pt, 0.0).collides:
                    occupied.append(pt)
                elif abs(z - z_base) < 1e-3:
                    free.append(pt)

        occ_msg = make_cloud(occupied, self.frame_id)
        free_msg = make_cloud(free, self.frame_id)
        now = self.get_clock().now().to_msg()
        occ_msg.header.stamp = now
        free_msg.header.stamp = now
        self.occupied_pub.publish(occ_msg)
        self.free_pub.publish(free_msg)

        status = String()
        status.data = (
            "REAL_FLIGHT_COMMAND=false "
            f"environment_mode={self.environment_mode} "
            f"complex_env_active={'true' if self.environment_mode == 'complex' and self.complex_env_received else 'false'} "
            f"sensing_radius={self.sensing_radius:.2f} "
            f"local_window_radius={self.local_window_radius:.2f} "
            f"occupied_points={len(occupied)} "
            f"free_points={len(free)} "
            f"odom_received={'true' if self.odom_received else 'false'}"
        )
        self.status_pub.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = LocalSensingLite()
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
