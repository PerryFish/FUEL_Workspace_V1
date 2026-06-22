# P2I RViz Crash Detection Fix

- result: PASS

## Root Cause
The earlier visual script could complete the recorder and still report PASS even when `rviz2` aborted with a core dump.

## Fix
- `scripts/run_p2i_visual_route_300s.sh` monitors the RViz PID.
- If RViz exits non-zero, the script prints:
  - `RVIZ_CRASHED=YES`
  - `RVIZ_EXIT_CODE=<code>`
  - `VISUAL_RESULT=PARTIAL_WITH_RVIZ_CRASH`

## Validation
- visual run: `test-log/20260622_143719_p2i_visual_route_300s.md`
- summary: `test-log-summary/20260622_144241_p2i_visual_route_300s_summary.md`
- full log: `test-log-summary/20260622_144247_p2i_visual_route_300s_full_log.md`
- observed: `RVIZ_CRASHED=YES`, `RVIZ_EXIT_CODE=134`, `VISUAL_RESULT=PARTIAL_WITH_RVIZ_CRASH`

## Goal Without Path Note
The same visual run still showed `TRAVEL_TRAJ_MISSING_AFTER_GOAL` and max missing duration 24.5s, but `uav_idle_due_to_no_path_duration_sec=0.0`. This is logged as a visual/trajectory-chain residual, not a hidden PASS.

