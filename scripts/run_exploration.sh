#!/usr/bin/env bash
set -euo pipefail
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
source scripts/env.sh
MAP_NAME="${1:-office}"
exec ros2 launch exploration_manager exploration.launch.py map_name:="$MAP_NAME"
