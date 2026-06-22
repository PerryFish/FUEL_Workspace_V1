# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T14:07:32+0800
- Task name: p2i_route_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140156_p2i_route_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_140723_p2i_route_300s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_140729_p2i_route_300s_after_fix_full_log.md

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
nuaa         368  1.6  0.0  27336 14064 ?        S    14:07   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2i_route_300s_after_fix --command ./scripts/run_p2i_route_300s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140156_p2i_route_300s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_140723_p2i_route_300s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T14:01:56+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140156_p2i_route_300s_after_fix.md

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
run_id=p2i_route_300s_after_fix_20260622_140158
mode=route_300s_after_fix
duration=300
2026-06-22T14:01:58+08:00
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
P2H_ROUTE_PROGRESS time_sec=30.021 coverage_proxy=0.108 odom_total_distance=5.958 coverage_gain_per_meter=0.004 path_length_regret_avg=0.196 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.828 route_tortuosity=1.107 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=60.046 coverage_proxy=0.129 odom_total_distance=12.830 coverage_gain_per_meter=0.003 path_length_regret_avg=-2.076 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.841 route_tortuosity=1.467 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=90.051 coverage_proxy=0.141 odom_total_distance=17.686 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.699 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.860 route_tortuosity=1.379 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=120.064 coverage_proxy=0.146 odom_total_distance=22.607 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.369 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.864 route_tortuosity=1.706 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=150.088 coverage_proxy=0.164 odom_total_distance=31.164 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.125 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.868 route_tortuosity=1.754 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=180.089 coverage_proxy=0.192 odom_total_distance=42.246 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.170 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.873 route_tortuosity=2.844 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=210.094 coverage_proxy=0.205 odom_total_distance=47.950 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.475 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.876 route_tortuosity=3.919 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=240.124 coverage_proxy=0.234 odom_total_distance=56.535 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.828 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.876 route_tortuosity=4.722 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=270.122 coverage_proxy=0.250 odom_total_distance=64.530 coverage_gain_per_meter=0.003 path_length_regret_avg=-0.783 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.872 route_tortuosity=4.347 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2H_ROUTE_PROGRESS time_sec=300.004 coverage_proxy=0.254 odom_total_distance=70.169 coverage_gain_per_meter=0.002 path_length_regret_avg=-0.839 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.871 route_tortuosity=5.404 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2i_route_300s_after_fix_20260622_140158
duration_sec=300.008273601532
odom_total_distance=70.16941368925721
coverage_proxy_gain=0.16860550728905904
coverage_gain_per_meter=0.002402834774075819
selected_goal_unique_count=20
path_length_regret_avg=-0.838739573843837
path_length_regret_max=12.625099437203264
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8705882352941177
route_tortuosity=5.404433266147319
active_path_endpoint_to_goal_distance_avg=0.10778229035037926
goal_without_path_count=4
goal_to_path_timeout_count=4
active_goal_without_active_path_max_duration_sec=298.7583529949188
active_goal_without_travel_traj_max_duration_sec=298.7583529949188
uav_idle_due_to_no_path_duration_sec=0.0
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
result=PASS
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
coverage_proxy_gain=0.16860550728905904
coverage_gain_per_meter=0.002402834774075819
odom_total_distance=70.16941368925721
selected_goal_unique_count=20
path_length_regret_avg=-0.838739573843837
path_length_regret_max=12.625099437203264
nearest_frontier_ignored_count=2
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8705882352941177
route_tortuosity=5.404433266147319
active_path_endpoint_to_goal_distance_avg=0.10778229035037926
active_path_endpoint_to_goal_distance_max=5.5901699437494745
P2I_route_300s_after_fix_DONE run_id=p2i_route_300s_after_fix_20260622_140158
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_140723_p2i_route_300s_after_fix_summary.md
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
### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140158/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- coverage_proxy_gain: 0.16860550728905904
- coverage_gain_per_meter: 0.002402834774075819
- odom_total_distance: 70.16941368925721
- selected_goal_unique_count: 20
- path_length_regret_avg: -0.838739573843837
- path_length_regret_max: 12.625099437203264
- nearest_frontier_ignored_count: 2
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8705882352941177
- route_tortuosity: 5.404433266147319
- active_path_endpoint_to_goal_distance_avg: 0.10778229035037926
- active_path_endpoint_to_goal_distance_max: 5.5901699437494745
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140158/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.008273601532
- odom_total_distance: 70.16941368925721
- coverage_proxy_start: 0.08511264909438963
- coverage_proxy_end: 0.2537181563834487
- coverage_proxy_gain: 0.16860550728905904
- coverage_gain_per_meter: 0.002402834774075819
- selected_goal_count: 575
- selected_goal_unique_count: 20
- selected_goal_distance_from_odom_avg: 6.338315555769568
- selected_goal_distance_from_odom_max: 10.702588080991376
- selected_goal_path_length_avg: 5.883834810108674
- selected_goal_path_length_max: 19.915050622923605
- selected_goal_path_efficiency_avg: 0.8176299771272502
- frontier_candidate_count_avg: 159.47869674185463
- frontier_viewpoint_count_avg: 21.87
- nearest_frontier_distance_avg: 6.710304317509918
- nearest_frontier_distance_min: 4.951748831225613
- nearest_frontier_ignored_count: 2
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 5.883834810108674
- path_length_to_nearest_candidate_avg: 6.722574383952464
- path_length_regret_avg: -0.838739573843837
- path_length_regret_max: 12.625099437203264
- coverage_gain_after_goal_avg: 0.013140456796534113
- coverage_gain_after_goal_per_meter_avg: 0.01826056961831154
- low_efficiency_goal_count: 0
- local_region_revisit_count: 0
- region_diversity_score: 1.0
- active_path_endpoint_to_goal_distance_avg: 0.10778229035037926
- active_path_endpoint_to_goal_distance_max: 5.5901699437494745
- route_backtracking_distance: 0.020846955664217005
- route_revisit_ratio: 0.8705882352941177
- route_tortuosity: 5.404433266147319
- active_path_update_count: 264
- position_cmd_update_count: 264
- frontier_candidate_count_end: 227
- frontier_viewpoint_count_end: 11
- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- goal_selected_count: 20
- goal_without_path_count: 4
- goal_without_path_ratio: 0.2
- goal_to_path_latency_avg_sec: 1.0158511400222778
- goal_to_path_latency_max_sec: 3.1227684020996094
- goal_to_path_timeout_count: 4
- goal_to_path_timeout_max_duration_sec: 298.7583529949188
- active_goal_without_active_path_max_duration_sec: 298.7583529949188
- active_goal_without_travel_traj_max_duration_sec: 298.7583529949188
- path_missing_after_goal_count: 4
- path_missing_after_goal_max_duration_sec: 298.7583529949188
- path_generation_fail_count: 22
- path_generation_fail_reasons: {'no_collision_free_grid_path': 20, 'goal_too_close': 2}
- goal_to_path_status_events: ['REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=37 wait_sec=5.497 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_WAITING goal_id=37 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=6.908 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=8.226 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=7.908 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=8.003 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=8.904 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=7.787 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=9.927 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=7.567 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=10.562 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.784 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=11.573 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.602 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=12.549 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.440 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=13.566 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.278 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=14.572 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.114 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=15.564 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.956 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=16.562 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.793 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=17.564 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.637 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=18.580 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.485 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=19.542 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.325 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=20.561 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.174 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=21.559 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.016 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=22.554 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=4.868 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=23.555 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=4.713 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_', 'REAL_F
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140158/route_events.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140158/route_events.csv
- file_size_bytes: 22

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140158/route_timeseries.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140158/route_timeseries.csv
- file_size_bytes: 1877

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_140158/route_rationality.json
```json
{
  "active_goal_without_active_path_max_duration_sec": 298.7583529949188,
  "active_goal_without_travel_traj_max_duration_sec": 298.7583529949188,
  "active_path_empty_count": 0,
  "active_path_endpoint_to_goal_distance_avg": 0.10778229035037926,
  "active_path_endpoint_to_goal_distance_max": 5.5901699437494745,
  "active_path_first_update_after_goal_sec": 1.0158511400222778,
  "active_path_update_count": 264,
  "coverage_gain_after_goal_avg": 0.013140456796534113,
  "coverage_gain_after_goal_per_meter_avg": 0.01826056961831154,
  "coverage_gain_per_meter": 0.002402834774075819,
  "coverage_proxy_end": 0.2537181563834487,
  "coverage_proxy_gain": 0.16860550728905904,
  "coverage_proxy_start": 0.08511264909438963,
  "duration_sec": 300.008273601532,
  "frontier_candidate_count_avg": 159.47869674185463,
  "frontier_candidate_count_end": 227,
  "frontier_viewpoint_count_avg": 21.87,
  "frontier_viewpoint_count_end": 11,
  "goal_reselect_due_to_no_path_count": 600,
  "goal_selected_count": 20,
  "goal_to_path_latency_avg_sec": 1.0158511400222778,
  "goal_to_path_latency_max_sec": 3.1227684020996094,
  "goal_to_path_status_events": [
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=37 wait_sec=5.497 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_WAITING goal_id=37 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=6.908 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=8.226 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=7.908 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=8.003 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=8.904 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=7.787 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=9.927 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=7.567 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segment",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=10.562 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.784 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=11.573 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.602 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=12.549 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.440 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=13.566 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.278 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=14.572 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=6.114 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=15.564 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.956 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=16.562 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.793 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=17.564 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.637 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.000 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=18.580 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.485 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=19.542 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.325 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=20.561 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.174 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=21.559 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=5.016 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=22.554 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=4.868 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=23.555 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=4.713 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=37 wait_sec=24.555 GOAL_TO_PATH_REQUEST goal_id=37 goal_key=(11.5, -0.5, 1.2) GOAL_TO_PATH_SUCCESS goal_id=37 path_len=4.557 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=1.250 first_collision_point=NONE collision_"
  ],
  "goal_to_path_timeout_count": 4,
  "goal_to_path_timeout_max_duration_sec": 298.7583529949188,
  "goal_without_path_count": 4,
  "goal_without_path_ratio": 0.2,
  "local_region_revisit_count": 0,
  "low_efficiency_goal_count": 0,
  "main_route_issue": "TRAVEL_TRAJ_MISSING_AFTER_GOAL",
  "near_high_gain_candidate_ignored_count": 0,
  "nearest_frontier_distance_avg": 6.710304317509918,
  "nearest_frontier_distance_min": 4.951748831225613,
  "nearest_frontier_ignored_count": 2,
  "no_path_blacklist_count": 600,
  "odom_total_distance": 70.16941368925721,
  "path_generation_fail_count": 22,
  "path_generation_fail_reasons": {
    "goal_too_close": 2,
    "no_collision_free_grid_path": 20
  },
  "path_length_regret_avg": -0.838739573843837,
  "path_length_regret_max": 12.625099437203264,
  "path_length_to_nearest_candidate_avg": 6.722574383952464,
  "path_length_to_selected_goal_avg": 5.883834810108674,
  "path_missing_after_goal_count": 4,
  "path_missing_after_goal_max_duration_sec": 298.7583529949188,
  "position_cmd_update_count": 264,
  "region_diversity_score": 1.0,
  "route_backtracking_distance": 0.020846955664217005,
  "route_revisit_ratio": 0.8705882352941177,
  "route_tortuosity": 5.404433266147319,
  "selected_goal_count": 575,
  "selected_goal_distance_from_odom_avg": 6.338315555769568,
  "selected_goal_distance_from_odom_max": 10.702588080991376,
  "selected_goal_path_efficiency_avg": 0.8176299771272502,
  "selected_goal_path_length_avg": 5.883834810108674,
  "selected_goal_path_length_max": 19.915050622923605,
  "selected_goal_unique_count": 20,
  "travel_traj_first_update_after_goal_sec": 0.9503097236156464,
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_140156_p2i_route_300s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_140723_p2i_route_300s_after_fix_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
