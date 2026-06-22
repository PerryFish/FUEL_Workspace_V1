#!/usr/bin/env bash
set -euo pipefail

PATTERN='exploration_manager|fuel_ros2|fuel_mvp|p11_lite|p10_lite|quadrotor_sim|traj_server|local_sensing|occupancy_grid|frontier_viewpoint|map_pub|fuel_world_cloud|fuel_topic_compat_bridge|fuel_p11_lite_core_exploration|rviz2_fuel|rviz2_p11_lite|ros2 launch exploration_manager|ros2 launch fuel_ros2'
pkill -f "$PATTERN" 2>/dev/null || true
sleep 1
pkill -9 -f "$PATTERN" 2>/dev/null || true
echo "[kill_fuel] requested shutdown for FUEL/RViz processes"
