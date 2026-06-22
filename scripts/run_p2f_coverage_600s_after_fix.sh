#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
P2F_MODE="after_fix" P2F_DURATION="600" ./scripts/run_p2f_coverage_common.sh
