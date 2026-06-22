#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics-dir", required=True)
    args = parser.parse_args()
    metrics_dir = Path(args.metrics_dir)
    data = json.loads((metrics_dir / "route_rationality.json").read_text(encoding="utf-8"))
    keys = [
        "main_route_issue",
        "coverage_proxy_gain",
        "coverage_gain_per_meter",
        "odom_total_distance",
        "selected_goal_unique_count",
        "path_length_regret_avg",
        "path_length_regret_max",
        "nearest_frontier_ignored_count",
        "near_high_gain_candidate_ignored_count",
        "route_revisit_ratio",
        "route_tortuosity",
        "active_path_endpoint_to_goal_distance_avg",
        "active_path_endpoint_to_goal_distance_max",
    ]
    out = {k: data.get(k, "UNAVAILABLE") for k in keys}
    (metrics_dir / "route_rationality_analysis.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# P2H Route Rationality Analysis", ""]
    for k, v in out.items():
        lines.append(f"- {k}: {v}")
    (metrics_dir / "route_rationality_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT")
    for k, v in out.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
