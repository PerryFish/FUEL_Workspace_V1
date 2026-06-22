#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import math
import os
import re
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

Point = Tuple[float, float, float]


@dataclass
class Sample:
    time_sec: float
    odom_total_distance: float
    odom_net_displacement: float
    goal_count: int
    active_path_count: int
    active_path_update_count: int
    travel_traj_count: int
    travel_traj_update_count: int
    position_cmd_count: int
    position_cmd_update_count: int
    frontier_candidates: int
    frontier_viewpoints: int


class MotionChainRecorder(Node):
    def __init__(self, args):
        super().__init__("fuel_motion_chain_recorder")
        self.args = args
        self.start = time.time()
        self.end = self.start + args.duration
        self.samples: List[Sample] = []
        self.events: List[Dict] = []
        self.msg_count: Dict[str, int] = {}
        self.status_latest: Dict[str, str] = {}

        self.odom_start: Optional[Point] = None
        self.odom_last: Optional[Point] = None
        self.odom_total_distance = 0.0
        self.odom_last_motion_time = self.start

        self.goal_points: List[Tuple[float, Point]] = []
        self.best_points: List[Tuple[float, Point]] = []
        self.goal_switch_count = 0
        self.goal_last: Optional[Point] = None

        self.active_path_hash = ""
        self.active_path_update_count = 0
        self.active_path_same_hash_start = self.start
        self.active_path_same_hash_max = 0.0
        self.active_path_endpoint: Optional[Point] = None
        self.active_path_lengths: List[float] = []
        self.active_path_endpoint_to_goal: List[float] = []

        self.travel_hash = ""
        self.travel_update_count = 0
        self.travel_same_hash_start = self.start
        self.travel_same_hash_max = 0.0
        self.travel_endpoint: Optional[Point] = None
        self.travel_endpoint_to_goal: List[float] = []

        self.cmd_last: Optional[Point] = None
        self.cmd_update_count = 0
        self.cmd_total_variation = 0.0
        self.cmd_same_pose_start = self.start
        self.cmd_same_pose_max = 0.0
        self.cmd_to_odom: List[float] = []

        self.traj_server_stale_path_hold_count = 0
        self.traj_server_events: List[str] = []
        self.quad_motion_blocked_count = 0
        self.quad_events: List[str] = []
        self.frontier_candidates_series: List[int] = []
        self.frontier_viewpoints_series: List[int] = []
        self.frontier_candidates = 0
        self.frontier_viewpoints = 0

        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self.goal_cb, 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/best_viewpoint", self.best_cb, 10)
        for topic in ["/fuel/p10_lite/position_cmd", "/planning/pos_cmd"]:
            self.create_subscription(PoseStamped, topic, lambda m, t=topic: self.cmd_cb(t, m), 10)
        for topic in ["/odom", "/state_ukf/odom", "/visual_slam/odom"]:
            self.create_subscription(Odometry, topic, lambda m, t=topic: self.odom_cb(t, m), 20)
        for topic in ["/fuel/p10_lite/active_path", "/planning/travel_traj", "/fuel/plan_manager/managed_trajectory"]:
            self.create_subscription(Path, topic, lambda m, t=topic: self.path_cb(t, m), 10)
        for topic in ["/fuel/p11_lite/goal_to_path_status", "/fuel/p11_lite/exploration_manager_status", "/fuel/p10_lite/traj_server_status", "/fuel/p10_lite/quadrotor_sim_status"]:
            self.create_subscription(String, topic, lambda m, t=topic: self.status_cb(t, m), 10)
        for topic in ["/fuel/p11_lite/frontier_viewpoints", "/fuel/p11_lite/frontier_candidates_raw"]:
            self.create_subscription(PointCloud2, topic, lambda m, t=topic: self.cloud_cb(t, m), 10)

    def elapsed(self) -> float:
        return time.time() - self.start

    def tick(self, topic: str) -> None:
        self.msg_count[topic] = self.msg_count.get(topic, 0) + 1

    @staticmethod
    def pose_point(msg: PoseStamped) -> Point:
        p = msg.pose.position
        return float(p.x), float(p.y), float(p.z)

    @staticmethod
    def path_points(msg: Path) -> List[Point]:
        return [(float(p.pose.position.x), float(p.pose.position.y), float(p.pose.position.z)) for p in msg.poses]

    @staticmethod
    def path_hash(points: List[Point]) -> str:
        text = ";".join(f"{x:.2f},{y:.2f},{z:.2f}" for x, y, z in points)
        return hashlib.sha1(text.encode("utf-8")).hexdigest()

    @staticmethod
    def path_length(points: List[Point]) -> float:
        return sum(math.dist(a, b) for a, b in zip(points, points[1:]))

    def current_goal(self) -> Optional[Point]:
        return self.goal_points[-1][1] if self.goal_points else None

    def odom_cb(self, topic: str, msg: Odometry) -> None:
        self.tick(topic)
        p = msg.pose.pose.position
        pos = (float(p.x), float(p.y), float(p.z))
        if self.odom_start is None:
            self.odom_start = pos
        if self.odom_last is not None:
            step = math.dist(self.odom_last, pos)
            self.odom_total_distance += step
            if step > 0.02:
                self.odom_last_motion_time = time.time()
        self.odom_last = pos

    def goal_cb(self, msg: PoseStamped) -> None:
        self.tick("/fuel/p11_lite/exploration_goal")
        p = self.pose_point(msg)
        if self.goal_last is not None and math.dist(self.goal_last, p) > 0.5:
            self.goal_switch_count += 1
        self.goal_last = p
        self.goal_points.append((self.elapsed(), p))

    def best_cb(self, msg: PoseStamped) -> None:
        self.tick("/fuel/p11_lite/best_viewpoint")
        self.best_points.append((self.elapsed(), self.pose_point(msg)))

    def path_cb(self, topic: str, msg: Path) -> None:
        self.tick(topic)
        points = self.path_points(msg)
        h = self.path_hash(points)
        now = time.time()
        endpoint = points[-1] if points else None
        goal = self.current_goal()
        if topic == "/fuel/p10_lite/active_path":
            if h != self.active_path_hash:
                self.active_path_same_hash_max = max(self.active_path_same_hash_max, now - self.active_path_same_hash_start)
                self.active_path_same_hash_start = now
                self.active_path_hash = h
                self.active_path_update_count += 1
            self.active_path_endpoint = endpoint
            self.active_path_lengths.append(self.path_length(points))
            if endpoint and goal:
                self.active_path_endpoint_to_goal.append(math.dist(endpoint, goal))
        elif topic in ["/planning/travel_traj", "/fuel/plan_manager/managed_trajectory"]:
            if h != self.travel_hash:
                self.travel_same_hash_max = max(self.travel_same_hash_max, now - self.travel_same_hash_start)
                self.travel_same_hash_start = now
                self.travel_hash = h
                self.travel_update_count += 1
            self.travel_endpoint = endpoint
            if endpoint and goal:
                self.travel_endpoint_to_goal.append(math.dist(endpoint, goal))

    def cmd_cb(self, topic: str, msg: PoseStamped) -> None:
        self.tick(topic)
        p = self.pose_point(msg)
        now = time.time()
        if self.cmd_last is None or math.dist(self.cmd_last, p) > 0.02:
            self.cmd_same_pose_max = max(self.cmd_same_pose_max, now - self.cmd_same_pose_start)
            self.cmd_same_pose_start = now
            self.cmd_update_count += 1
            if self.cmd_last is not None:
                self.cmd_total_variation += math.dist(self.cmd_last, p)
        self.cmd_last = p
        if self.odom_last is not None:
            self.cmd_to_odom.append(math.dist(p, self.odom_last))

    def status_cb(self, topic: str, msg: String) -> None:
        self.tick(topic)
        self.status_latest[topic] = msg.data
        if topic == "/fuel/p10_lite/traj_server_status":
            m = re.search(r"stale_path_hold_count=([0-9]+)", msg.data)
            if m:
                self.traj_server_stale_path_hold_count = max(self.traj_server_stale_path_hold_count, int(m.group(1)))
            if "STALE" in msg.data.upper() or "hold" in msg.data.lower():
                self.traj_server_events.append(msg.data[:240])
        if topic == "/fuel/p10_lite/quadrotor_sim_status":
            if "blocked" in msg.data.lower() or "stuck" in msg.data.lower():
                self.quad_motion_blocked_count += 1
                self.quad_events.append(msg.data[:240])

    def cloud_cb(self, topic: str, msg: PointCloud2) -> None:
        self.tick(topic)
        n = int(msg.width * msg.height)
        if topic == "/fuel/p11_lite/frontier_candidates_raw":
            self.frontier_candidates = n
            self.frontier_candidates_series.append(n)
        else:
            self.frontier_viewpoints = n
            self.frontier_viewpoints_series.append(n)

    def sample(self) -> None:
        self.samples.append(Sample(
            self.elapsed(),
            self.odom_total_distance,
            self.net_displacement(),
            len(self.goal_points),
            self.msg_count.get("/fuel/p10_lite/active_path", 0),
            self.active_path_update_count,
            self.msg_count.get("/planning/travel_traj", 0),
            self.travel_update_count,
            self.msg_count.get("/planning/pos_cmd", 0) + self.msg_count.get("/fuel/p10_lite/position_cmd", 0),
            self.cmd_update_count,
            self.frontier_candidates,
            self.frontier_viewpoints,
        ))

    def net_displacement(self) -> float:
        if self.odom_start is None or self.odom_last is None:
            return 0.0
        return math.dist(self.odom_start, self.odom_last)

    def max_no_motion_duration(self) -> float:
        if not self.samples:
            return 0.0
        max_span = 0.0
        start = self.samples[0]
        for sample in self.samples[1:]:
            if sample.odom_total_distance - start.odom_total_distance >= 0.2:
                start = sample
            else:
                max_span = max(max_span, sample.time_sec - start.time_sec)
        return max_span

    @staticmethod
    def avg(values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    def main_chain_break(self) -> str:
        active_path_count = self.msg_count.get("/fuel/p10_lite/active_path", 0)
        travel_count = self.msg_count.get("/planning/travel_traj", 0)
        pos_count = self.msg_count.get("/planning/pos_cmd", 0) + self.msg_count.get("/fuel/p10_lite/position_cmd", 0)
        endpoint_avg = self.avg(self.active_path_endpoint_to_goal)
        if len(self.goal_points) > 5 and (active_path_count == 0 or endpoint_avg > 1.5 or self.active_path_same_hash_max > 60.0):
            return "PATH_FEASIBILITY"
        if self.active_path_update_count > 5 and (self.travel_update_count <= 1 or self.travel_same_hash_max > 60.0):
            return "TRAJ_SERVER_STALE_PATH"
        if self.travel_update_count > 5 and (self.cmd_update_count <= 1 or self.cmd_same_pose_max > 60.0):
            return "POSITION_CMD_STALE"
        if self.cmd_update_count > 5 and self.odom_total_distance < 1.0 and self.avg(self.cmd_to_odom) > 1.0:
            return "SIM_TRACKING_FAIL"
        if self.odom_total_distance > 1.0:
            return "MAP_COVERAGE_STALL"
        return "UNKNOWN"

    def run(self) -> None:
        last_sample = 0.0
        last_progress = time.time()
        while rclpy.ok() and time.time() < self.end:
            rclpy.spin_once(self, timeout_sec=0.2)
            if time.time() - last_sample >= self.args.sample_period:
                last_sample = time.time()
                self.sample()
            if time.time() - last_progress >= self.args.progress_interval:
                last_progress = time.time()
                print(
                    "P2D_PROGRESS "
                    f"time={self.elapsed():.1f} "
                    f"odom_distance={self.odom_total_distance:.3f} "
                    f"active_path_updates={self.active_path_update_count} "
                    f"travel_updates={self.travel_update_count} "
                    f"cmd_updates={self.cmd_update_count} "
                    f"frontier={self.frontier_candidates}",
                    flush=True,
                )
        self.active_path_same_hash_max = max(self.active_path_same_hash_max, time.time() - self.active_path_same_hash_start)
        self.travel_same_hash_max = max(self.travel_same_hash_max, time.time() - self.travel_same_hash_start)
        self.cmd_same_pose_max = max(self.cmd_same_pose_max, time.time() - self.cmd_same_pose_start)
        if not self.samples:
            self.sample()

    def write_outputs(self) -> Dict:
        out_dir = os.path.join(self.args.output_root, self.args.run_id)
        os.makedirs(out_dir, exist_ok=True)
        chain = {
            "run_id": self.args.run_id,
            "duration_sec": self.elapsed(),
            "odom_total_distance": self.odom_total_distance,
            "uav_total_distance": self.odom_total_distance,
            "odom_net_displacement": self.net_displacement(),
            "uav_net_displacement": self.net_displacement(),
            "odom_max_no_motion_duration_sec": self.max_no_motion_duration(),
            "goal_msg_count": len(self.goal_points),
            "goal_switch_count": self.goal_switch_count,
            "active_goal_segments": [],
            "active_goal_to_path_endpoint_distance": self.active_path_endpoint_to_goal[-20:],
            "active_goal_to_current_odom_distance": math.dist(self.current_goal(), self.odom_last) if self.current_goal() and self.odom_last else 0.0,
            "active_goal_hold_duration": self.samples[-1].time_sec if self.samples else 0.0,
            "active_path_msg_count": self.msg_count.get("/fuel/p10_lite/active_path", 0),
            "active_path_update_count": self.active_path_update_count,
            "active_path_endpoint": self.active_path_endpoint,
            "active_path_length": self.active_path_lengths[-1] if self.active_path_lengths else 0.0,
            "active_path_endpoint_to_goal_distance_avg": self.avg(self.active_path_endpoint_to_goal),
            "active_path_endpoint_to_goal_distance_max": max(self.active_path_endpoint_to_goal) if self.active_path_endpoint_to_goal else 0.0,
            "active_path_stale_duration_sec": self.active_path_same_hash_max,
            "active_path_same_hash_max_duration_sec": self.active_path_same_hash_max,
            "travel_traj_msg_count": self.msg_count.get("/planning/travel_traj", 0),
            "travel_traj_update_count": self.travel_update_count,
            "travel_traj_endpoint": self.travel_endpoint,
            "travel_traj_endpoint_to_goal_distance_avg": self.avg(self.travel_endpoint_to_goal),
            "travel_traj_same_hash_max_duration_sec": self.travel_same_hash_max,
            "position_cmd_msg_count": self.msg_count.get("/planning/pos_cmd", 0) + self.msg_count.get("/fuel/p10_lite/position_cmd", 0),
            "position_cmd_update_count": self.cmd_update_count,
            "position_cmd_total_variation": self.cmd_total_variation,
            "position_cmd_to_odom_distance_avg": self.avg(self.cmd_to_odom),
            "position_cmd_to_odom_distance_max": max(self.cmd_to_odom) if self.cmd_to_odom else 0.0,
            "position_cmd_same_pose_max_duration_sec": self.cmd_same_pose_max,
            "traj_server_status_count": self.msg_count.get("/fuel/p10_lite/traj_server_status", 0),
            "traj_server_stale_path_hold_count": self.traj_server_stale_path_hold_count,
            "traj_server_status_events": self.traj_server_events[-20:],
            "quadrotor_sim_status_count": self.msg_count.get("/fuel/p10_lite/quadrotor_sim_status", 0),
            "quadrotor_sim_motion_blocked_count": self.quad_motion_blocked_count,
            "quadrotor_sim_status_events": self.quad_events[-20:],
            "frontier_viewpoint_count_series": self.frontier_viewpoints_series,
            "frontier_candidate_count_series": self.frontier_candidates_series,
            "frontier_count_start": self.frontier_candidates_series[0] if self.frontier_candidates_series else 0,
            "frontier_count_end": self.frontier_candidates_series[-1] if self.frontier_candidates_series else 0,
            "main_chain_break": self.main_chain_break(),
            "status_latest": self.status_latest,
        }
        with open(os.path.join(out_dir, "motion_chain.json"), "w", encoding="utf-8") as f:
            json.dump(chain, f, indent=2)
        with open(os.path.join(out_dir, "motion_chain.md"), "w", encoding="utf-8") as f:
            f.write(f"# P2D Motion Chain {self.args.run_id}\n\n")
            for key, value in chain.items():
                if key.endswith("_events") or key.endswith("_series") or key == "status_latest":
                    continue
                f.write(f"- {key}: {value}\n")
        with open(os.path.join(out_dir, "motion_chain_timeseries.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(Sample.__annotations__.keys()))
            writer.writeheader()
            for sample in self.samples:
                writer.writerow(sample.__dict__)
        with open(os.path.join(out_dir, "events.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["time_sec", "event_type", "detail"])
            writer.writeheader()
            for event in self.events:
                writer.writerow(event)
        return chain


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=300.0)
    parser.add_argument("--run-id", default=time.strftime("p2d_%Y%m%d_%H%M%S"))
    parser.add_argument("--output-root", default="reports/p2d_metrics")
    parser.add_argument("--sample-period", type=float, default=1.0)
    parser.add_argument("--progress-interval", type=float, default=30.0)
    args = parser.parse_args()
    rclpy.init()
    node = MotionChainRecorder(args)
    try:
        node.run()
        chain = node.write_outputs()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    print("P2D_MOTION_CHAIN_RECORDER_RESULT")
    for key in [
        "run_id", "duration_sec", "odom_total_distance", "odom_net_displacement",
        "goal_switch_count", "active_path_update_count", "active_path_same_hash_max_duration_sec",
        "travel_traj_update_count", "travel_traj_same_hash_max_duration_sec",
        "position_cmd_update_count", "position_cmd_total_variation",
        "position_cmd_same_pose_max_duration_sec", "position_cmd_to_odom_distance_avg",
        "traj_server_stale_path_hold_count", "quadrotor_sim_motion_blocked_count", "main_chain_break",
    ]:
        print(f"{key}={chain.get(key)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
