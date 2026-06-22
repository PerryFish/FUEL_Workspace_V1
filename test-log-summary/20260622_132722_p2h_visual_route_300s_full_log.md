# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T13:27:25+0800
- Task name: p2h_visual_route_300s
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2h_visual_route_300s.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_132155_p2h_visual_route_300s.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132717_p2h_visual_route_300s_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132722_p2h_visual_route_300s_full_log.md

## 2. Environment Snapshot
```bash
AMENT_PREFIX_PATH=/home/nuaa/ZHY/A_DWA/install/turtlebot3_simulations:/home/nuaa/ZHY/A_DWA/install/turtlebot3_manipulation_gazebo:/home/nuaa/ZHY/A_DWA/install/turtlebot3_gazebo:/home/nuaa/ZHY/A_DWA/install/turtlebot3_fake_node:/opt/ros/humble
COLCON_PREFIX_PATH=/home/nuaa/ZHY/A_DWA/install
DISPLAY=:0
LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:/opt/ros/humble/opt/rviz_ogre_vendor/lib:/opt/ros/humble/lib/x86_64-linux-gnu:/opt/ros/humble/lib:/usr/local/cuda-11.8/lib64:
PWD=/home/nuaa/ZHY/FUEL_PLANNER_V3
PYTHONPATH=/opt/ros/humble/lib/python3.10/site-packages:/opt/ros/humble/local/lib/python3.10/dist-packages
ROS_DISTRO=humble
ROS_LOCALHOST_ONLY=0
ROS_PYTHON_VERSION=3
ROS_VERSION=2
```

## 3. Git Snapshot
```text
?? ./
3b11fc5 feat: 稳定版本v1.0。已解决CPU过载和狭窄空间死锁问题，机器人可流畅自主探索。
master
3b11fc50c0ab8e84f9093f084ce80f4d1af6088d
```

## 4. Process Snapshot
```text
nuaa         359  2.0  0.0  27256 14244 ?        S    13:27   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2h_visual_route_300s --command ./scripts/run_p2h_visual_route_300s.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_132155_p2h_visual_route_300s.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132717_p2h_visual_route_300s_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
```

## 5. ROS Node Snapshot
```text
NO_OUTPUT
```

## 6. ROS Topic Snapshot
```text
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
```

## 7. Important Topic Availability
- /odom: NO_OR_NOT_RUNNING
- /planning/pos_cmd: NO_OR_NOT_RUNNING
- /planning/travel_traj: NO_OR_NOT_RUNNING
- /fuel/p10_lite/active_path: NO_OR_NOT_RUNNING
- /fuel/p10_lite/position_cmd: NO_OR_NOT_RUNNING
- /fuel/p10_lite/traj_server_status: NO_OR_NOT_RUNNING
- /fuel/p10_lite/quadrotor_sim_status: NO_OR_NOT_RUNNING
- /fuel/p11_lite/exploration_goal: NO_OR_NOT_RUNNING
- /fuel/p11_lite/best_viewpoint: NO_OR_NOT_RUNNING
- /fuel/p11_lite/frontier_candidates_raw: NO_OR_NOT_RUNNING
- /fuel/p11_lite/frontier_viewpoints: NO_OR_NOT_RUNNING
- /fuel/p11_lite/explored_grid: NO_OR_NOT_RUNNING
- /fuel/p11_lite/occupancy_grid: NO_OR_NOT_RUNNING
- /fuel/p11_lite/exploration_manager_status: NO_OR_NOT_RUNNING
- /fuel/p11_lite/goal_to_path_status: NO_OR_NOT_RUNNING
- /fuel/p11_lite/visual/all_markers: NO_OR_NOT_RUNNING
- /map_generator/global_cloud: NO_OR_NOT_RUNNING
- /pcl_render_node/cloud: NO_OR_NOT_RUNNING
- /tf_static: NO_OR_NOT_RUNNING

## 8. Raw Command Output
```text
# FUEL Run Log

## Metadata
- Date: 2026-06-22T13:21:55+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2h_visual_route_300s.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_132155_p2h_visual_route_300s.md

## Environment
```bash
DISPLAY=:0
LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:/usr/lib/x86_64-linux-gnu/gazebo-11/plugins:/opt/ros/humble/opt/rviz_ogre_vendor/lib:/opt/ros/humble/lib/x86_64-linux-gnu:/opt/ros/humble/lib:/usr/local/cuda-11.8/lib64:
PYTHONPATH=/opt/ros/humble/lib/python3.10/site-packages:/opt/ros/humble/local/lib/python3.10/dist-packages
```

## Git
```bash
src/FUEL is not a git repository yet
```

## Colcon Packages
```text
exploration_manager	src/exploration_manager	(ros.ament_cmake)
fuel_ros2	src/FUEL	(ros.ament_cmake)
```

## Command Output
```text
P2H_ROUTE_PROGRESS time_sec=30.024 coverage_proxy=0.099 odom_total_distance=6.666 coverage_gain_per_meter=0.004 path_length_regret_avg=1.038 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.848 route_tortuosity=1.209 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=60.025 coverage_proxy=0.119 odom_total_distance=14.992 coverage_gain_per_meter=0.003 path_length_regret_avg=-1.286 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.849 route_tortuosity=1.771 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=90.025 coverage_proxy=0.132 odom_total_distance=19.278 coverage_gain_per_meter=0.003 path_length_regret_avg=-1.805 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.860 route_tortuosity=1.656 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=120.057 coverage_proxy=0.132 odom_total_distance=19.278 coverage_gain_per_meter=0.003 path_length_regret_avg=-1.805 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.860 route_tortuosity=1.656 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=150.058 coverage_proxy=0.132 odom_total_distance=19.278 coverage_gain_per_meter=0.003 path_length_regret_avg=-1.805 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.860 route_tortuosity=1.656 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=180.058 coverage_proxy=0.142 odom_total_distance=24.282 coverage_gain_per_meter=0.003 path_length_regret_avg=0.787 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.862 route_tortuosity=2.339 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=210.076 coverage_proxy=0.159 odom_total_distance=29.324 coverage_gain_per_meter=0.003 path_length_regret_avg=1.255 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.871 route_tortuosity=2.502 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=240.091 coverage_proxy=0.180 odom_total_distance=35.809 coverage_gain_per_meter=0.003 path_length_regret_avg=0.431 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.872 route_tortuosity=2.429 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=270.091 coverage_proxy=0.201 odom_total_distance=41.553 coverage_gain_per_meter=0.003 path_length_regret_avg=0.188 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.874 route_tortuosity=2.432 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=300.024 coverage_proxy=0.219 odom_total_distance=48.384 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.320 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.879 route_tortuosity=3.187 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2h_visual_route_300s_20260622_132156
duration_sec=300.027055978775
odom_total_distance=48.384334500313635
coverage_proxy_gain=0.14659107642467972
coverage_gain_per_meter=0.003029721870489497
selected_goal_unique_count=29
path_length_regret_avg=-0.3196483680123871
path_length_regret_max=8.448331778512841
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8793103448275862
route_tortuosity=3.1870833821758944
active_path_endpoint_to_goal_distance_avg=0.15354724506666867
main_route_issue=PATH_COST_UNDERWEIGHTED
result=PASS
./scripts/run_p2h_visual_route_300s.sh: 第 36 行：   203 已中止               （核心已转储） rviz2 -d "$CONFIG" > "$OUT.rviz" 2>&1
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=PATH_COST_UNDERWEIGHTED
coverage_proxy_gain=0.14659107642467972
coverage_gain_per_meter=0.003029721870489497
odom_total_distance=48.384334500313635
selected_goal_unique_count=29
path_length_regret_avg=-0.3196483680123871
path_length_regret_max=8.448331778512841
nearest_frontier_ignored_count=1
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8793103448275862
route_tortuosity=3.1870833821758944
active_path_endpoint_to_goal_distance_avg=0.15354724506666867
active_path_endpoint_to_goal_distance_max=9.26162932629987
300s P2H visual route demo finished. Press Enter to cleanup, or inspect RViz now.
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132717_p2h_visual_route_300s_summary.md
```

## Visual Re-run Commands

Manual persistent visual demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh
```

Coverage visual diagnostic demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2g_visual_coverage_300s ./scripts/run_p2g_visual_coverage_300s.sh
```

Clean all FUEL/RViz processes:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh
```
```

## 9. Metrics Files Content
### reports/p2h_metrics/p2h_visual_route_300s_20260622_132156/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: PATH_COST_UNDERWEIGHTED
- coverage_proxy_gain: 0.14659107642467972
- coverage_gain_per_meter: 0.003029721870489497
- odom_total_distance: 48.384334500313635
- selected_goal_unique_count: 29
- path_length_regret_avg: -0.3196483680123871
- path_length_regret_max: 8.448331778512841
- nearest_frontier_ignored_count: 1
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8793103448275862
- route_tortuosity: 3.1870833821758944
- active_path_endpoint_to_goal_distance_avg: 0.15354724506666867
- active_path_endpoint_to_goal_distance_max: 9.26162932629987
```

### reports/p2h_metrics/p2h_visual_route_300s_20260622_132156/route_events.csv
- csv_path: reports/p2h_metrics/p2h_visual_route_300s_20260622_132156/route_events.csv
- file_size_bytes: 22

### reports/p2h_metrics/p2h_visual_route_300s_20260622_132156/route_timeseries.csv
- csv_path: reports/p2h_metrics/p2h_visual_route_300s_20260622_132156/route_timeseries.csv
- file_size_bytes: 1792

### reports/p2h_metrics/p2h_visual_route_300s_20260622_132156/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.027055978775
- odom_total_distance: 48.384334500313635
- coverage_proxy_start: 0.07222794875570608
- coverage_proxy_end: 0.21881902518038582
- coverage_proxy_gain: 0.14659107642467972
- coverage_gain_per_meter: 0.003029721870489497
- selected_goal_count: 360
- selected_goal_unique_count: 29
- selected_goal_distance_from_odom_avg: 4.594882905972641
- selected_goal_distance_from_odom_max: 10.76179740947835
- selected_goal_path_length_avg: 6.035487131772608
- selected_goal_path_length_max: 16.692388155425107
- selected_goal_path_efficiency_avg: 0.7563433106541081
- frontier_candidate_count_avg: 152.1375
- frontier_viewpoint_count_avg: 37.49333333333333
- nearest_frontier_distance_avg: 6.321279443703042
- nearest_frontier_distance_min: 5.075685915152757
- nearest_frontier_ignored_count: 1
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 6.035487131772608
- path_length_to_nearest_candidate_avg: 6.35513549978505
- path_length_regret_avg: -0.3196483680123871
- path_length_regret_max: 8.448331778512841
- coverage_gain_after_goal_avg: 0.007814965185013779
- coverage_gain_after_goal_per_meter_avg: 0.004046397912710853
- low_efficiency_goal_count: 0
- local_region_revisit_count: 3
- region_diversity_score: 0.896551724137931
- active_path_endpoint_to_goal_distance_avg: 0.15354724506666867
- active_path_endpoint_to_goal_distance_max: 9.26162932629987
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.8793103448275862
- route_tortuosity: 3.1870833821758944
- active_path_update_count: 186
- position_cmd_update_count: 187
- frontier_candidate_count_end: 206
- frontier_viewpoint_count_end: 34
- main_route_issue: PATH_COST_UNDERWEIGHTED
```

## 10. Reports Generated
- UNAVAILABLE


## 11. Debug Package
```text
lrwxrwxrwx 1 nuaa nuaa   56 Jun 22 09:23 reports/latest_p2d_debug_package.tar.gz -> FUEL_PLANNER_V3_P2D_DEBUG_PACKAGE_20260622_092321.tar.gz
-rw-rw-r-- 1 nuaa nuaa 783K Jun 22 11:22 reports/latest_p2f_debug_package.tar.gz
-rw-rw-r-- 1 nuaa nuaa 892K Jun 22 12:16 reports/latest_p2g_debug_package.tar.gz
```

## 12. Visual Re-run Commands
Manual persistent visual demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh
```

Coverage visual diagnostic demo:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2g_visual_coverage_300s ./scripts/run_p2g_visual_coverage_300s.sh
```

Clean all FUEL/RViz processes:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh
```

## 13. Final Diagnosis
- Command exit code: 0.
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_132155_p2h_visual_route_300s.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132717_p2h_visual_route_300s_summary.md.
- Matched metrics files: 4.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
