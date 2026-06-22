# P2F Coverage 300s Validation

## Baseline

- run_id: `p2f_coverage_300s_baseline_20260622_105056`
- summary_log: `test-log-summary/20260622_105622_p2f_coverage_300s_baseline_summary.md`
- duration_sec: 300.0266263484955
- odom_total_distance: 70.44073158711846
- coverage_proxy_gain: 0.20416728022382566
- coverage_stall_max_duration_sec: 60.02682113647461
- frontier_count_end: 184
- active_path_update_count: 221
- position_cmd_update_count: 221
- goal_reselect_after_path_done_count: 22
- goal_reselect_after_coverage_stall_count: 7
- main_coverage_blocker: COVERAGE_GROWING

## Final After-fix

- run_id: `p2f_coverage_300s_after_fix_20260622_111559`
- summary_log: `test-log-summary/20260622_112124_p2f_coverage_300s_after_fix_summary.md`
- duration_sec: 300.03342604637146
- odom_total_distance: 18.509696768056585
- coverage_proxy_start: 0.08511264909438963
- coverage_proxy_end: 0.10072154321896627
- coverage_proxy_gain: 0.015608894124576639
- coverage_stall_max_duration_sec: 179.96832275390625
- frontier_count_end: 114
- active_path_update_count: 66
- position_cmd_update_count: 66
- goal_reselect_after_path_done_count: 17
- goal_reselect_after_coverage_stall_count: 2
- path_done_without_reselect_count: 0
- coverage_stall_without_reselect_count: 0
- main_coverage_blocker: FRONTIER_SCORING_OR_REACHABILITY_LIMIT

## Conclusion

P2F 300s validation is PARTIAL. The best baseline run satisfies the P2F hard targets, but the final after-fix run did not reliably preserve that behavior. Since path_done and coverage_stall reselect counters are nonzero, the next blocker is likely frontier scoring/reachability rather than missing reselect publication.
