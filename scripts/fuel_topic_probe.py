#!/usr/bin/env python3
import argparse
import math
import time
from typing import Dict, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2
from visualization_msgs.msg import Marker, MarkerArray


class Stat:
    def __init__(self, topic: str):
        self.topic = topic
        self.count = 0
        self.first_time: Optional[float] = None
        self.last_time: Optional[float] = None
        self.sample = ""

    def tick(self, now: float, sample: str):
        self.count += 1
        self.first_time = self.first_time or now
        self.last_time = now
        if not self.sample:
            self.sample = sample


class FuelTopicProbe(Node):
    def __init__(self):
        super().__init__("fuel_topic_probe")
        self.stats: Dict[str, Stat] = {}
        self.odom_start: Optional[Tuple[float, float, float]] = None
        self.odom_end: Optional[Tuple[float, float, float]] = None
        self.odom_topic = ""
        self.create_subscription(Odometry, "/odom", lambda m: self.odom_cb("/odom", m), 20)
        self.create_subscription(Odometry, "/state_estimation", lambda m: self.odom_cb("/state_estimation", m), 20)
        self.create_subscription(Odometry, "/state_ukf/odom", lambda m: self.odom_cb("/state_ukf/odom", m), 20)
        self.create_subscription(Odometry, "/visual_slam/odom", lambda m: self.odom_cb("/visual_slam/odom", m), 20)
        self.create_subscription(PoseStamped, "/fuel/p10_lite/position_cmd", lambda m: self.pose_cb("/fuel/p10_lite/position_cmd", m), 10)
        self.create_subscription(PoseStamped, "/planning/pos_cmd", lambda m: self.pose_cb("/planning/pos_cmd", m), 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", lambda m: self.pose_cb("/fuel/p11_lite/exploration_goal", m), 10)
        self.create_subscription(PoseStamped, "/move_base_simple/goal", lambda m: self.pose_cb("/move_base_simple/goal", m), 10)
        for topic in [
            "/fuel/p10_lite/active_path",
            "/fuel/plan_manager/managed_trajectory",
            "/fuel/local_trajectory",
            "/fuel/global_path",
            "/planning/travel_traj",
            "/planning_vis/trajectory",
        ]:
            self.create_subscription(Path, topic, lambda m, t=topic: self.path_cb(t, m), 10)
        for topic in [
            "/global_cloud",
            "/map_cloud",
            "/map_generator/global_cloud",
            "/fuel/p11_lite/local_occupied_points",
            "/fuel/p11_lite/local_free_points",
            "/fuel/p11_lite/explored_grid",
            "/fuel/p11_lite/frontier_candidates_raw",
            "/pcl_render_node/cloud",
        ]:
            self.create_subscription(PointCloud2, topic, lambda m, t=topic: self.cloud_cb(t, m), 10)
        self.create_subscription(Image, "/pcl_render_node/depth", lambda m: self.image_cb("/pcl_render_node/depth", m), 10)
        self.create_subscription(MarkerArray, "/fuel/p11_lite/visual/all_markers", lambda m: self.marker_array_cb("/fuel/p11_lite/visual/all_markers", m), 10)
        self.create_subscription(MarkerArray, "/fuel/p11_lite/visual/path_markers", lambda m: self.marker_array_cb("/fuel/p11_lite/visual/path_markers", m), 10)
        self.create_subscription(MarkerArray, "/fuel/p11_lite/visual/frontier_markers", lambda m: self.marker_array_cb("/fuel/p11_lite/visual/frontier_markers", m), 10)
        self.create_subscription(MarkerArray, "/fuel/visual/world_bounds", lambda m: self.marker_array_cb("/fuel/visual/world_bounds", m), 10)
        self.create_subscription(MarkerArray, "/fuel/visual/world_obstacles", lambda m: self.marker_array_cb("/fuel/visual/world_obstacles", m), 10)
        self.create_subscription(Marker, "/fuel/p11_lite/visual/uav_marker", lambda m: self.marker_cb("/fuel/p11_lite/visual/uav_marker", m), 10)
        self.create_subscription(Marker, "/fuel/p11_lite/visual/uav_trail", lambda m: self.marker_cb("/fuel/p11_lite/visual/uav_trail", m), 10)
        self.create_subscription(Marker, "/fuel/p11_lite/visual/current_goal_marker", lambda m: self.marker_cb("/fuel/p11_lite/visual/current_goal_marker", m), 10)

    def stat(self, topic: str) -> Stat:
        if topic not in self.stats:
            self.stats[topic] = Stat(topic)
        return self.stats[topic]

    def odom_cb(self, topic: str, msg: Odometry):
        p = msg.pose.pose.position
        pos = (float(p.x), float(p.y), float(p.z))
        if self.odom_start is None:
            self.odom_start = pos
            self.odom_topic = topic
        self.odom_end = pos
        self.stat(topic).tick(time.time(), f"pos=({pos[0]:.3f},{pos[1]:.3f},{pos[2]:.3f}) frame={msg.header.frame_id}")

    def pose_cb(self, topic: str, msg: PoseStamped):
        p = msg.pose.position
        self.stat(topic).tick(time.time(), f"pose=({p.x:.3f},{p.y:.3f},{p.z:.3f}) frame={msg.header.frame_id}")

    def path_cb(self, topic: str, msg: Path):
        self.stat(topic).tick(time.time(), f"poses={len(msg.poses)} frame={msg.header.frame_id}")

    def cloud_cb(self, topic: str, msg: PointCloud2):
        self.stat(topic).tick(time.time(), f"points={msg.width * msg.height} frame={msg.header.frame_id}")

    def image_cb(self, topic: str, msg: Image):
        self.stat(topic).tick(time.time(), f"image={msg.width}x{msg.height} frame={msg.header.frame_id}")

    def marker_array_cb(self, topic: str, msg: MarkerArray):
        self.stat(topic).tick(time.time(), f"markers={len(msg.markers)}")

    def marker_cb(self, topic: str, msg: Marker):
        p = msg.pose.position
        self.stat(topic).tick(time.time(), f"marker=({p.x:.3f},{p.y:.3f},{p.z:.3f}) frame={msg.header.frame_id}")

    def distance_moved(self) -> float:
        if self.odom_start is None or self.odom_end is None:
            return 0.0
        return math.dist(self.odom_start, self.odom_end)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("--min-motion", type=float, default=0.2)
    args = parser.parse_args()
    rclpy.init()
    node = FuelTopicProbe()
    end = time.time() + args.duration
    try:
        while rclpy.ok() and time.time() < end:
            rclpy.spin_once(node, timeout_sec=0.2)
    finally:
        dist = node.distance_moved()
        planner_pos = node.stats.get("/planning/pos_cmd", Stat("/planning/pos_cmd")).count + node.stats.get("/fuel/p10_lite/position_cmd", Stat("/fuel/p10_lite/position_cmd")).count
        planner_traj = sum(node.stats.get(t, Stat(t)).count for t in ["/planning/travel_traj", "/fuel/p10_lite/active_path", "/fuel/plan_manager/managed_trajectory", "/fuel/local_trajectory", "/fuel/global_path"])
        map_count = sum(node.stats.get(t, Stat(t)).count for t in ["/map_generator/global_cloud", "/global_cloud", "/map_cloud"])
        local_count = sum(node.stats.get(t, Stat(t)).count for t in ["/pcl_render_node/cloud", "/fuel/p11_lite/local_occupied_points", "/fuel/p11_lite/local_free_points"])
        goal_count = sum(node.stats.get(t, Stat(t)).count for t in ["/move_base_simple/goal", "/fuel/p11_lite/exploration_goal"])
        odom_count = sum(node.stats.get(t, Stat(t)).count for t in ["/odom", "/state_estimation", "/state_ukf/odom", "/visual_slam/odom"])
        for topic in sorted(node.stats):
            s = node.stats[topic]
            print(f"TOPIC_STAT topic={topic} count={s.count} sample=\"{s.sample}\"")
        result = "PASS" if odom_count > 5 and map_count > 1 and planner_traj > 1 and dist > args.min_motion else "FAIL"
        print("FUEL_TOPIC_PROBE_RESULT")
        print(f"odom_topic={node.odom_topic or 'NONE'}")
        print(f"odom_msg_count={odom_count}")
        print(f"uav_distance_moved={dist:.3f}")
        print(f"goal_msg_count={goal_count}")
        print(f"planner_pos_cmd_count={planner_pos}")
        print(f"planner_traj_count={planner_traj}")
        print(f"map_cloud_count={map_count}")
        print(f"local_cloud_count={local_count}")
        print(f"result={result}")
        node.destroy_node()
        rclpy.shutdown()
        raise SystemExit(0 if result == "PASS" else 1)


if __name__ == "__main__":
    main()
