# P2I 300s Validation

- result: PASS
- run_id: `p2i_route_300s_after_fix_20260622_143133`
- raw log: `test-log/20260622_143131_p2i_route_300s_after_fix.md`
- summary: `test-log-summary/20260622_143658_p2i_route_300s_after_fix_summary.md`
- full log: `test-log-summary/20260622_143704_p2i_route_300s_after_fix_full_log.md`
- metrics: `reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_rationality.json`

| metric | value |
| --- | ---: |
| duration_sec | 300.008 |
| odom_total_distance | 77.931 |
| coverage_proxy_gain | 0.152481 |
| coverage_gain_per_meter | 0.001957 |
| selected_goal_unique_count | 27 |
| path_length_regret_avg | -2.448 |
| path_length_regret_max | 4.819 |
| route_revisit_ratio | 0.868 |
| route_tortuosity | 6.108 |
| active_path_endpoint_to_goal_distance_avg | 0.000 |
| active_path_endpoint_to_goal_distance_max | 0.000 |
| goal_without_path_count | 0 |
| goal_to_path_timeout_count | 6 |
| active_goal_without_active_path_max_duration_sec | 3.999 |
| active_goal_without_travel_traj_max_duration_sec | 3.999 |
| uav_idle_due_to_no_path_duration_sec | 0.000 |
| main_route_issue | GOAL_TO_PATH_TIMEOUT |

## Result
The 300s headless run no longer reproduced long UAV idle due to no path. Remaining timeout events are short and recover without idle.

