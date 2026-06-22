# FUEL Unified Run Summary

## Basic Info
- Date: 2026-06-22T11:15:40+0800
- Task name: p2f_colcon_build_after_tuning
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/build.sh
- Exit code: 0
- Result: PASS
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_111428_p2f_colcon_build_after_tuning.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_111535_p2f_colcon_build_after_tuning_summary.md

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
- latest diff patch if available: reports/p2f_after_final_coverage_recovery_tuning_diff_20260622_111428.patch

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
- duration_sec: 300.0097942352295
- odom_total_distance: 46.33995809483194
- uav_total_distance: UNAVAILABLE
- uav_net_displacement: 12.719930009365497
- odom_net_displacement: 12.719930009365497
- odom_max_no_motion_duration_sec: 190.60013389587402
- goal_msg_count: 418
- goal_switch_count: 18
- unique_goal_count: 19
- unique_goal_count_quantized_1p0m: UNAVAILABLE
- same_goal_max_duration_sec: 59.99911403656006
- goal_reselect_count: 18
- goal_reselect_after_path_done_count: 0
- goal_reselect_after_coverage_stall_count: 6
- goal_reselect_after_no_motion_count: 14
- active_path_update_count: 203
- active_path_done_event_count: 0
- active_path_same_hash_max_duration_sec: 37.88946199417114
- active_path_endpoint_to_goal_distance_avg: 0.42727784651420536
- active_path_endpoint_to_goal_distance_max: UNAVAILABLE
- travel_traj_update_count: UNAVAILABLE
- travel_traj_same_hash_max_duration_sec: UNAVAILABLE
- position_cmd_update_count: 204
- position_cmd_total_variation: 47.29908288330633
- position_cmd_same_pose_max_duration_sec: UNAVAILABLE
- position_cmd_to_odom_distance_avg: UNAVAILABLE
- trajectory_count: UNAVAILABLE
- frontier_count_start: 102
- frontier_count_end: 169
- frontier_count_avg: 126.93
- explored_grid_start: 1198
- explored_grid_end: 2607
- explored_grid_gain: 1409
- coverage_proxy_start: 0.08820497717567369
- coverage_proxy_end: 0.19194522161684582
- coverage_proxy_gain: 0.10374024444117214
- coverage_proxy_gain_per_min: 0.020747370715044063
- coverage_stall_count: UNAVAILABLE
- coverage_stall_event_count: 2
- coverage_stall_max_duration_sec: 90.0668535232544
- stuck_event_count: UNAVAILABLE
- path_done_without_reselect_count: 0
- coverage_stall_without_reselect_count: 0
- traj_server_stale_path_hold_count: UNAVAILABLE
- quadrotor_sim_motion_blocked_count: UNAVAILABLE
- main_chain_break: UNAVAILABLE
- main_stuck_cause: UNAVAILABLE
- main_coverage_blocker: COVERAGE_STALL_NO_RESELECT

## Generated Files
- test-log/20260622_111428_p2f_colcon_build_after_tuning.md
- reports/p2f_after_final_coverage_recovery_tuning_diff_20260622_111428.patch
- reports/p2f_before_final_coverage_recovery_tuning_diff_20260622_111402.patch
- test-log/20260622_110803_p2f_coverage_300s_after_fix.md
- test-log-summary/20260622_111330_p2f_coverage_300s_after_fix_summary.md
- reports/p2f_metrics/p2f_coverage_300s_after_fix_20260622_110805/coverage_stall_analysis.md
- reports/p2f_metrics/p2f_coverage_300s_after_fix_20260622_110805/coverage_stall_analysis.json
- reports/p2f_metrics/p2f_coverage_300s_after_fix_20260622_110805/coverage_timeseries.csv
- reports/p2f_metrics/p2f_coverage_300s_after_fix_20260622_110805/coverage_events.csv
- reports/p2f_metrics/p2f_coverage_300s_after_fix_20260622_110805/coverage_completion.md
- reports/p2f_metrics/p2f_coverage_300s_after_fix_20260622_110805/coverage_completion.json
- reports/p2f_after_recorder_global_cloud_fix_diff_20260622_110803.patch
- test-log/20260622_110613_p2f_coverage_300s_after_fix.md
- test-log/20260622_110458_p2f_colcon_build.md
- test-log-summary/20260622_110600_p2f_colcon_build_summary.md

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
- Investigate/fix `COVERAGE_STALL_NO_RESELECT` with the smallest targeted change.
