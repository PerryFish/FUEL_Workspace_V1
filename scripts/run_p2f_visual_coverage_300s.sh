#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh >/dev/null 2>&1 || true
export ROS_DOMAIN_ID=88
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_LOCALHOST_ONLY=1
export FASTDDS_BUILTIN_TRANSPORTS=UDPv4
source scripts/env.sh >/dev/null

mkdir -p reports/p2f_metrics test-log
STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ID="p2f_visual_coverage_300s_${STAMP}"
OUT="test-log/${STAMP}_p2f_visual_coverage_300s_runtime.txt"
CONFIG="install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz"
[ -f "$CONFIG" ] || CONFIG="src/FUEL/rviz/fuel_exploration_p2a_fixed_frame.rviz"
LAUNCH_PID=""
TF_PID=""
RVIZ_PID=""
cleanup() {
  [ -n "$RVIZ_PID" ] && kill "$RVIZ_PID" 2>/dev/null || true
  [ -n "$TF_PID" ] && kill "$TF_PID" 2>/dev/null || true
  [ -n "$LAUNCH_PID" ] && kill "$LAUNCH_PID" 2>/dev/null || true
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
python3 scripts/fuel_coverage_completion_recorder.py --duration 300 --run-id "$RUN_ID" --output-root reports/p2f_metrics --progress-interval 30 | tee "$OUT.recorder"
python3 scripts/analyze_coverage_stall_and_goal_reselect.py --metrics-dir "reports/p2f_metrics/$RUN_ID" | tee "$OUT.analysis" || true
echo "300s P2F visual coverage demo finished. Press Enter to cleanup, or inspect RViz now."
read -r _ || true
