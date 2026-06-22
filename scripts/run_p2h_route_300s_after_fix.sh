#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
P2H_MODE="route_300s_after_fix" P2H_DURATION=300 ./scripts/run_p2h_route_common.sh
