# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T12:13:50+0800
- Task name: p2g_coverage_600s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2g_coverage_600s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_120314_p2g_coverage_600s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_121341_p2g_coverage_600s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_121347_p2g_coverage_600s_after_fix_full_log.md

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
nuaa         366  1.6  0.0  27280 14044 ?        S    12:13   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2g_coverage_600s_after_fix --command ./scripts/run_p2g_coverage_600s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_120314_p2g_coverage_600s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_121341_p2g_coverage_600s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T12:03:14+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2g_coverage_600s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_120314_p2g_coverage_600s_after_fix.md

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
run_id=p2g_coverage_600s_after_fix_20260622_120315
mode=coverage_600s_after_fix
duration=600
2026-06-22T12:03:15+08:00
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
P2G_FRONTIER_PROGRESS time_sec=30.014 odom_total_distance=5.284 coverage_proxy=0.093 coverage_gain=0.013 frontier_candidate_count=111 frontier_viewpoint_count=39 selected_goal_unique_count=4 active_path_endpoint_to_goal_distance_avg=0.788 unreachable_goal_ratio=0.238 coverage_stall_max_duration=0.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=60.031 odom_total_distance=12.851 coverage_proxy=0.097 coverage_gain=0.017 frontier_candidate_count=118 frontier_viewpoint_count=37 selected_goal_unique_count=5 active_path_endpoint_to_goal_distance_avg=1.211 unreachable_goal_ratio=0.161 coverage_stall_max_duration=0.000 main_frontier_blocker=FRONTIER_SCORE_PLATEAU
P2G_FRONTIER_PROGRESS time_sec=90.032 odom_total_distance=17.969 coverage_proxy=0.099 coverage_gain=0.019 frontier_candidate_count=120 frontier_viewpoint_count=37 selected_goal_unique_count=6 active_path_endpoint_to_goal_distance_avg=0.908 unreachable_goal_ratio=0.122 coverage_stall_max_duration=30.000 main_frontier_blocker=FRONTIER_SCORE_PLATEAU
P2G_FRONTIER_PROGRESS time_sec=120.033 odom_total_distance=24.428 coverage_proxy=0.109 coverage_gain=0.030 frontier_candidate_count=130 frontier_viewpoint_count=39 selected_goal_unique_count=7 active_path_endpoint_to_goal_distance_avg=0.725 unreachable_goal_ratio=0.087 coverage_stall_max_duration=30.000 main_frontier_blocker=COVERAGE_GROWING
P2G_FRONTIER_PROGRESS time_sec=150.034 odom_total_distance=32.550 coverage_proxy=0.128 coverage_gain=0.048 frontier_candidate_count=142 frontier_viewpoint_count=28 selected_goal_unique_count=8 active_path_endpoint_to_goal_distance_avg=0.559 unreachable_goal_ratio=0.061 coverage_stall_max_duration=30.000 main_frontier_blocker=COVERAGE_GROWING
P2G_FRONTIER_PROGRESS time_sec=180.065 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.125 coverage_stall_max_duration=30.000 main_frontier_blocker=COVERAGE_GROWING
P2G_FRONTIER_PROGRESS time_sec=210.075 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.291 coverage_stall_max_duration=30.000 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=240.092 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.404 coverage_stall_max_duration=30.018 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=270.093 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.486 coverage_stall_max_duration=60.018 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=300.094 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.548 coverage_stall_max_duration=90.019 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=330.095 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.597 coverage_stall_max_duration=120.020 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=360.099 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.636 coverage_stall_max_duration=150.024 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=390.132 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.669 coverage_stall_max_duration=180.057 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=420.165 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.696 coverage_stall_max_duration=210.090 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=450.165 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.719 coverage_stall_max_duration=240.090 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=480.179 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.738 coverage_stall_max_duration=270.104 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=510.192 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.755 coverage_stall_max_duration=300.118 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=540.193 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.770 coverage_stall_max_duration=330.118 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=570.194 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.784 coverage_stall_max_duration=360.120 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_PROGRESS time_sec=600.031 odom_total_distance=41.137 coverage_proxy=0.152 coverage_gain=0.073 frontier_candidate_count=153 frontier_viewpoint_count=26 selected_goal_unique_count=11 active_path_endpoint_to_goal_distance_avg=0.489 unreachable_goal_ratio=0.796 coverage_stall_max_duration=389.957 main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
P2G_FRONTIER_REACHABILITY_RECORDER_RESULT
run_id=p2g_coverage_600s_after_fix_20260622_120315
duration_sec=600.0345666408539
odom_total_distance=41.13663133830588
coverage_proxy_gain=0.07281696362833162
frontier_candidate_count_end=153
frontier_viewpoint_count_end=26
selected_goal_unique_count=11
active_path_endpoint_to_goal_distance_avg=0.4885794815075092
unreachable_goal_ratio=0.7956204379562044
coverage_gain_after_goal_avg=0.015086143425121485
main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
result=PASS
P2G_FRONTIER_SCORING_ANALYSIS_RESULT
main_frontier_blocker=PATH_ENDPOINT_FAR_FROM_GOAL
coverage_proxy_gain=0.07281696362833162
frontier_candidate_count_end=153
frontier_viewpoint_count_end=26
selected_goal_unique_count=11
selected_goal_region_count=11
active_path_endpoint_to_goal_distance_avg=0.4885794815075092
active_path_endpoint_to_goal_distance_max=16.13483237378057
unreachable_goal_ratio=0.7956204379562044
coverage_gain_after_goal_avg=0.015086143425121485
low_gain_goal_count=2
P2G_coverage_600s_after_fix_DONE run_id=p2g_coverage_600s_after_fix_20260622_120315
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_121341_p2g_coverage_600s_after_fix_summary.md
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
### reports/p2g_metrics/p2g_coverage_600s_after_fix_20260622_120315/frontier_scoring_analysis.md
```markdown
# P2G Frontier Scoring And Reachability Analysis

- main_frontier_blocker: PATH_ENDPOINT_FAR_FROM_GOAL
- coverage_proxy_gain: 0.07281696362833162
- frontier_candidate_count_end: 153
- frontier_viewpoint_count_end: 26
- selected_goal_unique_count: 11
- selected_goal_region_count: 11
- active_path_endpoint_to_goal_distance_avg: 0.4885794815075092
- active_path_endpoint_to_goal_distance_max: 16.13483237378057
- unreachable_goal_ratio: 0.7956204379562044
- coverage_gain_after_goal_avg: 0.015086143425121485
- low_gain_goal_count: 2
```

### reports/p2g_metrics/p2g_coverage_600s_after_fix_20260622_120315/frontier_timeseries.csv
- csv_path: reports/p2g_metrics/p2g_coverage_600s_after_fix_20260622_120315/frontier_timeseries.csv
- file_size_bytes: 3605

### reports/p2g_metrics/p2g_coverage_600s_after_fix_20260622_120315/frontier_events.csv
- csv_path: reports/p2g_metrics/p2g_coverage_600s_after_fix_20260622_120315/frontier_events.csv
- file_size_bytes: 15

### reports/p2g_metrics/p2g_coverage_600s_after_fix_20260622_120315/frontier_reachability.json
```json
{
  "active_path_endpoint_to_best_viewpoint_distance_avg": 2.5319603333379823,
  "active_path_endpoint_to_goal_distance_avg": 0.4885794815075092,
  "active_path_endpoint_to_goal_distance_max": 16.13483237378057,
  "active_path_length_avg": 9.629957772353997,
  "active_path_length_max": 19.85931629457415,
  "active_path_update_count": 148,
  "best_viewpoint_count": 599,
  "best_viewpoint_to_odom_distance_avg": 7.169953644660661,
  "best_viewpoint_to_odom_distance_max": 17.004133262346333,
  "best_viewpoint_to_odom_distance_min": 3.439136959695815,
  "best_viewpoint_unique_count": 12,
  "coverage_gain_after_goal_avg": 0.015086143425121485,
  "coverage_gain_after_goal_max": 0.08334560447651303,
  "coverage_gain_after_goal_min": 0.0,
  "coverage_proxy_end": 0.15248122515093507,
  "coverage_proxy_gain": 0.07281696362833162,
  "coverage_proxy_start": 0.07966426152260345,
  "coverage_stall_max_duration_sec": 389.95678782463074,
  "duration_sec": 600.0345666408539,
  "frontier_candidate_count_avg": 144.945,
  "frontier_candidate_count_end": 153,
  "frontier_candidate_count_start": 112,
  "frontier_to_goal_distance_avg": 3.1026414612803648,
  "frontier_to_goal_distance_max": 6.356346523122184,
  "frontier_to_goal_distance_min": 0.4340204421821365,
  "frontier_viewpoint_count_avg": 28.746243739565944,
  "frontier_viewpoint_count_end": 26,
  "frontier_viewpoint_count_start": 44,
  "gain_reject_count": 1198,
  "goal_blacklist_count": 0,
  "low_gain_goal_count": 2,
  "main_frontier_blocker": "PATH_ENDPOINT_FAR_FROM_GOAL",
  "odom_net_displacement": 7.877557997583027,
  "odom_total_distance": 41.13663133830588,
  "reachability_reject_count": 436,
  "recent_region_penalty_count": 0,
  "score_reject_count": 1198,
  "selected_goal_count": 303,
  "selected_goal_region_count": 11,
  "selected_goal_same_region_max_duration_sec": 429.8550066947937,
  "selected_goal_unique_count": 11,
  "unreachable_goal_count": 436,
  "unreachable_goal_ratio": 0.7956204379562044
}
```

### reports/p2g_metrics/p2g_coverage_600s_after_fix_20260622_120315/frontier_reachability.md
```markdown
# P2G Frontier Reachability Metrics

- duration_sec: 600.0345666408539
- odom_total_distance: 41.13663133830588
- odom_net_displacement: 7.877557997583027
- coverage_proxy_start: 0.07966426152260345
- coverage_proxy_end: 0.15248122515093507
- coverage_proxy_gain: 0.07281696362833162
- coverage_stall_max_duration_sec: 389.95678782463074
- frontier_candidate_count_start: 112
- frontier_candidate_count_end: 153
- frontier_candidate_count_avg: 144.945
- frontier_viewpoint_count_start: 44
- frontier_viewpoint_count_end: 26
- frontier_viewpoint_count_avg: 28.746243739565944
- selected_goal_count: 303
- selected_goal_unique_count: 11
- selected_goal_region_count: 11
- selected_goal_same_region_max_duration_sec: 429.8550066947937
- best_viewpoint_count: 599
- best_viewpoint_unique_count: 12
- best_viewpoint_to_odom_distance_avg: 7.169953644660661
- best_viewpoint_to_odom_distance_min: 3.439136959695815
- best_viewpoint_to_odom_distance_max: 17.004133262346333
- active_path_update_count: 148
- active_path_endpoint_to_goal_distance_avg: 0.4885794815075092
- active_path_endpoint_to_goal_distance_max: 16.13483237378057
- active_path_endpoint_to_best_viewpoint_distance_avg: 2.5319603333379823
- active_path_length_avg: 9.629957772353997
- active_path_length_max: 19.85931629457415
- frontier_to_goal_distance_avg: 3.1026414612803648
- frontier_to_goal_distance_min: 0.4340204421821365
- frontier_to_goal_distance_max: 6.356346523122184
- unreachable_goal_count: 436
- unreachable_goal_ratio: 0.7956204379562044
- goal_blacklist_count: 0
- recent_region_penalty_count: 0
- score_reject_count: 1198
- reachability_reject_count: 436
- gain_reject_count: 1198
- coverage_gain_after_goal_avg: 0.015086143425121485
- coverage_gain_after_goal_min: 0.0
- coverage_gain_after_goal_max: 0.08334560447651303
- low_gain_goal_count: 2
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_120314_p2g_coverage_600s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_121341_p2g_coverage_600s_after_fix_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
