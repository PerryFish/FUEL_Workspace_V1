# FUEL Unified Run Summary

## Basic Info
- Date: 2026-06-22T10:45:50+0800
- Task name: summary_system_test
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: bash -lc echo SUMMARY_SYSTEM_TEST_PASS
- Exit code: 0
- Result: PARTIAL
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_104543_summary_system_test.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_104544_summary_system_test_summary.md

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
- latest diff patch if available: reports/p2f_before_unified_summary_fix_diff_20260622_104237.patch

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
- duration_sec: 304.5817446708679
- odom_total_distance: 0.10123519195861462
- uav_total_distance: 1.1785774688180406
- uav_net_displacement: 1.136237705610727
- odom_net_displacement: 0.10123519195861475
- odom_max_no_motion_duration_sec: 299.5630552768707
- goal_msg_count: 599
- goal_switch_count: 53
- unique_goal_count: 14
- unique_goal_count_quantized_1p0m: 12
- same_goal_max_duration_sec: 23.910722732543945
- goal_reselect_count: UNAVAILABLE
- goal_reselect_after_path_done_count: UNAVAILABLE
- goal_reselect_after_coverage_stall_count: UNAVAILABLE
- goal_reselect_after_no_motion_count: UNAVAILABLE
- active_path_update_count: 1
- active_path_done_event_count: UNAVAILABLE
- active_path_same_hash_max_duration_sec: 299.8745274543762
- active_path_endpoint_to_goal_distance_avg: 7.050957763302419
- active_path_endpoint_to_goal_distance_max: 7.805698684593535
- travel_traj_update_count: 47
- travel_traj_same_hash_max_duration_sec: 277.56186389923096
- position_cmd_update_count: 1
- position_cmd_total_variation: 0.0
- position_cmd_same_pose_max_duration_sec: 299.96006202697754
- position_cmd_to_odom_distance_avg: 0.00028513168686687527
- trajectory_count: 6166
- frontier_count_start: 0
- frontier_count_end: 119
- frontier_count_avg: UNAVAILABLE
- explored_grid_start: 1070
- explored_grid_end: 1140
- explored_grid_gain: UNAVAILABLE
- coverage_proxy_start: 0.0
- coverage_proxy_end: 0.08393461934913857
- coverage_proxy_gain: 0.08393461934913857
- coverage_proxy_gain_per_min: UNAVAILABLE
- coverage_stall_count: UNAVAILABLE
- coverage_stall_event_count: UNAVAILABLE
- coverage_stall_max_duration_sec: UNAVAILABLE
- stuck_event_count: 56
- path_done_without_reselect_count: UNAVAILABLE
- coverage_stall_without_reselect_count: UNAVAILABLE
- traj_server_stale_path_hold_count: 38
- quadrotor_sim_motion_blocked_count: 8999
- main_chain_break: PATH_FEASIBILITY
- main_stuck_cause: REPEATED_GOAL
- main_coverage_blocker: UNAVAILABLE

## Generated Files
- test-log/20260622_104543_summary_system_test.md
- reports/p2f_before_unified_summary_fix_diff_20260622_104237.patch
- reports/38_github_backup_report.md

## Diagnosis
- Result inferred as `PARTIAL` from exit code and raw log.
- Planner output metric: trajectory_count=6166.
- Odom/motion metric: uav_total_distance=1.1785774688180406.
- Main chain break: PATH_FEASIBILITY.
- Main stuck cause: REPEATED_GOAL.
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
- Investigate/fix `PATH_FEASIBILITY` with the smallest targeted change.
