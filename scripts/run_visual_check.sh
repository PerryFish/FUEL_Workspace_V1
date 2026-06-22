#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
source scripts/env.sh
mkdir -p reports/screenshots test-log
OUT="test-log/visual_check_runtime_$(date +%Y%m%d_%H%M%S).txt"
RVIZ_PID=""
EXPL_PID=""

cleanup() {
  [ -n "$RVIZ_PID" ] && kill "$RVIZ_PID" 2>/dev/null || true
  [ -n "$EXPL_PID" ] && kill "$EXPL_PID" 2>/dev/null || true
  ./scripts/kill_fuel.sh >/dev/null 2>&1 || true
}
trap cleanup EXIT

if [ -z "${DISPLAY:-}" ]; then
  echo "DISPLAY_ENVIRONMENT_LIMITATION DISPLAY is empty" | tee -a "$OUT"
  exit 0
fi

./scripts/run_rviz.sh >"$OUT.rviz" 2>&1 &
RVIZ_PID=$!
sleep 8
if kill -0 "$RVIZ_PID" 2>/dev/null; then
  echo "RVIZ_OPENED=YES" | tee -a "$OUT"
else
  echo "RVIZ_OPENED=NO" | tee -a "$OUT"
  echo "DISPLAY_ENVIRONMENT_LIMITATION rviz2 exited early" | tee -a "$OUT"
fi

./scripts/run_exploration.sh office >"$OUT.exploration" 2>&1 &
EXPL_PID=$!
sleep 12
./scripts/trigger_goal.sh | tee -a "$OUT" || true
sleep 25

timeout 18 ros2 topic list --no-daemon --spin-time 8 | sort | tee -a "$OUT" || true
timeout 8 ros2 topic echo --once /map_generator/global_cloud --no-daemon >/dev/null 2>&1 && echo "MAP_VISIBLE=UNKNOWN_TOPIC_DATA_YES" | tee -a "$OUT" || echo "MAP_VISIBLE=UNKNOWN_TOPIC_DATA_NO" | tee -a "$OUT"
timeout 8 ros2 topic echo --once /state_ukf/odom --no-daemon >/dev/null 2>&1 && echo "UAV_ODOM_VISIBLE=UNKNOWN_TOPIC_DATA_YES" | tee -a "$OUT" || echo "UAV_ODOM_VISIBLE=UNKNOWN_TOPIC_DATA_NO" | tee -a "$OUT"
timeout 8 ros2 topic echo --once /planning/travel_traj --no-daemon >/dev/null 2>&1 && echo "TRAJECTORY_VISIBLE=UNKNOWN_TOPIC_DATA_YES" | tee -a "$OUT" || echo "TRAJECTORY_VISIBLE=UNKNOWN_TOPIC_DATA_NO" | tee -a "$OUT"
timeout 8 ros2 topic echo --once /fuel/p11_lite/visual/all_markers --no-daemon >/dev/null 2>&1 && echo "FRONTIER_OR_PLANNING_VIS_VISIBLE=UNKNOWN_TOPIC_DATA_YES" | tee -a "$OUT" || echo "FRONTIER_OR_PLANNING_VIS_VISIBLE=UNKNOWN_TOPIC_DATA_NO" | tee -a "$OUT"
timeout 8 ros2 topic echo --once /pcl_render_node/cloud --no-daemon >/dev/null 2>&1 && echo "FOV_VISIBLE=UNKNOWN_TOPIC_DATA_YES" | tee -a "$OUT" || echo "FOV_VISIBLE=UNKNOWN_TOPIC_DATA_NO" | tee -a "$OUT"

if command -v gnome-screenshot >/dev/null 2>&1; then
  gnome-screenshot -f "reports/screenshots/fuel_visual_check_$(date +%Y%m%d_%H%M%S).png" || true
fi

echo "EXPLORATION_TRIGGERED=YES" | tee -a "$OUT"
echo "UAV_MOVED=UNKNOWN_SEE_HEADLESS_TEST" | tee -a "$OUT"
