#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export ROS_DOMAIN_ID="${P2A_ROS_DOMAIN_ID:-88}"
export RMW_IMPLEMENTATION="${P2A_RMW_IMPLEMENTATION:-rmw_fastrtps_cpp}"
export ROS_LOCALHOST_ONLY="${P2A_ROS_LOCALHOST_ONLY:-1}"
export FASTDDS_BUILTIN_TRANSPORTS="${P2A_FASTDDS_BUILTIN_TRANSPORTS:-UDPv4}"
source scripts/env.sh >/dev/null

mkdir -p reports/tf_frames_p2a

echo "# P2A TF tree check"
date -Is
env | sort | grep -E 'ROS|RMW|FAST|CYCLONE|DDS|AMENT|COLCON|FUEL' || true

topic_list="$(timeout 12 ros2 topic list -t --no-daemon --spin-time 5 2>/dev/null || true)"
echo "## selected topics"
echo "$topic_list" | grep -E '/tf|/tf_static|odom|map|visual|marker|cloud|traj|path' || true

tf_topic_exists=NO
tf_static_exists=NO
if echo "$topic_list" | grep -q '^/tf '; then tf_topic_exists=YES; fi
if echo "$topic_list" | grep -q '^/tf_static '; then tf_static_exists=YES; fi

echo "## /tf_static sample"
tf_static_sample="$(timeout 8 ros2 topic echo --once /tf_static --no-daemon --spin-time 5 2>&1 || true)"
echo "$tf_static_sample"
echo "## /tf sample"
timeout 8 ros2 topic echo --once /tf --no-daemon --spin-time 5 || true

map_frame_exists=NO
odom_frame_exists=NO
base_link_frame_exists=NO
anchor_frame_exists=NO

if echo "$tf_static_sample" | grep -q 'frame_id: map'; then
  map_frame_exists=YES
fi
if echo "$tf_static_sample" | grep -q 'child_frame_id: odom'; then
  odom_frame_exists=YES
fi
if echo "$tf_static_sample" | grep -q 'child_frame_id: fuel_rviz_anchor'; then
  anchor_frame_exists=YES
fi

timeout 8 ros2 run tf2_ros tf2_echo map odom >/tmp/p2a_tf_map_odom.txt 2>&1 || true
echo "## tf2_echo map odom"
cat /tmp/p2a_tf_map_odom.txt || true
if grep -q 'Translation:' /tmp/p2a_tf_map_odom.txt && ! grep -q 'Invalid frame ID "map"' /tmp/p2a_tf_map_odom.txt; then
  map_frame_exists=YES
  odom_frame_exists=YES
fi

timeout 8 ros2 run tf2_ros tf2_echo map base_link >/tmp/p2a_tf_map_base_link.txt 2>&1 || true
echo "## tf2_echo map base_link"
cat /tmp/p2a_tf_map_base_link.txt || true
if grep -q 'Translation:' /tmp/p2a_tf_map_base_link.txt && ! grep -q 'Invalid frame ID "map"' /tmp/p2a_tf_map_base_link.txt && ! grep -q 'Invalid frame ID "base_link"' /tmp/p2a_tf_map_base_link.txt; then
  map_frame_exists=YES
  base_link_frame_exists=YES
fi

timeout 8 ros2 run tf2_ros tf2_echo map fuel_rviz_anchor >/tmp/p2a_tf_map_anchor.txt 2>&1 || true
echo "## tf2_echo map fuel_rviz_anchor"
cat /tmp/p2a_tf_map_anchor.txt || true
if grep -q 'Translation:' /tmp/p2a_tf_map_anchor.txt && ! grep -q 'Invalid frame ID "map"' /tmp/p2a_tf_map_anchor.txt && ! grep -q 'Invalid frame ID "fuel_rviz_anchor"' /tmp/p2a_tf_map_anchor.txt; then
  map_frame_exists=YES
  anchor_frame_exists=YES
fi

if command -v ros2 >/dev/null 2>&1 && ros2 pkg list 2>/dev/null | grep -qx tf2_tools; then
  (
    cd reports/tf_frames_p2a
    timeout 15 ros2 run tf2_tools view_frames >/tmp/p2a_view_frames.txt 2>&1 || true
    cp /tmp/p2a_view_frames.txt view_frames_output_$(date +%Y%m%d_%H%M%S).txt || true
  )
else
  echo "TF2_TOOLS_NOT_AVAILABLE"
fi

rviz_ready=NO
if [ "$map_frame_exists" = YES ]; then rviz_ready=YES; fi

echo "TF_TOPIC_EXISTS=$tf_topic_exists"
echo "TF_STATIC_EXISTS=$tf_static_exists"
echo "MAP_FRAME_EXISTS=$map_frame_exists"
echo "ODOM_FRAME_EXISTS=$odom_frame_exists"
echo "BASE_LINK_FRAME_EXISTS=$base_link_frame_exists"
echo "FUEL_RVIZ_ANCHOR_FRAME_EXISTS=$anchor_frame_exists"
echo "RVIZ_FIXED_FRAME_READY=$rviz_ready"

if [ "$rviz_ready" = YES ]; then
  echo "P2A_TF_TREE_CHECK_PASS"
  exit 0
fi

echo "P2A_TF_TREE_CHECK_FAIL"
exit 1
