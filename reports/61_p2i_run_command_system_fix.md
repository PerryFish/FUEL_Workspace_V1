# P2I Run Command System Fix

- task: P2I_RUN_COMMANDS_FULL_VISUAL_AND_ENDPOINT_OUTLIER_FIX
- workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- result: PASS

## Changes
- Added P2I full/manual route commands to `scripts/fuel_run_commands_common.py`.
- Added `scripts/print_fuel_run_commands.sh`.
- Added:
  - `scripts/run_p2i_route_300s_after_fix.sh`
  - `scripts/run_p2i_visual_route_300s.sh`
  - `scripts/run_p2i_route_900s_after_fix.sh`
  - `scripts/run_p2i_visual_route_full.sh`
  - `scripts/run_p2i_route_full.sh`
- `scripts/run_p2i_route_full.sh --duration 0` now runs until Enter/Ctrl+C instead of using a fake 86400s duration.

## Validation
- command test: `./scripts/run_with_log.sh p2i_command_log_test bash -lc './scripts/print_fuel_run_commands.sh'`
- summary: `test-log-summary/20260622_135640_p2i_command_log_test_summary.md`
- full log: `test-log-summary/20260622_135646_p2i_command_log_test_full_log.md`

