#!/usr/bin/env bash
set -e

export FUEL_WS=/home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-78}"
export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY:-0}"
export FASTDDS_BUILTIN_TRANSPORTS="${FASTDDS_BUILTIN_TRANSPORTS:-UDPv4}"
export ROS_HOME="$FUEL_WS/.ros"
export ROS_LOG_DIR="$FUEL_WS/test-log/ros"
mkdir -p "$ROS_HOME" "$ROS_LOG_DIR"

unset AMENT_PREFIX_PATH
unset CMAKE_PREFIX_PATH
unset COLCON_PREFIX_PATH

set +u
source /opt/ros/humble/setup.bash
set -u

if [ -f "$FUEL_WS/install/local_setup.bash" ]; then
  set +u
  source "$FUEL_WS/install/local_setup.bash"
  set -u
elif [ -f "$FUEL_WS/install/setup.bash" ]; then
  set +u
  source "$FUEL_WS/install/setup.bash"
  set -u
fi

cd "$FUEL_WS"
echo "[FUEL ENV] FUEL_WS=$FUEL_WS"
echo "[FUEL ENV] ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
echo "[FUEL ENV] RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
echo "[FUEL ENV] FASTDDS_BUILTIN_TRANSPORTS=$FASTDDS_BUILTIN_TRANSPORTS"
echo "[FUEL ENV] ROS_LOG_DIR=$ROS_LOG_DIR"
