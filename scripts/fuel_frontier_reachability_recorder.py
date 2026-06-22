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


def d(a: Point, b: Point) -> float:
    return math.dist(a, b)


def avg(v: List[float]) -> float:
    return sum(v) / len(v) if v else 0.0


class FrontierReachabilityRecorder(Node):
    def __init__(self, args):
        super().__init__("fuel_frontier_reachability_recorder")
        self.args = args
        self.start = time.time()
        self.end = self.start + args.duration
        self.samples: List[Dict] = []
        self.events: List[Dict] = []
        self.msg_count: Dict[str, int] = {}
        self.status_latest: Dict[str, str] = {}

        self.odom_start: Optional[Point] = None
        self.odom_last: Optional[Point] = None
        self.odom_total = 0.0
        self.goal_points: List[Tuple[float, Point]] = []
        self.best_points: List[Tuple[float, Point]] = []
        self.goal_regions: Dict[Tuple[int, int], float] = {}
        self.region_current: Optional[Tuple[int, int]] = None
        self.region_start = 0.0
        self.region_max_duration = 0.0

        self.active_path_hash = ""
        self.active_path_updates = 0
        self.active_path_endpoint_to_goal: List[float] = []
        self.active_path_endpoint_to_best: List[float] = []
        self.active_path_lengths: List[float] = []
        self.cmd_hash = ""
        self.cmd_updates = 0

        self.frontier_candidate_series: List[int] = []
        self.frontier_viewpoint_series: List[int] = []
        self.explored_start: Optional[int] = None
        self.explored_end = 0
        self.global_cloud = 0
        self.coverage_series: List[Tuple[float, float]] = []
        self.coverage_stall_start: Optional[float] = None
        self.coverage_stall_max = 0.0

        self.unreachable_goal_count = 0
        self.goal_blacklist_count = 0
        self.recent_region_penalty_count = 0
        self.score_reject_count = 0
        self.reachability_reject_count = 0
        self.gain_reject_count = 0
        self.low_gain_goal_count = 0
        self.coverage_at_goal: List[Tuple[float, float]] = []
        self.coverage_gain_after_goal: List[float] = []
        self.last_goal_coverage = 0.0

        self.create_subscription(Odometry, "/odom", self.odom_cb, 20)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self.goal_cb, 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/best_viewpoint", self.best_cb, 10)
        for topic in ["/fuel/p10_lite/position_cmd", "/planning/pos_cmd"]:
            self.create_subscription(PoseStamped, topic, lambda m, t=topic: self.cmd_cb(t, m), 10)
        for topic in ["/fuel/p10_lite/active_path", "/planning/travel_traj"]:
            self.create_subscription(RosPath, topic, lambda m, t=topic: self.path_cb(t, m), 10)
        for topic in ["/fuel/p11_lite/exploration_manager_status", "/fuel/p11_lite/goal_to_path_status", "/fuel/p11_lite/frontier_status"]:
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
        return time.time() - self.start

    def tick(self, topic: str) -> None:
        self.msg_count[topic] = self.msg_count.get(topic, 0) + 1

    @staticmethod
    def pose(msg: PoseStamped) -> Point:
        p = msg.pose.position
        return float(p.x), float(p.y), float(p.z)

    @staticmethod
    def region(p: Point, size: float = 2.0) -> Tuple[int, int]:
        return int(math.floor(p[0] / size)), int(math.floor(p[1] / size))

    @staticmethod
    def path_points(msg: RosPath) -> List[Point]:
        return [(float(p.pose.position.x), float(p.pose.position.y), float(p.pose.position.z)) for p in msg.poses]

    @staticmethod
    def h(points: List[Point]) -> str:
        return hashlib.sha1(";".join(f"{x:.2f},{y:.2f},{z:.2f}" for x, y, z in points).encode()).hexdigest()

    @staticmethod
    def field(text: str, key: str, default: str = "") -> str:
        token = f"{key}="
        for part in text.split():
            if part.startswith(token):
                return part[len(token):]
        return default

    def coverage(self) -> float:
        if self.global_cloud < 1000:
            return 0.0
        return float(self.explored_end) / float(self.global_cloud)

    def odom_cb(self, msg: Odometry) -> None:
        self.tick("/odom")
        p = msg.pose.pose.position
        cur = (float(p.x), float(p.y), float(p.z))
        if self.odom_start is None:
            self.odom_start = cur
        if self.odom_last is not None:
            self.odom_total += d(self.odom_last, cur)
        self.odom_last = cur

    def goal_cb(self, msg: PoseStamped) -> None:
        self.tick("/fuel/p11_lite/exploration_goal")
        p = self.pose(msg)
        now = self.elapsed()
        if not self.goal_points or d(self.goal_points[-1][1], p) > 0.5:
            if self.goal_points:
                gain = self.coverage() - self.last_goal_coverage
                self.coverage_gain_after_goal.append(gain)
                if gain < 0.003:
                    self.low_gain_goal_count += 1
            self.last_goal_coverage = self.coverage()
            r = self.region(p)
            if self.region_current is not None:
                self.region_max_duration = max(self.region_max_duration, now - self.region_start)
            self.region_current = r
            self.region_start = now
            self.goal_regions[r] = self.goal_regions.get(r, 0.0) + 1.0
        self.goal_points.append((now, p))

    def best_cb(self, msg: PoseStamped) -> None:
        self.tick("/fuel/p11_lite/best_viewpoint")
        self.best_points.append((self.elapsed(), self.pose(msg)))

    def cmd_cb(self, topic: str, msg: PoseStamped) -> None:
        self.tick(topic)
        p = self.pose(msg)
        h = f"{p[0]:.2f},{p[1]:.2f},{p[2]:.2f}"
        if h != self.cmd_hash:
            self.cmd_hash = h
            self.cmd_updates += 1

    def path_cb(self, topic: str, msg: RosPath) -> None:
        self.tick(topic)
        pts = self.path_points(msg)
        if topic != "/fuel/p10_lite/active_path":
            return
        ph = self.h(pts)
        if ph != self.active_path_hash:
            self.active_path_hash = ph
            self.active_path_updates += 1
        if pts:
            self.active_path_lengths.append(sum(d(a, b) for a, b in zip(pts, pts[1:])))
            endpoint = pts[-1]
            if self.goal_points:
                self.active_path_endpoint_to_goal.append(d(endpoint, self.goal_points[-1][1]))
            if self.best_points:
                self.active_path_endpoint_to_best.append(d(endpoint, self.best_points[-1][1]))

    def status_cb(self, topic: str, msg: String) -> None:
        self.tick(topic)
        self.status_latest[topic] = msg.data
        text = msg.data
        if topic == "/fuel/p11_lite/goal_to_path_status":
            feasible = self.field(text, "path_feasible", "true")
            valid = self.field(text, "path_valid", "true")
            try:
                ep = float(self.field(text, "endpoint_to_goal_distance", "0"))
            except ValueError:
                ep = 0.0
            if feasible == "false" or valid == "false" or ep > 1.5:
                self.unreachable_goal_count += 1
                self.reachability_reject_count += 1
        if topic == "/fuel/p11_lite/exploration_manager_status":
            lower = text.lower()
            if "recent_region" in lower:
                self.recent_region_penalty_count += 1
            if "blacklist" in lower or "retired" in lower:
                self.goal_blacklist_count += 1
            if "low_gain" in lower:
                self.gain_reject_count += 1
            if "blocked_by_score" in lower:
                self.score_reject_count += 1

    def cloud_cb(self, topic: str, msg: PointCloud2) -> None:
        self.tick(topic)
        n = int(msg.width * msg.height)
        if topic == "/fuel/p11_lite/frontier_candidates_raw":
            self.frontier_candidate_series.append(n)
        elif topic == "/fuel/p11_lite/frontier_viewpoints":
            self.frontier_viewpoint_series.append(n)
        elif topic == "/fuel/p11_lite/explored_grid":
            if self.explored_start is None:
                self.explored_start = n
            self.explored_end = n
            if self.global_cloud >= 1000:
                self.coverage_series.append((self.elapsed(), self.coverage()))
        elif topic == "/map_generator/global_cloud":
            self.global_cloud = max(self.global_cloud, n)
            if self.global_cloud >= 1000:
                self.coverage_series.append((self.elapsed(), self.coverage()))

    def sample(self) -> None:
        now = self.elapsed()
        cov = self.coverage()
        frontier = self.frontier_candidate_series[-1] if self.frontier_candidate_series else 0
        if len(self.coverage_series) >= 2:
            recent = [(t, c) for t, c in self.coverage_series if now - t <= 30.0]
            gain = recent[-1][1] - recent[0][1] if len(recent) >= 2 else 0.0
        else:
            gain = 0.0
        if gain < 0.005 and frontier > 20:
            if self.coverage_stall_start is None:
                self.coverage_stall_start = now
            self.coverage_stall_max = max(self.coverage_stall_max, now - self.coverage_stall_start)
        else:
            self.coverage_stall_start = None
        row = {
            "time_sec": now,
            "odom_total_distance": self.odom_total,
            "coverage_proxy": cov,
            "coverage_gain": (cov - self.coverage_series[0][1]) if self.coverage_series else 0.0,
            "frontier_candidate_count": frontier,
            "frontier_viewpoint_count": self.frontier_viewpoint_series[-1] if self.frontier_viewpoint_series else 0,
            "selected_goal_unique_count": len({(round(p[0], 1), round(p[1], 1), round(p[2], 1)) for _t, p in self.goal_points}),
            "active_path_endpoint_to_goal_distance_avg": avg(self.active_path_endpoint_to_goal),
            "unreachable_goal_ratio": self.unreachable_goal_ratio(),
            "coverage_stall_max_duration": self.coverage_stall_max,
            "main_frontier_blocker": self.blocker(),
        }
        self.samples.append(row)
        print(
            "P2G_FRONTIER_PROGRESS "
            + " ".join(f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}" for k, v in row.items()),
            flush=True,
        )

    def unreachable_goal_ratio(self) -> float:
        denom = max(self.msg_count.get("/fuel/p11_lite/goal_to_path_status", 0), 1)
        return float(self.unreachable_goal_count) / float(denom)

    def blocker(self) -> str:
        ep_avg = avg(self.active_path_endpoint_to_goal)
        gain = (self.coverage() - self.coverage_series[0][1]) if self.coverage_series else 0.0
        fc = self.frontier_candidate_series[-1] if self.frontier_candidate_series else 0
        unique_regions = len(self.goal_regions)
        if ep_avg > 1.5 or self.unreachable_goal_ratio() > 0.2:
            return "PATH_ENDPOINT_FAR_FROM_GOAL"
        if unique_regions <= 3 and fc > 50 and len(self.goal_points) > 30:
            return "LOCAL_REGION_RESELECTION"
        if len(self.coverage_gain_after_goal) >= 3 and avg(self.coverage_gain_after_goal[-5:]) < 0.003:
            return "LOW_GAIN_FRONTIER"
        if fc > 50 and gain < 0.02:
            return "FRONTIER_SCORE_PLATEAU"
        if fc <= 5 and gain < 0.005:
            return "COVERAGE_NEAR_SATURATED"
        return "COVERAGE_GROWING"

    def result(self) -> Dict:
        if self.goal_points:
            self.region_max_duration = max(self.region_max_duration, self.elapsed() - self.region_start)
        start_cov = self.coverage_series[0][1] if self.coverage_series else 0.0
        end_cov = self.coverage()
        best_dists = [d(p, self.odom_last) for _t, p in self.best_points if self.odom_last is not None]
        goal_points = [p for _t, p in self.goal_points]
        frontier_to_goal = []
        if self.odom_last and goal_points:
            frontier_to_goal = [d(self.odom_last, p) for p in goal_points[-50:]]
        data = {
            "duration_sec": self.elapsed(),
            "odom_total_distance": self.odom_total,
            "odom_net_displacement": d(self.odom_start, self.odom_last) if self.odom_start and self.odom_last else 0.0,
            "coverage_proxy_start": start_cov,
            "coverage_proxy_end": end_cov,
            "coverage_proxy_gain": end_cov - start_cov,
            "coverage_stall_max_duration_sec": self.coverage_stall_max,
            "frontier_candidate_count_start": self.frontier_candidate_series[0] if self.frontier_candidate_series else 0,
            "frontier_candidate_count_end": self.frontier_candidate_series[-1] if self.frontier_candidate_series else 0,
            "frontier_candidate_count_avg": avg([float(x) for x in self.frontier_candidate_series]),
            "frontier_viewpoint_count_start": self.frontier_viewpoint_series[0] if self.frontier_viewpoint_series else 0,
            "frontier_viewpoint_count_end": self.frontier_viewpoint_series[-1] if self.frontier_viewpoint_series else 0,
            "frontier_viewpoint_count_avg": avg([float(x) for x in self.frontier_viewpoint_series]),
            "selected_goal_count": len(self.goal_points),
            "selected_goal_unique_count": len({(round(p[0], 1), round(p[1], 1), round(p[2], 1)) for p in goal_points}),
            "selected_goal_region_count": len(self.goal_regions),
            "selected_goal_same_region_max_duration_sec": self.region_max_duration,
            "best_viewpoint_count": len(self.best_points),
            "best_viewpoint_unique_count": len({(round(p[0], 1), round(p[1], 1), round(p[2], 1)) for _t, p in self.best_points}),
            "best_viewpoint_to_odom_distance_avg": avg(best_dists),
            "best_viewpoint_to_odom_distance_min": min(best_dists) if best_dists else 0.0,
            "best_viewpoint_to_odom_distance_max": max(best_dists) if best_dists else 0.0,
            "active_path_update_count": self.active_path_updates,
            "active_path_endpoint_to_goal_distance_avg": avg(self.active_path_endpoint_to_goal),
            "active_path_endpoint_to_goal_distance_max": max(self.active_path_endpoint_to_goal) if self.active_path_endpoint_to_goal else 0.0,
            "active_path_endpoint_to_best_viewpoint_distance_avg": avg(self.active_path_endpoint_to_best),
            "active_path_length_avg": avg(self.active_path_lengths),
            "active_path_length_max": max(self.active_path_lengths) if self.active_path_lengths else 0.0,
            "frontier_to_goal_distance_avg": avg(frontier_to_goal),
            "frontier_to_goal_distance_min": min(frontier_to_goal) if frontier_to_goal else 0.0,
            "frontier_to_goal_distance_max": max(frontier_to_goal) if frontier_to_goal else 0.0,
            "unreachable_goal_count": self.unreachable_goal_count,
            "unreachable_goal_ratio": self.unreachable_goal_ratio(),
            "goal_blacklist_count": self.goal_blacklist_count,
            "recent_region_penalty_count": self.recent_region_penalty_count,
            "score_reject_count": self.score_reject_count,
            "reachability_reject_count": self.reachability_reject_count,
            "gain_reject_count": self.gain_reject_count,
            "coverage_gain_after_goal_avg": avg(self.coverage_gain_after_goal),
            "coverage_gain_after_goal_min": min(self.coverage_gain_after_goal) if self.coverage_gain_after_goal else 0.0,
            "coverage_gain_after_goal_max": max(self.coverage_gain_after_goal) if self.coverage_gain_after_goal else 0.0,
            "low_gain_goal_count": self.low_gain_goal_count,
            "main_frontier_blocker": self.blocker(),
        }
        return data

    def run(self) -> Dict:
        last = time.time()
        while rclpy.ok() and time.time() < self.end:
            rclpy.spin_once(self, timeout_sec=0.2)
            if time.time() - last >= self.args.progress_interval:
                last = time.time()
                self.sample()
        self.sample()
        return self.result()


def write_outputs(root: Path, run_id: str, metrics: Dict, samples: List[Dict], events: List[Dict]) -> None:
    out = root / run_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "frontier_reachability.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    md = ["# P2G Frontier Reachability Metrics", ""]
    for k, v in metrics.items():
        md.append(f"- {k}: {v}")
    (out / "frontier_reachability.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    if samples:
        with (out / "frontier_timeseries.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(samples[0].keys()))
            w.writeheader()
            w.writerows(samples)
    with (out / "frontier_events.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["time_sec", "type"], extrasaction="ignore")
        w.writeheader()
        w.writerows(events)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=300.0)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", default="reports/p2g_metrics")
    parser.add_argument("--progress-interval", type=float, default=30.0)
    args = parser.parse_args()
    rclpy.init()
    node = FrontierReachabilityRecorder(args)
    try:
        metrics = node.run()
        write_outputs(Path(args.output_root), args.run_id, metrics, node.samples, node.events)
        result = "PASS" if metrics["coverage_proxy_gain"] > 0.05 and metrics["odom_total_distance"] > 20.0 else "PARTIAL"
        print("P2G_FRONTIER_REACHABILITY_RECORDER_RESULT")
        print(f"run_id={args.run_id}")
        for k in ["duration_sec", "odom_total_distance", "coverage_proxy_gain", "frontier_candidate_count_end", "frontier_viewpoint_count_end", "selected_goal_unique_count", "active_path_endpoint_to_goal_distance_avg", "unreachable_goal_ratio", "coverage_gain_after_goal_avg", "main_frontier_blocker"]:
            print(f"{k}={metrics.get(k)}")
        print(f"result={result}")
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
