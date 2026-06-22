#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID="${P2A_ROS_DOMAIN_ID:-88}"
export RMW_IMPLEMENTATION="${P2A_RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${P2A_ROS_LOCALHOST_ONLY:-1}"
export FASTDDS_BUILTIN_TRANSPORTS="${P2A_FASTDDS_BUILTIN_TRANSPORTS:-UDPv4}"
source scripts/env.sh >/dev/null

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="test-log/${STAMP}_p2a_rviz_tf_probe_runtime.txt"
mkdir -p test-log

echo "# P2A RViz TF probe" | tee "$OUT"
./scripts/kill_fuel.sh >/dev/null 2>&1 || true

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

ros2 launch exploration_manager exploration.launch.py map_name:=office >"$OUT.launch" 2>&1 &
LAUNCH_PID=$!
python3 scripts/publish_rviz_map_tf.py --mode static_anchor >"$OUT.tf" 2>&1 &
TF_PID=$!
sleep 12

./scripts/check_tf_tree.sh | tee -a "$OUT"
python3 scripts/fuel_topic_probe.py --duration 12 --min-motion 0.0 | tee "$OUT.probe" || true

echo "P2A_RVIZ_TF_PROBE_DONE" | tee -a "$OUT"
