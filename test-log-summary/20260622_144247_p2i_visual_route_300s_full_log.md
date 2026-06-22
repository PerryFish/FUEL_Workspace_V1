# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T14:42:50+0800
- Task name: p2i_visual_route_300s
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2i_visual_route_300s.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143719_p2i_visual_route_300s.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_144241_p2i_visual_route_300s_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_144247_p2i_visual_route_300s_full_log.md

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
nuaa         361  1.6  0.0  27336 14056 ?        S    14:42   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2i_visual_route_300s --command ./scripts/run_p2i_visual_route_300s.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143719_p2i_visual_route_300s.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_144241_p2i_visual_route_300s_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T14:37:19+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2i_visual_route_300s.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143719_p2i_visual_route_300s.md

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
P2I_ROUTE_PROGRESS time_sec=30.013 coverage_proxy=0.080 odom_total_distance=1.911 coverage_gain_per_meter=0.005 path_length_regret_avg=-4.881 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.700 route_tortuosity=1.076 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=60.018 coverage_proxy=0.087 odom_total_distance=5.526 coverage_gain_per_meter=0.003 path_length_regret_avg=4.381 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.846 route_tortuosity=1.962 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=90.019 coverage_proxy=0.091 odom_total_distance=12.127 coverage_gain_per_meter=0.002 path_length_regret_avg=5.381 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.881 route_tortuosity=1.563 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=120.035 coverage_proxy=0.099 odom_total_distance=17.237 coverage_gain_per_meter=0.002 path_length_regret_avg=3.553 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.869 route_tortuosity=2.057 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=150.068 coverage_proxy=0.121 odom_total_distance=28.735 coverage_gain_per_meter=0.002 path_length_regret_avg=1.580 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.856 route_tortuosity=4.298 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=180.101 coverage_proxy=0.130 odom_total_distance=33.573 coverage_gain_per_meter=0.002 path_length_regret_avg=2.452 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.871 route_tortuosity=5.592 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=210.101 coverage_proxy=0.131 odom_total_distance=38.748 coverage_gain_per_meter=0.002 path_length_regret_avg=3.045 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.883 route_tortuosity=4.843 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=240.115 coverage_proxy=0.137 odom_total_distance=48.204 coverage_gain_per_meter=0.001 path_length_regret_avg=2.313 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.889 route_tortuosity=3.894 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=270.124 coverage_proxy=0.148 odom_total_distance=53.963 coverage_gain_per_meter=0.001 path_length_regret_avg=2.147 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.885 route_tortuosity=3.294 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=300.002 coverage_proxy=0.158 odom_total_distance=59.036 coverage_gain_per_meter=0.001 path_length_regret_avg=1.786 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.884 route_tortuosity=3.102 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2i_visual_route_300s_20260622_143721
duration_sec=300.00527453422546
odom_total_distance=59.03625424911289
coverage_proxy_gain=0.08658518627595346
coverage_gain_per_meter=0.0014666443082684997
selected_goal_unique_count=24
path_length_regret_avg=1.7864743023215846
path_length_regret_max=11.999378898618428
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8842105263157894
route_tortuosity=3.102374812549027
active_path_endpoint_to_goal_distance_avg=0.1376063773315371
goal_without_path_count=2
goal_to_path_timeout_count=7
active_goal_without_active_path_max_duration_sec=24.499674558639526
active_goal_without_travel_traj_max_duration_sec=24.499674558639526
uav_idle_due_to_no_path_duration_sec=0.0
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
result=PASS
./scripts/run_p2i_visual_route_300s.sh: 第 38 行：   203 已中止               （核心已转储） rviz2 -d "$CONFIG" > "$OUT.rviz" 2>&1
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
coverage_proxy_gain=0.08658518627595346
coverage_gain_per_meter=0.0014666443082684997
odom_total_distance=59.03625424911289
selected_goal_unique_count=24
path_length_regret_avg=1.7864743023215846
path_length_regret_max=11.999378898618428
nearest_frontier_ignored_count=1
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8842105263157894
route_tortuosity=3.102374812549027
active_path_endpoint_to_goal_distance_avg=0.1376063773315371
active_path_endpoint_to_goal_distance_max=9.962429422585638
RVIZ_CRASHED=YES
RVIZ_EXIT_CODE=134
VISUAL_RESULT=PARTIAL_WITH_RVIZ_CRASH
P2I_visual_route_300s_DONE run_id=p2i_visual_route_300s_20260622_143721
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_144241_p2i_visual_route_300s_summary.md
```

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
```

## 9. Metrics Files Content
### reports/p2i_metrics/p2i_visual_route_300s_20260622_143721/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- coverage_proxy_gain: 0.08658518627595346
- coverage_gain_per_meter: 0.0014666443082684997
- odom_total_distance: 59.03625424911289
- selected_goal_unique_count: 24
- path_length_regret_avg: 1.7864743023215846
- path_length_regret_max: 11.999378898618428
- nearest_frontier_ignored_count: 1
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8842105263157894
- route_tortuosity: 3.102374812549027
- active_path_endpoint_to_goal_distance_avg: 0.1376063773315371
- active_path_endpoint_to_goal_distance_max: 9.962429422585638
```

### reports/p2i_metrics/p2i_visual_route_300s_20260622_143721/route_timeseries.csv
- csv_path: reports/p2i_metrics/p2i_visual_route_300s_20260622_143721/route_timeseries.csv
- file_size_bytes: 1859

### reports/p2i_metrics/p2i_visual_route_300s_20260622_143721/route_events.csv
- csv_path: reports/p2i_metrics/p2i_visual_route_300s_20260622_143721/route_events.csv
- file_size_bytes: 22

### reports/p2i_metrics/p2i_visual_route_300s_20260622_143721/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.00527453422546
- odom_total_distance: 59.03625424911289
- coverage_proxy_start: 0.07149168016492416
- coverage_proxy_end: 0.15807686644087762
- coverage_proxy_gain: 0.08658518627595346
- coverage_gain_per_meter: 0.0014666443082684997
- selected_goal_count: 388
- selected_goal_unique_count: 24
- selected_goal_distance_from_odom_avg: 4.981058582847763
- selected_goal_distance_from_odom_max: 8.214416066902634
- selected_goal_path_length_avg: 8.508125654546404
- selected_goal_path_length_max: 18.162508945586495
- selected_goal_path_efficiency_avg: 0.7747221485709198
- frontier_candidate_count_avg: 133.7675
- frontier_viewpoint_count_avg: 32.07333333333333
- nearest_frontier_distance_avg: 6.67164938298097
- nearest_frontier_distance_min: 5.514585833215584
- nearest_frontier_ignored_count: 1
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 8.508125654546404
- path_length_to_nearest_candidate_avg: 6.7216513522248915
- path_length_regret_avg: 1.7864743023215846
- path_length_regret_max: 11.999378898618428
- coverage_gain_after_goal_avg: 0.006568796296889105
- coverage_gain_after_goal_per_meter_avg: 0.019930876014824427
- low_efficiency_goal_count: 2
- local_region_revisit_count: 3
- region_diversity_score: 0.875
- active_path_endpoint_to_goal_distance_avg: 0.1376063773315371
- active_path_endpoint_to_goal_distance_max: 9.962429422585638
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.8842105263157894
- route_tortuosity: 3.102374812549027
- active_path_update_count: 230
- position_cmd_update_count: 229
- travel_traj_update_count: 561
- frontier_candidate_count_end: 178
- frontier_viewpoint_count_end: 29
- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- goal_selected_count: 24
- goal_without_path_count: 2
- goal_without_path_ratio: 0.08333333333333333
- goal_to_path_latency_avg_sec: 1.0035953381482292
- goal_to_path_latency_max_sec: 6.080636739730835
- goal_to_path_timeout_count: 7
- goal_to_path_timeout_max_duration_sec: 24.499674558639526
- active_goal_without_active_path_max_duration_sec: 24.499674558639526
- active_goal_without_travel_traj_max_duration_sec: 24.499674558639526
- path_missing_after_goal_count: 7
- path_missing_after_goal_max_duration_sec: 24.499674558639526
- path_generation_fail_count: 50
- path_generation_fail_reasons: {'goal_too_close': 7, 'no_collision_free_grid_path': 43}
- goal_to_path_status_events: ['REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=19.645 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.650 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=20.494 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.483 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=21.483 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.289 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=22.492 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.057 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=23.500 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=5.823 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=0.832 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=6.371 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=1.562 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.863 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=2.560 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.757 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=3.571 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.605 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=4.567 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.451 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=5.539 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.298 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=6.544 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.147 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=7.542 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.000 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=8.551 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.854 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=9.569 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.692 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_s', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=10.552 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.536 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=11.548 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.375 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=12.546 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.211 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.500 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=13.543 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.052 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.500 first_c
```

### reports/p2i_metrics/p2i_visual_route_300s_20260622_143721/route_rationality.json
```json
{
  "active_goal_without_active_path_max_duration_sec": 24.499674558639526,
  "active_goal_without_travel_traj_max_duration_sec": 24.499674558639526,
  "active_path_empty_count": 0,
  "active_path_endpoint_to_goal_distance_avg": 0.1376063773315371,
  "active_path_endpoint_to_goal_distance_max": 9.962429422585638,
  "active_path_first_update_after_goal_sec": 1.0035953381482292,
  "active_path_update_count": 230,
  "coverage_gain_after_goal_avg": 0.006568796296889105,
  "coverage_gain_after_goal_per_meter_avg": 0.019930876014824427,
  "coverage_gain_per_meter": 0.0014666443082684997,
  "coverage_proxy_end": 0.15807686644087762,
  "coverage_proxy_gain": 0.08658518627595346,
  "coverage_proxy_start": 0.07149168016492416,
  "duration_sec": 300.00527453422546,
  "frontier_candidate_count_avg": 133.7675,
  "frontier_candidate_count_end": 178,
  "frontier_viewpoint_count_avg": 32.07333333333333,
  "frontier_viewpoint_count_end": 29,
  "goal_reselect_due_to_no_path_count": 0,
  "goal_selected_count": 24,
  "goal_to_path_latency_avg_sec": 1.0035953381482292,
  "goal_to_path_latency_max_sec": 6.080636739730835,
  "goal_to_path_status_events": [
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=19.645 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.650 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=20.494 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.483 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=21.483 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.289 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=22.492 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=6.057 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=39 wait_sec=23.500 GOAL_TO_PATH_REQUEST goal_id=39 goal_key=(11.0, 10.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=39 path_len=5.823 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=0.832 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=6.371 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=1.562 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.863 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=2.560 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.757 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=3.571 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.605 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=4.567 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.451 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=5.539 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.298 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=6.544 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.147 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=7.542 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=5.000 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=8.551 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.854 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=9.569 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.692 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_s",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=10.552 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.536 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=11.548 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.375 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=12.546 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.211 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.500 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=13.543 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=4.052 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.500 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=40 wait_sec=14.550 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(11.5, 11.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=40 path_len=3.889 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_"
  ],
  "goal_to_path_timeout_count": 7,
  "goal_to_path_timeout_max_duration_sec": 24.499674558639526,
  "goal_without_path_count": 2,
  "goal_without_path_ratio": 0.08333333333333333,
  "local_region_revisit_count": 3,
  "low_efficiency_goal_count": 2,
  "main_route_issue": "TRAVEL_TRAJ_MISSING_AFTER_GOAL",
  "near_high_gain_candidate_ignored_count": 0,
  "nearest_frontier_distance_avg": 6.67164938298097,
  "nearest_frontier_distance_min": 5.514585833215584,
  "nearest_frontier_ignored_count": 1,
  "no_path_blacklist_count": 0,
  "odom_total_distance": 59.03625424911289,
  "path_generation_fail_count": 50,
  "path_generation_fail_reasons": {
    "goal_too_close": 7,
    "no_collision_free_grid_path": 43
  },
  "path_length_regret_avg": 1.7864743023215846,
  "path_length_regret_max": 11.999378898618428,
  "path_length_to_nearest_candidate_avg": 6.7216513522248915,
  "path_length_to_selected_goal_avg": 8.508125654546404,
  "path_missing_after_goal_count": 7,
  "path_missing_after_goal_max_duration_sec": 24.499674558639526,
  "position_cmd_update_count": 229,
  "region_diversity_score": 0.875,
  "route_backtracking_distance": 0.0,
  "route_revisit_ratio": 0.8842105263157894,
  "route_tortuosity": 3.102374812549027,
  "selected_goal_count": 388,
  "selected_goal_distance_from_odom_avg": 4.981058582847763,
  "selected_goal_distance_from_odom_max": 8.214416066902634,
  "selected_goal_path_efficiency_avg": 0.7747221485709198,
  "selected_goal_path_length_avg": 8.508125654546404,
  "selected_goal_path_length_max": 18.162508945586495,
  "selected_goal_unique_count": 24,
  "travel_traj_first_update_after_goal_sec": 0.9751153973972096,
  "travel_traj_update_count": 561,
  "uav_idle_due_to_no_path_duration_sec": 0.0
}
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

## 13. Final Diagnosis
- Command exit code: 0.
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143719_p2i_visual_route_300s.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_144241_p2i_visual_route_300s_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
