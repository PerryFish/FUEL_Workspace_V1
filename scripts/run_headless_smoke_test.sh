#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
source scripts/env.sh

mkdir -p test-log
OUT="test-log/headless_smoke_runtime_$(date +%Y%m%d_%H%M%S).txt"
LAUNCH_PID=""

cleanup() {
  if [ -n "$LAUNCH_PID" ] && kill -0 "$LAUNCH_PID" 2>/dev/null; then
    kill "$LAUNCH_PID" 2>/dev/null || true
    wait "$LAUNCH_PID" 2>/dev/null || true
  fi
  ./scripts/kill_fuel.sh >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "[smoke] starting exploration" | tee -a "$OUT"
ros2 launch exploration_manager exploration.launch.py map_name:=office >"$OUT.launch" 2>&1 &
LAUNCH_PID=$!
TOPICS=""
for _ in $(seq 1 12); do
  sleep 3
  TOPICS="$(timeout 18 ros2 topic list --no-daemon --spin-time 8 | sort || true)"
  if echo "$TOPICS" | grep -qx "/odom"; then
    break
  fi
done

echo "## NODE LIST" | tee -a "$OUT"
timeout 18 ros2 node list --no-daemon --spin-time 8 | sort | tee -a "$OUT" || true
echo "## TOPIC LIST" | tee -a "$OUT"
echo "$TOPICS" | tee -a "$OUT"

required_topics=(
  /global_cloud
  /map_cloud
  /map_generator/global_cloud
  /pcl_render_node/cloud
  /pcl_render_node/sensor_pose
  /odom
  /state_estimation
  /state_ukf/odom
  /planning/pos_cmd
  /planning/travel_traj
  /fuel/p11_lite/frontier_candidates_raw
  /fuel/p11_lite/explored_grid
  /fuel/p11_lite/visual/all_markers
)

missing=0
for topic in "${required_topics[@]}"; do
  if echo "$TOPICS" | grep -qx "$topic"; then
    echo "TOPIC_PRESENT $topic" | tee -a "$OUT"
  else
    echo "TOPIC_MISSING $topic" | tee -a "$OUT"
    missing=$((missing + 1))
  fi
done

echo "## SAMPLE DATA BEFORE GOAL" | tee -a "$OUT"
timeout 12 ros2 topic echo --once /map_generator/global_cloud >>"$OUT" 2>&1 || true
timeout 12 ros2 topic echo --once /state_ukf/odom >>"$OUT" 2>&1 || true

before="$(timeout 12 ros2 topic echo --once /odom 2>/dev/null | awk '/x:/{print $2; exit}' || true)"
./scripts/trigger_goal.sh | tee -a "$OUT" || true
sleep 35
after="$(timeout 12 ros2 topic echo --once /odom 2>/dev/null | awk '/x:/{print $2; exit}' || true)"

echo "ODOM_X_BEFORE=${before:-NONE}" | tee -a "$OUT"
echo "ODOM_X_AFTER=${after:-NONE}" | tee -a "$OUT"

planner_ok=0
timeout 12 ros2 topic echo --once /planning/pos_cmd >>"$OUT" 2>&1 && planner_ok=1 || true
timeout 12 ros2 topic echo --once /planning/travel_traj >>"$OUT" 2>&1 || true
timeout 12 ros2 topic echo --once /fuel/p11_lite/visual/all_markers >>"$OUT" 2>&1 || true

motion_ok=0
if [ -n "${before:-}" ] && [ -n "${after:-}" ] && [ "$before" != "$after" ]; then
  motion_ok=1
fi

echo "PLANNER_OUTPUT_OK=$planner_ok" | tee -a "$OUT"
echo "UAV_MOTION_OK=$motion_ok" | tee -a "$OUT"
echo "MISSING_TOPIC_COUNT=$missing" | tee -a "$OUT"

if [ "$planner_ok" -eq 1 ] && [ "$motion_ok" -eq 1 ] && [ "$missing" -le 1 ]; then
  echo "FUEL_HEADLESS_SMOKE_TEST_PASS" | tee -a "$OUT"
  exit 0
fi

echo "FUEL_HEADLESS_SMOKE_TEST_FAIL" | tee -a "$OUT"
echo "See $OUT and $OUT.launch" | tee -a "$OUT"
exit 1
