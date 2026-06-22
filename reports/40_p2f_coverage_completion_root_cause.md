# P2F Coverage Completion Root Cause

## Evidence

Baseline command:

```bash
./scripts/run_with_log.sh p2f_coverage_300s_baseline ./scripts/run_p2f_coverage_300s_baseline.sh
```

Baseline metrics:

- duration_sec: 300.0266263484955
- odom_total_distance: 70.44073158711846
- coverage_proxy_start: 0.0
- coverage_proxy_end: 0.20416728022382566
- coverage_proxy_gain: 0.20416728022382566
- coverage_stall_max_duration_sec: 60.02682113647461
- frontier_count_end: 184
- active_path_update_count: 221
- position_cmd_update_count: 221
- goal_reselect_after_path_done_count: 22
- goal_reselect_after_coverage_stall_count: 7
- path_done_without_reselect_count: 0
- coverage_stall_without_reselect_count: 0
- main_coverage_blocker: COVERAGE_GROWING

## Root Cause

The P2E path feasibility fix restored the active path and position command chain. The remaining coverage issue is not DDS, RViz, or stale trajectory holding. The system can continue moving and reselect goals, but runs are variable: some runs continue growing coverage, while others plateau with many frontier candidates still available.

The most likely remaining blocker is frontier scoring or reachability selection in local-minimum situations, not a missing path_done reselect hook.
