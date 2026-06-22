# P2I Goal Without Path Diagnosis And Fix

## User Observation
RViz showed a selected goal/direction marker, but no path or trajectory appeared for a long time, and the UAV stayed still.

## Diagnosis
The failing chain is:

`selected goal -> goal_to_path_bridge -> active_path -> travel_traj -> position_cmd -> odom motion`

Evidence from P2I runs:
- Before final timing/install fix, 300s runs showed `UAV_IDLE_DUE_TO_NO_PATH` or active/travel missing durations above 20s.
- Final headless 300s run:
  - `goal_without_path_count=0`
  - `active_goal_without_active_path_max_duration_sec=3.999`
  - `active_goal_without_travel_traj_max_duration_sec=3.999`
  - `uav_idle_due_to_no_path_duration_sec=0.0`
- Visual 300s still showed RViz crash and longer visual-mode travel-traj missing, but not UAV idle due to no path.
- 900s early run still reproduced long-run `UAV_IDLE_DUE_TO_NO_PATH`.

## Fix
- `src/FUEL/scripts/exploration_manager_lite.py`
  - subscribes `/fuel/p10_lite/active_path`
  - subscribes `/planning/travel_traj`
  - adds no-path watchdog
  - retires/blacklists/reselects no-path goals
  - outputs lifecycle events including `GOAL_TO_PATH_REQUEST`, `GOAL_TO_PATH_TIMEOUT`, `ACTIVE_PATH_MISSING`, `GOAL_RETIRED`, `GOAL_BLACKLIST`, `GOAL_RESELECT`
- `src/FUEL/scripts/p11_lite_goal_to_path_bridge.py`
  - adds `GOAL_TO_PATH_REQUEST/SUCCESS/WAITING/TIMEOUT/FAIL` status event fields
- `scripts/fuel_route_rationality_recorder.py`
  - records goal-without-path metrics
  - cuts goal missing durations at lifecycle retire events

## Before/After
- before final fix: max active/travel missing reached 74.85s and idle due to no path reached 89.90s in a 300s run.
- after final installed fix: max active/travel missing dropped to 3.999s and idle due to no path dropped to 0.0s in the final 300s headless run.

## Remaining
The 900s early run still reproduced long-run no-path idle. Next work should focus on why watchdog recovery did not continue to hold during long-run saturation/reselection.

