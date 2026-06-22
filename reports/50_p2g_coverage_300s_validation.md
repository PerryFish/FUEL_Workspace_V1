# P2G Coverage 300s Validation

## Baseline

- run_id: `p2g_frontier_300s_baseline_20260622_114700`
- duration_sec: 300.013
- odom_total_distance: 1.405m
- coverage_proxy_start: 0.079591
- coverage_proxy_end: 0.085923
- coverage_proxy_gain: 0.006332
- coverage_stall_max_duration_sec: 239.972
- frontier_candidate_count_end: 105
- frontier_viewpoint_count_end: 44
- selected_goal_unique_count: 4
- selected_goal_region_count: 4
- active_path_update_count: 2
- active_path_endpoint_to_goal_distance_avg: 0.000m
- active_path_endpoint_to_goal_distance_max: 0.000m
- unreachable_goal_ratio: 0.993
- main_frontier_blocker: `PATH_ENDPOINT_FAR_FROM_GOAL`

## After Fix

- run_id: `p2g_coverage_300s_after_fix_20260622_115723`
- duration_sec: 300.030
- odom_total_distance: 50.235m
- coverage_proxy_start: 0.083346
- coverage_proxy_end: 0.185245
- coverage_proxy_gain: 0.101900
- coverage_stall_max_duration_sec: 0.000
- frontier_candidate_count_end: 174
- frontier_viewpoint_count_end: 25
- selected_goal_unique_count: 29
- selected_goal_region_count: 27
- active_path_update_count: 155
- active_path_endpoint_to_goal_distance_avg: 0.113m
- active_path_endpoint_to_goal_distance_max: 5.662m
- unreachable_goal_ratio: 0.320
- coverage_gain_after_goal_avg: 0.006616
- low_gain_goal_count: 17
- main_frontier_blocker: `PATH_ENDPOINT_FAR_FROM_GOAL`

## Result

300s after-fix is a practical PASS for coverage continuity: motion, active path updates, goal diversity, and coverage gain all improved sharply. The residual blocker remains reachability because some candidates still produce infeasible path status messages, but those failures no longer dominate the 300s office run.
