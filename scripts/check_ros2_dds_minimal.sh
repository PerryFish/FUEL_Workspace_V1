#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
source scripts/env.sh

OUT="${1:-test-log/p1_dds_minimal_runtime_$(date +%Y%m%d_%H%M%S).txt}"
mkdir -p "$(dirname "$OUT")"
TALKER_PID=""
LISTENER_PID=""

cleanup() {
  [ -n "$TALKER_PID" ] && kill "$TALKER_PID" 2>/dev/null || true
  [ -n "$LISTENER_PID" ] && kill "$LISTENER_PID" 2>/dev/null || true
  wait "$TALKER_PID" 2>/dev/null || true
  wait "$LISTENER_PID" 2>/dev/null || true
}
trap cleanup EXIT

{
  echo "# DDS minimal test"
  date -Is
  env | sort | grep -E 'ROS|RMW|FAST|CYCLONE|DDS|AMENT|COLCON|FUEL' || true
  echo "demo_nodes_cpp prefix=$(ros2 pkg prefix demo_nodes_cpp 2>/dev/null || true)"
  echo "demo_nodes_py prefix=$(ros2 pkg prefix demo_nodes_py 2>/dev/null || true)"
} | tee "$OUT"

timeout 6 ros2 daemon stop >>"$OUT" 2>&1 || true
sleep 2
timeout 6 ros2 daemon start >>"$OUT" 2>&1 || true
sleep 2
timeout 6 ros2 daemon status >>"$OUT" 2>&1 || true

if ros2 pkg prefix demo_nodes_cpp >/dev/null 2>&1; then
  ros2 run demo_nodes_cpp talker >>"$OUT.talker" 2>&1 &
  TALKER_PID=$!
  ros2 run demo_nodes_cpp listener >>"$OUT.listener" 2>&1 &
  LISTENER_PID=$!
elif ros2 pkg prefix demo_nodes_py >/dev/null 2>&1; then
  ros2 run demo_nodes_py talker >>"$OUT.talker" 2>&1 &
  TALKER_PID=$!
  ros2 run demo_nodes_py listener >>"$OUT.listener" 2>&1 &
  LISTENER_PID=$!
else
  echo "DDS_MINIMAL_TEST_SKIP demo_nodes_cpp_and_demo_nodes_py_not_installed" | tee -a "$OUT"
  exit 0
fi

sleep 5
{
  echo "## node list"
  timeout 10 ros2 node list --no-daemon --spin-time 5 || true
  echo "## topic list"
  timeout 10 ros2 topic list --no-daemon --spin-time 5 || true
  echo "## topic list -t"
  timeout 10 ros2 topic list -t --no-daemon --spin-time 5 || true
  echo "## chatter echo"
} | tee -a "$OUT"

if timeout 10 ros2 topic echo --once /chatter >>"$OUT" 2>&1; then
  echo "DDS_MINIMAL_TEST_PASS" | tee -a "$OUT"
  exit 0
fi

if grep -q "I heard:" "$OUT.listener" 2>/dev/null; then
  echo "DDS_MINIMAL_TEST_PASS listener_received_chatter" | tee -a "$OUT"
  exit 0
fi

echo "DDS_MINIMAL_TEST_FAIL" | tee -a "$OUT"
exit 1
