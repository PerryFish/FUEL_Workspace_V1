# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T14:29:11+0800
- Task name: p2i_route_300s_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_142335_p2i_route_300s_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142903_p2i_route_300s_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142908_p2i_route_300s_after_fix_full_log.md

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
nuaa         368  1.6  0.0  27336 14128 ?        S    14:29   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2i_route_300s_after_fix --command ./scripts/run_p2i_route_300s_after_fix.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_142335_p2i_route_300s_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142903_p2i_route_300s_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T14:23:35+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/run_p2i_route_300s_after_fix.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_142335_p2i_route_300s_after_fix.md

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
run_id=p2i_route_300s_after_fix_20260622_142337
mode=route_300s_after_fix
duration=300
2026-06-22T14:23:37+08:00
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
P2I_ROUTE_PROGRESS time_sec=30.013 coverage_proxy=0.105 odom_total_distance=7.785 coverage_gain_per_meter=0.003 path_length_regret_avg=-1.107 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.838 route_tortuosity=1.919 main_route_issue=LOCAL_REGION_REVISIT
P2I_ROUTE_PROGRESS time_sec=60.015 coverage_proxy=0.125 odom_total_distance=16.124 coverage_gain_per_meter=0.003 path_length_regret_avg=-2.643 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.844 route_tortuosity=1.791 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=90.030 coverage_proxy=0.130 odom_total_distance=21.517 coverage_gain_per_meter=0.002 path_length_regret_avg=0.264 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.864 route_tortuosity=2.207 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=120.031 coverage_proxy=0.149 odom_total_distance=31.279 coverage_gain_per_meter=0.002 path_length_regret_avg=2.349 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.868 route_tortuosity=1.974 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=150.063 coverage_proxy=0.162 odom_total_distance=37.035 coverage_gain_per_meter=0.002 path_length_regret_avg=2.254 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.866 route_tortuosity=2.317 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=180.088 coverage_proxy=0.191 odom_total_distance=45.986 coverage_gain_per_meter=0.002 path_length_regret_avg=1.746 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.874 route_tortuosity=3.665 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=210.089 coverage_proxy=0.207 odom_total_distance=51.023 coverage_gain_per_meter=0.002 path_length_regret_avg=1.621 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.874 route_tortuosity=3.866 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=240.096 coverage_proxy=0.240 odom_total_distance=61.286 coverage_gain_per_meter=0.003 path_length_regret_avg=1.056 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.878 route_tortuosity=3.806 main_route_issue=GOAL_TO_PATH_TIMEOUT
P2I_ROUTE_PROGRESS time_sec=270.097 coverage_proxy=0.240 odom_total_distance=61.592 coverage_gain_per_meter=0.003 path_length_regret_avg=1.096 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.878 route_tortuosity=3.845 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_PROGRESS time_sec=300.003 coverage_proxy=0.244 odom_total_distance=68.015 coverage_gain_per_meter=0.002 path_length_regret_avg=1.236 near_high_gain_candidate_ignored_count=0 route_revisit_ratio=0.875 route_tortuosity=3.807 main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
P2I_ROUTE_RATIONALITY_RECORDER_RESULT
run_id=p2i_route_300s_after_fix_20260622_142337
duration_sec=300.0061626434326
odom_total_distance=68.01450664985022
coverage_proxy_gain=0.16470328375791488
coverage_gain_per_meter=0.002421590508710653
selected_goal_unique_count=26
path_length_regret_avg=1.2357435889919888
path_length_regret_max=14.947515828242906
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.875
route_tortuosity=3.8074107256276273
active_path_endpoint_to_goal_distance_avg=0.14458642482959477
goal_without_path_count=1
goal_to_path_timeout_count=6
active_goal_without_active_path_max_duration_sec=22.500386238098145
active_goal_without_travel_traj_max_duration_sec=22.500386238098145
uav_idle_due_to_no_path_duration_sec=0.0
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
result=PASS
P2H_ROUTE_RATIONALITY_ANALYSIS_RESULT
main_route_issue=TRAVEL_TRAJ_MISSING_AFTER_GOAL
coverage_proxy_gain=0.16470328375791488
coverage_gain_per_meter=0.002421590508710653
odom_total_distance=68.01450664985022
selected_goal_unique_count=26
path_length_regret_avg=1.2357435889919888
path_length_regret_max=14.947515828242906
nearest_frontier_ignored_count=6
near_high_gain_candidate_ignored_count=0
route_revisit_ratio=0.875
route_tortuosity=3.8074107256276273
active_path_endpoint_to_goal_distance_avg=0.14458642482959477
active_path_endpoint_to_goal_distance_max=7.905694150420948
P2I_route_300s_after_fix_DONE run_id=p2i_route_300s_after_fix_20260622_142337
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142903_p2i_route_300s_after_fix_summary.md
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
### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_142337/route_rationality_analysis.md
```markdown
# P2H Route Rationality Analysis

- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- coverage_proxy_gain: 0.16470328375791488
- coverage_gain_per_meter: 0.002421590508710653
- odom_total_distance: 68.01450664985022
- selected_goal_unique_count: 26
- path_length_regret_avg: 1.2357435889919888
- path_length_regret_max: 14.947515828242906
- nearest_frontier_ignored_count: 6
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.875
- route_tortuosity: 3.8074107256276273
- active_path_endpoint_to_goal_distance_avg: 0.14458642482959477
- active_path_endpoint_to_goal_distance_max: 7.905694150420948
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_142337/route_events.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_142337/route_events.csv
- file_size_bytes: 22

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_142337/route_timeseries.csv
- csv_path: reports/p2i_metrics/p2i_route_300s_after_fix_20260622_142337/route_timeseries.csv
- file_size_bytes: 1779

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_142337/route_rationality.json
```json
{
  "active_goal_without_active_path_max_duration_sec": 22.500386238098145,
  "active_goal_without_travel_traj_max_duration_sec": 22.500386238098145,
  "active_path_empty_count": 0,
  "active_path_endpoint_to_goal_distance_avg": 0.14458642482959477,
  "active_path_endpoint_to_goal_distance_max": 7.905694150420948,
  "active_path_first_update_after_goal_sec": 0.28170188665390017,
  "active_path_update_count": 236,
  "coverage_gain_after_goal_avg": 0.00967751435723752,
  "coverage_gain_after_goal_per_meter_avg": 0.004765415574995506,
  "coverage_gain_per_meter": 0.002421590508710653,
  "coverage_proxy_end": 0.24436754528051832,
  "coverage_proxy_gain": 0.16470328375791488,
  "coverage_proxy_start": 0.07966426152260345,
  "duration_sec": 300.0061626434326,
  "frontier_candidate_count_avg": 179.165,
  "frontier_candidate_count_end": 239,
  "frontier_viewpoint_count_avg": 26.643333333333334,
  "frontier_viewpoint_count_end": 11,
  "goal_reselect_due_to_no_path_count": 0,
  "goal_selected_count": 26,
  "goal_to_path_latency_avg_sec": 0.28170188665390017,
  "goal_to_path_latency_max_sec": 3.0100340843200684,
  "goal_to_path_status_events": [
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=15.669 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=9.043 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=16.580 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=8.816 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=17.246 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=8.589 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=17.852 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=8.424 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=0.898 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=10.143 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segme",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=1.858 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=9.822 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=2.838 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=9.597 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=3.819 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=9.379 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=44 wait_sec=4.601 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_WAITING goal_id=44 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=5.743 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.967 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=6.729 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.787 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=7.734 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.585 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=8.711 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.358 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=9.701 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.115 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=10.418 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=7.272 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=11.417 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=7.082 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=12.403 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.918 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=13.387 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.753 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=14.374 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.597 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision",
    "REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=15.366 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.436 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NONE collision"
  ],
  "goal_to_path_timeout_count": 6,
  "goal_to_path_timeout_max_duration_sec": 22.500386238098145,
  "goal_without_path_count": 1,
  "goal_without_path_ratio": 0.038461538461538464,
  "local_region_revisit_count": 1,
  "low_efficiency_goal_count": 0,
  "main_route_issue": "TRAVEL_TRAJ_MISSING_AFTER_GOAL",
  "near_high_gain_candidate_ignored_count": 0,
  "nearest_frontier_distance_avg": 6.494271399731679,
  "nearest_frontier_distance_min": 3.2989422767232703,
  "nearest_frontier_ignored_count": 6,
  "no_path_blacklist_count": 0,
  "odom_total_distance": 68.01450664985022,
  "path_generation_fail_count": 40,
  "path_generation_fail_reasons": {
    "no_collision_free_grid_path": 40
  },
  "path_length_regret_avg": 1.2357435889919888,
  "path_length_regret_max": 14.947515828242906,
  "path_length_to_nearest_candidate_avg": 6.475059645802511,
  "path_length_to_selected_goal_avg": 7.710803234794538,
  "path_missing_after_goal_count": 6,
  "path_missing_after_goal_max_duration_sec": 22.500386238098145,
  "position_cmd_update_count": 237,
  "region_diversity_score": 0.9615384615384616,
  "route_backtracking_distance": 0.0,
  "route_revisit_ratio": 0.875,
  "route_tortuosity": 3.8074107256276273,
  "selected_goal_count": 460,
  "selected_goal_distance_from_odom_avg": 5.681026660717577,
  "selected_goal_distance_from_odom_max": 13.641817721312387,
  "selected_goal_path_efficiency_avg": 0.8463101627701517,
  "selected_goal_path_length_avg": 7.710803234794538,
  "selected_goal_path_length_max": 22.2175144212722,
  "selected_goal_unique_count": 26,
  "travel_traj_first_update_after_goal_sec": 0.2408139228820801,
  "travel_traj_update_count": 650,
  "uav_idle_due_to_no_path_duration_sec": 0.0
}
```

### reports/p2i_metrics/p2i_route_300s_after_fix_20260622_142337/route_rationality.md
```markdown
# P2H Route Rationality Metrics

- duration_sec: 300.0061626434326
- odom_total_distance: 68.01450664985022
- coverage_proxy_start: 0.07966426152260345
- coverage_proxy_end: 0.24436754528051832
- coverage_proxy_gain: 0.16470328375791488
- coverage_gain_per_meter: 0.002421590508710653
- selected_goal_count: 460
- selected_goal_unique_count: 26
- selected_goal_distance_from_odom_avg: 5.681026660717577
- selected_goal_distance_from_odom_max: 13.641817721312387
- selected_goal_path_length_avg: 7.710803234794538
- selected_goal_path_length_max: 22.2175144212722
- selected_goal_path_efficiency_avg: 0.8463101627701517
- frontier_candidate_count_avg: 179.165
- frontier_viewpoint_count_avg: 26.643333333333334
- nearest_frontier_distance_avg: 6.494271399731679
- nearest_frontier_distance_min: 3.2989422767232703
- nearest_frontier_ignored_count: 6
- near_high_gain_candidate_ignored_count: 0
- path_length_to_selected_goal_avg: 7.710803234794538
- path_length_to_nearest_candidate_avg: 6.475059645802511
- path_length_regret_avg: 1.2357435889919888
- path_length_regret_max: 14.947515828242906
- coverage_gain_after_goal_avg: 0.00967751435723752
- coverage_gain_after_goal_per_meter_avg: 0.004765415574995506
- low_efficiency_goal_count: 0
- local_region_revisit_count: 1
- region_diversity_score: 0.9615384615384616
- active_path_endpoint_to_goal_distance_avg: 0.14458642482959477
- active_path_endpoint_to_goal_distance_max: 7.905694150420948
- route_backtracking_distance: 0.0
- route_revisit_ratio: 0.875
- route_tortuosity: 3.8074107256276273
- active_path_update_count: 236
- position_cmd_update_count: 237
- travel_traj_update_count: 650
- frontier_candidate_count_end: 239
- frontier_viewpoint_count_end: 11
- main_route_issue: TRAVEL_TRAJ_MISSING_AFTER_GOAL
- goal_selected_count: 26
- goal_without_path_count: 1
- goal_without_path_ratio: 0.038461538461538464
- goal_to_path_latency_avg_sec: 0.28170188665390017
- goal_to_path_latency_max_sec: 3.0100340843200684
- goal_to_path_timeout_count: 6
- goal_to_path_timeout_max_duration_sec: 22.500386238098145
- active_goal_without_active_path_max_duration_sec: 22.500386238098145
- active_goal_without_travel_traj_max_duration_sec: 22.500386238098145
- path_missing_after_goal_count: 6
- path_missing_after_goal_max_duration_sec: 22.500386238098145
- path_generation_fail_count: 40
- path_generation_fail_reasons: {'no_collision_free_grid_path': 40}
- goal_to_path_status_events: ['REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=15.669 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=9.043 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=16.580 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=8.816 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=17.246 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=8.589 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=43 wait_sec=17.852 GOAL_TO_PATH_REQUEST goal_id=43 goal_key=(-11.5, 0.9, 1.2) GOAL_TO_PATH_SUCCESS goal_id=43 path_len=8.424 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=0.898 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=10.143 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segme', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=1.858 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=9.822 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=2.838 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=9.597 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=3.819 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=9.379 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_WAITING goal_id=44 wait_sec=4.601 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_WAITING goal_id=44 path_len=0.000 endpoint_dist=-1.000 reason=no_collision_free_grid_path environment_mode=complex path_planner_mode=failed straight_path_collision=true astar_used=true astar_success=false fallback_used=false fallback_success=false final_path_collision_free=false path_collision_free=false min_clearance=0.000 first_collision', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=5.743 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.967 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=6.729 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.787 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=7.734 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.585 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=8.711 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.358 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=9.701 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=8.115 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=astar straight_path_collision=true astar_used=true astar_success=true fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.500 first_collision_point=NONE collision_segmen', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=10.418 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=7.272 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=11.417 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=7.082 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=12.403 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.918 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=13.387 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.753 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.559 first_collision_point=NONE collision', 'REAL_FLIGHT_COMMAND=false status_event=GOAL_TO_PATH_SUCCESS goal_id=44 wait_sec=14.374 GOAL_TO_PATH_REQUEST goal_id=44 goal_key=(-11.5, -1.0, 1.2) GOAL_TO_PATH_SUCCESS goal_id=44 path_len=6.597 endpoint_dist=0.000 reason=none environment_mode=complex path_planner_mode=straight straight_path_collision=false astar_used=false astar_success=false fallback_used=false fallback_success=false final_path_collision_free=true path_collision_free=true min_clearance=0.750 first_collision_point=NON
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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_142335_p2i_route_300s_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_142903_p2i_route_300s_after_fix_summary.md.
- Matched metrics files: 5.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
