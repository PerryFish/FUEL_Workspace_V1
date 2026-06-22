#!/usr/bin/env python3
import argparse
import csv
import json
import math
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
from visualization_msgs.msg import Marker, MarkerArray


Point = Tuple[float, float, float]


@dataclass
class Event:
    time_sec: float
    event_type: str
    reason: str
    position: Optional[Point] = None
    goal: Optional[Point] = None
    frontier_count: int = 0
    coverage_proxy: float = 0.0
    trajectory_count: int = 0


@dataclass
class SeriesSample:
    time_sec: float
    odom_distance: float
    net_displacement: float
    coverage_proxy: float
    explored_points: int
    occupancy_points: int
    global_cloud_points: int
    frontier_candidates: int
    frontier_viewpoints: int
    goal_count: int
    unique_goal_count: int
    trajectory_count: int
    planner_pos_cmd_count: int
    stuck_event_count: int


class ContinuousExplorationRecorder(Node):
    def __init__(self, args):
        super().__init__("fuel_continuous_exploration_recorder")
        self.args = args
        self.start_wall = time.time()
        self.end_wall = self.start_wall + args.duration
        self.last_sample_wall = 0.0
        self.last_progress_wall = self.start_wall
        self.samples: List[SeriesSample] = []
        self.events: List[Event] = []
        self.last_event_time: Dict[str, float] = {}

        self.msg_count: Dict[str, int] = {}
        self.status_latest: Dict[str, str] = {}
        self.odom_start: Optional[Point] = None
        self.odom_last: Optional[Point] = None
        self.odom_total_distance = 0.0
        self.last_motion_time = 0.0
        self.no_motion_window_start: Optional[Tuple[float, Point, float]] = None

        self.goal_last: Optional[Point] = None
        self.goal_points: List[Tuple[float, Point]] = []
        self.unique_goals: Dict[Tuple[int, int, int], int] = {}
        self.unique_goals_1m: Dict[Tuple[int, int, int], int] = {}
        self.goal_switch_count = 0
        self.goal_distance_values: List[float] = []
        self.consecutive_close_goals = 0
        self.goal_lifecycle_events: List[Dict] = []

        self.frontier_candidates = 0
        self.frontier_viewpoints = 0
        self.frontier_zero_start: Optional[float] = None
        self.frontier_last_change_time = self.start_wall
        self.frontier_last_value = -1

        self.explored_start: Optional[int] = None
        self.explored_last = 0
        self.occupancy_start: Optional[int] = None
        self.occupancy_last = 0
        self.global_cloud_points = 0
        self.local_cloud_count = 0
        self.map_cloud_count = 0

        self.planner_pos_cmd_count = 0
        self.trajectory_count = 0
        self.active_path_count = 0
        self.trajectory_last_change_time = self.start_wall
        self.last_trajectory_count = 0
        self.last_coverage_for_stall = 0.0
        self.coverage_stall_start: Optional[Tuple[float, float, int]] = None

        self.marker_counts: Dict[str, int] = {}

        self.create_subscription(Odometry, "/odom", lambda m: self.odom_cb("/odom", m), 20)
        self.create_subscription(Odometry, "/state_ukf/odom", lambda m: self.odom_cb("/state_ukf/odom", m), 20)
        self.create_subscription(Odometry, "/visual_slam/odom", lambda m: self.odom_cb("/visual_slam/odom", m), 20)

        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self.goal_cb, 10)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/best_viewpoint", lambda m: self.pose_count_cb("/fuel/p11_lite/best_viewpoint", m), 10)
        self.create_subscription(PoseStamped, "/fuel/p10_lite/position_cmd", lambda m: self.pos_cmd_cb("/fuel/p10_lite/position_cmd", m), 10)
        self.create_subscription(PoseStamped, "/planning/pos_cmd", lambda m: self.pos_cmd_cb("/planning/pos_cmd", m), 10)

        for topic in ["/fuel/p10_lite/active_path", "/planning/travel_traj", "/fuel/plan_manager/managed_trajectory"]:
            self.create_subscription(Path, topic, lambda m, t=topic: self.path_cb(t, m), 10)

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

        for topic in [
            "/fuel/p11_lite/exploration_manager_status",
            "/fuel/p11_lite/goal_lifecycle_status",
            "/fuel/p11_lite/frontier_status",
            "/fuel/p11_lite/map_status",
        ]:
            self.create_subscription(String, topic, lambda m, t=topic: self.status_cb(t, m), 10)

        self.create_subscription(Marker, "/fuel/p11_lite/visual/uav_marker", lambda m: self.marker_cb("/fuel/p11_lite/visual/uav_marker", m), 10)
        self.create_subscription(MarkerArray, "/fuel/p11_lite/visual/all_markers", lambda m: self.marker_array_cb("/fuel/p11_lite/visual/all_markers", m), 10)

    def elapsed(self) -> float:
        return max(0.0, time.time() - self.start_wall)

    def tick_count(self, topic: str) -> None:
        self.msg_count[topic] = self.msg_count.get(topic, 0) + 1

    @staticmethod
    def point_from_pose(msg: PoseStamped) -> Point:
        p = msg.pose.position
        return float(p.x), float(p.y), float(p.z)

    @staticmethod
    def point_key(p: Point, resolution: float = 0.5) -> Tuple[int, int, int]:
        return tuple(int(round(v / resolution)) for v in p)

    @staticmethod
    def parse_goal_event(data: str) -> Dict:
        fields = {"raw": data}
        for key in ["type", "reason", "source"]:
            match = re.search(rf"(?:^| ){key}=([^ ]+)", data)
            if match:
                fields[key] = match.group(1)
        for key in ["x", "y", "z", "duration", "score"]:
            match = re.search(rf"(?:^| ){key}=(-?nan|-?[0-9.]+)", data)
            if match:
                try:
                    fields[key] = float(match.group(1))
                except ValueError:
                    fields[key] = None
        return fields

    def odom_cb(self, topic: str, msg: Odometry) -> None:
        self.tick_count(topic)
        p = msg.pose.pose.position
        pos = (float(p.x), float(p.y), float(p.z))
        now = time.time()
        if self.odom_start is None:
            self.odom_start = pos
            self.last_motion_time = now
        if self.odom_last is not None:
            step = math.dist(self.odom_last, pos)
            self.odom_total_distance += step
            if step > 0.02:
                self.last_motion_time = now
        self.odom_last = pos

    def goal_cb(self, msg: PoseStamped) -> None:
        self.tick_count("/fuel/p11_lite/exploration_goal")
        p = self.point_from_pose(msg)
        now = time.time()
        self.goal_points.append((self.elapsed(), p))
        key = self.point_key(p)
        self.unique_goals[key] = self.unique_goals.get(key, 0) + 1
        key_1m = self.point_key(p, 1.0)
        self.unique_goals_1m[key_1m] = self.unique_goals_1m.get(key_1m, 0) + 1
        if self.goal_last is not None:
            d = math.dist(self.goal_last, p)
            self.goal_distance_values.append(d)
            if d > 0.5:
                self.goal_switch_count += 1
            if d < 0.5:
                self.consecutive_close_goals += 1
            else:
                self.consecutive_close_goals = 0
            if self.consecutive_close_goals >= 3:
                self.add_event("REPEATED_GOAL", "three_consecutive_goals_within_0.5m", now)
        self.goal_last = p

    def pose_count_cb(self, topic: str, _msg: PoseStamped) -> None:
        self.tick_count(topic)

    def pos_cmd_cb(self, topic: str, _msg: PoseStamped) -> None:
        self.tick_count(topic)
        self.planner_pos_cmd_count += 1

    def path_cb(self, topic: str, _msg: Path) -> None:
        self.tick_count(topic)
        self.trajectory_count += 1
        if topic == "/fuel/p10_lite/active_path":
            self.active_path_count += 1
        now = time.time()
        if self.trajectory_count != self.last_trajectory_count:
            self.trajectory_last_change_time = now
            self.last_trajectory_count = self.trajectory_count

    def cloud_cb(self, topic: str, msg: PointCloud2) -> None:
        self.tick_count(topic)
        points = int(msg.width * msg.height)
        if topic == "/fuel/p11_lite/frontier_candidates_raw":
            if points != self.frontier_last_value:
                self.frontier_last_change_time = time.time()
                self.frontier_last_value = points
            self.frontier_candidates = points
            if points == 0 and self.frontier_zero_start is None:
                self.frontier_zero_start = time.time()
            if points > 0:
                self.frontier_zero_start = None
        elif topic == "/fuel/p11_lite/frontier_viewpoints":
            self.frontier_viewpoints = points
        elif topic == "/fuel/p11_lite/explored_grid":
            if self.explored_start is None:
                self.explored_start = points
            self.explored_last = points
        elif topic == "/fuel/p11_lite/occupancy_grid":
            if self.occupancy_start is None:
                self.occupancy_start = points
            self.occupancy_last = points
        elif topic == "/map_generator/global_cloud":
            self.global_cloud_points = max(self.global_cloud_points, points)
            self.map_cloud_count += 1
        elif topic in ["/pcl_render_node/cloud", "/fuel/p11_lite/local_free_points", "/fuel/p11_lite/local_occupied_points"]:
            self.local_cloud_count += 1

    def status_cb(self, topic: str, msg: String) -> None:
        self.tick_count(topic)
        self.status_latest[topic] = msg.data
        if topic == "/fuel/p11_lite/goal_lifecycle_status":
            event = self.parse_goal_event(msg.data)
            event["time_sec"] = self.elapsed()
            self.goal_lifecycle_events.append(event)

    def marker_cb(self, topic: str, _msg: Marker) -> None:
        self.tick_count(topic)
        self.marker_counts[topic] = self.marker_counts.get(topic, 0) + 1

    def marker_array_cb(self, topic: str, msg: MarkerArray) -> None:
        self.tick_count(topic)
        self.marker_counts[topic] = len(msg.markers)

    def coverage_proxy(self) -> float:
        return float(self.explored_last) / float(max(self.global_cloud_points, 1))

    def net_displacement(self) -> float:
        if self.odom_start is None or self.odom_last is None:
            return 0.0
        return math.dist(self.odom_start, self.odom_last)

    def add_event(self, event_type: str, reason: str, now: float) -> None:
        last = self.last_event_time.get(event_type, -999.0)
        if now - last < 5.0:
            return
        self.last_event_time[event_type] = now
        self.events.append(
            Event(
                time_sec=self.elapsed(),
                event_type=event_type,
                reason=reason,
                position=self.odom_last,
                goal=self.goal_last,
                frontier_count=self.frontier_candidates,
                coverage_proxy=self.coverage_proxy(),
                trajectory_count=self.trajectory_count,
            )
        )

    def evaluate_events(self) -> None:
        now = time.time()
        if self.odom_last is not None and now - self.last_motion_time >= 20.0 and self.planner_pos_cmd_count > 10:
            self.add_event("MOTION_STUCK", "20s_displacement_below_0.2m_with_planner_output", now)
        if self.frontier_zero_start is not None and now - self.frontier_zero_start >= 10.0:
            self.add_event("FRONTIER_EMPTY", "frontier_candidate_count_zero_over_10s", now)
        if now - self.trajectory_last_change_time >= 20.0:
            self.add_event("PLANNER_STALL", "trajectory_count_not_updated_over_20s", now)
        cov = self.coverage_proxy()
        if self.coverage_stall_start is None:
            self.coverage_stall_start = (now, cov, self.frontier_candidates)
        else:
            start_t, start_cov, start_frontier = self.coverage_stall_start
            if abs(self.frontier_candidates - start_frontier) <= 1 and cov - start_cov < 0.01 and now - start_t >= 20.0:
                self.add_event("COVERAGE_STALL", "20s_frontier_stable_and_coverage_gain_below_0.01", now)
                self.coverage_stall_start = (now, cov, self.frontier_candidates)
            elif cov - start_cov >= 0.01 or abs(self.frontier_candidates - start_frontier) > 1:
                self.coverage_stall_start = (now, cov, self.frontier_candidates)

    def sample(self) -> None:
        s = SeriesSample(
            time_sec=self.elapsed(),
            odom_distance=self.odom_total_distance,
            net_displacement=self.net_displacement(),
            coverage_proxy=self.coverage_proxy(),
            explored_points=self.explored_last,
            occupancy_points=self.occupancy_last,
            global_cloud_points=self.global_cloud_points,
            frontier_candidates=self.frontier_candidates,
            frontier_viewpoints=self.frontier_viewpoints,
            goal_count=len(self.goal_points),
            unique_goal_count=len(self.unique_goals),
            trajectory_count=self.trajectory_count,
            planner_pos_cmd_count=self.planner_pos_cmd_count,
            stuck_event_count=len([e for e in self.events if e.event_type == "MOTION_STUCK"]),
        )
        self.samples.append(s)

    def maybe_progress(self) -> None:
        if time.time() - self.last_progress_wall < self.args.progress_interval:
            return
        self.last_progress_wall = time.time()
        print(
            "P2B_PROGRESS "
            f"time={self.elapsed():.1f} "
            f"uav_distance={self.odom_total_distance:.3f} "
            f"coverage_proxy={self.coverage_proxy():.4f} "
            f"frontier_count={self.frontier_candidates} "
            f"goal_count={len(self.goal_points)} "
            f"trajectory_count={self.trajectory_count} "
            f"stuck_events={len(self.events)}",
            flush=True,
        )

    def run(self) -> None:
        while rclpy.ok() and time.time() < self.end_wall:
            rclpy.spin_once(self, timeout_sec=0.2)
            self.evaluate_events()
            if time.time() - self.last_sample_wall >= self.args.sample_period:
                self.last_sample_wall = time.time()
                self.sample()
            self.maybe_progress()
        if not self.samples:
            self.sample()

    def result_status(self) -> str:
        odom_count = sum(self.msg_count.get(t, 0) for t in ["/odom", "/state_ukf/odom", "/visual_slam/odom"])
        cov_gain = self.coverage_gain()
        fatal = odom_count <= 0 or self.trajectory_count <= 0 or len(self.goal_points) <= 0
        longest_stuck = self.max_no_motion_duration()
        if fatal or self.odom_total_distance < 1.0:
            return "FAIL"
        if (
            odom_count > 100
            and self.trajectory_count > 10
            and len(self.goal_points) > 5
            and self.odom_total_distance > 5.0
            and cov_gain > 0.05
            and longest_stuck < 60.0
        ):
            return "PASS"
        return "PARTIAL"

    def coverage_gain(self) -> float:
        if not self.samples:
            return 0.0
        return self.samples[-1].coverage_proxy - self.samples[0].coverage_proxy

    def max_no_motion_duration(self) -> float:
        if not self.samples:
            return 0.0
        max_span = 0.0
        window_start = self.samples[0]
        for sample in self.samples[1:]:
            if sample.odom_distance - window_start.odom_distance >= 0.2:
                window_start = sample
            else:
                max_span = max(max_span, sample.time_sec - window_start.time_sec)
        return max_span

    def goal_segments(self, resolution: float = 0.5) -> List[Dict]:
        segments: List[Dict] = []
        current = None
        for t, point in self.goal_points:
            key = self.point_key(point, resolution)
            if current is None or current["key"] != key:
                if current is not None:
                    current["duration_sec"] = max(0.0, current["end_time_sec"] - current["start_time_sec"])
                    segments.append(current)
                current = {
                    "key": key,
                    "start_time_sec": t,
                    "end_time_sec": t,
                    "message_count": 1,
                    "representative_point": point,
                }
            else:
                current["end_time_sec"] = t
                current["message_count"] += 1
                current["representative_point"] = point
        if current is not None:
            current["duration_sec"] = max(0.0, current["end_time_sec"] - current["start_time_sec"])
            segments.append(current)
        return segments

    def goal_lifecycle_metrics(self) -> Dict:
        segments_05 = self.goal_segments(0.5)
        segments_10 = self.goal_segments(1.0)
        raw_goal_msg_count = len(self.goal_points)
        goal_republish_count = sum(max(0, seg["message_count"] - 1) for seg in segments_05)
        consecutive_same_goal_msg_count_max = max((seg["message_count"] for seg in segments_05), default=0)
        durations = [seg["duration_sec"] for seg in segments_05]
        seen_last_end: Dict[Tuple[int, int, int], float] = {}
        true_repeated_goal_count = 0
        for seg in segments_05:
            key = seg["key"]
            if key in seen_last_end and seg["start_time_sec"] - seen_last_end[key] <= 120.0:
                true_repeated_goal_count += 1
            seen_last_end[key] = seg["end_time_sec"]
        goal_retire_events = [e for e in self.goal_lifecycle_events if e.get("type") == "RETIRE_GOAL"]
        escape_events = [e for e in self.goal_lifecycle_events if e.get("type") == "ESCAPE_GOAL"]
        too_close_events = [
            e for e in self.goal_lifecycle_events
            if "too_close" in str(e.get("reason", "")).lower() or "TOO_CLOSE" in e.get("raw", "")
        ]
        retire_reasons: Dict[str, int] = {}
        for event in goal_retire_events:
            reason = str(event.get("reason", "unknown"))
            retire_reasons[reason] = retire_reasons.get(reason, 0) + 1
        return {
            "raw_goal_msg_count": raw_goal_msg_count,
            "unique_goal_count_quantized_0p5m": len(self.unique_goals),
            "unique_goal_count_quantized_1p0m": len(self.unique_goals_1m),
            "goal_switch_count": max(0, len(segments_05) - 1),
            "same_goal_max_duration_sec": max(durations, default=0.0),
            "same_goal_avg_duration_sec": sum(durations) / len(durations) if durations else 0.0,
            "active_goal_segments": segments_05,
            "active_goal_segment_count": len(segments_05),
            "consecutive_same_goal_msg_count_max": consecutive_same_goal_msg_count_max,
            "goal_republish_count": goal_republish_count,
            "true_repeated_goal_count": true_repeated_goal_count,
            "too_close_goal_event_count": len(too_close_events),
            "goal_retire_event_count": len(goal_retire_events),
            "goal_retire_reasons": retire_reasons,
            "escape_goal_count": len(escape_events),
            "goal_lifecycle_event_count": len(self.goal_lifecycle_events),
            "goal_lifecycle_events": self.goal_lifecycle_events,
            "segments_quantized_1p0m": segments_10,
        }

    def write_outputs(self) -> Dict:
        out_dir = os.path.join(self.args.output_root, self.args.run_id)
        os.makedirs(out_dir, exist_ok=True)
        try:
            snapshot = subprocess.run(
                ["bash", "-lc", "ros2 topic list -t --no-daemon --spin-time 4"],
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            with open(os.path.join(out_dir, "topic_snapshot.txt"), "w", encoding="utf-8") as f:
                f.write(snapshot.stdout)
                f.write(snapshot.stderr)
        except Exception as exc:
            with open(os.path.join(out_dir, "topic_snapshot.txt"), "w", encoding="utf-8") as f:
                f.write(f"topic snapshot failed: {exc}\n")

        with open(os.path.join(out_dir, "time_series.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(SeriesSample.__annotations__.keys()))
            writer.writeheader()
            for sample in self.samples:
                writer.writerow(sample.__dict__)

        with open(os.path.join(out_dir, "events.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(Event.__annotations__.keys()))
            writer.writeheader()
            for event in self.events:
                row = event.__dict__.copy()
                row["position"] = json.dumps(row["position"])
                row["goal"] = json.dumps(row["goal"])
                writer.writerow(row)

        goal_dist = self.goal_distance_values
        lifecycle = self.goal_lifecycle_metrics()
        metrics = {
            "run_id": self.args.run_id,
            "duration_sec": self.elapsed(),
            "coverage_proxy_is_not_exact_metric": True,
            "odom_msg_count": sum(self.msg_count.get(t, 0) for t in ["/odom", "/state_ukf/odom", "/visual_slam/odom"]),
            "uav_start_position": self.odom_start,
            "uav_end_position": self.odom_last,
            "uav_total_distance": self.odom_total_distance,
            "uav_net_displacement": self.net_displacement(),
            "max_no_motion_duration_sec": self.max_no_motion_duration(),
            "stuck_event_count": len([e for e in self.events if e.event_type == "MOTION_STUCK"]),
            "stuck_events": [e.__dict__ for e in self.events],
            "goal_msg_count": len(self.goal_points),
            "raw_goal_msg_count": lifecycle["raw_goal_msg_count"],
            "unique_goal_count": len(self.unique_goals),
            "unique_goal_count_quantized_0p5m": lifecycle["unique_goal_count_quantized_0p5m"],
            "unique_goal_count_quantized_1p0m": lifecycle["unique_goal_count_quantized_1p0m"],
            "repeated_goal_count": sum(max(0, c - 1) for c in self.unique_goals.values()),
            "goal_switch_count": self.goal_switch_count,
            "goal_lifecycle_goal_switch_count": lifecycle["goal_switch_count"],
            "same_goal_max_duration_sec": lifecycle["same_goal_max_duration_sec"],
            "same_goal_avg_duration_sec": lifecycle["same_goal_avg_duration_sec"],
            "active_goal_segment_count": lifecycle["active_goal_segment_count"],
            "consecutive_same_goal_msg_count_max": lifecycle["consecutive_same_goal_msg_count_max"],
            "goal_republish_count": lifecycle["goal_republish_count"],
            "true_repeated_goal_count": lifecycle["true_repeated_goal_count"],
            "too_close_goal_event_count": lifecycle["too_close_goal_event_count"],
            "goal_retire_event_count": lifecycle["goal_retire_event_count"],
            "goal_retire_reasons": lifecycle["goal_retire_reasons"],
            "escape_goal_count": lifecycle["escape_goal_count"],
            "average_goal_distance": sum(goal_dist) / len(goal_dist) if goal_dist else 0.0,
            "min_goal_distance": min(goal_dist) if goal_dist else 0.0,
            "max_goal_distance": max(goal_dist) if goal_dist else 0.0,
            "frontier_candidate_count_series": [s.frontier_candidates for s in self.samples],
            "frontier_viewpoint_count_series": [s.frontier_viewpoints for s in self.samples],
            "frontier_count_zero_duration": 0.0 if self.frontier_zero_start is None else max(0.0, time.time() - self.frontier_zero_start),
            "planner_pos_cmd_count": self.planner_pos_cmd_count,
            "trajectory_count": self.trajectory_count,
            "trajectory_update_rate": self.trajectory_count / max(self.elapsed(), 1.0),
            "active_path_count": self.active_path_count,
            "map_cloud_count": self.map_cloud_count,
            "local_cloud_count": self.local_cloud_count,
            "explored_grid_point_count_start": self.explored_start or 0,
            "explored_grid_point_count_end": self.explored_last,
            "explored_grid_point_gain": self.explored_last - (self.explored_start or 0),
            "occupancy_grid_point_count_start": self.occupancy_start or 0,
            "occupancy_grid_point_count_end": self.occupancy_last,
            "coverage_proxy_start": self.samples[0].coverage_proxy if self.samples else 0.0,
            "coverage_proxy_end": self.samples[-1].coverage_proxy if self.samples else 0.0,
            "coverage_proxy_gain": self.coverage_gain(),
            "coverage_stall_events": [e.__dict__ for e in self.events if e.event_type == "COVERAGE_STALL"],
            "event_counts": {k: len([e for e in self.events if e.event_type == k]) for k in sorted({e.event_type for e in self.events})},
            "status_latest": self.status_latest,
            "result": self.result_status(),
        }
        with open(os.path.join(out_dir, "metrics.json"), "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        with open(os.path.join(out_dir, "goal_lifecycle.json"), "w", encoding="utf-8") as f:
            json.dump(lifecycle, f, indent=2)

        with open(os.path.join(out_dir, "goal_lifecycle.md"), "w", encoding="utf-8") as f:
            f.write(f"# Goal Lifecycle {self.args.run_id}\n\n")
            for key in [
                "raw_goal_msg_count",
                "unique_goal_count_quantized_0p5m",
                "unique_goal_count_quantized_1p0m",
                "goal_switch_count",
                "same_goal_max_duration_sec",
                "same_goal_avg_duration_sec",
                "active_goal_segment_count",
                "consecutive_same_goal_msg_count_max",
                "goal_republish_count",
                "true_repeated_goal_count",
                "too_close_goal_event_count",
                "goal_retire_event_count",
                "goal_retire_reasons",
                "escape_goal_count",
                "goal_lifecycle_event_count",
            ]:
                f.write(f"- {key}: {lifecycle[key]}\n")

        with open(os.path.join(out_dir, "metrics.md"), "w", encoding="utf-8") as f:
            f.write(f"# P2B Metrics {self.args.run_id}\n\n")
            for key in [
                "duration_sec",
                "uav_total_distance",
                "uav_net_displacement",
                "max_no_motion_duration_sec",
                "goal_msg_count",
                "raw_goal_msg_count",
                "unique_goal_count",
                "unique_goal_count_quantized_1p0m",
                "repeated_goal_count",
                "goal_republish_count",
                "true_repeated_goal_count",
                "escape_goal_count",
                "trajectory_count",
                "explored_grid_point_count_start",
                "explored_grid_point_count_end",
                "coverage_proxy_start",
                "coverage_proxy_end",
                "coverage_proxy_gain",
                "stuck_event_count",
                "result",
            ]:
                f.write(f"- {key}: {metrics[key]}\n")
            f.write("\ncoverage_proxy_is_not_exact_metric=YES\n")

        return metrics


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=300.0)
    parser.add_argument("--run-id", default=time.strftime("p2b_%Y%m%d_%H%M%S"))
    parser.add_argument("--output-root", default="reports/p2b_metrics")
    parser.add_argument("--sample-period", type=float, default=1.0)
    parser.add_argument("--progress-interval", type=float, default=30.0)
    return parser.parse_args()


def main():
    args = parse_args()
    rclpy.init()
    node = ContinuousExplorationRecorder(args)
    try:
        node.run()
        metrics = node.write_outputs()
    finally:
        node.destroy_node()
        rclpy.shutdown()

    print("P2B_CONTINUOUS_EXPLORATION_RECORDER_RESULT")
    print(f"run_id={metrics['run_id']}")
    print(f"duration_sec={metrics['duration_sec']:.1f}")
    print(f"uav_total_distance={metrics['uav_total_distance']:.3f}")
    print(f"uav_net_displacement={metrics['uav_net_displacement']:.3f}")
    print(f"goal_msg_count={metrics['goal_msg_count']}")
    print(f"unique_goal_count={metrics['unique_goal_count']}")
    print(f"trajectory_count={metrics['trajectory_count']}")
    last_frontier = metrics["frontier_candidate_count_series"][-1] if metrics["frontier_candidate_count_series"] else 0
    print(f"frontier_candidate_count_last={last_frontier}")
    print(f"explored_grid_start={metrics['explored_grid_point_count_start']}")
    print(f"explored_grid_end={metrics['explored_grid_point_count_end']}")
    print(f"coverage_proxy_start={metrics['coverage_proxy_start']:.6f}")
    print(f"coverage_proxy_end={metrics['coverage_proxy_end']:.6f}")
    print(f"coverage_proxy_gain={metrics['coverage_proxy_gain']:.6f}")
    print(f"stuck_event_count={metrics['stuck_event_count']}")
    print(f"coverage_stall_event_count={len(metrics['coverage_stall_events'])}")
    print(f"repeated_goal_count={metrics['repeated_goal_count']}")
    print(f"result={metrics['result']}")
    return 0 if metrics["result"] in ["PASS", "PARTIAL"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
