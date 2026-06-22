# FUEL Unified Run Summary

## Basic Info
- Date: 2026-06-22T14:23:04+0800
- Task name: p2i_build_after_no_path_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/build.sh
- Exit code: 0
- Result: PASS
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_142156_p2i_build_after_no_path_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142258_p2i_build_after_no_path_fix_summary.md

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
- latest diff patch if available: reports/p2i_after_no_path_timing_fix_diff_20260622_141543.patch

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
- metrics_source: NONE
- metrics_source_path: UNAVAILABLE
- metrics_source_reason: no current-run metrics matched task_name/run_id/timestamp
- matched_by: NONE
- duration_sec: UNAVAILABLE
- odom_total_distance: UNAVAILABLE
- uav_total_distance: UNAVAILABLE
- uav_net_displacement: UNAVAILABLE
- odom_net_displacement: UNAVAILABLE
- odom_max_no_motion_duration_sec: UNAVAILABLE
- goal_msg_count: UNAVAILABLE
- goal_switch_count: UNAVAILABLE
- unique_goal_count: UNAVAILABLE
- unique_goal_count_quantized_1p0m: UNAVAILABLE
- same_goal_max_duration_sec: UNAVAILABLE
- goal_reselect_count: UNAVAILABLE
- goal_reselect_after_path_done_count: UNAVAILABLE
- goal_reselect_after_coverage_stall_count: UNAVAILABLE
- goal_reselect_after_no_motion_count: UNAVAILABLE
- active_path_update_count: UNAVAILABLE
- active_path_done_event_count: UNAVAILABLE
- active_path_same_hash_max_duration_sec: UNAVAILABLE
- active_path_endpoint_to_goal_distance_avg: UNAVAILABLE
- active_path_endpoint_to_goal_distance_max: UNAVAILABLE
- travel_traj_update_count: UNAVAILABLE
- travel_traj_same_hash_max_duration_sec: UNAVAILABLE
- position_cmd_update_count: UNAVAILABLE
- position_cmd_total_variation: UNAVAILABLE
- position_cmd_same_pose_max_duration_sec: UNAVAILABLE
- position_cmd_to_odom_distance_avg: UNAVAILABLE
- trajectory_count: UNAVAILABLE
- frontier_count_start: UNAVAILABLE
- frontier_count_end: UNAVAILABLE
- frontier_count_avg: UNAVAILABLE
- explored_grid_start: UNAVAILABLE
- explored_grid_end: UNAVAILABLE
- explored_grid_gain: UNAVAILABLE
- coverage_proxy_start: UNAVAILABLE
- coverage_proxy_end: UNAVAILABLE
- coverage_proxy_gain: UNAVAILABLE
- coverage_proxy_gain_per_min: UNAVAILABLE
- coverage_stall_count: UNAVAILABLE
- coverage_stall_event_count: UNAVAILABLE
- coverage_stall_max_duration_sec: UNAVAILABLE
- stuck_event_count: UNAVAILABLE
- path_done_without_reselect_count: UNAVAILABLE
- coverage_stall_without_reselect_count: UNAVAILABLE
- traj_server_stale_path_hold_count: UNAVAILABLE
- quadrotor_sim_motion_blocked_count: UNAVAILABLE
- main_chain_break: UNAVAILABLE
- main_stuck_cause: UNAVAILABLE
- main_coverage_blocker: UNAVAILABLE
- main_route_issue: UNAVAILABLE
- coverage_gain_per_meter: UNAVAILABLE
- selected_goal_unique_count: UNAVAILABLE
- path_length_regret_avg: UNAVAILABLE
- path_length_regret_max: UNAVAILABLE
- near_high_gain_candidate_ignored_count: UNAVAILABLE
- route_revisit_ratio: UNAVAILABLE
- route_tortuosity: UNAVAILABLE
- goal_selected_count: UNAVAILABLE
- goal_without_path_count: UNAVAILABLE
- goal_without_path_ratio: UNAVAILABLE
- goal_to_path_latency_avg_sec: UNAVAILABLE
- goal_to_path_latency_max_sec: UNAVAILABLE
- goal_to_path_timeout_count: UNAVAILABLE
- goal_to_path_timeout_max_duration_sec: UNAVAILABLE
- active_goal_without_active_path_max_duration_sec: UNAVAILABLE
- active_goal_without_travel_traj_max_duration_sec: UNAVAILABLE
- path_missing_after_goal_count: UNAVAILABLE
- path_missing_after_goal_max_duration_sec: UNAVAILABLE
- path_generation_fail_count: UNAVAILABLE
- path_generation_fail_reasons: UNAVAILABLE
- active_path_empty_count: UNAVAILABLE
- active_path_first_update_after_goal_sec: UNAVAILABLE
- travel_traj_first_update_after_goal_sec: UNAVAILABLE
- uav_idle_due_to_no_path_duration_sec: UNAVAILABLE
- no_path_blacklist_count: UNAVAILABLE
- goal_reselect_due_to_no_path_count: UNAVAILABLE

## Generated Files
- test-log/20260622_142156_p2i_build_after_no_path_fix.md

## Diagnosis
- Result inferred as `PASS` from exit code and raw log.
- Planner output metric: trajectory_count=UNAVAILABLE.
- Odom/motion metric: uav_total_distance=UNAVAILABLE.
- Main chain break: UNAVAILABLE.
- Main stuck cause: UNAVAILABLE.
- RViz visual chain is expected to remain unchanged unless this task explicitly ran a visual check.

## Run Commands

### Full Manual Visual Run

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh
```

### P2I Full Route Visual Run

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_visual_route_full ./scripts/run_p2i_visual_route_full.sh
```

### P2I 300s Route Visual Run

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_visual_route_300s ./scripts/run_p2i_visual_route_300s.sh
```

### P2I 300s Headless Route Benchmark

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_route_300s_after_fix ./scripts/run_p2i_route_300s_after_fix.sh
```

### P2I 900s Headless Route Benchmark

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_route_900s_after_fix ./scripts/run_p2i_route_900s_after_fix.sh
```

### P2I Full Headless Route Run

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_route_full_900s ./scripts/run_p2i_route_full.sh --duration 900
```

### Clean All FUEL/RViz Processes

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh
```

### Latest Debug Packages

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
ls -lh reports/latest_p2i_debug_package.tar.gz reports/latest_p2h_debug_package.tar.gz reports/latest_p2g_debug_package.tar.gz reports/latest_p2f_debug_package.tar.gz 2>/dev/null || true
```

## Next Action
- Run the next targeted diagnostic using `scripts/run_with_log.sh` so this summary system captures it.
