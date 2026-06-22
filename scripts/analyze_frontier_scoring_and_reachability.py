#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics-dir", required=True)
    args = parser.parse_args()
    metrics_dir = Path(args.metrics_dir)
    data = json.loads((metrics_dir / "frontier_reachability.json").read_text(encoding="utf-8"))
    keys = [
        "main_frontier_blocker",
        "coverage_proxy_gain",
        "frontier_candidate_count_end",
        "frontier_viewpoint_count_end",
        "selected_goal_unique_count",
        "selected_goal_region_count",
        "active_path_endpoint_to_goal_distance_avg",
        "active_path_endpoint_to_goal_distance_max",
        "unreachable_goal_ratio",
        "coverage_gain_after_goal_avg",
        "low_gain_goal_count",
    ]
    out = {k: data.get(k, "UNAVAILABLE") for k in keys}
    (metrics_dir / "frontier_scoring_analysis.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# P2G Frontier Scoring And Reachability Analysis", ""]
    for k, v in out.items():
        lines.append(f"- {k}: {v}")
    (metrics_dir / "frontier_scoring_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("P2G_FRONTIER_SCORING_ANALYSIS_RESULT")
    for k, v in out.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
