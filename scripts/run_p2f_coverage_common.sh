#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
MODE="${P2F_MODE:-after_fix}"
DURATION="${P2F_DURATION:-300}"
./scripts/kill_fuel.sh >/dev/null 2>&1 || true
export ROS_DOMAIN_ID=88
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_LOCALHOST_ONLY=1
export FASTDDS_BUILTIN_TRANSPORTS=UDPv4
source scripts/env.sh >/dev/null

mkdir -p reports/p2f_metrics test-log
STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ID="p2f_coverage_${DURATION}s_${MODE}_${STAMP}"
OUT="test-log/${STAMP}_p2f_coverage_${DURATION}s_${MODE}_runtime.txt"
LAUNCH_PID=""
TF_PID=""
cleanup() {
  [ -n "$TF_PID" ] && kill "$TF_PID" 2>/dev/null || true
  [ -n "$LAUNCH_PID" ] && kill "$LAUNCH_PID" 2>/dev/null || true
  wait "$TF_PID" 2>/dev/null || true
  wait "$LAUNCH_PID" 2>/dev/null || true
  ./scripts/kill_fuel.sh >/dev/null 2>&1 || true
}
trap cleanup EXIT

{
  echo "# P2F coverage ${DURATION}s ${MODE}"
  echo "run_id=$RUN_ID"
  date -Is
  env | sort | grep -E 'ROS|RMW|FAST|DDS|FUEL|AMENT|COLCON' || true
} | tee "$OUT"

ros2 launch exploration_manager exploration.launch.py map_name:=office >"$OUT.launch" 2>&1 &
LAUNCH_PID=$!
python3 scripts/publish_rviz_map_tf.py --mode static_anchor >"$OUT.tf" 2>&1 &
TF_PID=$!
sleep 12
timeout 12 ros2 topic list -t --no-daemon --spin-time 5 | tee "$OUT.topic_list" || true
./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --frame map --x 5.0 --y 0.0 --z 1.2 --repeat 8 --rate 2.0 >"$OUT.goal" 2>&1 || true

python3 scripts/fuel_coverage_completion_recorder.py \
  --duration "$DURATION" \
  --run-id "$RUN_ID" \
  --output-root reports/p2f_metrics \
  --progress-interval 30 | tee "$OUT.recorder"
REC=${PIPESTATUS[0]}
python3 scripts/analyze_coverage_stall_and_goal_reselect.py --metrics-dir "reports/p2f_metrics/$RUN_ID" | tee "$OUT.analysis" || true
echo "P2F_COVERAGE_${DURATION}S_${MODE}_DONE run_id=$RUN_ID" | tee -a "$OUT"
exit "$REC"
