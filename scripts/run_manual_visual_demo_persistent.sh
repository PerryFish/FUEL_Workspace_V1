#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID="${P2A_ROS_DOMAIN_ID:-88}"
export RMW_IMPLEMENTATION="${P2A_RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${P2A_ROS_LOCALHOST_ONLY:-1}"
export FASTDDS_BUILTIN_TRANSPORTS="${P2A_FASTDDS_BUILTIN_TRANSPORTS:-UDPv4}"
source scripts/env.sh

mkdir -p test-log reports/screenshots
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="test-log/${STAMP}_p2a_manual_visual_demo_runtime.txt"
CONFIG="install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz"
if [ ! -f "$CONFIG" ]; then
  CONFIG="src/FUEL/rviz/fuel_exploration_p2a_fixed_frame.rviz"
fi

echo "# P2A manual visual persistent demo" | tee "$OUT"
./scripts/kill_fuel.sh >/dev/null 2>&1 || true

LAUNCH_PID=""
TF_PID=""
RVIZ_PID=""
PROBE_PID=""
cleanup() {
  echo "## cleanup snapshot" | tee -a "$OUT"
  timeout 8 ros2 topic list -t --no-daemon --spin-time 4 >>"$OUT" 2>&1 || true
  ./scripts/check_tf_tree.sh >>"$OUT" 2>&1 || true
  [ -n "$PROBE_PID" ] && kill "$PROBE_PID" 2>/dev/null || true
  [ -n "$RVIZ_PID" ] && kill "$RVIZ_PID" 2>/dev/null || true
  [ -n "$TF_PID" ] && kill "$TF_PID" 2>/dev/null || true
  [ -n "$LAUNCH_PID" ] && kill "$LAUNCH_PID" 2>/dev/null || true
  wait "$PROBE_PID" 2>/dev/null || true
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

./scripts/check_tf_tree.sh | tee -a "$OUT" || true

rviz2 -d "$CONFIG" >"$OUT.rviz" 2>&1 &
RVIZ_PID=$!
sleep 4

./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --frame map --x 5.0 --y 0.0 --z 1.2 --repeat 8 --rate 2.0 >"$OUT.goal" 2>&1 || true
python3 scripts/fuel_topic_probe.py --duration 3600 --min-motion 0.0 >"$OUT.probe" 2>&1 &
PROBE_PID=$!

cat <<'MSG' | tee -a "$OUT"
MANUAL_VISUAL_DEMO_RUNNING
请在 RViz 中检查：
1. 是否不再出现 Frame [map] does not exist
2. 是否看到地图点云/障碍物
3. 是否看到 UAV marker
4. 是否看到轨迹
5. 是否看到 frontier/path/goal markers
确认完成后，在本终端按 Enter 清理退出。
MSG

read -r _ || true
echo "FUEL_MANUAL_VISUAL_DEMO_PERSISTENT_DONE" | tee -a "$OUT"
