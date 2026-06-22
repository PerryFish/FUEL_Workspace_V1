#!/usr/bin/env bash
set -euo pipefail
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
exec ./scripts/run_continuous_exploration_benchmark.sh --map office --duration 300
