#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
P2I_MODE="route_300s_after_fix" P2I_DURATION=300 ./scripts/run_p2i_route_common.sh
