# P2I 900s Validation

- result: FAIL_EARLY_UAV_IDLE_DUE_TO_NO_PATH
- planned_duration_sec: 900
- stopped_at_sec: approximately 180
- exit_code: 130
- raw log: `test-log/20260622_144302_p2i_route_900s_after_fix.md`
- summary: `test-log-summary/20260622_144729_p2i_route_900s_after_fix_summary.md`
- full log: `test-log-summary/20260622_144735_p2i_route_900s_after_fix_full_log.md`

## Evidence
The 900s run was stopped early because it reproduced the long-run issue:
- 90s: odom_total_distance stayed at 9.896m
- 120s: `main_route_issue=UAV_IDLE_DUE_TO_NO_PATH`
- 150s: still `UAV_IDLE_DUE_TO_NO_PATH`
- 180s: still reported `UAV_IDLE_DUE_TO_NO_PATH`, with only minor movement afterward

## Result
The 300s no-path watchdog fix is effective in the final headless 300s run, but long-run completion is still not solved. Do not mark 900s PASS.

