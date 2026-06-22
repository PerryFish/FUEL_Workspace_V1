#!/usr/bin/env python3
import argparse
import json
import os
import re
import socket
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    from fuel_run_commands_common import RUN_COMMANDS_MARKDOWN
except ImportError:  # pragma: no cover
    RUN_COMMANDS_MARKDOWN = ""


IMPORTANT_TOPICS = [
    "/odom",
    "/planning/pos_cmd",
    "/planning/travel_traj",
    "/fuel/p10_lite/active_path",
    "/fuel/p10_lite/traj_server_status",
    "/fuel/p11_lite/goal_to_path_status",
    "/fuel/p11_lite/exploration_goal",
    "/fuel/p11_lite/frontier_viewpoints",
    "/fuel/p11_lite/frontier_candidates_raw",
    "/fuel/p11_lite/visual/all_markers",
]

METRIC_KEYS = [
    "duration_sec",
    "odom_total_distance",
    "uav_total_distance",
    "uav_net_displacement",
    "odom_net_displacement",
    "odom_max_no_motion_duration_sec",
    "goal_msg_count",
    "goal_switch_count",
    "unique_goal_count",
    "unique_goal_count_quantized_1p0m",
    "same_goal_max_duration_sec",
    "goal_reselect_count",
    "goal_reselect_after_path_done_count",
    "goal_reselect_after_coverage_stall_count",
    "goal_reselect_after_no_motion_count",
    "active_path_update_count",
    "active_path_done_event_count",
    "active_path_same_hash_max_duration_sec",
    "active_path_endpoint_to_goal_distance_avg",
    "active_path_endpoint_to_goal_distance_max",
    "travel_traj_update_count",
    "travel_traj_same_hash_max_duration_sec",
    "position_cmd_update_count",
    "position_cmd_total_variation",
    "position_cmd_same_pose_max_duration_sec",
    "position_cmd_to_odom_distance_avg",
    "trajectory_count",
    "frontier_count_start",
    "frontier_count_end",
    "frontier_count_avg",
    "explored_grid_start",
    "explored_grid_end",
    "explored_grid_gain",
    "coverage_proxy_start",
    "coverage_proxy_end",
    "coverage_proxy_gain",
    "coverage_proxy_gain_per_min",
    "coverage_stall_count",
    "coverage_stall_event_count",
    "coverage_stall_max_duration_sec",
    "stuck_event_count",
    "path_done_without_reselect_count",
    "coverage_stall_without_reselect_count",
    "traj_server_stale_path_hold_count",
    "quadrotor_sim_motion_blocked_count",
    "main_chain_break",
    "main_stuck_cause",
    "main_coverage_blocker",
    "main_route_issue",
    "coverage_gain_per_meter",
    "selected_goal_unique_count",
    "path_length_regret_avg",
    "path_length_regret_max",
    "near_high_gain_candidate_ignored_count",
    "route_revisit_ratio",
    "route_tortuosity",
    "goal_selected_count",
    "goal_without_path_count",
    "goal_without_path_ratio",
    "goal_to_path_latency_avg_sec",
    "goal_to_path_latency_max_sec",
    "goal_to_path_timeout_count",
    "goal_to_path_timeout_max_duration_sec",
    "active_goal_without_active_path_max_duration_sec",
    "active_goal_without_travel_traj_max_duration_sec",
    "path_missing_after_goal_count",
    "path_missing_after_goal_max_duration_sec",
    "path_generation_fail_count",
    "path_generation_fail_reasons",
    "active_path_empty_count",
    "active_path_first_update_after_goal_sec",
    "travel_traj_first_update_after_goal_sec",
    "uav_idle_due_to_no_path_duration_sec",
    "no_path_blacklist_count",
    "goal_reselect_due_to_no_path_count",
]


def run(cmd: List[str], cwd: Path, timeout: int = 8) -> str:
    try:
        return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, timeout=timeout, check=False).stdout.strip()
    except Exception as exc:
        return f"UNAVAILABLE ({type(exc).__name__}: {exc})"


def safe_task(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "task"


def recent_files(workspace: Path, patterns: Iterable[str], since: float) -> List[Path]:
    files: List[Path] = []
    for pattern in patterns:
        for path in workspace.glob(pattern):
            if path.is_file() and path.stat().st_mtime >= since:
                files.append(path)
    return sorted(set(files), key=lambda p: p.stat().st_mtime, reverse=True)


def raw_log_start_time(raw_log: Path) -> float:
    match = re.search(r"(\d{8})_(\d{6})", raw_log.name)
    if not match:
        return raw_log.stat().st_mtime if raw_log.exists() else time.time()
    try:
        return time.mktime(time.strptime("_".join(match.groups()), "%Y%m%d_%H%M%S"))
    except ValueError:
        return raw_log.stat().st_mtime if raw_log.exists() else time.time()


def run_ids_from_raw(raw_text: str) -> List[str]:
    ids = []
    for match in re.finditer(r"\brun_id=([A-Za-z0-9_.:-]+)", raw_text):
        ids.append(match.group(1))
    return list(dict.fromkeys(ids))


def latest_files(workspace: Path, patterns: Iterable[str], limit: int = 20) -> List[Path]:
    files: List[Path] = []
    for pattern in patterns:
        files.extend([p for p in workspace.glob(pattern) if p.is_file()])
    return sorted(set(files), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def set_if_missing(metrics: Dict[str, Any], key: str, value: Any) -> None:
    if value not in (None, "", [], {}) and metrics.get(key, "UNAVAILABLE") == "UNAVAILABLE":
        metrics[key] = value


def collect_metrics(workspace: Path, since: float, task_name: str, raw_text: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
    metrics = {key: "UNAVAILABLE" for key in METRIC_KEYS}
    source = {
        "metrics_source": "NONE",
        "metrics_source_path": "UNAVAILABLE",
        "metrics_source_reason": "no current-run metrics matched task_name/run_id/timestamp",
        "matched_by": "NONE",
    }
    all_candidates = recent_files(
        workspace,
        [
            "reports/p2*_metrics/*/motion_chain.json",
            "reports/p2*_metrics/*/coverage_completion.json",
            "reports/p2*_metrics/*/frontier_reachability.json",
            "reports/p2*_metrics/*/route_rationality.json",
            "reports/p2*_metrics/*/metrics.json",
            "reports/p2*_metrics/*/goal_lifecycle.json",
            "reports/p2*_metrics/*/stuck_analysis.json",
            "reports/p2*_metrics/*/traj_server_analysis.json",
            "reports/p2*_metrics/*/path_feasibility.json",
        ],
        since,
    )
    task = safe_task(task_name)
    run_ids = run_ids_from_raw(raw_text)
    json_candidates: List[Path] = []
    matched_by = "NONE"
    for path in all_candidates:
        text_path = str(path)
        if any(run_id and run_id in text_path for run_id in run_ids):
            json_candidates.append(path)
            matched_by = "run_id"
    if not json_candidates and task:
        for path in all_candidates:
            if task in str(path):
                json_candidates.append(path)
                matched_by = "task_name"
    if not json_candidates:
        raw_metrics = parse_metrics_from_raw(raw_text)
        if raw_metrics:
            for key, value in raw_metrics.items():
                if key in metrics:
                    metrics[key] = value
            source = {
                "metrics_source": "RAW_LOG_RECORDER_RESULT",
                "metrics_source_path": str(raw_log_hint(raw_text)),
                "metrics_source_reason": "parsed P2H/P2I recorder result directly from raw log",
                "matched_by": "raw_log_reference",
            }
            return metrics, source
        return metrics, source
    for path in reversed(json_candidates):
        data = load_json(path)
        for key in METRIC_KEYS:
            if key in data:
                set_if_missing(metrics, key, data[key])
        if "frontier_candidate_count_series" in data and isinstance(data["frontier_candidate_count_series"], list):
            series = data["frontier_candidate_count_series"]
            if series:
                set_if_missing(metrics, "frontier_count_start", series[0])
                set_if_missing(metrics, "frontier_count_end", series[-1])
        aliases = {
            "explored_grid_point_count_start": "explored_grid_start",
            "explored_grid_point_count_end": "explored_grid_end",
            "goal_lifecycle_goal_switch_count": "goal_switch_count",
            "odom_net_displacement": "uav_net_displacement",
        }
        for src, dst in aliases.items():
            if src in data:
                set_if_missing(metrics, dst, data[src])
        if "main_goal_lifecycle_cause" in data:
            set_if_missing(metrics, "main_stuck_cause", data["main_goal_lifecycle_cause"])
    source = {
        "metrics_source": "CURRENT_RUN" if matched_by == "run_id" else "LATEST_MATCHED_TASK",
        "metrics_source_path": rel(workspace, json_candidates[0]),
        "metrics_source_reason": f"matched current run metrics by {matched_by} after raw log start timestamp",
        "matched_by": matched_by,
    }
    return metrics, source


def raw_log_hint(raw_text: str) -> str:
    ids = run_ids_from_raw(raw_text)
    return ids[-1] if ids else "raw_log"


def parse_metrics_from_raw(raw_text: str) -> Dict[str, Any]:
    markers = [
        "P2H_ROUTE_RATIONALITY_RECORDER_RESULT",
        "P2I_ROUTE_RATIONALITY_RECORDER_RESULT",
        "P2G_FRONTIER_REACHABILITY_RECORDER_RESULT",
        "P2F_COVERAGE_COMPLETION_RECORDER_RESULT",
    ]
    if not any(marker in raw_text for marker in markers):
        return {}
    parsed: Dict[str, Any] = {}
    active = False
    for line in raw_text.splitlines():
        if any(marker in line for marker in markers):
            active = True
            continue
        if active and re.match(r"^[A-Za-z0-9_]+=", line):
            key, value = line.split("=", 1)
            if key in METRIC_KEYS:
                parsed[key] = coerce_value(value.strip())
        elif active and line.startswith("P2") and "RESULT" in line:
            continue
        elif active and line.strip() == "":
            active = False
    return parsed


def coerce_value(value: str) -> Any:
    if value in ("true", "false"):
        return value
    try:
        if re.match(r"^-?\d+$", value):
            return int(value)
        return float(value)
    except ValueError:
        return value


def infer_result(exit_code: int, raw_text: str, metrics: Dict[str, Any]) -> str:
    if exit_code != 0:
        return "FAIL"
    upper = raw_text.upper()
    if "FAIL" in upper and "PASS" not in upper:
        return "FAIL"
    if "PARTIAL" in upper or metrics.get("main_chain_break") not in ("UNAVAILABLE", None, ""):
        return "PARTIAL"
    if "PASS" in upper:
        return "PASS"
    return "UNKNOWN" if not raw_text.strip() else "PASS"


def rel(workspace: Path, path: Path) -> str:
    try:
        return str(path.relative_to(workspace))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-name", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--exit-code", required=True, type=int)
    parser.add_argument("--raw-log", required=True)
    parser.add_argument("--workspace", default="/home/nuaa/ZHY/FUEL_PLANNER_V3")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    summary_dir = workspace / "test-log-summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    task = safe_task(args.task_name)
    summary = summary_dir / f"{stamp}_{task}_summary.md"
    raw_log = Path(args.raw_log).resolve()
    raw_text = raw_log.read_text(encoding="utf-8", errors="replace") if raw_log.exists() else ""
    since = raw_log_start_time(raw_log) - 5.0
    metrics, metric_source = collect_metrics(workspace, since, args.task_name, raw_text)
    result = infer_result(args.exit_code, raw_text, metrics)

    env = os.environ
    source_commit = run(["git", "-C", str(workspace), "rev-parse", "HEAD"], workspace, timeout=4)
    git_status = run(["git", "-C", str(workspace), "status", "--short", "--", "."], workspace, timeout=4)
    if len(git_status.splitlines()) > 80:
        lines = git_status.splitlines()
        git_status = "\n".join(lines[:80] + [f"... truncated {len(lines) - 80} additional lines ..."])
    changed = "\n".join(line[3:] if len(line) > 3 else line for line in git_status.splitlines()) or "UNAVAILABLE"
    latest_patch = latest_files(workspace, ["reports/*diff*.patch"], limit=1)
    node_list = run(["bash", "-lc", "source scripts/env.sh >/dev/null 2>&1 || true; ros2 node list --no-daemon --spin-time 2 2>/dev/null | head -80"], workspace)
    topic_list = run(["bash", "-lc", "source scripts/env.sh >/dev/null 2>&1 || true; ros2 topic list --no-daemon --spin-time 2 2>/dev/null | head -120"], workspace)
    topics = set(topic_list.splitlines())

    generated = recent_files(
        workspace,
        [
            "test-log/*.md",
            "test-log-summary/*.md",
            "reports/*.md",
            "reports/*debug_package*.tar.gz",
            "reports/latest_*_debug_package.tar.gz",
            "reports/p2*_metrics/*/*",
            "reports/*diff*.patch",
            "reports/screenshots/*",
        ],
        since,
    )

    diagnosis = [
        f"Result inferred as `{result}` from exit code and raw log.",
        f"Planner output metric: trajectory_count={metrics.get('trajectory_count', 'UNAVAILABLE')}.",
        f"Odom/motion metric: uav_total_distance={metrics.get('uav_total_distance', metrics.get('odom_total_distance', 'UNAVAILABLE'))}.",
        f"Main chain break: {metrics.get('main_chain_break', 'UNAVAILABLE')}.",
        f"Main stuck cause: {metrics.get('main_stuck_cause', 'UNAVAILABLE')}.",
        "RViz visual chain is expected to remain unchanged unless this task explicitly ran a visual check.",
    ]

    with summary.open("w", encoding="utf-8") as f:
        f.write("# FUEL Unified Run Summary\n\n")
        f.write("## Basic Info\n")
        f.write(f"- Date: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n")
        f.write(f"- Task name: {args.task_name}\n")
        f.write(f"- Workspace: {workspace}\n")
        f.write(f"- Command: {args.command}\n")
        f.write(f"- Exit code: {args.exit_code}\n")
        f.write(f"- Result: {result}\n")
        f.write(f"- Raw log file: {raw_log}\n")
        f.write(f"- Summary log file: {summary}\n\n")
        f.write("## Environment\n")
        for key in ["ROS_DISTRO", "ROS_DOMAIN_ID", "RMW_IMPLEMENTATION", "ROS_LOCALHOST_ONLY", "FASTDDS_BUILTIN_TRANSPORTS", "DISPLAY", "FUEL_WS"]:
            f.write(f"- {key}: {env.get(key, 'UNAVAILABLE')}\n")
        f.write("\n## Git / Source State\n")
        f.write(f"- current_commit: {source_commit}\n")
        f.write("- git status short:\n\n```text\n" + (git_status or "clean") + "\n```\n")
        f.write("- changed files:\n\n```text\n" + changed + "\n```\n")
        f.write(f"- latest diff patch if available: {rel(workspace, latest_patch[0]) if latest_patch else 'UNAVAILABLE'}\n\n")
        f.write("## Key Runtime Evidence\n")
        f.write("### Node List Summary\n```text\n" + (node_list or "UNAVAILABLE") + "\n```\n")
        f.write("### Topic List Summary\n```text\n" + (topic_list or "UNAVAILABLE") + "\n```\n")
        f.write("### Important Topics Detected\n")
        for topic in IMPORTANT_TOPICS:
            f.write(f"- {topic}: {'YES' if topic in topics else 'NO_OR_NOT_RUNNING'}\n")
        f.write("\n### Process Cleanup Status\n```text\n")
        f.write(run(["bash", "-lc", "ps aux | grep -E 'fuel|exploration|traj|quadrotor|pcl_render|rviz2' | grep -v grep || true"], workspace, timeout=4) or "NO_MATCHING_PROCESS_OR_NOT_CHECKED")
        f.write("\n```\n")
        f.write("\n## Metrics Summary\n")
        for key in ["metrics_source", "metrics_source_path", "metrics_source_reason", "matched_by"]:
            f.write(f"- {key}: {metric_source.get(key, 'UNAVAILABLE')}\n")
        for key in METRIC_KEYS:
            f.write(f"- {key}: {metrics.get(key, 'UNAVAILABLE')}\n")
        f.write("\n## Generated Files\n")
        if generated:
            for path in generated[:120]:
                f.write(f"- {rel(workspace, path)}\n")
        else:
            f.write("- UNAVAILABLE\n")
        f.write("\n## Diagnosis\n")
        for line in diagnosis:
            f.write(f"- {line}\n")
        f.write("\n")
        f.write(RUN_COMMANDS_MARKDOWN or "## Run Commands\n\nUNAVAILABLE\n")
        f.write("\n")
        f.write("### Latest Debug Packages\n\n```bash\ncd /home/nuaa/ZHY/FUEL_PLANNER_V3\nls -lh reports/latest_p2i_debug_package.tar.gz reports/latest_p2h_debug_package.tar.gz reports/latest_p2g_debug_package.tar.gz reports/latest_p2f_debug_package.tar.gz 2>/dev/null || true\n```\n\n")
        f.write("## Next Action\n")
        if metrics.get("main_coverage_blocker") not in ("UNAVAILABLE", None, ""):
            f.write(f"- Investigate/fix `{metrics.get('main_coverage_blocker')}` with the smallest targeted change.\n")
        elif metrics.get("main_chain_break") not in ("UNAVAILABLE", None, ""):
            f.write(f"- Investigate/fix `{metrics.get('main_chain_break')}` with the smallest targeted change.\n")
        else:
            f.write("- Run the next targeted diagnostic using `scripts/run_with_log.sh` so this summary system captures it.\n")

    print(f"UNIFIED_SUMMARY_LOG_CREATED={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
