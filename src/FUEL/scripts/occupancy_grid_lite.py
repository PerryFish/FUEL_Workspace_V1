#!/usr/bin/env python3
from typing import Dict, Tuple

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

from p11_lite_utils import make_cloud, parse_bounds, read_cloud, world_config_path


GridKey = Tuple[int, int]


class OccupancyGridLite(Node):
    UNKNOWN = 0
    FREE = 1
    OCCUPIED = 2

    def __init__(self):
        super().__init__("occupancy_grid_lite")
        self.world_config = world_config_path(str(self.declare_parameter("world_config", "").value))
        self.resolution = float(self.declare_parameter("grid_resolution", 0.5).value)
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.bounds = parse_bounds(self.world_config)
        self.grid: Dict[GridKey, int] = {}
        self.map_update_count = 0

        self.create_subscription(PointCloud2, "/fuel/p11_lite/local_occupied_points", self._occupied_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/local_free_points", self._free_cb, 10)
        self.occupancy_pub = self.create_publisher(PointCloud2, "/fuel/p11_lite/occupancy_grid", 10)
        self.explored_pub = self.create_publisher(PointCloud2, "/fuel/p11_lite/explored_grid", 10)
        self.frontier_pub = self.create_publisher(PointCloud2, "/fuel/p11_lite/frontier_candidates_raw", 10)
        self.status_pub = self.create_publisher(String, "/fuel/p11_lite/map_status", 10)
        self.timer = self.create_timer(0.75, self._publish)
        self.get_logger().info("P11_LITE_OCCUPANCY_GRID_READY REAL_FLIGHT_COMMAND=false")

    def _key(self, x: float, y: float) -> GridKey:
        return (int(round((x - self.bounds["min_x"]) / self.resolution)), int(round((y - self.bounds["min_y"]) / self.resolution)))

    def _pos(self, key: GridKey, z: float = 1.2):
        return (self.bounds["min_x"] + key[0] * self.resolution, self.bounds["min_y"] + key[1] * self.resolution, z)

    def _free_cb(self, msg: PointCloud2) -> None:
        for x, y, _ in read_cloud(msg):
            self.grid.setdefault(self._key(x, y), self.FREE)
        self.map_update_count += 1

    def _occupied_cb(self, msg: PointCloud2) -> None:
        for x, y, _ in read_cloud(msg):
            self.grid[self._key(x, y)] = self.OCCUPIED
        self.map_update_count += 1

    def _frontiers(self):
        result = []
        for key, state in self.grid.items():
            if state != self.FREE:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if self.grid.get((key[0] + dx, key[1] + dy), self.UNKNOWN) == self.UNKNOWN:
                    result.append(self._pos(key))
                    break
        return result

    def _publish(self) -> None:
        occupied = [self._pos(k) for k, v in self.grid.items() if v == self.OCCUPIED]
        explored = [self._pos(k) for k, v in self.grid.items() if v in (self.FREE, self.OCCUPIED)]
        frontiers = self._frontiers()
        now = self.get_clock().now().to_msg()
        for pub, pts in ((self.occupancy_pub, occupied), (self.explored_pub, explored), (self.frontier_pub, frontiers)):
            msg = make_cloud(pts, self.frame_id)
            msg.header.stamp = now
            pub.publish(msg)
        status = String()
        status.data = (
            "REAL_FLIGHT_COMMAND=false "
            f"explored_cell_count={len(explored)} "
            f"occupied_cell_count={len(occupied)} "
            f"frontier_candidate_count={len(frontiers)} "
            f"map_update_count={self.map_update_count}"
        )
        self.status_pub.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = OccupancyGridLite()
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
