# FUEL Full Run Log

## 1. Basic Info
- Date: 2026-06-22T13:14:27+0800
- Task name: p2h_colcon_build_after_fix
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Command: ./scripts/build.sh
- Exit code: 0
- Raw log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131312_p2h_colcon_build_after_fix.md
- Summary log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131418_p2h_colcon_build_after_fix_summary.md
- Full log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131424_p2h_colcon_build_after_fix_full_log.md

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
nuaa         811  1.6  0.0  27276 14076 ?        S    13:14   0:00 python3 /home/nuaa/ZHY/FUEL_PLANNER_V3/scripts/generate_full_run_log.py --task-name p2h_colcon_build_after_fix --command ./scripts/build.sh --exit-code 0 --raw-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131312_p2h_colcon_build_after_fix.md --summary-log /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131418_p2h_colcon_build_after_fix_summary.md --workspace /home/nuaa/ZHY/FUEL_PLANNER_V3
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
- Date: 2026-06-22T13:13:12+08:00
- Host: nuaa-dell
- User: nuaa
- Workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Pwd: /home/nuaa/ZHY/FUEL_PLANNER_V3
- Shell: /bin/bash
- Command: ./scripts/build.sh
- Log file: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131312_p2h_colcon_build_after_fix.md

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
[FUEL ENV] FUEL_WS=/home/nuaa/ZHY/FUEL_PLANNER_V3
[FUEL ENV] ROS_DOMAIN_ID=78
[FUEL ENV] RMW_IMPLEMENTATION=rmw_fastrtps_cpp
[FUEL ENV] FASTDDS_BUILTIN_TRANSPORTS=UDPv4
[FUEL ENV] ROS_LOG_DIR=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/ros
[0.438s] WARNING:colcon.colcon_ros.prefix_path.ament:The path '/home/nuaa/ZHY/FUEL_PLANNER_V3/install/exploration_manager' in the environment variable AMENT_PREFIX_PATH doesn't exist
[0.438s] WARNING:colcon.colcon_ros.prefix_path.ament:The path '/home/nuaa/ZHY/FUEL_PLANNER_V3/install/fuel_ros2' in the environment variable AMENT_PREFIX_PATH doesn't exist
[0.438s] WARNING:colcon.colcon_ros.prefix_path.catkin:The path '/home/nuaa/ZHY/FUEL_PLANNER_V3/install/exploration_manager' in the environment variable CMAKE_PREFIX_PATH doesn't exist
[0.438s] WARNING:colcon.colcon_ros.prefix_path.catkin:The path '/home/nuaa/ZHY/FUEL_PLANNER_V3/install/fuel_ros2' in the environment variable CMAKE_PREFIX_PATH doesn't exist
Starting >>> fuel_ros2
--- stderr: fuel_ros2
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp: In member function ‘void fuel_ros2::FuelPlanManagerAdapter::reset()’:
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:75:38: warning: converting to ‘nav_msgs::msg::Path’ {aka ‘nav_msgs::msg::Path_<std::allocator<void> >’} from initializer list would use explicit constructor ‘nav_msgs::msg::Path_<ContainerAllocator>::Path_(rosidl_runtime_cpp::MessageInitialization) [with ContainerAllocator = std::allocator<void>]’
   75 |   contract_ = FuelTrajectoryContract{};
      |                                      ^
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:75:38: note: in C++11 and above a default constructor can be explicit
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:75:38: warning: converting to ‘nav_msgs::msg::Path’ {aka ‘nav_msgs::msg::Path_<std::allocator<void> >’} from initializer list would use explicit constructor ‘nav_msgs::msg::Path_<ContainerAllocator>::Path_(rosidl_runtime_cpp::MessageInitialization) [with ContainerAllocator = std::allocator<void>]’
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:75:38: note: in C++11 and above a default constructor can be explicit
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp: In member function ‘bool fuel_ros2::FuelPlanManagerAdapter::evaluateAndSelectFinalContract()’:
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:112:38: warning: converting to ‘nav_msgs::msg::Path’ {aka ‘nav_msgs::msg::Path_<std::allocator<void> >’} from initializer list would use explicit constructor ‘nav_msgs::msg::Path_<ContainerAllocator>::Path_(rosidl_runtime_cpp::MessageInitialization) [with ContainerAllocator = std::allocator<void>]’
  112 |   contract_ = FuelTrajectoryContract{};
      |                                      ^
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:112:38: note: in C++11 and above a default constructor can be explicit
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:112:38: warning: converting to ‘nav_msgs::msg::Path’ {aka ‘nav_msgs::msg::Path_<std::allocator<void> >’} from initializer list would use explicit constructor ‘nav_msgs::msg::Path_<ContainerAllocator>::Path_(rosidl_runtime_cpp::MessageInitialization) [with ContainerAllocator = std::allocator<void>]’
/home/nuaa/ZHY/FUEL_PLANNER_V3/src/FUEL/src/plan_manager/fuel_plan_manager_adapter.cpp:112:38: note: in C++11 and above a default constructor can be explicit
---
[Processing: fuel_ros2]
[Processing: fuel_ros2]
Finished <<< fuel_ros2 [1min 2s]
Starting >>> exploration_manager
Finished <<< exploration_manager [2.03s]

Summary: 2 packages finished [1min 5s]
  1 package had stderr output: fuel_ros2
```

## Exit Code
0

## Result
PASS

## Next Action
- Continue with the next deployment or verification phase.

## Unified Summary Log

```text
UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131418_p2h_colcon_build_after_fix_summary.md
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
- UNAVAILABLE

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
- Raw log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_131312_p2h_colcon_build_after_fix.md.
- Summary log path: /home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_131418_p2h_colcon_build_after_fix_summary.md.
- Matched metrics files: 0.
- This full log intentionally includes raw output and snapshots so it can be shared as one debugging artifact.
- If ROS nodes/topics are absent here, the command likely finished before this full-log post-snapshot was collected.
- Use metrics JSON content above for run-time evidence when available.

## 14. Next Action
- Use the summary log for high-level status and this full log for detailed debugging evidence.
