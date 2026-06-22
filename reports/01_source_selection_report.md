# 01 Source Selection Report

Attempted source strategy:
- Tried HKUST original repository and PR #89 fetch from `https://github.com/HKUST-Aerial-Robotics/FUEL`.
- Network clone stalled twice and was interrupted; partial directories were backed up under `backup_*`.
- The local original FUEL tree at `/home/nuaa/ZHY/FUEL_PLANNER/upstream/FUEL` was inspected and confirmed to be ROS1/catkin, not directly buildable in ROS2 Humble.

Selected source:
- Copied local ROS2 Humble candidate from `/home/nuaa/ZHY/FUEL_PLANNER_V2/ros2_ws/src/fuel_ros2` to `src/FUEL`.
- Package name: `fuel_ros2`
- Commit: `3b11fc50c0ab8e84f9093f084ce80f4d1af6088d`
- Branch: `master`
- This is not verified as PR #89. It is a local ROS2/ament FUEL-style port already present on the machine.

Changes made:
- Added original PCD maps into `src/FUEL/maps`: `office.pcd`, `office2.pcd`, `office3.pcd`, `pillar.pcd`.
- Added `fuel_topic_compat_bridge.py` to alias actual ROS2-port topics to original FUEL-style topic names.
- Added `fuel_ros2` launch files `exploration.launch.py` and `rviz.launch.py`.
- Added compatibility package `src/exploration_manager` so `ros2 launch exploration_manager exploration.launch.py` and `rviz.launch.py` work.

Rationale:
- The original local FUEL source is ROS1/catkin.
- The network path to fetch PR #89 was not usable during this run.
- The selected local ROS2 source builds under Humble and starts planner/simulation nodes.
