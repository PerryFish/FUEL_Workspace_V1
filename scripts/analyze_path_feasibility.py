#!/usr/bin/env python3
import argparse, json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--metrics-dir", required=True)
args = parser.parse_args()
p = Path(args.metrics_dir)
data = json.loads((p / "motion_chain.json").read_text())
result = {
    "active_path_msg_count": data.get("active_path_msg_count", 0),
    "active_path_update_count": data.get("active_path_update_count", 0),
    "active_path_endpoint_to_goal_distance_avg": data.get("active_path_endpoint_to_goal_distance_avg", 0),
    "active_path_endpoint_to_goal_distance_max": data.get("active_path_endpoint_to_goal_distance_max", 0),
    "active_path_same_hash_max_duration_sec": data.get("active_path_same_hash_max_duration_sec", 0),
    "path_feasibility_break": data.get("main_chain_break") == "PATH_FEASIBILITY",
}
(p / "path_feasibility.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
(p / "path_feasibility.md").write_text("# P2D Path Feasibility Analysis\n\n" + "\n".join(f"- {k}: {v}" for k, v in result.items()) + "\n", encoding="utf-8")
print("P2D_PATH_FEASIBILITY_ANALYSIS_RESULT")
for k, v in result.items():
    print(f"{k}={v}")
