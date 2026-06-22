#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
DURATION="0"
if [ "${1:-}" = "--duration" ]; then
  DURATION="${2:-0}"
fi

if [ "$DURATION" = "0" ]; then
  P2I_MODE="route_full" P2I_DURATION=0 ./scripts/run_p2i_route_common.sh
else
  P2I_MODE="route_full_${DURATION}s" P2I_DURATION="$DURATION" ./scripts/run_p2i_route_common.sh
fi
