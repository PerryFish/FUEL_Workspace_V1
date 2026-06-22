# FUEL Unified Run Summary

## Basic Info
- Date: 2026-06-22T14:21:37+0800
- Task name: p2i_route_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Exit code: 0
- Result: PARTIAL
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_141604_p2i_route_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142132_p2i_route_300s_after_fix_summary.md

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
- metrics_source: CURRENT_RUN
- metrics_source_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality.json
- metrics_source_reason: matched current run metrics by run_id after raw log start timestamp
- matched_by: run_id
- duration_sec: 300.0155794620514
- odom_total_distance: 33.14057674968115
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
- active_path_update_count: 127
- active_path_done_event_count: UNAVAILABLE
- active_path_same_hash_max_duration_sec: UNAVAILABLE
- active_path_endpoint_to_goal_distance_avg: 0.420888167191617
- active_path_endpoint_to_goal_distance_max: 5.0
- travel_traj_update_count: 302
- travel_traj_same_hash_max_duration_sec: UNAVAILABLE
- position_cmd_update_count: 128
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
- coverage_proxy_start: 0.07767633632749227
- coverage_proxy_end: 0.12604918274186422
- coverage_proxy_gain: 0.04837284641437195
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
- main_route_issue: UAV_IDLE_DUE_TO_NO_PATH
- coverage_gain_per_meter: 0.0014596259678805183
- selected_goal_unique_count: 21
- path_length_regret_avg: 2.6688439674569713
- path_length_regret_max: 10.841272891958297
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8695652173913043
- route_tortuosity: 4.585606949619388
- goal_selected_count: 21
- goal_without_path_count: 4
- goal_without_path_ratio: 0.19047619047619047
- goal_to_path_latency_avg_sec: 0.5284361441930135
- goal_to_path_latency_max_sec: 3.2557754516601562
- goal_to_path_timeout_count: 9
- goal_to_path_timeout_max_duration_sec: 74.84858107566833
- active_goal_without_active_path_max_duration_sec: 74.84858107566833
- active_goal_without_travel_traj_max_duration_sec: 74.84858107566833
- path_missing_after_goal_count: 9
- path_missing_after_goal_max_duration_sec: 74.84858107566833
- path_generation_fail_count: 62
- path_generation_fail_reasons: {'no_collision_free_grid_path': 62}
- active_path_empty_count: 0
- active_path_first_update_after_goal_sec: 0.5284361441930135
- travel_traj_first_update_after_goal_sec: 0.4804527958234151
- uav_idle_due_to_no_path_duration_sec: 89.89823865890503
- no_path_blacklist_count: 0
- goal_reselect_due_to_no_path_count: 0

## Generated Files
- test-log/20260622_141604_p2i_route_300s_after_fix.md
- reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality_analysis.json
- reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality_analysis.md
- reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_events.csv
- reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_timeseries.csv
- reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality.md
- reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality.json

## Diagnosis
- Result inferred as `PARTIAL` from exit code and raw log.
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
