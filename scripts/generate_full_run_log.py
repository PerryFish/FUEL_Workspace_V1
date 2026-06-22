#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Iterable, List


IMPORTANT_TOPICS = [
    "/odom",
    "/planning/pos_cmd",
    "/planning/travel_traj",
    "/fuel/p10_lite/active_path",
    "/fuel/p10_lite/position_cmd",
    "/fuel/p10_lite/traj_server_status",
    "/fuel/p10_lite/quadrotor_sim_status",
    "/fuel/p11_lite/exploration_goal",
    "/fuel/p11_lite/best_viewpoint",
    "/fuel/p11_lite/frontier_candidates_raw",
    "/fuel/p11_lite/frontier_viewpoints",
    "/fuel/p11_lite/explored_grid",
    "/fuel/p11_lite/occupancy_grid",
    "/fuel/p11_lite/exploration_manager_status",
    "/fuel/p11_lite/goal_to_path_status",
    "/fuel/p11_lite/visual/all_markers",
    "/map_generator/global_cloud",
    "/pcl_render_node/cloud",
    "/tf_static",
]

METRIC_NAMES = {
    "metrics.json",
    "coverage_completion.json",
    "frontier_reachability.json",
    "motion_chain.json",
    "goal_lifecycle.json",
    "path_feasibility.json",
    "traj_server_analysis.json",
    "stuck_analysis.json",
}


def safe_task(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "task"


def run(cmd: List[str], cwd: Path, timeout: int = 12) -> str:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, timeout=timeout, check=False)
        text = proc.stdout
        if proc.stderr:
            text += ("\n--- stderr ---\n" + proc.stderr)
        return text.strip() or "NO_OUTPUT"
    except Exception as exc:
        return f"UNAVAILABLE ({type(exc).__name__}: {exc})"


def raw_log_start_time(raw_log: Path) -> float:
    match = re.search(r"(\d{8})_(\d{6})", raw_log.name)
    if not match:
        return raw_log.stat().st_mtime if raw_log.exists() else time.time()
    try:
        return time.mktime(time.strptime("_".join(match.groups()), "%Y%m%d_%H%M%S"))
    except ValueError:
        return raw_log.stat().st_mtime if raw_log.exists() else time.time()


def run_ids_from_raw(raw_text: str) -> List[str]:
    return list(dict.fromkeys(m.group(1) for m in re.finditer(r"\brun_id=([A-Za-z0-9_.:-]+)", raw_text)))


def recent_files(workspace: Path, patterns: Iterable[str], since: float) -> List[Path]:
    files: List[Path] = []
    for pattern in patterns:
        for path in workspace.glob(pattern):
            if path.is_file() and path.stat().st_mtime >= since:
                files.append(path)
    return sorted(set(files), key=lambda p: p.stat().st_mtime, reverse=True)


def rel(workspace: Path, path: Path) -> str:
    try:
        return str(path.relative_to(workspace))
    except ValueError:
        return str(path)


def matched_metric_files(workspace: Path, since: float, task_name: str, raw_text: str) -> List[Path]:
    candidates = recent_files(workspace, ["reports/p2*_metrics/*/*"], since)
    candidates = [p for p in candidates if p.name in METRIC_NAMES or p.suffix in (".md", ".csv")]
    run_ids = run_ids_from_raw(raw_text)
    task = safe_task(task_name)
    matched = [p for p in candidates if any(run_id in str(p) for run_id in run_ids)]
    if matched:
        return matched
    return [p for p in candidates if task in str(p)]


def write_codeblock(f, lang: str, text: str) -> None:
    f.write(f"```{lang}\n")
    f.write(text.rstrip() + "\n")
    f.write("```\n\n")


def summarize_json(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(data, dict):
        return path.read_text(encoding="utf-8", errors="replace")
    keys = [
        "duration_sec",
        "odom_total_distance",
        "coverage_proxy_start",
        "coverage_proxy_end",
        "coverage_proxy_gain",
        "coverage_stall_max_duration_sec",
        "frontier_candidate_count_end",
        "frontier_viewpoint_count_end",
        "selected_goal_unique_count",
        "active_path_endpoint_to_goal_distance_avg",
        "unreachable_goal_ratio",
        "main_frontier_blocker",
        "main_coverage_blocker",
    ]
    return "\n".join(f"{key}={data.get(key, 'UNAVAILABLE')}" for key in keys)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-name", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--exit-code", required=True, type=int)
    parser.add_argument("--raw-log", required=True)
    parser.add_argument("--summary-log", default="")
    parser.add_argument("--workspace", default="/home/nuaa/ZHY/FUEL_PLANNER_V3")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    raw_log = Path(args.raw_log).resolve()
    raw_text = raw_log.read_text(encoding="utf-8", errors="replace") if raw_log.exists() else ""
    summary_log = Path(args.summary_log).resolve() if args.summary_log else Path("")
    out_dir = workspace / "test-log-summary"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    task = safe_task(args.task_name)
    full_log = out_dir / f"{stamp}_{task}_full_log.md"
    since = raw_log_start_time(raw_log) - 5.0
    metrics = matched_metric_files(workspace, since, args.task_name, raw_text)
    generated_reports = recent_files(workspace, ["reports/*.md"], since)
    topics_text = run(["bash", "-lc", "source scripts/env.sh >/dev/null 2>&1 || true; ros2 topic list -t --no-daemon --spin-time 2 2>/dev/null || true"], workspace, timeout=8)
    topic_lines = {line.split()[0] for line in topics_text.splitlines() if line.startswith("/")}

    with full_log.open("w", encoding="utf-8") as f:
        f.write("# FUEL Full Run Log\n\n")
        f.write("## 1. Basic Info\n")
        f.write(f"- Date: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}\n")
        f.write(f"- Task name: {args.task_name}\n")
        f.write(f"- Workspace: {workspace}\n")
        f.write(f"- Command: {args.command}\n")
        f.write(f"- Exit code: {args.exit_code}\n")
        f.write(f"- Raw log file: {raw_log}\n")
        f.write(f"- Summary log file: {summary_log if args.summary_log else 'UNAVAILABLE'}\n")
        f.write(f"- Full log file: {full_log}\n\n")

        f.write("## 2. Environment Snapshot\n")
        write_codeblock(f, "bash", run(["bash", "-lc", "env | sort | grep -E 'ROS|RMW|FAST|CYCLONE|DDS|AMENT|COLCON|FUEL|DISPLAY|LD_LIBRARY_PATH|PYTHONPATH' || true"], workspace))

        f.write("## 3. Git Snapshot\n")
        write_codeblock(f, "text", run(["bash", "-lc", "git -C /home/nuaa/ZHY/FUEL_PLANNER_V3 status --short -- .; git -C /home/nuaa/ZHY/FUEL_PLANNER_V3 log --oneline -5; git -C /home/nuaa/ZHY/FUEL_PLANNER_V3 branch --show-current; git -C /home/nuaa/ZHY/FUEL_PLANNER_V3 rev-parse HEAD"], workspace))

        f.write("## 4. Process Snapshot\n")
        write_codeblock(f, "text", run(["bash", "-lc", "ps aux | grep -E 'ros2|rviz|fuel|exploration|traj|waypoint|map_pub|quadrotor|pcl_render|so3|python' | grep -v grep || true"], workspace))

        f.write("## 5. ROS Node Snapshot\n")
        write_codeblock(f, "text", run(["bash", "-lc", "source scripts/env.sh >/dev/null 2>&1 || true; ros2 node list --no-daemon --spin-time 2 2>/dev/null || true"], workspace))

        f.write("## 6. ROS Topic Snapshot\n")
        write_codeblock(f, "text", topics_text)

        f.write("## 7. Important Topic Availability\n")
        for topic in IMPORTANT_TOPICS:
            f.write(f"- {topic}: {'YES' if topic in topic_lines else 'NO_OR_NOT_RUNNING'}\n")
        f.write("\n")

        f.write("## 8. Raw Command Output\n")
        write_codeblock(f, "text", raw_text or "UNAVAILABLE")

        f.write("## 9. Metrics Files Content\n")
        if not metrics:
            f.write("- UNAVAILABLE\n\n")
        for path in metrics[:40]:
            f.write(f"### {rel(workspace, path)}\n")
            if path.suffix == ".json":
                if path.stat().st_size < 300_000:
                    write_codeblock(f, "json", path.read_text(encoding="utf-8", errors="replace"))
                else:
                    f.write(f"- file_size_bytes: {path.stat().st_size}\n")
                    write_codeblock(f, "text", summarize_json(path))
            elif path.suffix == ".csv":
                f.write(f"- csv_path: {rel(workspace, path)}\n")
                f.write(f"- file_size_bytes: {path.stat().st_size}\n\n")
            else:
                write_codeblock(f, "markdown", path.read_text(encoding="utf-8", errors="replace")[:12000])

        f.write("## 10. Reports Generated\n")
        if not generated_reports:
            f.write("- UNAVAILABLE\n\n")
        for path in generated_reports[:40]:
            f.write(f"- {rel(workspace, path)}\n")
        f.write("\n")

        f.write("## 11. Debug Package\n")
        write_codeblock(f, "text", run(["bash", "-lc", "ls -lh reports/latest_p2g_debug_package.tar.gz reports/latest_p2f_debug_package.tar.gz reports/latest_p2d_debug_package.tar.gz 2>/dev/null || true"], workspace))

        f.write("## 12. Visual Re-run Commands\n")
        f.write("Manual persistent visual demo:\n\n```bash\ncd /home/nuaa/ZHY/FUEL_PLANNER_V3\n./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh\n```\n\n")
        f.write("Coverage visual diagnostic demo:\n\n```bash\ncd /home/nuaa/ZHY/FUEL_PLANNER_V3\n./scripts/run_with_log.sh p2g_visual_coverage_300s ./scripts/run_p2g_visual_coverage_300s.sh\n```\n\n")
        f.write("Clean all FUEL/RViz processes:\n\n```bash\ncd /home/nuaa/ZHY/FUEL_PLANNER_V3\n./scripts/kill_fuel.sh\n```\n\n")

        f.write("## 13. Final Diagnosis\n")
        f.write(f"- Command exit code: {args.exit_code}.\n")
        f.write(f"- Raw log path: {raw_log}.\n")
        f.write(f"- Summary log path: {summary_log if args.summary_log else 'UNAVAILABLE'}.\n")
        f.write(f"- Matched metrics files: {len(metrics)}.\n")
        f.write("- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.\n")
        f.write("- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.\n")
        f.write("- Use metrics JSON content above for run-time evidence when available.\n\n")

        f.write("## 14. Next Action\n")
        f.write("- Use the summary log for high-level status and this full log for detailed debugging evidence.\n")

    print(f"FULL_RUN_LOG_CREATED={full_log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
