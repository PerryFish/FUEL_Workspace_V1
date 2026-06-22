#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_continuous_exploration_benchmark.sh \
  --map office \
  --duration 300 \
  --output-root reports/p2c_metrics \
  --run-prefix p2c_before
