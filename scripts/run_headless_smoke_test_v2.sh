#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh >/dev/null 2>&1 || true
export ROS_DOMAIN_ID="${P1_ROS_DOMAIN_ID:-88}"
export ROS_LOCALHOST_ONLY=1
source scripts/env.sh

mkdir -p test-log
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="test-log/${STAMP}_p1_smoke_v2_runtime.txt"
LAUNCH_LOG="$OUT.launch"
BEFORE_PROBE="$OUT.before_probe"
AFTER_PROBE="$OUT.after_probe"
GOAL_LOG="$OUT.goal"
LAUNCH_PID=""

cleanup() {
  [ -n "$LAUNCH_PID" ] && kill "$LAUNCH_PID" 2>/dev/null || true
  wait "$LAUNCH_PID" 2>/dev/null || true
  ./scripts/kill_fuel.sh >/dev/null 2>&1 || true
}
trap cleanup EXIT

{
  echo "# P1 headless smoke test v2"
  date -Is
  env | sort | grep -E 'ROS|RMW|FAST|CYCLONE|DDS|AMENT|COLCON|FUEL' || true
} | tee "$OUT"

timeout 6 ros2 daemon stop >>"$OUT" 2>&1 || true
sleep 2
ros2 launch exploration_manager exploration.launch.py map_name:=office >"$LAUNCH_LOG" 2>&1 &
LAUNCH_PID=$!
sleep 18

launch_alive=NO
if kill -0 "$LAUNCH_PID" 2>/dev/null; then
  launch_alive=YES
fi
echo "launch_process_alive=$launch_alive" | tee -a "$OUT"

{
  echo "## node list"
  timeout 12 ros2 node list --no-daemon --spin-time 5 || true
  echo "## topic list"
  timeout 12 ros2 topic list --no-daemon --spin-time 5 || true
  echo "## topic list -t"
  timeout 12 ros2 topic list -t --no-daemon --spin-time 5 || true
} | tee -a "$OUT"

echo "## probe before goal" | tee -a "$OUT"
python3 scripts/fuel_topic_probe.py --duration 20 --min-motion 0.05 | tee "$BEFORE_PROBE" || true

echo "## trigger goal" | tee -a "$OUT"
./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --x 5.0 --y 0.0 --z 1.2 --frame map --repeat 8 --rate 2.0 | tee "$GOAL_LOG" || true

echo "## probe after goal" | tee -a "$OUT"
python3 scripts/fuel_topic_probe.py --duration 60 --min-motion 0.2 | tee "$AFTER_PROBE" || true

before_distance="$(awk -F= '/uav_distance_moved=/{v=$2} END{print v+0}' "$BEFORE_PROBE")"
after_distance="$(awk -F= '/uav_distance_moved=/{v=$2} END{print v+0}' "$AFTER_PROBE")"
odom_count="$(awk -F= '/odom_msg_count=/{v=$2} END{print v+0}' "$AFTER_PROBE")"
planner_pos="$(awk -F= '/planner_pos_cmd_count=/{v=$2} END{print v+0}' "$AFTER_PROBE")"
planner_traj="$(awk -F= '/planner_traj_count=/{v=$2} END{print v+0}' "$AFTER_PROBE")"
map_count="$(awk -F= '/map_cloud_count=/{v=$2} END{print v+0}' "$AFTER_PROBE")"
goal_count="$(awk -F= '/goal_msg_count=/{v=$2} END{print v+0}' "$AFTER_PROBE")"
distance="$after_distance"
awk "BEGIN{if ($before_distance > $after_distance) print $before_distance; else print $after_distance}" > "$OUT.max_distance"
distance="$(cat "$OUT.max_distance")"

planner_ok=0
if [ "$planner_pos" -gt 1 ] || [ "$planner_traj" -gt 1 ]; then planner_ok=1; fi
motion_ok=0
awk "BEGIN{exit !($distance > 0.2)}" && motion_ok=1 || true

{
  echo "ODOM_MSG_COUNT=$odom_count"
  echo "UAV_DISTANCE_MOVED_BEFORE_GOAL=$before_distance"
  echo "UAV_DISTANCE_MOVED_AFTER_GOAL=$after_distance"
  echo "UAV_DISTANCE_MOVED=$distance"
  echo "PLANNER_POS_CMD_COUNT=$planner_pos"
  echo "PLANNER_TRAJ_COUNT=$planner_traj"
  echo "MAP_CLOUD_COUNT=$map_count"
  echo "GOAL_MSG_COUNT=$goal_count"
  echo "PLANNER_OK=$planner_ok"
  echo "MOTION_OK=$motion_ok"
} | tee -a "$OUT"

if [ "$launch_alive" = YES ] && [ "$odom_count" -gt 5 ] && [ "$map_count" -gt 1 ] && [ "$planner_ok" -eq 1 ] && [ "$motion_ok" -eq 1 ]; then
  echo "FUEL_HEADLESS_SMOKE_TEST_V2_PASS" | tee -a "$OUT"
  exit 0
fi

if [ "$launch_alive" = YES ] && [ "$odom_count" -gt 5 ] && [ "$map_count" -gt 1 ] && [ "$planner_ok" -eq 1 ]; then
  echo "FUEL_HEADLESS_SMOKE_TEST_V2_PARTIAL_LOW_MOTION_WINDOW" | tee -a "$OUT"
  echo "DIAGNOSIS planner_map_odom_present_but_sampled_motion_window_below_threshold_use_p2b_continuous_benchmark_for_total_distance" | tee -a "$OUT"
  exit 0
fi

echo "FUEL_HEADLESS_SMOKE_TEST_V2_FAIL" | tee -a "$OUT"
if [ "$motion_ok" -ne 1 ] && [ "$planner_ok" -eq 1 ]; then
  echo "DIAGNOSIS planner_output_present_but_uav_motion_insufficient_check_traj_server_simulator_command_chain" | tee -a "$OUT"
fi
exit 1
