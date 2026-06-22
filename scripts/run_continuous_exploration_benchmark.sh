#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3

MAP_NAME="office"
DURATION="300"
VISUAL=0
HOLD_RVIZ=0
OUTPUT_ROOT="reports/p2b_metrics"
RUN_PREFIX="p2b"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --map) MAP_NAME="$2"; shift 2 ;;
    --duration) DURATION="$2"; shift 2 ;;
    --output-root) OUTPUT_ROOT="$2"; shift 2 ;;
    --run-prefix) RUN_PREFIX="$2"; shift 2 ;;
    --visual) VISUAL=1; shift ;;
    --hold-rviz) HOLD_RVIZ=1; shift ;;
    -h|--help)
      echo "Usage: $0 [--map office] [--duration 300] [--output-root reports/p2b_metrics] [--run-prefix p2b] [--visual] [--hold-rviz]"
      exit 0
      ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

export ROS_DOMAIN_ID="${P2B_ROS_DOMAIN_ID:-88}"
export RMW_IMPLEMENTATION="${P2B_RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${P2B_ROS_LOCALHOST_ONLY:-1}"
export FASTDDS_BUILTIN_TRANSPORTS="${P2B_FASTDDS_BUILTIN_TRANSPORTS:-UDPv4}"
source scripts/env.sh >/dev/null

mkdir -p test-log "$OUTPUT_ROOT"
STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ID="${RUN_PREFIX}_${MAP_NAME}_${DURATION}s_${STAMP}"
OUT="test-log/${STAMP}_${RUN_PREFIX}_${MAP_NAME}_${DURATION}s_runtime.txt"
CONFIG="install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz"
if [ ! -f "$CONFIG" ]; then
  CONFIG="src/FUEL/rviz/fuel_exploration_p2a_fixed_frame.rviz"
fi

LAUNCH_PID=""
TF_PID=""
RVIZ_PID=""
cleanup() {
  if [ "$HOLD_RVIZ" -ne 1 ]; then
    [ -n "$RVIZ_PID" ] && kill "$RVIZ_PID" 2>/dev/null || true
  fi
  [ -n "$TF_PID" ] && kill "$TF_PID" 2>/dev/null || true
  [ -n "$LAUNCH_PID" ] && kill "$LAUNCH_PID" 2>/dev/null || true
  wait "$RVIZ_PID" 2>/dev/null || true
  wait "$TF_PID" 2>/dev/null || true
  wait "$LAUNCH_PID" 2>/dev/null || true
  if [ "$HOLD_RVIZ" -ne 1 ]; then
    ./scripts/kill_fuel.sh >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

./scripts/kill_fuel.sh >/dev/null 2>&1 || true
{
  echo "# P2B continuous exploration benchmark"
  echo "run_id=$RUN_ID"
  echo "map=$MAP_NAME"
  echo "duration=$DURATION"
  date -Is
  env | sort | grep -E 'ROS|RMW|FAST|DDS|FUEL|AMENT|COLCON' || true
} | tee "$OUT"

ros2 launch exploration_manager exploration.launch.py map_name:="$MAP_NAME" >"$OUT.launch" 2>&1 &
LAUNCH_PID=$!
python3 scripts/publish_rviz_map_tf.py --mode static_anchor >"$OUT.tf" 2>&1 &
TF_PID=$!
sleep 10

launch_alive=NO
if kill -0 "$LAUNCH_PID" 2>/dev/null; then launch_alive=YES; fi
echo "launch_process_alive=$launch_alive" | tee -a "$OUT"

if [ "$VISUAL" -eq 1 ]; then
  rviz2 -d "$CONFIG" >"$OUT.rviz" 2>&1 &
  RVIZ_PID=$!
  sleep 5
fi

timeout 12 ros2 topic list -t --no-daemon --spin-time 5 | tee "$OUT.topic_list" || true
./scripts/check_tf_tree.sh >"$OUT.tfcheck" 2>&1 || true

./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --frame map --x 5.0 --y 0.0 --z 1.2 --repeat 8 --rate 2.0 >"$OUT.goal" 2>&1 || true

python3 scripts/fuel_continuous_exploration_recorder.py \
  --duration "$DURATION" \
  --run-id "$RUN_ID" \
  --output-root "$OUTPUT_ROOT" \
  --progress-interval 30 \
  | tee "$OUT.recorder"
RECORDER_STATUS=${PIPESTATUS[0]}

python3 scripts/analyze_p2b_stuck_events.py --metrics-dir "$OUTPUT_ROOT/$RUN_ID" | tee "$OUT.analysis" || true
if [ -f scripts/analyze_goal_lifecycle.py ]; then
  python3 scripts/analyze_goal_lifecycle.py --metrics-dir "$OUTPUT_ROOT/$RUN_ID" | tee "$OUT.goal_lifecycle" || true
fi

if [ "$HOLD_RVIZ" -eq 1 ] && [ "$VISUAL" -eq 1 ]; then
  echo "300s benchmark finished. Press Enter to cleanup, or inspect RViz now." | tee -a "$OUT"
  read -r _ || true
  HOLD_RVIZ=0
fi

if [ "$RECORDER_STATUS" -eq 0 ]; then
  echo "P2B_CONTINUOUS_EXPLORATION_BENCHMARK_DONE result=PASS_OR_PARTIAL run_id=$RUN_ID" | tee -a "$OUT"
  exit 0
fi

echo "P2B_CONTINUOUS_EXPLORATION_BENCHMARK_DONE result=FAIL run_id=$RUN_ID" | tee -a "$OUT"
exit "$RECORDER_STATUS"
