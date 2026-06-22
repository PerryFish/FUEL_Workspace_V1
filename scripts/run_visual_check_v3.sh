#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID="${P2A_ROS_DOMAIN_ID:-88}"
export RMW_IMPLEMENTATION="${P2A_RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${P2A_ROS_LOCALHOST_ONLY:-1}"
export FASTDDS_BUILTIN_TRANSPORTS="${P2A_FASTDDS_BUILTIN_TRANSPORTS:-UDPv4}"
source scripts/env.sh >/dev/null

mkdir -p test-log reports/screenshots
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="test-log/${STAMP}_p2a_visual_check_v3_runtime.txt"
CONFIG="install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz"
if [ ! -f "$CONFIG" ]; then
  CONFIG="src/FUEL/rviz/fuel_exploration_p2a_fixed_frame.rviz"
fi

echo "# P2A visual check v3" | tee "$OUT"
./scripts/kill_fuel.sh >/dev/null 2>&1 || true

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
sleep 15

tf_ok=0
if ./scripts/check_tf_tree.sh | tee "$OUT.tfcheck"; then
  tf_ok=1
fi
cat "$OUT.tfcheck" >> "$OUT"

./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --frame map --x 5.0 --y 0.0 --z 1.2 --repeat 6 --rate 2.0 >"$OUT.goal" 2>&1 || true
python3 scripts/fuel_topic_probe.py --duration 25 --min-motion 0.0 | tee "$OUT.probe" || true

rviz_started=NO
if [ -n "${DISPLAY:-}" ]; then
  rviz2 -d "$CONFIG" >"$OUT.rviz" 2>&1 &
  RVIZ_PID=$!
  sleep 8
  if kill -0 "$RVIZ_PID" 2>/dev/null; then
    rviz_started=YES
  fi
  if grep -Eqi 'Frame \[map\] does not exist|Fixed Frame.*map.*does not exist' "$OUT.rviz" 2>/dev/null; then
    echo "RVIZ_FIXED_FRAME_ERROR=YES" | tee -a "$OUT"
    echo "FUEL_VISUAL_CHECK_V3_FAIL" | tee -a "$OUT"
    exit 1
  fi
else
  echo "DISPLAY_NOT_SET" | tee -a "$OUT"
fi

extract_topic_count() {
  local topic="$1"
  sed -n "s|.*topic=${topic} count=\\([0-9][0-9]*\\).*|\\1|p" "$OUT.probe" | tail -1
}

uav_marker_count="$(extract_topic_count "/fuel/p11_lite/visual/uav_marker")"
all_markers_count="$(extract_topic_count "/fuel/p11_lite/visual/all_markers")"
path_markers_count="$(extract_topic_count "/fuel/p11_lite/visual/path_markers")"
uav_marker_count="${uav_marker_count:-0}"
all_markers_count="${all_markers_count:-0}"
path_markers_count="${path_markers_count:-0}"
map_cloud_count="$(awk -F= '/map_cloud_count=/{v=$2} END{print v+0}' "$OUT.probe")"
planner_traj_count="$(awk -F= '/planner_traj_count=/{v=$2} END{print v+0}' "$OUT.probe")"
odom_msg_count="$(awk -F= '/odom_msg_count=/{v=$2} END{print v+0}' "$OUT.probe")"

{
  echo "RVIZ_STARTED=$rviz_started"
  echo "TF_CHECK_OK=$tf_ok"
  echo "uav_marker_count=$uav_marker_count"
  echo "all_markers_count=$all_markers_count"
  echo "path_markers_count=$path_markers_count"
  echo "map_cloud_count=$map_cloud_count"
  echo "planner_traj_count=$planner_traj_count"
  echo "odom_msg_count=$odom_msg_count"
} | tee -a "$OUT"

if command -v gnome-screenshot >/dev/null 2>&1 && [ "$rviz_started" = YES ]; then
  gnome-screenshot -f "reports/screenshots/p2a_visual_v3_${STAMP}.png" >>"$OUT" 2>&1 || true
fi

if [ "$tf_ok" -eq 1 ] && [ "$uav_marker_count" -gt 0 ] && [ "$all_markers_count" -gt 0 ] && [ "$map_cloud_count" -gt 0 ] && [ "$planner_traj_count" -gt 0 ] && [ "$odom_msg_count" -gt 0 ]; then
  echo "FUEL_VISUAL_CHECK_V3_PASS_DATA_READY_MANUAL_CONFIRM_REQUIRED" | tee -a "$OUT"
  exit 0
fi

echo "FUEL_VISUAL_CHECK_V3_FAIL" | tee -a "$OUT"
exit 1
