#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
P2G_MODE="coverage_600s_after_fix" P2G_DURATION=600 ./scripts/run_p2g_frontier_common.sh
