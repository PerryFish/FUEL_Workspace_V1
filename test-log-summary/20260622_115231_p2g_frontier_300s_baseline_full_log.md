# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T11:52:34+0800
- Task name: p2g_frontier_300s_baseline
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2g_frontier_300s_baseline.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_114658_p2g_frontier_300s_baseline.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_115226_p2g_frontier_300s_baseline_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_115231_p2g_frontier_300s_baseline_full_log.md

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
nuaa         366  1.3  0.0  27272 14048 ?        S    11:52   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2g_frontier_300s_baseline --command ./scripts/run_p2g_frontier_300s_baseline.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_114658_p2g_frontier_300s_baseline.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_115226_p2g_frontier_300s_baseline_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T11:46:58+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2g_frontier_300s_baseline.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_114658_p2g_frontier_300s_baseline.md

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
run_id=p2g_frontier_300s_baseline_20260622_114700
mode=frontier_300s_baseline
duration=300
2026-06-22T11:47:00+08:00
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
P2G_FRONTIER_PROGRESS time_sec=30.039 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.933 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=60.039 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.967 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=90.040 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.978 coverage_stall_max_duration=30.001 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=120.042 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.983 coverage_stall_max_duration=60.002 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=150.045 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.987 coverage_stall_max_duration=90.006 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=180.078 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.989 coverage_stall_max_duration=120.039 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=210.079 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.990 coverage_stall_max_duration=150.039 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=240.079 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.992 coverage_stall_max_duration=180.040 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=270.098 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.993 coverage_stall_max_duration=210.059 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=300.012 odom_total_distance=1.405 coverage_proxy=0.086 coverage_gain=0.006 frontier_candidate_count=105 frontier_viewpoint_count=44 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.000 unreachable_goal_ratio=0.993 coverage_stall_max_duration=239.972 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_REACHABILITY_RECORDER_RESULT
run_id=p2g_frontier_300s_baseline_20260622_114700
duration_sec=300.01301169395447
odom_total_distance=1.4051964123804885
coverage_proxy_gain=0.00633190988072449
frontier_candidate_count_end=105
frontier_viewpoint_count_end=44
selected_goal_unique_count=4
active_path_endpoint_to_goal_distance_avg=0.0
unreachable_goal_ratio=0.9933333333333333
coverage_gain_after_goal_avg=0.028640848181416583
main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
result=PARTIAL
P2G_FRONTIER_SCORING_ANALYSIS_RESULT
main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
coverage_proxy_gain=0.00633190988072449
frontier_candidate_count_end=105
frontier_viewpoint_count_end=44
selected_goal_unique_count=4
selected_goal_region_count=4
active_path_endpoint_to_goal_distance_avg=0.0
active_path_endpoint_to_goal_distance_max=0.0
unreachable_goal_ratio=0.9933333333333333
coverage_gain_after_goal_avg=0.028640848181416583
low_gain_goal_count=1
P2G_frontier_300s_baseline_DONE run_id=p2g_frontier_300s_baseline_20260622_114700
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_115226_p2g_frontier_300s_baseline_summary.md
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
### reports/p2g_metrics/p2g_frontier_300s_baseline_20260622_114700/frontier_scoring_analysis.md
```markdown
# P2G Frontier Scoring And Reachability Analysis

- main_frontier_blocker: PATH_ENDPOINT_FAR_FROM_GOAL
- coverage_proxy_gain: 0.00633190988072449
- frontier_candidate_count_end: 105
- frontier_viewpoint_count_end: 44
- selected_goal_unique_count: 4
- selected_goal_region_count: 4
- active_path_endpoint_to_goal_distance_avg: 0.0
- active_path_endpoint_to_goal_distance_max: 0.0
- unreachable_goal_ratio: 0.9933333333333333
- coverage_gain_after_goal_avg: 0.028640848181416583
- low_gain_goal_count: 1
```

### reports/p2g_metrics/p2g_frontier_300s_baseline_20260622_114700/frontier_events.csv
- csv_path: reports/p2g_metrics/p2g_frontier_300s_baseline_20260622_114700/frontier_events.csv
- file_size_bytes: 15

### reports/p2g_metrics/p2g_frontier_300s_baseline_20260622_114700/frontier_timeseries.csv
- csv_path: reports/p2g_metrics/p2g_frontier_300s_baseline_20260622_114700/frontier_timeseries.csv
- file_size_bytes: 1792

### reports/p2g_metrics/p2g_frontier_300s_baseline_20260622_114700/frontier_reachability.json
```json
{
  "active_path_endpoint_to_best_viewpoint_distance_avg": 5.608695107018817,
  "active_path_endpoint_to_goal_distance_avg": 0.0,
  "active_path_endpoint_to_goal_distance_max": 0.0,
  "active_path_length_avg": 0.7636539298137223,
  "active_path_length_max": 0.9960703432352902,
  "active_path_update_count": 2,
  "best_viewpoint_count": 300,
  "best_viewpoint_to_odom_distance_avg": 6.252122352797588,
  "best_viewpoint_to_odom_distance_max": 6.253908587202724,
  "best_viewpoint_to_odom_distance_min": 6.0752851466909705,
  "best_viewpoint_unique_count": 2,
  "coverage_gain_after_goal_avg": 0.028640848181416583,
  "coverage_gain_after_goal_max": 0.08290384332204388,
  "coverage_gain_after_goal_min": 0.0,
  "coverage_proxy_end": 0.08592254454424975,
  "coverage_proxy_gain": 0.00633190988072449,
  "coverage_proxy_start": 0.07959063466352526,
  "coverage_stall_max_duration_sec": 239.972318649292,
  "duration_sec": 300.01301169395447,
  "frontier_candidate_count_avg": 105.0675,
  "frontier_candidate_count_end": 105,
  "frontier_candidate_count_start": 112,
  "frontier_to_goal_distance_avg": 2.409887684902906,
  "frontier_to_goal_distance_max": 6.253908587202724,
  "frontier_to_goal_distance_min": 0.49803517161765026,
  "frontier_viewpoint_count_avg": 44.01,
  "frontier_viewpoint_count_end": 44,
  "frontier_viewpoint_count_start": 45,
  "gain_reject_count": 600,
  "goal_blacklist_count": 0,
  "low_gain_goal_count": 1,
  "main_frontier_blocker": "PATH_ENDPOINT_FAR_FROM_GOAL",
  "odom_net_displacement": 1.405196356576871,
  "odom_total_distance": 1.4051964123804885,
  "reachability_reject_count": 298,
  "recent_region_penalty_count": 0,
  "score_reject_count": 600,
  "selected_goal_count": 16,
  "selected_goal_region_count": 4,
  "selected_goal_same_region_max_duration_sec": 293.40965700149536,
  "selected_goal_unique_count": 4,
  "unreachable_goal_count": 298,
  "unreachable_goal_ratio": 0.9933333333333333
}
```

### reports/p2g_metrics/p2g_frontier_300s_baseline_20260622_114700/frontier_reachability.md
```markdown
# P2G Frontier Reachability Metrics

- duration_sec: 300.01301169395447
- odom_total_distance: 1.4051964123804885
- odom_net_displacement: 1.405196356576871
- coverage_proxy_start: 0.07959063466352526
- coverage_proxy_end: 0.08592254454424975
- coverage_proxy_gain: 0.00633190988072449
- coverage_stall_max_duration_sec: 239.972318649292
- frontier_candidate_count_start: 112
- frontier_candidate_count_end: 105
- frontier_candidate_count_avg: 105.0675
- frontier_viewpoint_count_start: 45
- frontier_viewpoint_count_end: 44
- frontier_viewpoint_count_avg: 44.01
- selected_goal_count: 16
- selected_goal_unique_count: 4
- selected_goal_region_count: 4
- selected_goal_same_region_max_duration_sec: 293.40965700149536
- best_viewpoint_count: 300
- best_viewpoint_unique_count: 2
- best_viewpoint_to_odom_distance_avg: 6.252122352797588
- best_viewpoint_to_odom_distance_min: 6.0752851466909705
- best_viewpoint_to_odom_distance_max: 6.253908587202724
- active_path_update_count: 2
- active_path_endpoint_to_goal_distance_avg: 0.0
- active_path_endpoint_to_goal_distance_max: 0.0
- active_path_endpoint_to_best_viewpoint_distance_avg: 5.608695107018817
- active_path_length_avg: 0.7636539298137223
- active_path_length_max: 0.9960703432352902
- frontier_to_goal_distance_avg: 2.409887684902906
- frontier_to_goal_distance_min: 0.49803517161765026
- frontier_to_goal_distance_max: 6.253908587202724
- unreachable_goal_count: 298
- unreachable_goal_ratio: 0.9933333333333333
- goal_blacklist_count: 0
- recent_region_penalty_count: 0
- score_reject_count: 600
- reachability_reject_count: 298
- gain_reject_count: 600
- coverage_gain_after_goal_avg: 0.028640848181416583
- coverage_gain_after_goal_min: 0.0
- coverage_gain_after_goal_max: 0.08290384332204388
- low_gain_goal_count: 1
- main_frontier_blocker: PATH_ENDPOINT_FAR_FROM_GOAL
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_114658_p2g_frontier_300s_baseline.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_115226_p2g_frontier_300s_baseline_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
