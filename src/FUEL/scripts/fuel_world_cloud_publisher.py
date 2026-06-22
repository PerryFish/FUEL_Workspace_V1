#!/usr/bin/env python3
import math
import os
import struct
from typing import Dict, List, Tuple

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point as RosPoint

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


Point = Tuple[float, float, float]


DEFAULT_CONFIG = {
    "frame_id": "map",
    "world_name": "fuel_office_aligned",
    "resolution": 0.2,
    "bounds": {
        "min_x": -5.0,
        "max_x": 5.0,
        "min_y": -5.0,
        "max_y": 5.0,
        "min_z": 0.0,
        "max_z": 3.0,
    },
    "obstacles": [
        {"name": "left_wall", "type": "box", "center": [-1.8, 0.0, 1.0], "size": [0.2, 6.0, 2.0]},
        {"name": "right_wall", "type": "box", "center": [1.8, 0.0, 1.0], "size": [0.2, 6.0, 2.0]},
        {"name": "front_box", "type": "box", "center": [0.0, 2.2, 0.6], "size": [0.8, 0.8, 1.2]},
        {"name": "pillar", "type": "cylinder", "center": [0.0, -1.5, 0.8], "radius": 0.25, "height": 1.6},
    ],
}


def load_visual_world_config(path: str) -> Dict:
    if not path or not os.path.exists(path) or yaml is None:
        return DEFAULT_CONFIG
    with open(path, "r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}
    params = data.get("fuel_ros2", {}).get("ros__parameters", {})
    return params.get("visual_world", DEFAULT_CONFIG)


def frange(start: float, stop: float, step: float):
    value = start
    while value <= stop + 1e-9:
        yield value
        value += step


def add_box_surface(points: List[Point], center: List[float], size: List[float], resolution: float) -> None:
    cx, cy, cz = center
    sx, sy, sz = size
    min_x, max_x = cx - sx / 2.0, cx + sx / 2.0
    min_y, max_y = cy - sy / 2.0, cy + sy / 2.0
    min_z, max_z = cz - sz / 2.0, cz + sz / 2.0
    for x in frange(min_x, max_x, resolution):
        for y in frange(min_y, max_y, resolution):
            points.append((x, y, min_z))
            points.append((x, y, max_z))
    for x in frange(min_x, max_x, resolution):
        for z in frange(min_z, max_z, resolution):
            points.append((x, min_y, z))
            points.append((x, max_y, z))
    for y in frange(min_y, max_y, resolution):
        for z in frange(min_z, max_z, resolution):
            points.append((min_x, y, z))
            points.append((max_x, y, z))


def add_cylinder_surface(points: List[Point], center: List[float], radius: float, height: float, resolution: float) -> None:
    cx, cy, cz = center
    min_z, max_z = cz - height / 2.0, cz + height / 2.0
    angle_step = max(0.12, resolution / max(radius, 0.05))
    for z in frange(min_z, max_z, resolution):
        angle = 0.0
        while angle < 2.0 * math.pi:
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle), z))
            angle += angle_step
    for z in (min_z, max_z):
        r = 0.0
        while r <= radius + 1e-9:
            angle = 0.0
            while angle < 2.0 * math.pi:
                points.append((cx + r * math.cos(angle), cy + r * math.sin(angle), z))
                angle += angle_step
            r += resolution


def make_cloud(frame_id: str, stamp, points: List[Point]) -> PointCloud2:
    cloud = PointCloud2()
    cloud.header = Header(frame_id=frame_id, stamp=stamp)
    cloud.height = 1
    cloud.width = len(points)
    cloud.fields = [
        PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
    ]
    cloud.is_bigendian = False
    cloud.point_step = 12
    cloud.row_step = cloud.point_step * cloud.width
    cloud.is_dense = True
    cloud.data = b"".join(struct.pack("<fff", *point) for point in points)
    return cloud


class FuelWorldCloudPublisher(Node):
    def __init__(self):
        super().__init__("fuel_world_cloud_publisher")
        default_path = os.environ.get(
            "VISUAL_WORLD_CONFIG",
            "/home/nuaa/ZHY/FUEL_PLANNER_V2/ros2_ws/src/fuel_ros2/config/fuel_visual_world.yaml",
        )
        config_path = self.declare_parameter("config_path", default_path).value
        self.config = load_visual_world_config(config_path)
        self.frame_id = self.config.get("frame_id", "map")
        self.resolution = float(self.config.get("resolution", 0.2))
        self.obstacles = self.config.get("obstacles", DEFAULT_CONFIG["obstacles"])
        self.bounds = self.config.get("bounds", DEFAULT_CONFIG["bounds"])
        self.points = self._build_points()
        env_stride = os.environ.get("VISUAL_DEMO_CLOUD_STRIDE", "1")
        self.cloud_stride = max(1, int(self.declare_parameter("VISUAL_DEMO_CLOUD_STRIDE", int(env_stride)).value))
        if self.cloud_stride > 1:
            self.points = self.points[:: self.cloud_stride]
        self.qos_mode = str(self.declare_parameter("qos_mode", "rviz_compatible").value)

        qos = self._make_qos(self.qos_mode)
        self.map_pub = self.create_publisher(PointCloud2, "/map_cloud", qos)
        self.global_pub = self.create_publisher(PointCloud2, "/global_cloud", qos)
        self.obstacle_pub = self.create_publisher(MarkerArray, "/fuel/visual/world_obstacles", qos)
        self.bounds_pub = self.create_publisher(MarkerArray, "/fuel/visual/world_bounds", qos)
        self.timer = self.create_timer(1.0, self.publish_world)
        self.get_logger().info(
            f"FUEL_WORLD_CLOUD_PUBLISHER_RUNNING frame={self.frame_id} points={len(self.points)} "
            f"obstacles={len(self.obstacles)} cloud_stride={self.cloud_stride} config={config_path} qos_mode={self.qos_mode} "
            f"reliability={qos.reliability.name} durability={qos.durability.name} depth={qos.depth}"
        )

    def _make_qos(self, mode: str) -> QoSProfile:
        qos = QoSProfile(depth=1)
        normalized = (mode or "rviz_compatible").strip().lower()
        if normalized in ("sensor_data", "best_effort"):
            qos.reliability = ReliabilityPolicy.BEST_EFFORT
            qos.durability = DurabilityPolicy.VOLATILE
        else:
            qos.reliability = ReliabilityPolicy.RELIABLE
            qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        return qos

    def _build_points(self) -> List[Point]:
        points: List[Point] = []
        for obstacle in self.obstacles:
            if obstacle.get("type") == "box":
                add_box_surface(points, obstacle["center"], obstacle["size"], self.resolution)
            elif obstacle.get("type") == "cylinder":
                add_cylinder_surface(points, obstacle["center"], float(obstacle["radius"]), float(obstacle["height"]), self.resolution)
        return points

    def publish_world(self):
        stamp = self.get_clock().now().to_msg()
        cloud = make_cloud(self.frame_id, stamp, self.points)
        self.map_pub.publish(cloud)
        self.global_pub.publish(cloud)
        self.obstacle_pub.publish(self._make_obstacle_markers(stamp))
        self.bounds_pub.publish(self._make_bounds_markers(stamp))

    def _make_obstacle_markers(self, stamp) -> MarkerArray:
        markers = MarkerArray()
        for index, obstacle in enumerate(self.obstacles):
            marker = Marker()
            marker.header.frame_id = self.frame_id
            marker.header.stamp = stamp
            marker.ns = "fuel_visual_world"
            marker.id = index
            marker.action = Marker.ADD
            marker.pose.position.x = float(obstacle["center"][0])
            marker.pose.position.y = float(obstacle["center"][1])
            marker.pose.position.z = float(obstacle["center"][2])
            marker.pose.orientation.w = 1.0
            marker.color.a = 0.72
            marker.color.r = 0.62 + 0.08 * (index % 2)
            marker.color.g = 0.78
            marker.color.b = 0.92
            if obstacle.get("type") == "box":
                marker.type = Marker.CUBE
                marker.scale.x = float(obstacle["size"][0])
                marker.scale.y = float(obstacle["size"][1])
                marker.scale.z = float(obstacle["size"][2])
            else:
                marker.type = Marker.CYLINDER
                marker.scale.x = float(obstacle["radius"]) * 2.0
                marker.scale.y = float(obstacle["radius"]) * 2.0
                marker.scale.z = float(obstacle["height"])
            markers.markers.append(marker)
        return markers

    def _make_bounds_markers(self, stamp) -> MarkerArray:
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = stamp
        marker.ns = "fuel_visual_bounds"
        marker.id = 0
        marker.type = Marker.LINE_LIST
        marker.action = Marker.ADD
        marker.scale.x = 0.04
        marker.color.a = 0.9
        marker.color.r = 0.95
        marker.color.g = 0.95
        marker.color.b = 0.95
        b = self.bounds
        corners = [
            (b["min_x"], b["min_y"], b["min_z"]), (b["max_x"], b["min_y"], b["min_z"]),
            (b["max_x"], b["max_y"], b["min_z"]), (b["min_x"], b["max_y"], b["min_z"]),
            (b["min_x"], b["min_y"], b["max_z"]), (b["max_x"], b["min_y"], b["max_z"]),
            (b["max_x"], b["max_y"], b["max_z"]), (b["min_x"], b["max_y"], b["max_z"]),
        ]
        edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        for a, c in edges:
            for idx in (a, c):
                point = RosPoint()
                point.x, point.y, point.z = corners[idx]
                marker.points.append(point)
        return MarkerArray(markers=[marker])


def main():
    rclpy.init()
    node = FuelWorldCloudPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()
