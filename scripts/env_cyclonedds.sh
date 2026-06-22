#!/usr/bin/env bash
set -e

export FUEL_WS=/home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID=78
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_LOCALHOST_ONLY=1
export ROS_HOME="$FUEL_WS/.ros"
export ROS_LOG_DIR="$FUEL_WS/test-log/ros"
mkdir -p "$ROS_HOME" "$ROS_LOG_DIR"

set +u
source /opt/ros/humble/setup.bash
set -u

if [ -f "$FUEL_WS/install/setup.bash" ]; then
  set +u
  source "$FUEL_WS/install/setup.bash"
  set -u
fi

cd "$FUEL_WS"
echo "[FUEL ENV CYCLONEDDS] FUEL_WS=$FUEL_WS"
echo "[FUEL ENV CYCLONEDDS] ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
echo "[FUEL ENV CYCLONEDDS] RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
echo "[FUEL ENV CYCLONEDDS] ROS_LOCALHOST_ONLY=$ROS_LOCALHOST_ONLY"
