# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T13:11:31+0800
- Task name: p2h_route_300s_baseline
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2h_route_300s_baseline.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_130555_p2h_route_300s_baseline.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131123_p2h_route_300s_baseline_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131128_p2h_route_300s_baseline_full_log.md

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
nuaa         366  1.3  0.0  27276 14072 ?        S    13:11   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2h_route_300s_baseline --command ./scripts/run_p2h_route_300s_baseline.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_130555_p2h_route_300s_baseline.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131123_p2h_route_300s_baseline_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T13:05:55+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2h_route_300s_baseline.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_130555_p2h_route_300s_baseline.md

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
# P2H route rationality run
run_id=p2h_route_300s_baseline_20260622_130557
mode=route_300s_baseline
duration=300
2026-06-22T13:05:57+08:00
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
P2H_ROUTE_PROGRESS time_sec=30.027 coverage_proxy=0.085 odom_total_distance=4.690 coverage_gain_per_meter=0.002 path_length_regret_avg=8.733 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.833 route_tortuosity=1.079 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=60.034 coverage_proxy=0.086 odom_total_distance=11.522 coverage_gain_per_meter=0.001 path_length_regret_avg=6.405 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.893 route_tortuosity=1.770 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=90.036 coverage_proxy=0.093 odom_total_distance=17.722 coverage_gain_per_meter=0.001 path_length_regret_avg=5.074 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.895 route_tortuosity=1.759 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=120.041 coverage_proxy=0.126 odom_total_distance=29.565 coverage_gain_per_meter=0.002 path_length_regret_avg=3.538 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.894 route_tortuosity=3.675 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=150.041 coverage_proxy=0.148 odom_total_distance=41.817 coverage_gain_per_meter=0.002 path_length_regret_avg=2.028 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.881 route_tortuosity=22.414 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=180.067 coverage_proxy=0.163 odom_total_distance=47.295 coverage_gain_per_meter=0.002 path_length_regret_avg=1.568 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.881 route_tortuosity=9.549 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=210.074 coverage_proxy=0.171 odom_total_distance=52.285 coverage_gain_per_meter=0.002 path_length_regret_avg=1.811 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.877 route_tortuosity=8.632 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=240.074 coverage_proxy=0.176 odom_total_distance=57.307 coverage_gain_per_meter=0.002 path_length_regret_avg=1.250 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.884 route_tortuosity=6.173 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=270.075 coverage_proxy=0.176 odom_total_distance=61.325 coverage_gain_per_meter=0.002 path_length_regret_avg=1.096 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.892 route_tortuosity=6.973 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=300.008 coverage_proxy=0.183 odom_total_distance=67.132 coverage_gain_per_meter=0.002 path_length_regret_avg=1.744 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.892 route_tortuosity=6.760 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2h_route_300s_baseline_20260622_130557
duration_sec=300.0134801864624
odom_total_distance=67.13169860621946
coverage_proxy_gain=0.10491827418642322
coverage_gain_per_meter=0.0015628723295361842
selected_goal_unique_count=18
path_length_regret_avg=1.7435592920212972
path_length_regret_max=13.401764770616861
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.891640866873065
route_tortuosity=6.760289541159452
active_path_endpoint_to_goal_distance_avg=0.2514647964215105
main_route_issue=PATH_COST_UNDERWEIGHTED
result=PASS
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=PATH_COST_UNDERWEIGHTED
coverage_proxy_gain=0.10491827418642322
coverage_gain_per_meter=0.0015628723295361842
odom_total_distance=67.13169860621946
selected_goal_unique_count=18
path_length_regret_avg=1.7435592920212972
path_length_regret_max=13.401764770616861
nearest_frontier_ignored_count=7
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.891640866873065
route_tortuosity=6.760289541159452
active_path_endpoint_to_goal_distance_avg=0.2514647964215105
active_path_endpoint_to_goal_distance_max=17.54458605952275
P2H_route_300s_baseline_DONE run_id=p2h_route_300s_baseline_20260622_130557
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131123_p2h_route_300s_baseline_summary.md
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
### reports/p2h_metrics/p2h_route_300s_baseline_20260622_130557/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: PATH_COST_UNDERWEIGHTED
- coverage_proxy_gain: 0.10491827418642322
- coverage_gain_per_meter: 0.0015628723295361842
- odom_total_distance: 67.13169860621946
- selected_goal_unique_count: 18
- path_length_regret_avg: 1.7435592920212972
- path_length_regret_max: 13.401764770616861
- nearest_frontier_ignored_count: 7
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.891640866873065
- route_tortuosity: 6.760289541159452
- active_path_endpoint_to_goal_distance_avg: 0.2514647964215105
- active_path_endpoint_to_goal_distance_max: 17.54458605952275
```

### reports/p2h_metrics/p2h_route_300s_baseline_20260622_130557/route_timeseries.csv
- csv_path: reports/p2h_metrics/p2h_route_300s_baseline_20260622_130557/route_timeseries.csv
- file_size_bytes: 1795

### reports/p2h_metrics/p2h_route_300s_baseline_20260622_130557/route_events.csv
- csv_path: reports/p2h_metrics/p2h_route_300s_baseline_20260622_130557/route_events.csv
- file_size_bytes: 22

### reports/p2h_metrics/p2h_route_300s_baseline_20260622_130557/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.0134801864624
- odom_total_distance: 67.13169860621946
- coverage_proxy_start: 0.07774996318657046
- coverage_proxy_end: 0.18266823737299367
- coverage_proxy_gain: 0.10491827418642322
- coverage_gain_per_meter: 0.0015628723295361842
- selected_goal_count: 479
- selected_goal_unique_count: 18
- selected_goal_distance_from_odom_avg: 7.706821190152947
- selected_goal_distance_from_odom_max: 15.672887465675162
- selected_goal_path_length_avg: 8.560848055244959
- selected_goal_path_length_max: 20.850953965255272
- selected_goal_path_efficiency_avg: 0.7585639469618448
- frontier_candidate_count_avg: 143.08
- frontier_viewpoint_count_avg: 32.63666666666666
- nearest_frontier_distance_avg: 6.879793193042497
- nearest_frontier_distance_min: 5.345440702641841
- nearest_frontier_ignored_count: 7
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 8.560848055244959
- path_length_to_nearest_candidate_avg: 6.8172887632235435
- path_length_regret_avg: 1.7435592920212972
- path_length_regret_max: 13.401764770616861
- coverage_gain_after_goal_avg: 0.010437690022261296
- coverage_gain_after_goal_per_meter_avg: 3.1248630857807753
- low_efficiency_goal_count: 1
- local_region_revisit_count: 3
- region_diversity_score: 0.8333333333333334
- active_path_endpoint_to_goal_distance_avg: 0.2514647964215105
- active_path_endpoint_to_goal_distance_max: 17.54458605952275
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.891640866873065
- route_tortuosity: 6.760289541159452
- active_path_update_count: 258
- position_cmd_update_count: 258
- frontier_candidate_count_end: 183
- frontier_viewpoint_count_end: 24
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_130555_p2h_route_300s_baseline.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131123_p2h_route_300s_baseline_summary.md.
- Matched metrics files: 4.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
