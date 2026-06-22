# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T14:14:51+0800
- Task name: p2i_route_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140915_p2i_route_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_141443_p2i_route_300s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_141449_p2i_route_300s_after_fix_full_log.md

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
nuaa         368  1.0  0.0  27336 14032 ?        S    14:14   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2i_route_300s_after_fix --command ./scripts/run_p2i_route_300s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140915_p2i_route_300s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_141443_p2i_route_300s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T14:09:15+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140915_p2i_route_300s_after_fix.md

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
# P2I route run
run_id=p2i_route_300s_after_fix_20260622_140917
mode=route_300s_after_fix
duration=300
2026-06-22T14:09:17+08:00
AMENT_PREFIX_PATH=/home/nuaa/ZHY/FUEL_PLANNER_V3/install/exploration_manager:/home/nuaa/ZHY/FUEL_PLANNER_V3/install/fuel_ros2:/opt/ros/humble
CMAKE_PREFIX_PATH=/home/nuaa/ZHY/FUEL_PLANNER_V3/install/exploration_manager:/home/nuaa/ZHY/FUEL_PLANNER_V3/install/fuel_ros2
COLCON_PREFIX_PATH=/home/nuaa/ZHY/FUEL_PLANNER_V3/install
FASTDDS_BUILTIN_TRANSPORTS=UDPv4
FUEL_WS=/home/nuaa/ZHY/FUEL_PLANNER_V3
OLDPWD=/home/nuaa/ZHY/FUEL_PLANNER_V3
PWD=/home/nuaa/ZHY/FUEL_PLANNER_V3
RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ROS_DISTRO=humble
ROS_DOMAIN_ID=88
ROS_HOME=/home/nuaa/ZHY/FUEL_PLANNER_V3/.ros
ROS_LOCALHOST_ONLY=1
ROS_LOG_DIR=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/ros
ROS_PYTHON_VERSION=3
ROS_VERSION=2
/fuel/compat/status [std_msgs/msg/String]
/fuel/global_path [nav_msgs/msg/Path]
/fuel/local_trajectory [nav_msgs/msg/Path]
/fuel/p10_lite/active_path [nav_msgs/msg/Path]
/fuel/p10_lite/position_cmd [geometry_msgs/msg/PoseStamped]
/fuel/p10_lite/quadrotor_sim_status [std_msgs/msg/String]
/fuel/p10_lite/traj_server_status [std_msgs/msg/String]
/fuel/p11_lite/best_viewpoint [geometry_msgs/msg/PoseStamped]
/fuel/p11_lite/complex_env/free_boundary [visualization_msgs/msg/Marker]
/fuel/p11_lite/complex_env/map_boundary [visualization_msgs/msg/Marker]
/fuel/p11_lite/complex_env/occupied_points [sensor_msgs/msg/PointCloud2]
/fuel/p11_lite/complex_env/status [std_msgs/msg/String]
/fuel/p11_lite/complex_env/wall_markers [visualization_msgs/msg/MarkerArray]
/fuel/p11_lite/exploration_goal [geometry_msgs/msg/PoseStamped]
/fuel/p11_lite/exploration_manager_status [std_msgs/msg/String]
/fuel/p11_lite/explored_grid [sensor_msgs/msg/PointCloud2]
/fuel/p11_lite/frontier_candidates_raw [sensor_msgs/msg/PointCloud2]
/fuel/p11_lite/frontier_status [std_msgs/msg/String]
/fuel/p11_lite/frontier_viewpoints [sensor_msgs/msg/PointCloud2]
/fuel/p11_lite/goal_lifecycle_status [std_msgs/msg/String]
/fuel/p11_lite/goal_to_path_status [std_msgs/msg/String]
/fuel/p11_lite/local_free_points [sensor_msgs/msg/PointCloud2]
/fuel/p11_lite/local_occupied_points [sensor_msgs/msg/PointCloud2]
/fuel/p11_lite/map_status [std_msgs/msg/String]
/fuel/p11_lite/occupancy_grid [sensor_msgs/msg/PointCloud2]
/fuel/p11_lite/sensing_status [std_msgs/msg/String]
/fuel/p11_lite/visual/all_markers [visualization_msgs/msg/MarkerArray]
/fuel/p11_lite/visual/best_viewpoint_marker [visualization_msgs/msg/Marker]
/fuel/p11_lite/visual/current_goal_marker [visualization_msgs/msg/Marker]
/fuel/p11_lite/visual/frontier_markers [visualization_msgs/msg/MarkerArray]
/fuel/p11_lite/visual/legend_markers [visualization_msgs/msg/MarkerArray]
/fuel/p11_lite/visual/map_boundary_marker [visualization_msgs/msg/Marker]
/fuel/p11_lite/visual/path_markers [visualization_msgs/msg/MarkerArray]
/fuel/p11_lite/visual/uav_marker [visualization_msgs/msg/Marker]
/fuel/p11_lite/visual/uav_trail [visualization_msgs/msg/Marker]
/fuel/plan_manager/managed_trajectory [nav_msgs/msg/Path]
/fuel/visual/world_bounds [visualization_msgs/msg/MarkerArray]
/fuel/visual/world_obstacles [visualization_msgs/msg/MarkerArray]
/global_cloud [sensor_msgs/msg/PointCloud2]
/map_cloud [sensor_msgs/msg/PointCloud2]
/map_generator/global_cloud [sensor_msgs/msg/PointCloud2]
/move_base_simple/goal [geometry_msgs/msg/PoseStamped]
/odom [nav_msgs/msg/Odometry]
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/pcl_render_node/cloud [sensor_msgs/msg/PointCloud2]
/pcl_render_node/depth [sensor_msgs/msg/PointCloud2]
/pcl_render_node/sensor_pose [geometry_msgs/msg/PoseStamped]
/planning/pos_cmd [geometry_msgs/msg/PoseStamped]
/planning/travel_traj [nav_msgs/msg/Path]
/rosout [rcl_interfaces/msg/Log]
/state_estimation [nav_msgs/msg/Odometry]
/state_ukf/odom [nav_msgs/msg/Odometry]
/tf_static [tf2_msgs/msg/TFMessage]
/visual_slam/odom [nav_msgs/msg/Odometry]
P2I_ROUTE_PROGRESS time_sec=30.025 coverage_proxy=0.134 odom_total_distance=10.648 coverage_gain_per_meter=0.004 path_length_regret_avg=-3.918 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.863 route_tortuosity=1.265 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=60.026 coverage_proxy=0.168 odom_total_distance=21.511 coverage_gain_per_meter=0.004 path_length_regret_avg=-4.138 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.854 route_tortuosity=1.426 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=90.059 coverage_proxy=0.169 odom_total_distance=26.616 coverage_gain_per_meter=0.003 path_length_regret_avg=-2.383 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.859 route_tortuosity=1.592 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=120.075 coverage_proxy=0.174 odom_total_distance=33.667 coverage_gain_per_meter=0.002 path_length_regret_avg=3.064 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.864 route_tortuosity=2.344 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=150.075 coverage_proxy=0.194 odom_total_distance=40.214 coverage_gain_per_meter=0.003 path_length_regret_avg=4.530 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.871 route_tortuosity=2.667 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=180.092 coverage_proxy=0.208 odom_total_distance=46.697 coverage_gain_per_meter=0.003 path_length_regret_avg=3.950 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.876 route_tortuosity=2.785 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=210.126 coverage_proxy=0.212 odom_total_distance=49.934 coverage_gain_per_meter=0.002 path_length_regret_avg=3.430 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.880 route_tortuosity=3.683 main_route_issue=ACTIVE_PATH_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=240.126 coverage_proxy=0.212 odom_total_distance=49.934 coverage_gain_per_meter=0.002 path_length_regret_avg=3.430 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.880 route_tortuosity=3.683 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=270.159 coverage_proxy=0.216 odom_total_distance=52.091 coverage_gain_per_meter=0.002 path_length_regret_avg=3.502 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.881 route_tortuosity=3.834 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=300.025 coverage_proxy=0.217 odom_total_distance=53.705 coverage_gain_per_meter=0.002 path_length_regret_avg=3.559 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.881 route_tortuosity=3.633 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2i_route_300s_after_fix_20260622_140917
duration_sec=300.02916264533997
odom_total_distance=53.70499945212549
coverage_proxy_gain=0.12582830216462967
coverage_gain_per_meter=0.002342953234303585
selected_goal_unique_count=25
path_length_regret_avg=3.558820359661196
path_length_regret_max=17.712966770707673
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8807692307692307
route_tortuosity=3.6327633305493348
active_path_endpoint_to_goal_distance_avg=0.14468877099030356
goal_without_path_count=5
goal_to_path_timeout_count=6
active_goal_without_active_path_max_duration_sec=25.99843120574951
active_goal_without_travel_traj_max_duration_sec=25.99843120574951
uav_idle_due_to_no_path_duration_sec=0.0
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
result=PASS
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
coverage_proxy_gain=0.12582830216462967
coverage_gain_per_meter=0.002342953234303585
odom_total_distance=53.70499945212549
selected_goal_unique_count=25
path_length_regret_avg=3.558820359661196
path_length_regret_max=17.712966770707673
nearest_frontier_ignored_count=5
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8807692307692307
route_tortuosity=3.6327633305493348
active_path_endpoint_to_goal_distance_avg=0.14468877099030356
active_path_endpoint_to_goal_distance_max=5.794046373918307
P2I_route_300s_after_fix_DONE run_id=p2i_route_300s_after_fix_20260622_140917
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_141443_p2i_route_300s_after_fix_summary.md
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
### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140917/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- coverage_proxy_gain: 0.12582830216462967
- coverage_gain_per_meter: 0.002342953234303585
- odom_total_distance: 53.70499945212549
- selected_goal_unique_count: 25
- path_length_regret_avg: 3.558820359661196
- path_length_regret_max: 17.712966770707673
- nearest_frontier_ignored_count: 5
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8807692307692307
- route_tortuosity: 3.6327633305493348
- active_path_endpoint_to_goal_distance_avg: 0.14468877099030356
- active_path_endpoint_to_goal_distance_max: 5.794046373918307
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140917/route_events.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140917/route_events.csv
- file_size_bytes: 22

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140917/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.02916264533997
- odom_total_distance: 53.70499945212549
- coverage_proxy_start: 0.09100279782064497
- coverage_proxy_end: 0.21683109998527464
- coverage_proxy_gain: 0.12582830216462967
- coverage_gain_per_meter: 0.002342953234303585
- selected_goal_count: 396
- selected_goal_unique_count: 25
- selected_goal_distance_from_odom_avg: 6.1076443066574475
- selected_goal_distance_from_odom_max: 14.846201472570788
- selected_goal_path_length_avg: 10.777416017515462
- selected_goal_path_length_max: 27.90420627223184
- selected_goal_path_efficiency_avg: 0.7038304056733397
- frontier_candidate_count_avg: 188.64661654135338
- frontier_viewpoint_count_avg: 35.61
- nearest_frontier_distance_avg: 7.147025024914858
- nearest_frontier_distance_min: 5.083211833664399
- nearest_frontier_ignored_count: 5
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 10.777416017515462
- path_length_to_nearest_candidate_avg: 7.2291805483019065
- path_length_regret_avg: 3.558820359661196
- path_length_regret_max: 17.712966770707673
- coverage_gain_after_goal_avg: 0.009007019093898788
- coverage_gain_after_goal_per_meter_avg: 0.047565635186813206
- low_efficiency_goal_count: 0
- local_region_revisit_count: 2
- region_diversity_score: 0.92
- active_path_endpoint_to_goal_distance_avg: 0.14468877099030356
- active_path_endpoint_to_goal_distance_max: 5.794046373918307
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.8807692307692307
- route_tortuosity: 3.6327633305493348
- active_path_update_count: 188
- position_cmd_update_count: 188
- travel_traj_update_count: 442
- frontier_candidate_count_end: 222
- frontier_viewpoint_count_end: 21
- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- goal_selected_count: 25
- goal_without_path_count: 5
- goal_without_path_ratio: 0.2
- goal_to_path_latency_avg_sec: 1.299915419684516
- goal_to_path_latency_max_sec: 5.8021275997161865
- goal_to_path_timeout_count: 6
- goal_to_path_timeout_max_duration_sec: 25.99843120574951
- active_goal_without_active_path_max_duration_sec: 25.99843120574951
- active_goal_without_travel_traj_max_duration_sec: 25.99843120574951
- path_missing_after_goal_count: 7
- path_missing_after_goal_max_duration_sec: 25.99843120574951
- path_generation_fail_count: 59
- path_generation_fail_reasons: {'goal_too_close': 6, 'no_collision_free_grid_path': 51, 'waiting_for_odom_or_goal': 2}
- goal_to_path_status_events: ['REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=3.874 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=5.791 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=7.708 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=9.616 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=11.514 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=13.394 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=15.291 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=17.287 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=19.239 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=21.128 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=23.017 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=1.723 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=3.442 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=5.126 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=6.816 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=1.688 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.596 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=3.416 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.596 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=5.163 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.509 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=6.848 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.247 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 fi
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140917/route_timeseries.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140917/route_timeseries.csv
- file_size_bytes: 1808

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140917/route_rationality.json
```json
{
  "active_goal_without_active_path_max_duration_sec": 25.99843120574951,
  "active_goal_without_travel_traj_max_duration_sec": 25.99843120574951,
  "active_path_empty_count": 0,
  "active_path_endpoint_to_goal_distance_avg": 0.14468877099030356,
  "active_path_endpoint_to_goal_distance_max": 5.794046373918307,
  "active_path_first_update_after_goal_sec": 1.299915419684516,
  "active_path_update_count": 188,
  "coverage_gain_after_goal_avg": 0.009007019093898788,
  "coverage_gain_after_goal_per_meter_avg": 0.047565635186813206,
  "coverage_gain_per_meter": 0.002342953234303585,
  "coverage_proxy_end": 0.21683109998527464,
  "coverage_proxy_gain": 0.12582830216462967,
  "coverage_proxy_start": 0.09100279782064497,
  "duration_sec": 300.02916264533997,
  "frontier_candidate_count_avg": 188.64661654135338,
  "frontier_candidate_count_end": 222,
  "frontier_viewpoint_count_avg": 35.61,
  "frontier_viewpoint_count_end": 21,
  "goal_reselect_due_to_no_path_count": 0,
  "goal_selected_count": 25,
  "goal_to_path_latency_avg_sec": 1.299915419684516,
  "goal_to_path_latency_max_sec": 5.8021275997161865,
  "goal_to_path_status_events": [
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=3.874 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=5.791 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=7.708 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=9.616 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=11.514 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=13.394 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=15.291 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=17.287 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=19.239 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=21.128 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=23.017 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(8.8, -2.3, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=1.723 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=3.442 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=5.126 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=41 wait_sec=6.816 GOAL_TO_PATH_REQUEST goal_id=41 goal_key=(8.5, -6.5, 1.2) GOAL_TO_PATH_WAITING goal_id=41 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=1.688 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.596 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=3.416 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.596 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=5.163 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.509 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=6.848 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=12.247 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=8.354 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(11.5, 0.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=11.909 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment"
  ],
  "goal_to_path_timeout_count": 6,
  "goal_to_path_timeout_max_duration_sec": 25.99843120574951,
  "goal_without_path_count": 5,
  "goal_without_path_ratio": 0.2,
  "local_region_revisit_count": 2,
  "low_efficiency_goal_count": 0,
  "main_route_issue": "TRAVEL_TRAJ_MISSING_AFTER_GOAL",
  "near_high_gain_candidate_ignored_count": 0,
  "nearest_frontier_distance_avg": 7.147025024914858,
  "nearest_frontier_distance_min": 5.083211833664399,
  "nearest_frontier_ignored_count": 5,
  "no_path_blacklist_count": 0,
  "odom_total_distance": 53.70499945212549,
  "path_generation_fail_count": 59,
  "path_generation_fail_reasons": {
    "goal_too_close": 6,
    "no_collision_free_grid_path": 51,
    "waiting_for_odom_or_goal": 2
  },
  "path_length_regret_avg": 3.558820359661196,
  "path_length_regret_max": 17.712966770707673,
  "path_length_to_nearest_candidate_avg": 7.2291805483019065,
  "path_length_to_selected_goal_avg": 10.777416017515462,
  "path_missing_after_goal_count": 7,
  "path_missing_after_goal_max_duration_sec": 25.99843120574951,
  "position_cmd_update_count": 188,
  "region_diversity_score": 0.92,
  "route_backtracking_distance": 0.0,
  "route_revisit_ratio": 0.8807692307692307,
  "route_tortuosity": 3.6327633305493348,
  "selected_goal_count": 396,
  "selected_goal_distance_from_odom_avg": 6.1076443066574475,
  "selected_goal_distance_from_odom_max": 14.846201472570788,
  "selected_goal_path_efficiency_avg": 0.7038304056733397,
  "selected_goal_path_length_avg": 10.777416017515462,
  "selected_goal_path_length_max": 27.90420627223184,
  "selected_goal_unique_count": 25,
  "travel_traj_first_update_after_goal_sec": 0.8829982406214664,
  "travel_traj_update_count": 442,
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140915_p2i_route_300s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_141443_p2i_route_300s_after_fix_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
