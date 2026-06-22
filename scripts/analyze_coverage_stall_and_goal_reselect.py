#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics-dir", required=True)
    args = parser.parse_args()
    metrics_dir = Path(args.metrics_dir)
    data = json.loads((metrics_dir / "coverage_completion.json").read_text(encoding="utf-8"))
    blocker = data.get("main_coverage_blocker", "UNKNOWN")
    out = {
        "main_coverage_blocker": blocker,
        "coverage_stall_max_duration_sec": data.get("coverage_stall_max_duration_sec"),
        "path_done_without_reselect_count": data.get("path_done_without_reselect_count"),
        "coverage_stall_without_reselect_count": data.get("coverage_stall_without_reselect_count"),
        "goal_reselect_after_path_done_count": data.get("goal_reselect_after_path_done_count"),
        "goal_reselect_after_coverage_stall_count": data.get("goal_reselect_after_coverage_stall_count"),
    }
    (metrics_dir / "coverage_stall_analysis.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# P2F Coverage Stall And Goal Reselect Analysis", ""]
    for key, value in out.items():
        lines.append(f"- {key}: {value}")
    (metrics_dir / "coverage_stall_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("P2F_COVERAGE_STALL_ANALYSIS_RESULT")
    for key, value in out.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
