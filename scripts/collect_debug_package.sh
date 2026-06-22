#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
STAMP="$(date +%Y%m%d_%H%M%S)"
DEST="reports/debug_package_$STAMP"
mkdir -p "$DEST"
cp -a test-log "$DEST/" 2>/dev/null || true
cp -a reports/*.md "$DEST/" 2>/dev/null || true
ros2 topic list >"$DEST/topic_list.txt" 2>&1 || true
ros2 node list >"$DEST/node_list.txt" 2>&1 || true
tar -czf "reports/debug_package_$STAMP.tar.gz" -C reports "debug_package_$STAMP"
echo "reports/debug_package_$STAMP.tar.gz"
