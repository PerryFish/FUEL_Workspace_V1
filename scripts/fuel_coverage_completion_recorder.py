#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import math
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path as RosPath
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

Point = Tuple[float, float, float]


def dist(a: Point, b: Point) -> float:
    return math.dist(a, b)


def avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


class CoverageCompletionRecorder(Node):
    def __init__(self, args):
        super().__init__("fuel_coverage_completion_recorder")
        self.args = args
        self.start_wall = time.time()
        self.end_wall = self.start_wall + args.duration
        self.samples: List[Dict] = []
        self.events: List[Dict] = []
        self.status_latest: Dict[str, str] = {}
        self.msg_count: Dict[str, int] = {}

        self.odom_start: Optional[Point] = None
        self.odom_last: Optional[Point] = None
        self.odom_total_distance = 0.0
        self.odom_last_motion_wall = self.start_wall
        self.odom_max_no_motion = 0.0

        self.goal_last: Optional[Point] = None
        self.goal_points: List[Tuple[float, Point]] = []
        self.goal_switch_count = 0
        self.goal_segments: List[Tuple[float, float, Point]] = []
        self.current_goal_start = 0.0

        self.active_path_hash = ""
        self.active_path_update_count = 0
        self.active_path_same_start = self.start_wall
        self.active_path_same_max = 0.0
        self.active_path_endpoint: Optional[Point] = None
        self.active_path_endpoint_to_goal: List[float] = []
        self.active_path_done_event_count = 0
        self.path_done_without_reselect_count = 0
        self.last_path_done_wall = -999.0

        self.travel_hash = ""
        self.travel_update_count = 0
        self.position_cmd_last: Optional[Point] = None
        self.position_cmd_update_count = 0
        self.position_cmd_total_variation = 0.0
        self.position_cmd_same_start = self.start_wall
        self.position_cmd_idle_max = 0.0

        self.frontier_candidates = 0
        self.frontier_viewpoints = 0
        self.frontier_series: List[Tuple[float, int]] = []
        self.explored_start: Optional[int] = None
        self.explored_end = 0
        self.occupancy_end = 0
        self.local_free_end = 0
        self.local_occupied_end = 0
        self.global_cloud_points = 0
        self.coverage_series: List[Tuple[float, float]] = []
        self.coverage_stall_events: List[Dict] = []
        self.coverage_stall_active = False
        self.coverage_stall_start = 0.0
        self.coverage_stall_max = 0.0
        self.coverage_stall_without_reselect_count = 0

        self.goal_reselect_count = 0
        self.goal_reselect_after_path_done_count = 0
        self.goal_reselect_after_coverage_stall_count = 0
        self.goal_reselect_after_no_motion_count = 0

        self.create_subscription(Odometry, "/odom", self.odom_cb, 20)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self.goal_cb, 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/best_viewpoint", lambda m: self.tick("/fuel/p11_lite/best_viewpoint"), 10)
        for topic in ["/fuel/p10_lite/position_cmd", "/planning/pos_cmd"]:
            self.create_subscription(PoseStamped, topic, lambda m, t=topic: self.cmd_cb(t, m), 10)
        for topic in ["/fuel/p10_lite/active_path", "/planning/travel_traj"]:
            self.create_subscription(RosPath, topic, lambda m, t=topic: self.path_cb(t, m), 10)
        for topic in ["/fuel/p11_lite/exploration_manager_status", "/fuel/p11_lite/goal_to_path_status"]:
            self.create_subscription(String, topic, lambda m, t=topic: self.status_cb(t, m), 10)
        for topic in [
            "/fuel/p11_lite/frontier_candidates_raw",
            "/fuel/p11_lite/frontier_viewpoints",
            "/fuel/p11_lite/explored_grid",
            "/fuel/p11_lite/occupancy_grid",
            "/fuel/p11_lite/local_free_points",
            "/fuel/p11_lite/local_occupied_points",
            "/map_generator/global_cloud",
            "/pcl_render_node/cloud",
        ]:
            self.create_subscription(PointCloud2, topic, lambda m, t=topic: self.cloud_cb(t, m), 10)

    def elapsed(self) -> float:
        return time.time() - self.start_wall

    def tick(self, topic: str) -> None:
        self.msg_count[topic] = self.msg_count.get(topic, 0) + 1

    @staticmethod
    def pose_point(msg: PoseStamped) -> Point:
        p = msg.pose.position
        return float(p.x), float(p.y), float(p.z)

    @staticmethod
    def path_points(msg: RosPath) -> List[Point]:
        return [(float(p.pose.position.x), float(p.pose.position.y), float(p.pose.position.z)) for p in msg.poses]

    @staticmethod
    def hash_points(points: List[Point]) -> str:
        return hashlib.sha1(";".join(f"{x:.2f},{y:.2f},{z:.2f}" for x, y, z in points).encode()).hexdigest()

    def current_goal(self) -> Optional[Point]:
        return self.goal_points[-1][1] if self.goal_points else None

    def odom_cb(self, msg: Odometry) -> None:
        self.tick("/odom")
        p = msg.pose.pose.position
        now = time.time()
        point = (float(p.x), float(p.y), float(p.z))
        if self.odom_start is None:
            self.odom_start = point
        if self.odom_last is not None:
            step = dist(self.odom_last, point)
            self.odom_total_distance += step
            if step > 0.02:
                self.odom_max_no_motion = max(self.odom_max_no_motion, now - self.odom_last_motion_wall)
                self.odom_last_motion_wall = now
        self.odom_last = point

    def goal_cb(self, msg: PoseStamped) -> None:
        self.tick("/fuel/p11_lite/exploration_goal")
        point = self.pose_point(msg)
        now_e = self.elapsed()
        if self.goal_last is None:
            self.current_goal_start = now_e
        elif dist(self.goal_last, point) > 0.5:
            self.goal_switch_count += 1
            self.goal_reselect_count += 1
            self.goal_segments.append((self.current_goal_start, now_e, self.goal_last))
            if time.time() - self.last_path_done_wall <= 15.0:
                self.goal_reselect_after_path_done_count += 1
            if self.coverage_stall_active or (self.coverage_stall_events and now_e - self.coverage_stall_events[-1]["end_sec"] <= 15.0):
                self.goal_reselect_after_coverage_stall_count += 1
            if time.time() - self.odom_last_motion_wall >= 20.0:
                self.goal_reselect_after_no_motion_count += 1
            self.current_goal_start = now_e
        self.goal_last = point
        self.goal_points.append((now_e, point))

    def path_cb(self, topic: str, msg: RosPath) -> None:
        self.tick(topic)
        points = self.path_points(msg)
        h = self.hash_points(points)
        now = time.time()
        if topic == "/fuel/p10_lite/active_path":
            if h != self.active_path_hash:
                self.active_path_same_max = max(self.active_path_same_max, now - self.active_path_same_start)
                self.active_path_same_start = now
                self.active_path_hash = h
                self.active_path_update_count += 1
            self.active_path_endpoint = points[-1] if points else None
            goal = self.current_goal()
            if self.active_path_endpoint and goal:
                self.active_path_endpoint_to_goal.append(dist(self.active_path_endpoint, goal))
                if self.odom_last and dist(self.odom_last, self.active_path_endpoint) < 0.8:
                    if now - self.last_path_done_wall > 5.0:
                        self.active_path_done_event_count += 1
                        self.events.append({"time_sec": self.elapsed(), "type": "PATH_DONE"})
                    self.last_path_done_wall = now
        elif topic == "/planning/travel_traj":
            if h != self.travel_hash:
                self.travel_hash = h
                self.travel_update_count += 1

    def cmd_cb(self, topic: str, msg: PoseStamped) -> None:
        self.tick(topic)
        point = self.pose_point(msg)
        now = time.time()
        if self.position_cmd_last is None or dist(self.position_cmd_last, point) > 0.02:
            self.position_cmd_idle_max = max(self.position_cmd_idle_max, now - self.position_cmd_same_start)
            self.position_cmd_same_start = now
            self.position_cmd_update_count += 1
            if self.position_cmd_last is not None:
                self.position_cmd_total_variation += dist(self.position_cmd_last, point)
        self.position_cmd_last = point

    @staticmethod
    def field(text: str, key: str, default: str = "UNAVAILABLE") -> str:
        token = f"{key}="
        for part in text.split():
            if part.startswith(token):
                return part[len(token):]
        return default

    def status_cb(self, topic: str, msg: String) -> None:
        self.tick(topic)
        self.status_latest[topic] = msg.data
        if topic == "/fuel/p11_lite/exploration_manager_status":
            reason = self.field(msg.data, "last_switch_reason", self.field(msg.data, "switch_reason", ""))
            if "coverage_stall" in reason:
                self.goal_reselect_after_coverage_stall_count = max(self.goal_reselect_after_coverage_stall_count, self.goal_reselect_after_coverage_stall_count + 1)
            if "path_done" in reason or "goal_reached" in reason:
                self.goal_reselect_after_path_done_count = max(self.goal_reselect_after_path_done_count, self.goal_reselect_after_path_done_count + 1)

    def cloud_cb(self, topic: str, msg: PointCloud2) -> None:
        self.tick(topic)
        n = int(msg.width * msg.height)
        if topic == "/fuel/p11_lite/frontier_candidates_raw":
            self.frontier_candidates = n
            self.frontier_series.append((self.elapsed(), n))
        elif topic == "/fuel/p11_lite/frontier_viewpoints":
            self.frontier_viewpoints = n
        elif topic == "/fuel/p11_lite/explored_grid":
            if self.explored_start is None:
                self.explored_start = n
            self.explored_end = n
            self.record_coverage()
        elif topic == "/fuel/p11_lite/occupancy_grid":
            self.occupancy_end = n
        elif topic == "/fuel/p11_lite/local_free_points":
            self.local_free_end = n
        elif topic == "/fuel/p11_lite/local_occupied_points":
            self.local_occupied_end = n
        elif topic == "/map_generator/global_cloud":
            self.global_cloud_points = max(self.global_cloud_points, n)
            self.record_coverage()
        elif topic == "/pcl_render_node/cloud":
            pass

    def coverage_proxy(self) -> float:
        if self.global_cloud_points < 1000:
            return 0.0
        return float(self.explored_end) / float(self.global_cloud_points)

    def record_coverage(self) -> None:
        if self.global_cloud_points < 1000:
            return
        self.coverage_series.append((self.elapsed(), self.coverage_proxy()))

    def window_coverage_gain(self, window: float) -> float:
        recent = [(t, v) for t, v in self.coverage_series if self.elapsed() - t <= window]
        if len(recent) < 2:
            return 0.0
        return recent[-1][1] - recent[0][1]

    def sample(self) -> None:
        t = self.elapsed()
        cov = self.coverage_proxy()
        frontier = self.frontier_candidates or self.frontier_viewpoints
        stall = self.window_coverage_gain(30.0) < 0.005 and frontier > 20
        if stall and not self.coverage_stall_active:
            self.coverage_stall_active = True
            self.coverage_stall_start = t
        elif not stall and self.coverage_stall_active:
            dur = t - self.coverage_stall_start
            self.coverage_stall_max = max(self.coverage_stall_max, dur)
            self.coverage_stall_events.append({"start_sec": self.coverage_stall_start, "end_sec": t, "duration_sec": dur})
            if self.goal_reselect_count == 0 or (self.goal_points and self.goal_points[-1][0] < self.coverage_stall_start):
                self.coverage_stall_without_reselect_count += 1
            self.coverage_stall_active = False
        if time.time() - self.last_path_done_wall > 20.0 and self.last_path_done_wall > 0 and self.goal_points:
            if self.goal_points[-1][0] < self.elapsed() - (time.time() - self.last_path_done_wall):
                self.path_done_without_reselect_count += 1
                self.last_path_done_wall = -999.0
        self.samples.append({
            "time_sec": t,
            "odom_total_distance": self.odom_total_distance,
            "coverage_proxy": cov,
            "coverage_gain": cov - (self.coverage_series[0][1] if self.coverage_series else cov),
            "frontier_count": frontier,
            "active_path_update_count": self.active_path_update_count,
            "position_cmd_update_count": self.position_cmd_update_count,
            "goal_reselect_count": self.goal_reselect_count,
            "coverage_stall_event_count": len(self.coverage_stall_events) + (1 if self.coverage_stall_active else 0),
        })

    def result(self) -> Dict:
        now = time.time()
        self.active_path_same_max = max(self.active_path_same_max, now - self.active_path_same_start)
        self.position_cmd_idle_max = max(self.position_cmd_idle_max, now - self.position_cmd_same_start)
        if self.coverage_stall_active:
            dur = self.elapsed() - self.coverage_stall_start
            self.coverage_stall_max = max(self.coverage_stall_max, dur)
        start_cov = self.coverage_series[0][1] if self.coverage_series else 0.0
        end_cov = self.coverage_proxy()
        gain = end_cov - start_cov
        frontier_values = [v for _t, v in self.frontier_series]
        if (
            self.coverage_stall_max >= 90.0
            and (self.frontier_candidates or self.frontier_viewpoints) > 20
            and self.coverage_stall_without_reselect_count > 0
        ):
            blocker = "COVERAGE_STALL_NO_RESELECT"
        elif self.path_done_without_reselect_count > 0:
            blocker = "PATH_DONE_NO_RESELECT"
        elif (self.frontier_candidates or self.frontier_viewpoints) > 50 and gain < 0.02:
            blocker = "FRONTIER_SCORING_OR_REACHABILITY_LIMIT"
        elif gain < 0.005 and (self.frontier_candidates or self.frontier_viewpoints) <= 5:
            blocker = "COVERAGE_SATURATED"
        else:
            blocker = "COVERAGE_GROWING"
        return {
            "duration_sec": self.elapsed(),
            "odom_total_distance": self.odom_total_distance,
            "odom_net_displacement": dist(self.odom_start, self.odom_last) if self.odom_start and self.odom_last else 0.0,
            "odom_max_no_motion_duration_sec": max(self.odom_max_no_motion, now - self.odom_last_motion_wall),
            "coverage_proxy_start": start_cov,
            "coverage_proxy_end": end_cov,
            "coverage_proxy_gain": gain,
            "coverage_proxy_gain_per_min": gain / max(self.elapsed() / 60.0, 1e-6),
            "coverage_stall_event_count": len(self.coverage_stall_events) + (1 if self.coverage_stall_active else 0),
            "coverage_stall_max_duration_sec": self.coverage_stall_max,
            "coverage_stall_events": self.coverage_stall_events,
            "explored_grid_start": self.explored_start or 0,
            "explored_grid_end": self.explored_end,
            "explored_grid_gain": self.explored_end - (self.explored_start or self.explored_end),
            "global_cloud_points": self.global_cloud_points,
            "frontier_count_start": frontier_values[0] if frontier_values else 0,
            "frontier_count_end": frontier_values[-1] if frontier_values else 0,
            "frontier_count_avg": avg([float(v) for v in frontier_values]),
            "frontier_nonzero_duration_sec": sum(1 for s in self.samples if s["frontier_count"] > 0) * self.args.progress_interval,
            "frontier_zero_duration_sec": sum(1 for s in self.samples if s["frontier_count"] == 0) * self.args.progress_interval,
            "goal_msg_count": self.msg_count.get("/fuel/p11_lite/exploration_goal", 0),
            "goal_switch_count": self.goal_switch_count,
            "unique_goal_count": len({(round(p[0], 1), round(p[1], 1), round(p[2], 1)) for _t, p in self.goal_points}),
            "same_goal_max_duration_sec": max([b - a for a, b, _p in self.goal_segments] or [self.elapsed() - self.current_goal_start if self.goal_points else 0.0]),
            "goal_reselect_count": self.goal_reselect_count,
            "goal_reselect_after_path_done_count": self.goal_reselect_after_path_done_count,
            "goal_reselect_after_coverage_stall_count": self.goal_reselect_after_coverage_stall_count,
            "goal_reselect_after_no_motion_count": self.goal_reselect_after_no_motion_count,
            "active_path_update_count": self.active_path_update_count,
            "active_path_done_event_count": self.active_path_done_event_count,
            "active_path_same_hash_max_duration_sec": self.active_path_same_max,
            "active_path_endpoint_to_goal_distance_avg": avg(self.active_path_endpoint_to_goal),
            "position_cmd_update_count": self.position_cmd_update_count,
            "position_cmd_total_variation": self.position_cmd_total_variation,
            "position_cmd_idle_duration_sec": self.position_cmd_idle_max,
            "path_done_without_reselect_count": self.path_done_without_reselect_count,
            "coverage_stall_without_reselect_count": self.coverage_stall_without_reselect_count,
            "main_coverage_blocker": blocker,
            "status_latest": self.status_latest,
        }

    def run(self) -> Dict:
        last = time.time()
        while rclpy.ok() and time.time() < self.end_wall:
            rclpy.spin_once(self, timeout_sec=0.2)
            if time.time() - last >= self.args.progress_interval:
                last = time.time()
                self.sample()
                latest = self.samples[-1]
                print(
                    "P2F_COVERAGE_PROGRESS "
                    f"time={latest['time_sec']:.1f} "
                    f"odom_total_distance={latest['odom_total_distance']:.3f} "
                    f"coverage_proxy={latest['coverage_proxy']:.6f} "
                    f"coverage_gain={latest['coverage_gain']:.6f} "
                    f"frontier_count={latest['frontier_count']} "
                    f"active_path_update_count={latest['active_path_update_count']} "
                    f"position_cmd_update_count={latest['position_cmd_update_count']} "
                    f"goal_reselect_count={latest['goal_reselect_count']} "
                    f"coverage_stall_event_count={latest['coverage_stall_event_count']}",
                    flush=True,
                )
        self.sample()
        return self.result()


def write_outputs(root: Path, run_id: str, metrics: Dict, samples: List[Dict], events: List[Dict]) -> None:
    out = root / run_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "coverage_completion.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    with (out / "coverage_timeseries.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(samples[0].keys()) if samples else ["time_sec"])
        writer.writeheader()
        writer.writerows(samples)
    with (out / "coverage_events.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["time_sec", "type"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(events)
    md = ["# P2F Coverage Completion Metrics", ""]
    for key, value in metrics.items():
        if key in ("status_latest", "coverage_stall_events"):
            continue
        md.append(f"- {key}: {value}")
    (out / "coverage_completion.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=300.0)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", default="reports/p2f_metrics")
    parser.add_argument("--progress-interval", type=float, default=30.0)
    args = parser.parse_args()
    rclpy.init()
    node = CoverageCompletionRecorder(args)
    try:
        metrics = node.run()
        write_outputs(Path(args.output_root), args.run_id, metrics, node.samples, node.events)
        print("P2F_COVERAGE_COMPLETION_RESULT")
        for key in [
            "duration_sec",
            "odom_total_distance",
            "coverage_proxy_start",
            "coverage_proxy_end",
            "coverage_proxy_gain",
            "coverage_stall_max_duration_sec",
            "frontier_count_end",
            "active_path_update_count",
            "position_cmd_update_count",
            "goal_reselect_after_path_done_count",
            "goal_reselect_after_coverage_stall_count",
            "path_done_without_reselect_count",
            "coverage_stall_without_reselect_count",
            "main_coverage_blocker",
        ]:
            print(f"{key}={metrics.get(key, 'UNAVAILABLE')}")
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
