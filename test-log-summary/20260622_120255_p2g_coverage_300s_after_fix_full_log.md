# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T12:02:58+0800
- Task name: p2g_coverage_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2g_coverage_300s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_115721_p2g_coverage_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_120249_p2g_coverage_300s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_120255_p2g_coverage_300s_after_fix_full_log.md

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
nuaa         366  1.0  0.0  27276 14120 ?        S    12:02   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2g_coverage_300s_after_fix --command ./scripts/run_p2g_coverage_300s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_115721_p2g_coverage_300s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_120249_p2g_coverage_300s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T11:57:21+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2g_coverage_300s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_115721_p2g_coverage_300s_after_fix.md

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
# P2G frontier/reachability run
run_id=p2g_coverage_300s_after_fix_20260622_115723
mode=coverage_300s_after_fix
duration=300
2026-06-22T11:57:23+08:00
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
P2G_FRONTIER_PROGRESS time_sec=30.028 odom_total_distance=7.835 coverage_proxy=0.122 coverage_gain=0.039 frontier_candidate_count=136 frontier_viewpoint_count=51 selected_goal_unique_count=6 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.393 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=60.029 odom_total_distance=12.881 coverage_proxy=0.136 coverage_gain=0.053 frontier_candidate_count=141 frontier_viewpoint_count=41 selected_goal_unique_count=13 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.440 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=90.031 odom_total_distance=12.881 coverage_proxy=0.136 coverage_gain=0.053 frontier_candidate_count=141 frontier_viewpoint_count=40 selected_goal_unique_count=13 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.500 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=120.067 odom_total_distance=18.330 coverage_proxy=0.150 coverage_gain=0.067 frontier_candidate_count=146 frontier_viewpoint_count=44 selected_goal_unique_count=15 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.452 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=150.097 odom_total_distance=18.332 coverage_proxy=0.150 coverage_gain=0.067 frontier_candidate_count=146 frontier_viewpoint_count=46 selected_goal_unique_count=16 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.518 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=180.098 odom_total_distance=27.496 coverage_proxy=0.164 coverage_gain=0.081 frontier_candidate_count=158 frontier_viewpoint_count=33 selected_goal_unique_count=22 active_path_endpoint_to_goal_distance_avg=0.104 unreachable_goal_ratio=0.425 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=210.138 odom_total_distance=35.993 coverage_proxy=0.164 coverage_gain=0.081 frontier_candidate_count=158 frontier_viewpoint_count=33 selected_goal_unique_count=23 active_path_endpoint_to_goal_distance_avg=0.077 unreachable_goal_ratio=0.374 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=240.149 odom_total_distance=42.330 coverage_proxy=0.169 coverage_gain=0.086 frontier_candidate_count=163 frontier_viewpoint_count=32 selected_goal_unique_count=24 active_path_endpoint_to_goal_distance_avg=0.154 unreachable_goal_ratio=0.336 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=270.164 odom_total_distance=47.418 coverage_proxy=0.179 coverage_gain=0.095 frontier_candidate_count=172 frontier_viewpoint_count=36 selected_goal_unique_count=25 active_path_endpoint_to_goal_distance_avg=0.124 unreachable_goal_ratio=0.296 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=300.027 odom_total_distance=50.235 coverage_proxy=0.185 coverage_gain=0.102 frontier_candidate_count=174 frontier_viewpoint_count=25 selected_goal_unique_count=29 active_path_endpoint_to_goal_distance_avg=0.113 unreachable_goal_ratio=0.320 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_REACHABILITY_RECORDER_RESULT
run_id=p2g_coverage_300s_after_fix_20260622_115723
duration_sec=300.0298957824707
odom_total_distance=50.23462801425659
coverage_proxy_gain=0.10189957296421735
frontier_candidate_count_end=174
frontier_viewpoint_count_end=25
selected_goal_unique_count=29
active_path_endpoint_to_goal_distance_avg=0.11311380216403147
unreachable_goal_ratio=0.31958762886597936
coverage_gain_after_goal_avg=0.006615899194311799
main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
result=PASS
P2G_FRONTIER_SCORING_ANALYSIS_RESULT
main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
coverage_proxy_gain=0.10189957296421735
frontier_candidate_count_end=174
frontier_viewpoint_count_end=25
selected_goal_unique_count=29
selected_goal_region_count=27
active_path_endpoint_to_goal_distance_avg=0.11311380216403147
active_path_endpoint_to_goal_distance_max=5.662097888592178
unreachable_goal_ratio=0.31958762886597936
coverage_gain_after_goal_avg=0.006615899194311799
low_gain_goal_count=17
P2G_coverage_300s_after_fix_DONE run_id=p2g_coverage_300s_after_fix_20260622_115723
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_120249_p2g_coverage_300s_after_fix_summary.md
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
### reports/p2g_metrics/p2g_coverage_300s_after_fix_20260622_115723/frontier_scoring_analysis.md
```markdown
# P2G Frontier Scoring And Reachability Analysis

- main_frontier_blocker: PATH_ENDPOINT_FAR_FROM_GOAL
- coverage_proxy_gain: 0.10189957296421735
- frontier_candidate_count_end: 174
- frontier_viewpoint_count_end: 25
- selected_goal_unique_count: 29
- selected_goal_region_count: 27
- active_path_endpoint_to_goal_distance_avg: 0.11311380216403147
- active_path_endpoint_to_goal_distance_max: 5.662097888592178
- unreachable_goal_ratio: 0.31958762886597936
- coverage_gain_after_goal_avg: 0.006615899194311799
- low_gain_goal_count: 17
```

### reports/p2g_metrics/p2g_coverage_300s_after_fix_20260622_115723/frontier_reachability.md
```markdown
# P2G Frontier Reachability Metrics

- duration_sec: 300.0298957824707
- odom_total_distance: 50.23462801425659
- odom_net_displacement: 9.77610241270359
- coverage_proxy_start: 0.08334560447651303
- coverage_proxy_end: 0.18524517744073038
- coverage_proxy_gain: 0.10189957296421735
- coverage_stall_max_duration_sec: 0.0
- frontier_candidate_count_start: 115
- frontier_candidate_count_end: 174
- frontier_candidate_count_avg: 150.065
- frontier_viewpoint_count_start: 44
- frontier_viewpoint_count_end: 25
- frontier_viewpoint_count_avg: 37.96666666666667
- selected_goal_count: 350
- selected_goal_unique_count: 29
- selected_goal_region_count: 27
- selected_goal_same_region_max_duration_sec: 46.0009970664978
- best_viewpoint_count: 300
- best_viewpoint_unique_count: 17
- best_viewpoint_to_odom_distance_avg: 11.409402480156587
- best_viewpoint_to_odom_distance_min: 1.4142135622049896
- best_viewpoint_to_odom_distance_max: 22.610838109326682
- active_path_update_count: 155
- active_path_endpoint_to_goal_distance_avg: 0.11311380216403147
- active_path_endpoint_to_goal_distance_max: 5.662097888592178
- active_path_endpoint_to_best_viewpoint_distance_avg: 4.763430590072077
- active_path_length_avg: 9.556100406282006
- active_path_length_max: 22.899494936611703
- frontier_to_goal_distance_avg: 7.911916298743158
- frontier_to_goal_distance_min: 7.020135524662949
- frontier_to_goal_distance_max: 17.500000000237854
- unreachable_goal_count: 62
- unreachable_goal_ratio: 0.31958762886597936
- goal_blacklist_count: 0
- recent_region_penalty_count: 0
- score_reject_count: 600
- reachability_reject_count: 62
- gain_reject_count: 600
- coverage_gain_after_goal_avg: 0.006615899194311799
- coverage_gain_after_goal_min: 0.0
- coverage_gain_after_goal_max: 0.09335885731114711
- low_gain_goal_count: 17
- main_frontier_blocker: PATH_ENDPOINT_FAR_FROM_GOAL
```

### reports/p2g_metrics/p2g_coverage_300s_after_fix_20260622_115723/frontier_events.csv
- csv_path: reports/p2g_metrics/p2g_coverage_300s_after_fix_20260622_115723/frontier_events.csv
- file_size_bytes: 15

### reports/p2g_metrics/p2g_coverage_300s_after_fix_20260622_115723/frontier_timeseries.csv
- csv_path: reports/p2g_metrics/p2g_coverage_300s_after_fix_20260622_115723/frontier_timeseries.csv
- file_size_bytes: 1817

### reports/p2g_metrics/p2g_coverage_300s_after_fix_20260622_115723/frontier_reachability.json
```json
{
  "active_path_endpoint_to_best_viewpoint_distance_avg": 4.763430590072077,
  "active_path_endpoint_to_goal_distance_avg": 0.11311380216403147,
  "active_path_endpoint_to_goal_distance_max": 5.662097888592178,
  "active_path_length_avg": 9.556100406282006,
  "active_path_length_max": 22.899494936611703,
  "active_path_update_count": 155,
  "best_viewpoint_count": 300,
  "best_viewpoint_to_odom_distance_avg": 11.409402480156587,
  "best_viewpoint_to_odom_distance_max": 22.610838109326682,
  "best_viewpoint_to_odom_distance_min": 1.4142135622049896,
  "best_viewpoint_unique_count": 17,
  "coverage_gain_after_goal_avg": 0.006615899194311799,
  "coverage_gain_after_goal_max": 0.09335885731114711,
  "coverage_gain_after_goal_min": 0.0,
  "coverage_proxy_end": 0.18524517744073038,
  "coverage_proxy_gain": 0.10189957296421735,
  "coverage_proxy_start": 0.08334560447651303,
  "coverage_stall_max_duration_sec": 0.0,
  "duration_sec": 300.0298957824707,
  "frontier_candidate_count_avg": 150.065,
  "frontier_candidate_count_end": 174,
  "frontier_candidate_count_start": 115,
  "frontier_to_goal_distance_avg": 7.911916298743158,
  "frontier_to_goal_distance_max": 17.500000000237854,
  "frontier_to_goal_distance_min": 7.020135524662949,
  "frontier_viewpoint_count_avg": 37.96666666666667,
  "frontier_viewpoint_count_end": 25,
  "frontier_viewpoint_count_start": 44,
  "gain_reject_count": 600,
  "goal_blacklist_count": 0,
  "low_gain_goal_count": 17,
  "main_frontier_blocker": "PATH_ENDPOINT_FAR_FROM_GOAL",
  "odom_net_displacement": 9.77610241270359,
  "odom_total_distance": 50.23462801425659,
  "reachability_reject_count": 62,
  "recent_region_penalty_count": 0,
  "score_reject_count": 600,
  "selected_goal_count": 350,
  "selected_goal_region_count": 27,
  "selected_goal_same_region_max_duration_sec": 46.0009970664978,
  "selected_goal_unique_count": 29,
  "unreachable_goal_count": 62,
  "unreachable_goal_ratio": 0.31958762886597936
}
```

## 10. Reports Generated
- UNAVAILABLE


## 11. Debug Package
```text
lrwxrwxrwx 1 nuaa nuaa   56 Jun 22 09:23 reports/latest_p2d_debug_package.tar.gz -> FUEL_PLANNER_V3_P2D_DEBUG_PACKAGE_20260622_092321.tar.gz
-rw-rw-r-- 1 nuaa nuaa 783K Jun 22 11:22 reports/latest_p2f_debug_package.tar.gz
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_115721_p2g_coverage_300s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_120249_p2g_coverage_300s_after_fix_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
