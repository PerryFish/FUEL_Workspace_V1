#!/usr/bin/env bash
set -euo pipefail
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
source scripts/env.sh
exec ros2 launch exploration_manager rviz.launch.py
