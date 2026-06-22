#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh >/dev/null 2>&1 || true
export ROS_DOMAIN_ID=88
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_LOCALHOST_ONLY=1
export FASTDDS_BUILTIN_TRANSPORTS=UDPv4
source scripts/env.sh >/dev/null
mkdir -p reports/p2i_metrics test-log
STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ID="p2i_visual_route_full_${STAMP}"
OUT="test-log/${STAMP}_p2i_visual_route_full_runtime.txt"
CONFIG="install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz"
[ -f "$CONFIG" ] || CONFIG="src/FUEL/rviz/fuel_exploration_p2a_fixed_frame.rviz"
LAUNCH_PID=""; TF_PID=""; RVIZ_PID=""; REC_PID=""
RVIZ_CRASHED="NO"; RVIZ_EXIT_CODE="0"
cleanup() {
  [ -n "$REC_PID" ] && kill -INT "$REC_PID" 2>/dev/null || true
  [ -n "$RVIZ_PID" ] && kill "$RVIZ_PID" 2>/dev/null || true
  [ -n "$TF_PID" ] && kill "$TF_PID" 2>/dev/null || true
  [ -n "$LAUNCH_PID" ] && kill "$LAUNCH_PID" 2>/dev/null || true
  wait "$REC_PID" 2>/dev/null || true
  wait "$RVIZ_PID" 2>/dev/null || true
  wait "$TF_PID" 2>/dev/null || true
  wait "$LAUNCH_PID" 2>/dev/null || true
  ./scripts/kill_fuel.sh >/dev/null 2>&1 || true
}
trap cleanup EXIT

ros2 launch exploration_manager exploration.launch.py map_name:=office >"$OUT.launch" 2>&1 &
LAUNCH_PID=$!
python3 scripts/publish_rviz_map_tf.py --mode static_anchor >"$OUT.tf" 2>&1 &
TF_PID=$!
sleep 12
rviz2 -d "$CONFIG" >"$OUT.rviz" 2>&1 &
RVIZ_PID=$!
./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --frame map --x 5.0 --y 0.0 --z 1.2 --repeat 8 --rate 2.0 >"$OUT.goal" 2>&1 || true
python3 scripts/fuel_route_rationality_recorder.py --duration 0 --run-id "$RUN_ID" --output-root reports/p2i_metrics --progress-interval 30 | tee "$OUT.recorder" &
REC_PID=$!
cat <<'EOF'
P2I_FULL_VISUAL_ROUTE_RUNNING

请在 RViz 中观察：
1. 是否优先探索附近未知区域；
2. 是否有明显绕路；
3. 是否有局部反复；
4. 是否 goal、path、trajectory 一致；
5. 是否覆盖率持续增长。

观察完成后，在本终端按 Enter 清理退出。
EOF
read -r _ || true
if ! kill -0 "$RVIZ_PID" 2>/dev/null; then
  set +e
  wait "$RVIZ_PID"
  RVIZ_EXIT_CODE="$?"
  set -e
  [ "$RVIZ_EXIT_CODE" -ne 0 ] && RVIZ_CRASHED="YES"
fi
kill -INT "$REC_PID" 2>/dev/null || true
wait "$REC_PID" 2>/dev/null || true
python3 scripts/analyze_route_rationality.py --metrics-dir "reports/p2i_metrics/$RUN_ID" | tee "$OUT.analysis" || true
echo "RVIZ_CRASHED=$RVIZ_CRASHED"
echo "RVIZ_EXIT_CODE=$RVIZ_EXIT_CODE"
echo "VISUAL_RESULT=$([ "$RVIZ_CRASHED" = YES ] && echo PARTIAL_WITH_RVIZ_CRASH || echo PASS)"
echo "P2I_visual_route_full_DONE run_id=$RUN_ID"
