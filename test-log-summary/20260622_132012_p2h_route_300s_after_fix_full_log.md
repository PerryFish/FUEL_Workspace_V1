# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T13:20:15+0800
- Task name: p2h_route_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2h_route_300s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131438_p2h_route_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132006_p2h_route_300s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132012_p2h_route_300s_after_fix_full_log.md

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
nuaa         366  1.3  0.0  27276 14156 ?        S    13:20   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2h_route_300s_after_fix --command ./scripts/run_p2h_route_300s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131438_p2h_route_300s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132006_p2h_route_300s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T13:14:38+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2h_route_300s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131438_p2h_route_300s_after_fix.md

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
run_id=p2h_route_300s_after_fix_20260622_131440
mode=route_300s_after_fix
duration=300
2026-06-22T13:14:40+08:00
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
P2H_ROUTE_PROGRESS time_sec=30.028 coverage_proxy=0.104 odom_total_distance=5.607 coverage_gain_per_meter=0.004 path_length_regret_avg=0.065 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.815 route_tortuosity=1.274 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=60.029 coverage_proxy=0.122 odom_total_distance=13.883 coverage_gain_per_meter=0.003 path_length_regret_avg=-1.746 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.851 route_tortuosity=2.090 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=90.035 coverage_proxy=0.128 odom_total_distance=22.999 coverage_gain_per_meter=0.002 path_length_regret_avg=-3.142 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.874 route_tortuosity=2.516 main_route_issue=LOCAL_REGION_REVISIT
P2H_ROUTE_PROGRESS time_sec=120.035 coverage_proxy=0.142 odom_total_distance=30.615 coverage_gain_per_meter=0.002 path_length_regret_avg=-0.970 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.878 route_tortuosity=2.652 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=150.040 coverage_proxy=0.151 odom_total_distance=35.769 coverage_gain_per_meter=0.002 path_length_regret_avg=0.114 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.879 route_tortuosity=2.293 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=180.061 coverage_proxy=0.169 odom_total_distance=44.238 coverage_gain_per_meter=0.002 path_length_regret_avg=-0.162 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.869 route_tortuosity=2.632 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=210.094 coverage_proxy=0.196 odom_total_distance=54.711 coverage_gain_per_meter=0.002 path_length_regret_avg=-0.288 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.875 route_tortuosity=4.569 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=240.095 coverage_proxy=0.233 odom_total_distance=65.037 coverage_gain_per_meter=0.002 path_length_regret_avg=-0.321 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.875 route_tortuosity=4.021 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=270.128 coverage_proxy=0.240 odom_total_distance=70.122 coverage_gain_per_meter=0.002 path_length_regret_avg=-0.278 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.876 route_tortuosity=3.984 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_PROGRESS time_sec=300.027 coverage_proxy=0.242 odom_total_distance=74.239 coverage_gain_per_meter=0.002 path_length_regret_avg=-0.024 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.877 route_tortuosity=3.770 main_route_issue=PATH_COST_UNDERWEIGHTED
P2H_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2h_route_300s_after_fix_20260622_131440
duration_sec=300.03067922592163
odom_total_distance=74.23876774138787
coverage_proxy_gain=0.15903401560889413
coverage_gain_per_meter=0.0021421963274349067
selected_goal_unique_count=31
path_length_regret_avg=-0.024262699831228432
path_length_regret_max=14.88362721314616
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8770949720670391
route_tortuosity=3.770145537369512
active_path_endpoint_to_goal_distance_avg=0.29701837091593164
main_route_issue=PATH_COST_UNDERWEIGHTED
result=PASS
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=PATH_COST_UNDERWEIGHTED
coverage_proxy_gain=0.15903401560889413
coverage_gain_per_meter=0.0021421963274349067
odom_total_distance=74.23876774138787
selected_goal_unique_count=31
path_length_regret_avg=-0.024262699831228432
path_length_regret_max=14.88362721314616
nearest_frontier_ignored_count=4
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.8770949720670391
route_tortuosity=3.770145537369512
active_path_endpoint_to_goal_distance_avg=0.29701837091593164
active_path_endpoint_to_goal_distance_max=7.163274390947201
P2H_route_300s_after_fix_DONE run_id=p2h_route_300s_after_fix_20260622_131440
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132006_p2h_route_300s_after_fix_summary.md
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
### reports/p2h_metrics/p2h_route_300s_after_fix_20260622_131440/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: PATH_COST_UNDERWEIGHTED
- coverage_proxy_gain: 0.15903401560889413
- coverage_gain_per_meter: 0.0021421963274349067
- odom_total_distance: 74.23876774138787
- selected_goal_unique_count: 31
- path_length_regret_avg: -0.024262699831228432
- path_length_regret_max: 14.88362721314616
- nearest_frontier_ignored_count: 4
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.8770949720670391
- route_tortuosity: 3.770145537369512
- active_path_endpoint_to_goal_distance_avg: 0.29701837091593164
- active_path_endpoint_to_goal_distance_max: 7.163274390947201
```

### reports/p2h_metrics/p2h_route_300s_after_fix_20260622_131440/route_events.csv
- csv_path: reports/p2h_metrics/p2h_route_300s_after_fix_20260622_131440/route_events.csv
- file_size_bytes: 22

### reports/p2h_metrics/p2h_route_300s_after_fix_20260622_131440/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.03067922592163
- odom_total_distance: 74.23876774138787
- coverage_proxy_start: 0.08297747018112207
- coverage_proxy_end: 0.2420114857900162
- coverage_proxy_gain: 0.15903401560889413
- coverage_gain_per_meter: 0.0021421963274349067
- selected_goal_count: 457
- selected_goal_unique_count: 31
- selected_goal_distance_from_odom_avg: 5.401164115314492
- selected_goal_distance_from_odom_max: 12.812310010180447
- selected_goal_path_length_avg: 6.5103262111824485
- selected_goal_path_length_max: 22.0928494114064
- selected_goal_path_efficiency_avg: 0.8260781094083928
- frontier_candidate_count_avg: 173.9175
- frontier_viewpoint_count_avg: 28.59
- nearest_frontier_distance_avg: 6.515608647119476
- nearest_frontier_distance_min: 4.706259666582355
- nearest_frontier_ignored_count: 4
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 6.5103262111824485
- path_length_to_nearest_candidate_avg: 6.534588911013634
- path_length_regret_avg: -0.024262699831228432
- path_length_regret_max: 14.88362721314616
- coverage_gain_after_goal_avg: 0.005229961223187553
- coverage_gain_after_goal_per_meter_avg: 0.015710980448988488
- low_efficiency_goal_count: 0
- local_region_revisit_count: 1
- region_diversity_score: 0.967741935483871
- active_path_endpoint_to_goal_distance_avg: 0.29701837091593164
- active_path_endpoint_to_goal_distance_max: 7.163274390947201
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.8770949720670391
- route_tortuosity: 3.770145537369512
- active_path_update_count: 246
- position_cmd_update_count: 246
- frontier_candidate_count_end: 239
- frontier_viewpoint_count_end: 16
- main_route_issue: PATH_COST_UNDERWEIGHTED
```

### reports/p2h_metrics/p2h_route_300s_after_fix_20260622_131440/route_timeseries.csv
- csv_path: reports/p2h_metrics/p2h_route_300s_after_fix_20260622_131440/route_timeseries.csv
- file_size_bytes: 1804

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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131438_p2h_route_300s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_132006_p2h_route_300s_after_fix_summary.md.
- Matched metrics files: 4.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
