#!/usr/bin/env python3
import argparse, json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--metrics-dir", required=True)
args = parser.parse_args()
p = Path(args.metrics_dir)
data = json.loads((p / "motion_chain.json").read_text())
result = {
    "active_path_update_count": data.get("active_path_update_count", 0),
    "travel_traj_update_count": data.get("travel_traj_update_count", 0),
    "travel_traj_same_hash_max_duration_sec": data.get("travel_traj_same_hash_max_duration_sec", 0),
    "traj_server_stale_path_hold_count": data.get("traj_server_stale_path_hold_count", 0),
    "traj_server_break": data.get("main_chain_break") == "TRAJ_SERVER_STALE_PATH",
}
(p / "traj_server_analysis.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
(p / "traj_server_analysis.md").write_text("# P2D Traj Server Stale Path Analysis\n\n" + "\n".join(f"- {k}: {v}" for k, v in result.items()) + "\n", encoding="utf-8")
print("P2D_TRAJ_SERVER_ANALYSIS_RESULT")
for k, v in result.items():
    print(f"{k}={v}")
