#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
P2G_MODE="frontier_300s_baseline" P2G_DURATION=300 ./scripts/run_p2g_frontier_common.sh
