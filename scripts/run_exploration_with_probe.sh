#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-88}"
export ROS_LOCALHOST_ONLY="${ROS_LOCALHOST_ONLY:-1}"
source scripts/env.sh

mkdir -p test-log
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="test-log/${STAMP}_p1_exploration_with_probe.txt"
LAUNCH_PID=""

cleanup() {
  [ -n "$LAUNCH_PID" ] && kill "$LAUNCH_PID" 2>/dev/null || true
  wait "$LAUNCH_PID" 2>/dev/null || true
}
trap cleanup EXIT

timeout 6 ros2 daemon stop >>"$OUT" 2>&1 || true
ros2 launch exploration_manager exploration.launch.py map_name:=office >"$OUT.launch" 2>&1 &
LAUNCH_PID=$!
sleep 15

echo "## BEFORE_GOAL_PROBE" | tee -a "$OUT"
python3 scripts/fuel_topic_probe.py --duration 20 --min-motion 0.05 | tee -a "$OUT.before_probe" || true

echo "## TRIGGER_GOAL" | tee -a "$OUT"
./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --x 5.0 --y 0.0 --z 1.2 --frame map --repeat 8 --rate 2.0 | tee -a "$OUT.goal" || true

echo "## AFTER_GOAL_PROBE" | tee -a "$OUT"
python3 scripts/fuel_topic_probe.py --duration 60 --min-motion 0.2 | tee -a "$OUT.after_probe"
