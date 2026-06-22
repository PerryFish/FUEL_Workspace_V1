# P2I Final Summary

- workspace: `/home/nuaa/ZHY/FUEL_PLANNER_V3`
- colcon_build: PASS
- command/log system: PASS
- summary metrics matching: PASS
- RViz crash detection: PASS
- 300s headless: PASS
- 300s visual: PARTIAL_WITH_RVIZ_CRASH
- 900s headless: FAIL_EARLY_UAV_IDLE_DUE_TO_NO_PATH

## Key Metrics
- final 300s run_id: `p2i_route_300s_after_fix_20260622_143133`
- coverage_proxy_gain_300s: 0.152481
- odom_total_distance_300s: 77.931
- selected_goal_unique_count_300s: 27
- path_length_regret_avg_300s: -2.448
- path_length_regret_max_300s: 4.819
- route_revisit_ratio_300s: 0.868
- route_tortuosity_300s: 6.108
- goal_without_path_count_300s: 0
- goal_to_path_timeout_count_300s: 6
- active_goal_without_active_path_max_duration_sec_300s: 3.999
- active_goal_without_travel_traj_max_duration_sec_300s: 3.999
- uav_idle_due_to_no_path_duration_sec_300s: 0.0

## Root Cause
RViz goal-without-path was caused by goal-to-path/path publication gaps, not by DDS/RViz display alone. The final 300s fix prevents short-run idle by retiring/reselecting no-path goals and by rejecting endpoint outliers faster. Long-run 900s still exposes a residual no-path idle state, so completion is partial.

## Next Action
Start a focused P2J long-run watchdog and travel trajectory recovery task. Use the 900s early-fail raw/full logs as the primary reproduction instead of changing path cost again.

