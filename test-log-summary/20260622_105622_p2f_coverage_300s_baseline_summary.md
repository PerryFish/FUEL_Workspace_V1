# FUEL Unified Run Summary

## Basic Info
- Date: 2026-06-22T10:56:27+0800
- Task name: p2f_coverage_300s_baseline
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2f_coverage_300s_baseline.sh
- Exit code: 0
- Result: PASS
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_105054_p2f_coverage_300s_baseline.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_105622_p2f_coverage_300s_baseline_summary.md

## Environment
- ROS_DISTRO: humble
- ROS_DOMAIN_ID: UNAVAILABLE
- RMW_IMPLEMENTATION: UNAVAILABLE
- ROS_LOCALHOST_ONLY: 0
- FASTDDS_BUILTIN_TRANSPORTS: UNAVAILABLE
- DISPLAY: :0
- FUEL_WS: UNAVAILABLE

## Git / Source State
- current_commit: 3b11fc50c0ab8e84f9093f084ce80f4d1af6088d
- git status short:

```text
?? ./
```
- changed files:

```text
./
```
- latest diff patch if available: reports/p2f_after_log_and_recorder_scripts_diff_20260622_105046.patch

## Key Runtime Evidence
### Node List Summary
```text
UNAVAILABLE
```
### Topic List Summary
```text
/parameter_events
/rosout
```
### Important Topics Detected
- /odom: NO_OR_NOT_RUNNING
- /planning/pos_cmd: NO_OR_NOT_RUNNING
- /planning/travel_traj: NO_OR_NOT_RUNNING
- /fuel/p10_lite/active_path: NO_OR_NOT_RUNNING
- /fuel/p10_lite/traj_server_status: NO_OR_NOT_RUNNING
- /fuel/p11_lite/goal_to_path_status: NO_OR_NOT_RUNNING
- /fuel/p11_lite/exploration_goal: NO_OR_NOT_RUNNING
- /fuel/p11_lite/frontier_viewpoints: NO_OR_NOT_RUNNING
- /fuel/p11_lite/frontier_candidates_raw: NO_OR_NOT_RUNNING
- /fuel/p11_lite/visual/all_markers: NO_OR_NOT_RUNNING

### Process Cleanup Status
```text
NO_MATCHING_PROCESS_OR_NOT_CHECKED
```

## Metrics Summary
- duration_sec: 300.0266263484955
- odom_total_distance: 70.44073158711846
- uav_total_distance: UNAVAILABLE
- uav_net_displacement: 20.383187871749765
- odom_net_displacement: 20.383187871749765
- odom_max_no_motion_duration_sec: 68.7003002166748
- goal_msg_count: 463
- goal_switch_count: 21
- unique_goal_count: 22
- unique_goal_count_quantized_1p0m: UNAVAILABLE
- same_goal_max_duration_sec: 40.00255298614502
- goal_reselect_count: 21
- goal_reselect_after_path_done_count: 22
- goal_reselect_after_coverage_stall_count: 7
- goal_reselect_after_no_motion_count: 7
- active_path_update_count: 221
- active_path_done_event_count: 0
- active_path_same_hash_max_duration_sec: 45.000773429870605
- active_path_endpoint_to_goal_distance_avg: 0.04609657593959517
- active_path_endpoint_to_goal_distance_max: UNAVAILABLE
- travel_traj_update_count: UNAVAILABLE
- travel_traj_same_hash_max_duration_sec: UNAVAILABLE
- position_cmd_update_count: 221
- position_cmd_total_variation: 71.58514950381429
- position_cmd_same_pose_max_duration_sec: UNAVAILABLE
- position_cmd_to_odom_distance_avg: UNAVAILABLE
- trajectory_count: UNAVAILABLE
- frontier_count_start: 98
- frontier_count_end: 184
- frontier_count_avg: 134.025
- explored_grid_start: 1094
- explored_grid_end: 2773
- explored_grid_gain: 1679
- coverage_proxy_start: 0.0
- coverage_proxy_end: 0.20416728022382566
- coverage_proxy_gain: 0.20416728022382566
- coverage_proxy_gain_per_min: 0.04082983104557952
- coverage_stall_count: UNAVAILABLE
- coverage_stall_event_count: 2
- coverage_stall_max_duration_sec: 60.02682113647461
- stuck_event_count: UNAVAILABLE
- path_done_without_reselect_count: 0
- coverage_stall_without_reselect_count: 0
- traj_server_stale_path_hold_count: UNAVAILABLE
- quadrotor_sim_motion_blocked_count: UNAVAILABLE
- main_chain_break: UNAVAILABLE
- main_stuck_cause: UNAVAILABLE
- main_coverage_blocker: COVERAGE_GROWING

## Generated Files
- test-log/20260622_105054_p2f_coverage_300s_baseline.md
- reports/p2f_metrics/p2f_coverage_300s_baseline_20260622_105056/coverage_stall_analysis.md
- reports/p2f_metrics/p2f_coverage_300s_baseline_20260622_105056/coverage_stall_analysis.json
- reports/p2f_metrics/p2f_coverage_300s_baseline_20260622_105056/coverage_completion.md
- reports/p2f_metrics/p2f_coverage_300s_baseline_20260622_105056/coverage_events.csv
- reports/p2f_metrics/p2f_coverage_300s_baseline_20260622_105056/coverage_completion.json
- reports/p2f_metrics/p2f_coverage_300s_baseline_20260622_105056/coverage_timeseries.csv
- reports/p2f_after_log_and_recorder_scripts_diff_20260622_105046.patch
- reports/39_p2f_unified_summary_log_fix_report.md
- test-log/20260622_104637_summary_system_test.md
- test-log-summary/20260622_104638_summary_system_test_summary.md

## Diagnosis
- Result inferred as `PASS` from exit code and raw log.
- Planner output metric: trajectory_count=UNAVAILABLE.
- Odom/motion metric: uav_total_distance=UNAVAILABLE.
- Main chain break: UNAVAILABLE.
- Main stuck cause: UNAVAILABLE.
- RViz visual chain is expected to remain unchanged unless this task explicitly ran a visual check.

## Visual Re-run Commands
Manual persistent visual demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh
```

Coverage visual diagnostic demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2f_visual_coverage_300s ./scripts/run_p2f_visual_coverage_300s.sh
```

Clean all FUEL/RViz processes:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh
```

Latest debug package:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
ls -lh reports/latest_p2f_debug_package.tar.gz reports/latest_p2e_debug_package.tar.gz reports/latest_p2d_debug_package.tar.gz reports/latest_p2c_debug_package.tar.gz 2>/dev/null || true
```

## Next Action
- Investigate/fix `COVERAGE_GROWING` with the smallest targeted change.
