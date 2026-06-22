# P2G Coverage 600s Validation

- run_id: `p2g_coverage_600s_after_fix_20260622_120315`
- duration_sec: 600.035
- odom_total_distance: 41.137m
- coverage_proxy_start: 0.079664
- coverage_proxy_end: 0.152481
- coverage_proxy_gain: 0.072817
- coverage_stall_max_duration_sec: 389.957
- frontier_candidate_count_end: 153
- frontier_viewpoint_count_end: 26
- selected_goal_unique_count: 11
- selected_goal_region_count: 11
- active_path_update_count: 148
- active_path_endpoint_to_goal_distance_avg: 0.489m
- active_path_endpoint_to_goal_distance_max: 16.135m
- unreachable_goal_ratio: 0.796
- coverage_gain_after_goal_avg: 0.015086
- low_gain_goal_count: 2
- main_frontier_blocker: `PATH_ENDPOINT_FAR_FROM_GOAL`

## Result

The 600s run was stable and did not crash, but it became stalled after about 210s. Coverage grew early, then stopped while frontier candidates and viewpoints remained. The long-run status is `STALLED`, not `COVERAGE_SATURATED`.

The remaining issue is a second-order reachability/scoring problem: after reachable high-value regions are consumed, the remaining frontiers still produce many infeasible path attempts. P2G's temporary region blacklist improves the 300s window but is not strong enough for long-run completion.
