#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID="${P2A_ROS_DOMAIN_ID:-88}"
export RMW_IMPLEMENTATION="${P2A_RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${P2A_ROS_LOCALHOST_ONLY:-1}"
export FASTDDS_BUILTIN_TRANSPORTS="${P2A_FASTDDS_BUILTIN_TRANSPORTS:-UDPv4}"
source scripts/env.sh

CONFIG="${1:-install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz}"
if [ ! -f "$CONFIG" ]; then
  CONFIG="src/FUEL/rviz/fuel_exploration_p2a_fixed_frame.rviz"
fi

echo "RVIZ_ENV_READY"
echo "ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
echo "RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
echo "ROS_LOCALHOST_ONLY=$ROS_LOCALHOST_ONLY"
echo "CONFIG=$CONFIG"
exec rviz2 -d "$CONFIG"
