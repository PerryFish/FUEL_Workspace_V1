#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import math
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path as RosPath
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String

try:
    from sensor_msgs_py import point_cloud2
except ImportError:  # pragma: no cover
    point_cloud2 = None

Point = Tuple[float, float, float]


def dist(a: Point, b: Point) -> float:
    return math.dist(a, b)


def avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


class RouteRationalityRecorder(Node):
    def __init__(self, args):
        super().__init__("fuel_route_rationality_recorder")
        self.args = args
        self.start_wall = time.time()
        self.end_wall = self.start_wall + args.duration
        self.samples: List[Dict] = []
        self.events: List[Dict] = []
        self.msg_count: Dict[str, int] = {}

        self.odom_start: Optional[Point] = None
        self.odom_last: Optional[Point] = None
        self.odom_total = 0.0
        self.odom_points: List[Tuple[float, Point]] = []
        self.backtracking_distance = 0.0
        self.last_motion_dir: Optional[Tuple[float, float]] = None

        self.current_goal: Optional[Point] = None
        self.goal_points: List[Tuple[float, Point]] = []
        self.goal_distances: List[float] = []
        self.goal_regions: Dict[Tuple[int, int], int] = {}
        self.local_region_revisit_count = 0
        self.last_goal_coverage = 0.0
        self.coverage_gain_after_goal: List[float] = []
        self.coverage_gain_after_goal_per_meter: List[float] = []
        self.goal_odom_at_switch: Optional[float] = None

        self.best_viewpoint: Optional[Point] = None
        self.frontier_candidates: List[Point] = []
        self.frontier_viewpoints: List[Point] = []
        self.frontier_candidate_counts: List[int] = []
        self.frontier_viewpoint_counts: List[int] = []
        self.nearest_frontier_distances: List[float] = []
        self.nearest_frontier_ignored_count = 0
        self.near_high_gain_candidate_ignored_count = 0

        self.active_path_hash = ""
        self.active_path_update_count = 0
        self.active_path_lengths: List[float] = []
        self.active_path_endpoint_to_goal: List[float] = []
        self.selected_goal_path_lengths: List[float] = []
        self.selected_goal_path_efficiencies: List[float] = []
        self.path_length_to_selected_goal: List[float] = []
        self.path_length_to_nearest_candidate: List[float] = []
        self.path_length_regrets: List[float] = []
        self.position_cmd_hash = ""
        self.position_cmd_update_count = 0

        self.explored_start: Optional[int] = None
        self.explored_end = 0
        self.global_cloud = 0
        self.coverage_series: List[Tuple[float, float]] = []
        self.low_efficiency_goal_count = 0

        self.path_status_latest = ""
        self.manager_status_latest = ""

        self.create_subscription(Odometry, "/odom", self.odom_cb, 20)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self.goal_cb, 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/best_viewpoint", self.best_cb, 10)
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
            "/map_generator/global_cloud",
            "/pcl_render_node/cloud",
        ]:
            self.create_subscription(PointCloud2, topic, lambda m, t=topic: self.cloud_cb(t, m), 10)

    def elapsed(self) -> float:
        return time.time() - self.start_wall

    def tick(self, topic: str) -> None:
        self.msg_count[topic] = self.msg_count.get(topic, 0) + 1

    @staticmethod
    def pose(msg: PoseStamped) -> Point:
        p = msg.pose.position
        return float(p.x), float(p.y), float(p.z)

    @staticmethod
    def region(point: Point, size: float = 2.0) -> Tuple[int, int]:
        return int(math.floor(point[0] / size)), int(math.floor(point[1] / size))

    @staticmethod
    def path_points(msg: RosPath) -> List[Point]:
        return [(float(p.pose.position.x), float(p.pose.position.y), float(p.pose.position.z)) for p in msg.poses]

    @staticmethod
    def path_hash(points: List[Point]) -> str:
        return hashlib.sha1(";".join(f"{x:.2f},{y:.2f},{z:.2f}" for x, y, z in points).encode()).hexdigest()

    @staticmethod
    def path_length(points: List[Point]) -> float:
        return sum(dist(a, b) for a, b in zip(points, points[1:])) if len(points) >= 2 else 0.0

    @staticmethod
    def field(text: str, key: str, default: str = "") -> str:
        token = f"{key}="
        for part in text.split():
            if part.startswith(token):
                return part[len(token):]
        return default

    def read_cloud_points(self, msg: PointCloud2, limit: int = 600) -> List[Point]:
        if point_cloud2 is None:
            return []
        points: List[Point] = []
        try:
            for idx, p in enumerate(point_cloud2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)):
                if idx >= limit:
                    break
                x, y, z = float(p[0]), float(p[1]), float(p[2])
                if math.isfinite(x) and math.isfinite(y) and math.isfinite(z):
                    points.append((x, y, z))
        except Exception as exc:
            self.events.append({"time_sec": self.elapsed(), "type": "CLOUD_PARSE_FAILED", "detail": type(exc).__name__})
        return points

    def coverage(self) -> float:
        return float(self.explored_end) / float(self.global_cloud) if self.global_cloud >= 1000 else 0.0

    def candidate_gain(self, candidate: Point) -> float:
        if not self.frontier_candidates:
            return 0.0
        near_2 = sum(1 for p in self.frontier_candidates if math.hypot(p[0] - candidate[0], p[1] - candidate[1]) <= 2.0)
        near_3 = sum(1 for p in self.frontier_candidates if math.hypot(p[0] - candidate[0], p[1] - candidate[1]) <= 3.0)
        return clamp(0.7 * near_2 / 12.0 + 0.3 * near_3 / 20.0, 0.0, 1.0)

    def nearest_candidate_distance(self) -> float:
        if self.odom_last is None:
            return 0.0
        pts = self.frontier_viewpoints or self.frontier_candidates
        return min((dist(self.odom_last, p) for p in pts), default=0.0)

    def route_revisit_ratio(self) -> float:
        if not self.odom_points:
            return 0.0
        regions = [self.region(p) for _t, p in self.odom_points]
        return 1.0 - float(len(set(regions))) / float(max(1, len(regions)))

    def route_tortuosity(self) -> float:
        if self.odom_start is None or self.odom_last is None:
            return 0.0
        return self.odom_total / max(dist(self.odom_start, self.odom_last), 1e-6)

    def odom_cb(self, msg: Odometry) -> None:
        self.tick("/odom")
        p = msg.pose.pose.position
        cur = (float(p.x), float(p.y), float(p.z))
        if self.odom_start is None:
            self.odom_start = cur
        if self.odom_last is not None:
            step = dist(self.odom_last, cur)
            self.odom_total += step
            if step > 0.02:
                dx, dy = cur[0] - self.odom_last[0], cur[1] - self.odom_last[1]
                norm = math.hypot(dx, dy)
                direction = (dx / norm, dy / norm)
                if self.last_motion_dir is not None:
                    dot = clamp(direction[0] * self.last_motion_dir[0] + direction[1] * self.last_motion_dir[1], -1.0, 1.0)
                    if math.degrees(math.acos(dot)) > 135.0:
                        self.backtracking_distance += step
                self.last_motion_dir = direction
        self.odom_last = cur
        now = self.elapsed()
        if not self.odom_points or dist(self.odom_points[-1][1], cur) > 0.2:
            self.odom_points.append((now, cur))

    def goal_cb(self, msg: PoseStamped) -> None:
        self.tick("/fuel/p11_lite/exploration_goal")
        point = self.pose(msg)
        now = self.elapsed()
        if self.current_goal is None or dist(self.current_goal, point) > 0.5:
            if self.current_goal is not None:
                gain = self.coverage() - self.last_goal_coverage
                meters = self.odom_total - (self.goal_odom_at_switch or self.odom_total)
                self.coverage_gain_after_goal.append(gain)
                self.coverage_gain_after_goal_per_meter.append(gain / max(meters, 1e-6))
                if gain < 0.003 and meters > 4.0:
                    self.low_efficiency_goal_count += 1
            self.current_goal = point
            self.last_goal_coverage = self.coverage()
            self.goal_odom_at_switch = self.odom_total
            if self.odom_last is not None:
                goal_dist = dist(self.odom_last, point)
                self.goal_distances.append(goal_dist)
                near_dist = self.nearest_candidate_distance()
                if near_dist > 0.0 and goal_dist > near_dist + 1.5:
                    self.nearest_frontier_ignored_count += 1
                selected_gain = self.candidate_gain(point)
                near_candidates = [p for p in (self.frontier_viewpoints or self.frontier_candidates) if dist(self.odom_last, p) < 4.0]
                for candidate in near_candidates:
                    if dist(self.odom_last, candidate) + 0.5 < goal_dist and self.candidate_gain(candidate) >= 0.7 * max(selected_gain, 1e-3):
                        self.near_high_gain_candidate_ignored_count += 1
                        break
            region = self.region(point)
            if region in self.goal_regions:
                self.local_region_revisit_count += 1
            self.goal_regions[region] = self.goal_regions.get(region, 0) + 1
        self.goal_points.append((now, point))

    def best_cb(self, msg: PoseStamped) -> None:
        self.tick("/fuel/p11_lite/best_viewpoint")
        self.best_viewpoint = self.pose(msg)

    def cmd_cb(self, topic: str, msg: PoseStamped) -> None:
        self.tick(topic)
        p = self.pose(msg)
        h = f"{p[0]:.2f},{p[1]:.2f},{p[2]:.2f}"
        if h != self.position_cmd_hash:
            self.position_cmd_hash = h
            self.position_cmd_update_count += 1

    def path_cb(self, topic: str, msg: RosPath) -> None:
        self.tick(topic)
        if topic != "/fuel/p10_lite/active_path":
            return
        points = self.path_points(msg)
        h = self.path_hash(points)
        if h != self.active_path_hash:
            self.active_path_hash = h
            self.active_path_update_count += 1
        if not points:
            return
        length = self.path_length(points)
        self.active_path_lengths.append(length)
        if self.current_goal is not None:
            endpoint_dist = dist(points[-1], self.current_goal)
            self.active_path_endpoint_to_goal.append(endpoint_dist)
            self.path_length_to_selected_goal.append(length)
            euclid = dist(points[0], self.current_goal)
            self.selected_goal_path_lengths.append(length)
            self.selected_goal_path_efficiencies.append(euclid / max(length, 1e-6))
        nearest = self.nearest_candidate_distance()
        if nearest > 0.0:
            self.path_length_to_nearest_candidate.append(nearest)
            self.path_length_regrets.append(length - nearest)

    def status_cb(self, topic: str, msg: String) -> None:
        self.tick(topic)
        if topic == "/fuel/p11_lite/goal_to_path_status":
            self.path_status_latest = msg.data
        elif topic == "/fuel/p11_lite/exploration_manager_status":
            self.manager_status_latest = msg.data

    def cloud_cb(self, topic: str, msg: PointCloud2) -> None:
        self.tick(topic)
        count = int(msg.width * msg.height)
        if topic == "/fuel/p11_lite/frontier_candidates_raw":
            self.frontier_candidate_counts.append(count)
            self.frontier_candidates = self.read_cloud_points(msg)
        elif topic == "/fuel/p11_lite/frontier_viewpoints":
            self.frontier_viewpoint_counts.append(count)
            self.frontier_viewpoints = self.read_cloud_points(msg)
        elif topic == "/fuel/p11_lite/explored_grid":
            if self.explored_start is None:
                self.explored_start = count
            self.explored_end = count
            if self.global_cloud >= 1000:
                self.coverage_series.append((self.elapsed(), self.coverage()))
        elif topic == "/map_generator/global_cloud":
            self.global_cloud = max(self.global_cloud, count)
            if self.global_cloud >= 1000:
                self.coverage_series.append((self.elapsed(), self.coverage()))
        if self.odom_last is not None and (self.frontier_viewpoints or self.frontier_candidates):
            self.nearest_frontier_distances.append(self.nearest_candidate_distance())

    def main_issue(self) -> str:
        gain = self.coverage_gain()
        if self.frontier_candidate_counts and self.frontier_candidate_counts[-1] < 5 and gain < 0.005:
            return "COVERAGE_SATURATED"
        if avg(self.active_path_endpoint_to_goal) > 1.5:
            return "PATH_ENDPOINT_MISMATCH"
        if avg(self.path_length_regrets) > 3.0 or max(self.path_length_regrets or [0.0]) > 8.0:
            return "PATH_COST_UNDERWEIGHTED"
        if self.near_high_gain_candidate_ignored_count >= 3:
            return "NEAR_HIGH_GAIN_FRONTIER_IGNORED"
        if self.route_revisit_ratio() > 0.65 or self.local_region_revisit_count >= 5:
            return "LOCAL_REGION_REVISIT"
        if avg(self.coverage_gain_after_goal_per_meter) < 0.0005 and self.odom_total > 15.0:
            return "GAIN_OVERWEIGHTED"
        if avg(self.selected_goal_path_efficiencies) < 0.45 and self.active_path_update_count > 5:
            return "VIEWPOINT_REFINEMENT_MISSING"
        return "ROUTE_REASONABLE"

    def coverage_gain(self) -> float:
        if not self.coverage_series:
            return 0.0
        return self.coverage() - self.coverage_series[0][1]

    def sample(self) -> None:
        row = {
            "time_sec": self.elapsed(),
            "coverage_proxy": self.coverage(),
            "odom_total_distance": self.odom_total,
            "coverage_gain_per_meter": self.coverage_gain() / max(self.odom_total, 1e-6),
            "path_length_regret_avg": avg(self.path_length_regrets),
            "near_high_gain_candidate_ignored_count": self.near_high_gain_candidate_ignored_count,
            "route_revisit_ratio": self.route_revisit_ratio(),
            "route_tortuosity": self.route_tortuosity(),
            "main_route_issue": self.main_issue(),
        }
        self.samples.append(row)
        print(
            "P2H_ROUTE_PROGRESS "
            + " ".join(f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}" for k, v in row.items()),
            flush=True,
        )

    def result(self) -> Dict:
        coverage_gain = self.coverage_gain()
        selected_unique = len({(round(p[0], 1), round(p[1], 1), round(p[2], 1)) for _t, p in self.goal_points})
        net = dist(self.odom_start, self.odom_last) if self.odom_start and self.odom_last else 0.0
        data = {
            "duration_sec": self.elapsed(),
            "odom_total_distance": self.odom_total,
            "coverage_proxy_start": self.coverage_series[0][1] if self.coverage_series else 0.0,
            "coverage_proxy_end": self.coverage(),
            "coverage_proxy_gain": coverage_gain,
            "coverage_gain_per_meter": coverage_gain / max(self.odom_total, 1e-6),
            "selected_goal_count": len(self.goal_points),
            "selected_goal_unique_count": selected_unique,
            "selected_goal_distance_from_odom_avg": avg(self.goal_distances),
            "selected_goal_distance_from_odom_max": max(self.goal_distances) if self.goal_distances else 0.0,
            "selected_goal_path_length_avg": avg(self.selected_goal_path_lengths),
            "selected_goal_path_length_max": max(self.selected_goal_path_lengths) if self.selected_goal_path_lengths else 0.0,
            "selected_goal_path_efficiency_avg": avg(self.selected_goal_path_efficiencies),
            "frontier_candidate_count_avg": avg([float(x) for x in self.frontier_candidate_counts]),
            "frontier_viewpoint_count_avg": avg([float(x) for x in self.frontier_viewpoint_counts]),
            "nearest_frontier_distance_avg": avg(self.nearest_frontier_distances),
            "nearest_frontier_distance_min": min(self.nearest_frontier_distances) if self.nearest_frontier_distances else 0.0,
            "nearest_frontier_ignored_count": self.nearest_frontier_ignored_count,
            "near_high_gain_candidate_ignored_count": self.near_high_gain_candidate_ignored_count,
            "path_length_to_selected_goal_avg": avg(self.path_length_to_selected_goal),
            "path_length_to_nearest_candidate_avg": avg(self.path_length_to_nearest_candidate),
            "path_length_regret_avg": avg(self.path_length_regrets),
            "path_length_regret_max": max(self.path_length_regrets) if self.path_length_regrets else 0.0,
            "coverage_gain_after_goal_avg": avg(self.coverage_gain_after_goal),
            "coverage_gain_after_goal_per_meter_avg": avg(self.coverage_gain_after_goal_per_meter),
            "low_efficiency_goal_count": self.low_efficiency_goal_count,
            "local_region_revisit_count": self.local_region_revisit_count,
            "region_diversity_score": float(len(self.goal_regions)) / float(max(1, selected_unique)),
            "active_path_endpoint_to_goal_distance_avg": avg(self.active_path_endpoint_to_goal),
            "active_path_endpoint_to_goal_distance_max": max(self.active_path_endpoint_to_goal) if self.active_path_endpoint_to_goal else 0.0,
            "route_backtracking_distance": self.backtracking_distance,
            "route_revisit_ratio": self.route_revisit_ratio(),
            "route_tortuosity": self.odom_total / max(net, 1e-6),
            "active_path_update_count": self.active_path_update_count,
            "position_cmd_update_count": self.position_cmd_update_count,
            "frontier_candidate_count_end": self.frontier_candidate_counts[-1] if self.frontier_candidate_counts else 0,
            "frontier_viewpoint_count_end": self.frontier_viewpoint_counts[-1] if self.frontier_viewpoint_counts else 0,
            "main_route_issue": self.main_issue(),
        }
        return data

    def run(self) -> Dict:
        last_sample = time.time()
        while rclpy.ok() and time.time() < self.end_wall:
            rclpy.spin_once(self, timeout_sec=0.2)
            if time.time() - last_sample >= self.args.progress_interval:
                last_sample = time.time()
                self.sample()
        self.sample()
        return self.result()


def write_outputs(root: Path, run_id: str, metrics: Dict, samples: List[Dict], events: List[Dict]) -> None:
    out = root / run_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "route_rationality.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    md = ["# P2H Route Rationality Metrics", ""]
    for k, v in metrics.items():
        md.append(f"- {k}: {v}")
    (out / "route_rationality.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    if samples:
        with (out / "route_timeseries.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(samples[0].keys()))
            writer.writeheader()
            writer.writerows(samples)
    with (out / "route_events.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["time_sec", "type", "detail"], extrasaction="ignore")
        writer.writeheader()
        writer.writerows(events)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=300.0)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", default="reports/p2h_metrics")
    parser.add_argument("--progress-interval", type=float, default=30.0)
    args = parser.parse_args()
    rclpy.init()
    node = RouteRationalityRecorder(args)
    try:
        metrics = node.run()
        write_outputs(Path(args.output_root), args.run_id, metrics, node.samples, node.events)
        result = "PASS" if metrics["duration_sec"] >= 290.0 and metrics["coverage_proxy_gain"] > 0.05 else "PARTIAL"
        print("P2H_ROUTE_RATIONALITY_RECORDER_RESULT")
        print(f"run_id={args.run_id}")
        for key in [
            "duration_sec",
            "odom_total_distance",
            "coverage_proxy_gain",
            "coverage_gain_per_meter",
            "selected_goal_unique_count",
            "path_length_regret_avg",
            "path_length_regret_max",
            "near_high_gain_candidate_ignored_count",
            "route_revisit_ratio",
            "route_tortuosity",
            "active_path_endpoint_to_goal_distance_avg",
            "main_route_issue",
        ]:
            print(f"{key}={metrics.get(key)}")
        print(f"result={result}")
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
