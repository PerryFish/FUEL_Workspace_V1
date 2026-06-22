# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T14:37:07+0800
- Task name: p2i_route_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143131_p2i_route_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_143658_p2i_route_300s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_143704_p2i_route_300s_after_fix_full_log.md

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
nuaa         368  1.6  0.0  27336 14136 ?        S    14:37   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2i_route_300s_after_fix --command ./scripts/run_p2i_route_300s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143131_p2i_route_300s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_143658_p2i_route_300s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T14:31:31+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143131_p2i_route_300s_after_fix.md

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
run_id=p2i_route_300s_after_fix_20260622_143133
mode=route_300s_after_fix
duration=300
2026-06-22T14:31:33+08:00
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
P2I_ROUTE_PROGRESS time_sec=30.026 coverage_proxy=0.109 odom_total_distance=6.311 coverage_gain_per_meter=0.004 path_length_regret_avg=0.066 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.839 route_tortuosity=1.148 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=60.059 coverage_proxy=0.133 odom_total_distance=14.409 coverage_gain_per_meter=0.003 path_length_regret_avg=-2.009 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.843 route_tortuosity=1.571 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=90.060 coverage_proxy=0.140 odom_total_distance=22.775 coverage_gain_per_meter=0.002 path_length_regret_avg=-2.842 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.864 route_tortuosity=1.872 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=120.060 coverage_proxy=0.140 odom_total_distance=30.364 coverage_gain_per_meter=0.002 path_length_regret_avg=-3.924 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.857 route_tortuosity=3.928 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=150.065 coverage_proxy=0.146 odom_total_distance=36.379 coverage_gain_per_meter=0.002 path_length_regret_avg=-2.969 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.859 route_tortuosity=3.505 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=180.080 coverage_proxy=0.159 odom_total_distance=42.464 coverage_gain_per_meter=0.002 path_length_regret_avg=-2.635 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.859 route_tortuosity=4.941 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=210.081 coverage_proxy=0.188 odom_total_distance=55.680 coverage_gain_per_meter=0.002 path_length_regret_avg=-2.846 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.867 route_tortuosity=5.089 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=240.088 coverage_proxy=0.201 odom_total_distance=61.715 coverage_gain_per_meter=0.002 path_length_regret_avg=-2.307 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.866 route_tortuosity=4.001 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=270.093 coverage_proxy=0.216 odom_total_distance=68.670 coverage_gain_per_meter=0.002 path_length_regret_avg=-2.322 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.865 route_tortuosity=4.587 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=300.005 coverage_proxy=0.238 odom_total_distance=77.931 coverage_gain_per_meter=0.002 path_length_regret_avg=-2.448 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.868 route_tortuosity=6.108 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2i_route_300s_after_fix_20260622_143133
duration_sec=300.00813603401184
odom_total_distance=77.93106382489415
coverage_proxy_gain=0.15248122515093504
coverage_gain_per_meter=0.001956616754180978
selected_goal_unique_count=27
path_length_regret_avg=-2.4483595027917473
path_length_regret_max=4.819330834823785
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8677248677248677
route_tortuosity=6.107834695317354
active_path_endpoint_to_goal_distance_avg=2.0935403231009504e-17
goal_without_path_count=0
goal_to_path_timeout_count=6
active_goal_without_active_path_max_duration_sec=3.9994752407073975
active_goal_without_travel_traj_max_duration_sec=3.9994752407073975
uav_idle_due_to_no_path_duration_sec=0.0
main_route_issue=GOAL_TO_PATH_TIMEOUT
result=PASS
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=GOAL_TO_PATH_TIMEOUT
coverage_proxy_gain=0.15248122515093504
coverage_gain_per_meter=0.001956616754180978
odom_total_distance=77.93106382489415
selected_goal_unique_count=27
path_length_regret_avg=-2.4483595027917473
path_length_regret_max=4.819330834823785
nearest_frontier_ignored_count=0
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8677248677248677
route_tortuosity=6.107834695317354
active_path_endpoint_to_goal_distance_avg=2.0935403231009504e-17
active_path_endpoint_to_goal_distance_max=4.440892098500626e-16
P2I_route_300s_after_fix_DONE run_id=p2i_route_300s_after_fix_20260622_143133
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_143658_p2i_route_300s_after_fix_summary.md
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
### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: GOAL_TO_PATH_TIMEOUT
- coverage_proxy_gain: 0.15248122515093504
- coverage_gain_per_meter: 0.001956616754180978
- odom_total_distance: 77.93106382489415
- selected_goal_unique_count: 27
- path_length_regret_avg: -2.4483595027917473
- path_length_regret_max: 4.819330834823785
- nearest_frontier_ignored_count: 0
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8677248677248677
- route_tortuosity: 6.107834695317354
- active_path_endpoint_to_goal_distance_avg: 2.0935403231009504e-17
- active_path_endpoint_to_goal_distance_max: 4.440892098500626e-16
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_events.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_events.csv
- file_size_bytes: 22

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_timeseries.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_timeseries.csv
- file_size_bytes: 1773

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.00813603401184
- odom_total_distance: 77.93106382489415
- coverage_proxy_start: 0.08511264909438963
- coverage_proxy_end: 0.2375938742453247
- coverage_proxy_gain: 0.15248122515093504
- coverage_gain_per_meter: 0.001956616754180978
- selected_goal_count: 500
- selected_goal_unique_count: 27
- selected_goal_distance_from_odom_avg: 4.626475704123153
- selected_goal_distance_from_odom_max: 7.4604565871650435
- selected_goal_path_length_avg: 4.810704043971799
- selected_goal_path_length_max: 11.082855407527683
- selected_goal_path_efficiency_avg: 0.8620877207190076
- frontier_candidate_count_avg: 155.99248120300751
- frontier_viewpoint_count_avg: 25.19
- nearest_frontier_distance_avg: 7.233840800396645
- nearest_frontier_distance_min: 5.2087564498083445
- nearest_frontier_ignored_count: 0
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 4.810704043971799
- path_length_to_nearest_candidate_avg: 7.266050744763395
- path_length_regret_avg: -2.4483595027917473
- path_length_regret_max: 4.819330834823785
- coverage_gain_after_goal_avg: 0.00893716797118358
- coverage_gain_after_goal_per_meter_avg: 0.020409049117079876
- low_efficiency_goal_count: 2
- local_region_revisit_count: 2
- region_diversity_score: 0.9259259259259259
- active_path_endpoint_to_goal_distance_avg: 2.0935403231009504e-17
- active_path_endpoint_to_goal_distance_max: 4.440892098500626e-16
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.8677248677248677
- route_tortuosity: 6.107834695317354
- active_path_update_count: 271
- position_cmd_update_count: 270
- travel_traj_update_count: 798
- frontier_candidate_count_end: 214
- frontier_viewpoint_count_end: 12
- main_route_issue: GOAL_TO_PATH_TIMEOUT
- goal_selected_count: 27
- goal_without_path_count: 0
- goal_without_path_ratio: 0.0
- goal_to_path_latency_avg_sec: 0.5549580369676862
- goal_to_path_latency_max_sec: 1.977797508239746
- goal_to_path_timeout_count: 6
- goal_to_path_timeout_max_duration_sec: 3.9994752407073975
- active_goal_without_active_path_max_duration_sec: 3.9994752407073975
- active_goal_without_travel_traj_max_duration_sec: 3.9994752407073975
- path_missing_after_goal_count: 6
- path_missing_after_goal_max_duration_sec: 3.9994752407073975
- path_generation_fail_count: 21
- path_generation_fail_reasons: {'no_collision_free_grid_path': 20, 'goal_too_close': 1}
- goal_to_path_status_events: ['REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=3.041 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=2.565 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=4.038 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=2.149 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=5.035 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=1.734 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=6.017 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=1.324 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=0.043 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=2.941 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=1.042 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=2.595 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=2.033 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=2.210 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=3.038 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=1.772 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=4.035 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=1.295 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=0.711 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.216 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=1.642 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.016 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=2.631 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.950 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=3.670 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.192 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=4.697 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.240 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=5.584 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.566 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=6.593 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.459 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=7.564 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.224 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=8.548 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.111 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=9.495 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=4.886 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=N
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_rationality.json
```json
{
  "active_goal_without_active_path_max_duration_sec": 3.9994752407073975,
  "active_goal_without_travel_traj_max_duration_sec": 3.9994752407073975,
  "active_path_empty_count": 0,
  "active_path_endpoint_to_goal_distance_avg": 2.0935403231009504e-17,
  "active_path_endpoint_to_goal_distance_max": 4.440892098500626e-16,
  "active_path_first_update_after_goal_sec": 0.5549580369676862,
  "active_path_update_count": 271,
  "coverage_gain_after_goal_avg": 0.00893716797118358,
  "coverage_gain_after_goal_per_meter_avg": 0.020409049117079876,
  "coverage_gain_per_meter": 0.001956616754180978,
  "coverage_proxy_end": 0.2375938742453247,
  "coverage_proxy_gain": 0.15248122515093504,
  "coverage_proxy_start": 0.08511264909438963,
  "duration_sec": 300.00813603401184,
  "frontier_candidate_count_avg": 155.99248120300751,
  "frontier_candidate_count_end": 214,
  "frontier_viewpoint_count_avg": 25.19,
  "frontier_viewpoint_count_end": 12,
  "goal_reselect_due_to_no_path_count": 0,
  "goal_selected_count": 27,
  "goal_to_path_latency_avg_sec": 0.5549580369676862,
  "goal_to_path_latency_max_sec": 1.977797508239746,
  "goal_to_path_status_events": [
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=3.041 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=2.565 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=4.038 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=2.149 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=5.035 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=1.734 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=42 wait_sec=6.017 GOAL_TO_PATH_REQUEST goal_id=42 goal_key=(3.6, 7.4, 1.2) GOAL_TO_PATH_SUCCESS goal_id=42 path_len=1.324 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.521 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=0.043 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=2.941 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=1.042 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=2.595 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=2.033 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=2.210 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=3.038 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=1.772 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=4.035 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(1.6, 7.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=1.295 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_seg",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=0.711 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.216 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=1.642 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.016 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=2.631 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.950 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=3.670 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.192 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=4.697 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.240 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=5.584 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.566 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=6.593 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.459 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=7.564 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.224 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=8.548 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=5.111 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=9.495 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=4.886 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=10.461 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-1.0, 6.7, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=4.764 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment"
  ],
  "goal_to_path_timeout_count": 6,
  "goal_to_path_timeout_max_duration_sec": 3.9994752407073975,
  "goal_without_path_count": 0,
  "goal_without_path_ratio": 0.0,
  "local_region_revisit_count": 2,
  "low_efficiency_goal_count": 2,
  "main_route_issue": "GOAL_TO_PATH_TIMEOUT",
  "near_high_gain_candidate_ignored_count": 0,
  "nearest_frontier_distance_avg": 7.233840800396645,
  "nearest_frontier_distance_min": 5.2087564498083445,
  "nearest_frontier_ignored_count": 0,
  "no_path_blacklist_count": 0,
  "odom_total_distance": 77.93106382489415,
  "path_generation_fail_count": 21,
  "path_generation_fail_reasons": {
    "goal_too_close": 1,
    "no_collision_free_grid_path": 20
  },
  "path_length_regret_avg": -2.4483595027917473,
  "path_length_regret_max": 4.819330834823785,
  "path_length_to_nearest_candidate_avg": 7.266050744763395,
  "path_length_to_selected_goal_avg": 4.810704043971799,
  "path_missing_after_goal_count": 6,
  "path_missing_after_goal_max_duration_sec": 3.9994752407073975,
  "position_cmd_update_count": 270,
  "region_diversity_score": 0.9259259259259259,
  "route_backtracking_distance": 0.0,
  "route_revisit_ratio": 0.8677248677248677,
  "route_tortuosity": 6.107834695317354,
  "selected_goal_count": 500,
  "selected_goal_distance_from_odom_avg": 4.626475704123153,
  "selected_goal_distance_from_odom_max": 7.4604565871650435,
  "selected_goal_path_efficiency_avg": 0.8620877207190076,
  "selected_goal_path_length_avg": 4.810704043971799,
  "selected_goal_path_length_max": 11.082855407527683,
  "selected_goal_unique_count": 27,
  "travel_traj_first_update_after_goal_sec": 0.5217232590629941,
  "travel_traj_update_count": 798,
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_143131_p2i_route_300s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_143658_p2i_route_300s_after_fix_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
