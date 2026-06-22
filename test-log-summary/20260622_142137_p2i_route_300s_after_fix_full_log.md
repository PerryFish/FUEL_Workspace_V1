# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T14:21:40+0800
- Task name: p2i_route_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_141604_p2i_route_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142132_p2i_route_300s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142137_p2i_route_300s_after_fix_full_log.md

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
nuaa         368  1.6  0.0  27336 14156 ?        S    14:21   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2i_route_300s_after_fix --command ./scripts/run_p2i_route_300s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_141604_p2i_route_300s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142132_p2i_route_300s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T14:16:04+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_141604_p2i_route_300s_after_fix.md

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
run_id=p2i_route_300s_after_fix_20260622_141606
mode=route_300s_after_fix
duration=300
2026-06-22T14:16:06+08:00
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
P2I_ROUTE_PROGRESS time_sec=30.031 coverage_proxy=0.085 odom_total_distance=4.920 coverage_gain_per_meter=0.002 path_length_regret_avg=7.320 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.880 route_tortuosity=1.072 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=60.042 coverage_proxy=0.089 odom_total_distance=11.324 coverage_gain_per_meter=0.001 path_length_regret_avg=4.965 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.875 route_tortuosity=1.419 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=90.057 coverage_proxy=0.106 odom_total_distance=21.609 coverage_gain_per_meter=0.001 path_length_regret_avg=2.024 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.868 route_tortuosity=3.065 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=120.063 coverage_proxy=0.122 odom_total_distance=27.720 coverage_gain_per_meter=0.002 path_length_regret_avg=0.988 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.867 route_tortuosity=5.240 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=150.075 coverage_proxy=0.122 odom_total_distance=28.088 coverage_gain_per_meter=0.002 path_length_regret_avg=1.156 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.861 route_tortuosity=4.965 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=180.108 coverage_proxy=0.126 odom_total_distance=32.094 coverage_gain_per_meter=0.002 path_length_regret_avg=2.505 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.865 route_tortuosity=4.736 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=210.116 coverage_proxy=0.126 odom_total_distance=33.141 coverage_gain_per_meter=0.001 path_length_regret_avg=2.669 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.870 route_tortuosity=4.586 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=240.117 coverage_proxy=0.126 odom_total_distance=33.141 coverage_gain_per_meter=0.001 path_length_regret_avg=2.669 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.870 route_tortuosity=4.586 main_route_issue=UAV_IDLE_DUE_TO_NO_PATH
P2I_ROUTE_PROGRESS time_sec=270.117 coverage_proxy=0.126 odom_total_distance=33.141 coverage_gain_per_meter=0.001 path_length_regret_avg=2.669 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.870 route_tortuosity=4.586 main_route_issue=UAV_IDLE_DUE_TO_NO_PATH
P2I_ROUTE_PROGRESS time_sec=300.009 coverage_proxy=0.126 odom_total_distance=33.141 coverage_gain_per_meter=0.001 path_length_regret_avg=2.669 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.870 route_tortuosity=4.586 main_route_issue=UAV_IDLE_DUE_TO_NO_PATH
P2I_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2i_route_300s_after_fix_20260622_141606
duration_sec=300.0155794620514
odom_total_distance=33.14057674968115
coverage_proxy_gain=0.04837284641437195
coverage_gain_per_meter=0.0014596259678805183
selected_goal_unique_count=21
path_length_regret_avg=2.6688439674569713
path_length_regret_max=10.841272891958297
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8695652173913043
route_tortuosity=4.585606949619388
active_path_endpoint_to_goal_distance_avg=0.420888167191617
goal_without_path_count=4
goal_to_path_timeout_count=9
active_goal_without_active_path_max_duration_sec=74.84858107566833
active_goal_without_travel_traj_max_duration_sec=74.84858107566833
uav_idle_due_to_no_path_duration_sec=89.89823865890503
main_route_issue=UAV_IDLE_DUE_TO_NO_PATH
result=PARTIAL
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=UAV_IDLE_DUE_TO_NO_PATH
coverage_proxy_gain=0.04837284641437195
coverage_gain_per_meter=0.0014596259678805183
odom_total_distance=33.14057674968115
selected_goal_unique_count=21
path_length_regret_avg=2.6688439674569713
path_length_regret_max=10.841272891958297
nearest_frontier_ignored_count=4
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8695652173913043
route_tortuosity=4.585606949619388
active_path_endpoint_to_goal_distance_avg=0.420888167191617
active_path_endpoint_to_goal_distance_max=5.0
P2I_route_300s_after_fix_DONE run_id=p2i_route_300s_after_fix_20260622_141606
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142132_p2i_route_300s_after_fix_summary.md
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
### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: UAV_IDLE_DUE_TO_NO_PATH
- coverage_proxy_gain: 0.04837284641437195
- coverage_gain_per_meter: 0.0014596259678805183
- odom_total_distance: 33.14057674968115
- selected_goal_unique_count: 21
- path_length_regret_avg: 2.6688439674569713
- path_length_regret_max: 10.841272891958297
- nearest_frontier_ignored_count: 4
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8695652173913043
- route_tortuosity: 4.585606949619388
- active_path_endpoint_to_goal_distance_avg: 0.420888167191617
- active_path_endpoint_to_goal_distance_max: 5.0
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_timeseries.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_timeseries.csv
- file_size_bytes: 1790

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_events.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_events.csv
- file_size_bytes: 22

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.0155794620514
- odom_total_distance: 33.14057674968115
- coverage_proxy_start: 0.07767633632749227
- coverage_proxy_end: 0.12604918274186422
- coverage_proxy_gain: 0.04837284641437195
- coverage_gain_per_meter: 0.0014596259678805183
- selected_goal_count: 284
- selected_goal_unique_count: 21
- selected_goal_distance_from_odom_avg: 6.467389842067417
- selected_goal_distance_from_odom_max: 12.901132279949293
- selected_goal_path_length_avg: 9.20614098917274
- selected_goal_path_length_max: 17.09129000040779
- selected_goal_path_efficiency_avg: 0.7263689984086258
- frontier_candidate_count_avg: 131.5825
- frontier_viewpoint_count_avg: 30.573333333333334
- nearest_frontier_distance_avg: 7.345813894537582
- nearest_frontier_distance_min: 5.483085646228038
- nearest_frontier_ignored_count: 4
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 9.20614098917274
- path_length_to_nearest_candidate_avg: 6.537297021715791
- path_length_regret_avg: 2.6688439674569713
- path_length_regret_max: 10.841272891958297
- coverage_gain_after_goal_avg: 0.006302459137093211
- coverage_gain_after_goal_per_meter_avg: 0.048375529444379645
- low_efficiency_goal_count: 0
- local_region_revisit_count: 3
- region_diversity_score: 0.8571428571428571
- active_path_endpoint_to_goal_distance_avg: 0.420888167191617
- active_path_endpoint_to_goal_distance_max: 5.0
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.8695652173913043
- route_tortuosity: 4.585606949619388
- active_path_update_count: 127
- position_cmd_update_count: 128
- travel_traj_update_count: 302
- frontier_candidate_count_end: 140
- frontier_viewpoint_count_end: 27
- main_route_issue: UAV_IDLE_DUE_TO_NO_PATH
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
- goal_to_path_status_events: ['REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=12.217 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=13.318 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=14.425 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=15.531 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=16.688 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=17.771 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=18.899 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=20.024 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=21.123 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=22.270 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=23.365 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=24.466 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=25.558 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=26.685 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=27.846 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=28.992 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=30.125 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=31.238 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=32.337 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p', 'R
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_141606/route_rationality.json
```json
{
  "active_goal_without_active_path_max_duration_sec": 74.84858107566833,
  "active_goal_without_travel_traj_max_duration_sec": 74.84858107566833,
  "active_path_empty_count": 0,
  "active_path_endpoint_to_goal_distance_avg": 0.420888167191617,
  "active_path_endpoint_to_goal_distance_max": 5.0,
  "active_path_first_update_after_goal_sec": 0.5284361441930135,
  "active_path_update_count": 127,
  "coverage_gain_after_goal_avg": 0.006302459137093211,
  "coverage_gain_after_goal_per_meter_avg": 0.048375529444379645,
  "coverage_gain_per_meter": 0.0014596259678805183,
  "coverage_proxy_end": 0.12604918274186422,
  "coverage_proxy_gain": 0.04837284641437195,
  "coverage_proxy_start": 0.07767633632749227,
  "duration_sec": 300.0155794620514,
  "frontier_candidate_count_avg": 131.5825,
  "frontier_candidate_count_end": 140,
  "frontier_viewpoint_count_avg": 30.573333333333334,
  "frontier_viewpoint_count_end": 27,
  "goal_reselect_due_to_no_path_count": 0,
  "goal_selected_count": 21,
  "goal_to_path_latency_avg_sec": 0.5284361441930135,
  "goal_to_path_latency_max_sec": 3.2557754516601562,
  "goal_to_path_status_events": [
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=12.217 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=13.318 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=40 wait_sec=14.425 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_WAITING goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=15.531 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=16.688 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=17.771 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=18.899 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=20.024 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=21.123 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=22.270 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=23.365 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=24.466 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=25.558 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=26.685 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=27.846 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=28.992 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=30.125 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=31.238 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=32.337 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_TIMEOUT goal_id=40 wait_sec=33.452 GOAL_TO_PATH_REQUEST goal_id=40 goal_key=(6.5, 6.2, 1.2) GOAL_TO_PATH_TIMEOUT goal_id=40 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_p"
  ],
  "goal_to_path_timeout_count": 9,
  "goal_to_path_timeout_max_duration_sec": 74.84858107566833,
  "goal_without_path_count": 4,
  "goal_without_path_ratio": 0.19047619047619047,
  "local_region_revisit_count": 3,
  "low_efficiency_goal_count": 0,
  "main_route_issue": "UAV_IDLE_DUE_TO_NO_PATH",
  "near_high_gain_candidate_ignored_count": 0,
  "nearest_frontier_distance_avg": 7.345813894537582,
  "nearest_frontier_distance_min": 5.483085646228038,
  "nearest_frontier_ignored_count": 4,
  "no_path_blacklist_count": 0,
  "odom_total_distance": 33.14057674968115,
  "path_generation_fail_count": 62,
  "path_generation_fail_reasons": {
    "no_collision_free_grid_path": 62
  },
  "path_length_regret_avg": 2.6688439674569713,
  "path_length_regret_max": 10.841272891958297,
  "path_length_to_nearest_candidate_avg": 6.537297021715791,
  "path_length_to_selected_goal_avg": 9.20614098917274,
  "path_missing_after_goal_count": 9,
  "path_missing_after_goal_max_duration_sec": 74.84858107566833,
  "position_cmd_update_count": 128,
  "region_diversity_score": 0.8571428571428571,
  "route_backtracking_distance": 0.0,
  "route_revisit_ratio": 0.8695652173913043,
  "route_tortuosity": 4.585606949619388,
  "selected_goal_count": 284,
  "selected_goal_distance_from_odom_avg": 6.467389842067417,
  "selected_goal_distance_from_odom_max": 12.901132279949293,
  "selected_goal_path_efficiency_avg": 0.7263689984086258,
  "selected_goal_path_length_avg": 9.20614098917274,
  "selected_goal_path_length_max": 17.09129000040779,
  "selected_goal_unique_count": 21,
  "travel_traj_first_update_after_goal_sec": 0.4804527958234151,
  "travel_traj_update_count": 302,
  "uav_idle_due_to_no_path_duration_sec": 89.89823865890503
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_141604_p2i_route_300s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142132_p2i_route_300s_after_fix_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
