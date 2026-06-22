#!/usr/bin/env python3
import math
from pathlib import Path
from typing import List, Sequence, Tuple

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
from visualization_msgs.msg import Marker, MarkerArray

from p11_lite_utils import make_cloud, parse_bounds, world_config_path
from world_collision_checker import Obstacle, load_obstacles


Point3 = Tuple[float, float, float]


class P11LiteComplexEnvironmentAdapter(Node):
    def __init__(self):
        super().__init__("p11_lite_complex_environment_adapter")
        self.world_config = world_config_path(str(self.declare_parameter("world_config", "").value))
        self.environment_name = str(self.declare_parameter("environment_name", "").value) or self.world_config.stem
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.sample_resolution = float(self.declare_parameter("sample_resolution", 0.25).value)
        self.bounds = parse_bounds(self.world_config)
        self.obstacles = load_obstacles(self.world_config)
        self.occupied_points = self._sample_obstacles(self.obstacles, self.sample_resolution)

        self.occupied_pub = self.create_publisher(PointCloud2, "/fuel/p11_lite/complex_env/occupied_points", 10)
        self.free_boundary_pub = self.create_publisher(Marker, "/fuel/p11_lite/complex_env/free_boundary", 10)
        self.map_boundary_pub = self.create_publisher(Marker, "/fuel/p11_lite/complex_env/map_boundary", 10)
        self.wall_markers_pub = self.create_publisher(MarkerArray, "/fuel/p11_lite/complex_env/wall_markers", 10)
        self.status_pub = self.create_publisher(String, "/fuel/p11_lite/complex_env/status", 10)
        self.timer = self.create_timer(0.5, self._publish)
        self.get_logger().info("P11_LITE_COMPLEX_ENV_ADAPTER_READY REAL_FLIGHT_COMMAND=false")

    def _sample_obstacles(self, obstacles: Sequence[Obstacle], resolution: float) -> List[Point3]:
        points: List[Point3] = []
        for obstacle in obstacles:
            if obstacle.kind == "box":
                cx, cy, cz = obstacle.center
                sx, sy, sz = obstacle.size
                nx = max(1, int(math.ceil(sx / resolution)))
                ny = max(1, int(math.ceil(sy / resolution)))
                nz = max(1, int(math.ceil(sz / max(resolution * 2.0, 0.25))))
                for ix in range(nx + 1):
                    x = cx - sx * 0.5 + ix * sx / max(1, nx)
                    for iy in range(ny + 1):
                        y = cy - sy * 0.5 + iy * sy / max(1, ny)
                        edge_xy = ix in (0, nx) or iy in (0, ny)
                        for iz in range(nz + 1):
                            z = cz - sz * 0.5 + iz * sz / max(1, nz)
                            edge_z = iz in (0, nz)
                            if edge_xy or edge_z:
                                points.append((x, y, z))
            elif obstacle.kind == "cylinder":
                cx, cy, cz = obstacle.center
                rings = max(16, int(math.ceil(2.0 * math.pi * max(obstacle.radius, resolution) / resolution)))
                nz = max(1, int(math.ceil(obstacle.height / max(resolution * 2.0, 0.25))))
                for iz in range(nz + 1):
                    z = cz - obstacle.height * 0.5 + iz * obstacle.height / max(1, nz)
                    for i in range(rings):
                        a = 2.0 * math.pi * i / rings
                        points.append((cx + math.cos(a) * obstacle.radius, cy + math.sin(a) * obstacle.radius, z))
        return points

    def _marker(self, ns: str, mid: int, marker_type: int) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = ns
        marker.id = mid
        marker.type = marker_type
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        return marker

    @staticmethod
    def _color(marker: Marker, r: float, g: float, b: float, a: float) -> Marker:
        marker.color.r = r
        marker.color.g = g
        marker.color.b = b
        marker.color.a = a
        return marker

    @staticmethod
    def _point(x: float, y: float, z: float):
        from geometry_msgs.msg import Point

        point = Point()
        point.x = float(x)
        point.y = float(y)
        point.z = float(z)
        return point

    def _boundary_marker(self, ns: str, mid: int, z: float, width: float) -> Marker:
        marker = self._marker(ns, mid, Marker.LINE_STRIP)
        marker.scale.x = width
        min_x, max_x = self.bounds["min_x"], self.bounds["max_x"]
        min_y, max_y = self.bounds["min_y"], self.bounds["max_y"]
        for x, y in ((min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y), (min_x, min_y)):
            marker.points.append(self._point(x, y, z))
        return self._color(marker, 0.92, 0.92, 0.92, 1.0)

    def _wall_markers(self) -> MarkerArray:
        array = MarkerArray()
        for i, obstacle in enumerate(self.obstacles):
            marker = self._marker("complex_wall_obstacle", i, Marker.CUBE if obstacle.kind == "box" else Marker.CYLINDER)
            marker.pose.position = self._point(*obstacle.center)
            if obstacle.kind == "box":
                marker.scale.x, marker.scale.y, marker.scale.z = obstacle.size
            else:
                marker.scale.x = marker.scale.y = obstacle.radius * 2.0
                marker.scale.z = obstacle.height
            if "wall" in obstacle.name or max(marker.scale.x, marker.scale.y) > 3.0:
                self._color(marker, 0.72, 0.72, 0.78, 0.88)
            else:
                self._color(marker, 0.95, 0.18, 0.12, 0.86)
            array.markers.append(marker)
        return array

    def _publish(self) -> None:
        now = self.get_clock().now().to_msg()
        cloud = make_cloud(self.occupied_points, self.frame_id)
        cloud.header.stamp = now
        self.occupied_pub.publish(cloud)
        self.map_boundary_pub.publish(self._boundary_marker("complex_map_boundary", 1, 0.08, 0.14))
        self.free_boundary_pub.publish(self._boundary_marker("complex_free_boundary", 2, 0.05, 0.06))
        self.wall_markers_pub.publish(self._wall_markers())

        wall_count = sum(1 for o in self.obstacles if "wall" in o.name or (o.kind == "box" and max(o.size[0], o.size[1]) > 3.0))
        status = String()
        status.data = (
            f"env_name={self.environment_name} "
            f"world_config={self.world_config} "
            f"obstacle_count={len(self.obstacles)} "
            f"wall_count={wall_count} "
            f"occupied_point_count={len(self.occupied_points)} "
            f"boundary=[{self.bounds['min_x']:.2f},{self.bounds['max_x']:.2f},{self.bounds['min_y']:.2f},{self.bounds['max_y']:.2f},{self.bounds['min_z']:.2f},{self.bounds['max_z']:.2f}] "
            "adapter_ready=true "
            "real_flight_command=false"
        )
        self.status_pub.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = P11LiteComplexEnvironmentAdapter()
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
