#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p test-log reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="test-log/${STAMP}_p1_dds_matrix_runtime.md"

run_combo() {
  local name="$1"
  local rmw="$2"
  local localhost="$3"
  local extra="$4"
  local combo_out="test-log/${STAMP}_p1_dds_${name}.txt"
  {
    echo "## $name"
    echo "- RMW_IMPLEMENTATION=$rmw"
    echo "- ROS_LOCALHOST_ONLY=$localhost"
    echo "- Extra=$extra"
  } >> "$OUT"
  (
    set +u
    source /opt/ros/humble/setup.bash
    [ -f install/setup.bash ] && source install/setup.bash
    set -u
    export FUEL_WS=/home/nuaa/ZHY/FUEL_PLANNER_V3
    export ROS_DOMAIN_ID=78
    export RMW_IMPLEMENTATION="$rmw"
    export ROS_LOCALHOST_ONLY="$localhost"
    export ROS_HOME="$FUEL_WS/.ros"
    export ROS_LOG_DIR="$FUEL_WS/test-log/ros"
    mkdir -p "$ROS_HOME" "$ROS_LOG_DIR"
    unset FASTRTPS_DEFAULT_PROFILES_FILE
    unset FASTDDS_DEFAULT_PROFILES_FILE
    unset CYCLONEDDS_URI
    if [ "$extra" = "fast_udp" ]; then
      export FASTDDS_BUILTIN_TRANSPORTS=UDPv4
    else
      unset FASTDDS_BUILTIN_TRANSPORTS
    fi
    ./scripts/check_ros2_dds_minimal.sh "$combo_out"
  )
  local code=$?
  if grep -q 'DDS_MINIMAL_TEST_PASS' "$combo_out" 2>/dev/null; then
    echo "| $name | $rmw | $localhost | $extra | PASS |" >> "$OUT"
  elif grep -q 'DDS_MINIMAL_TEST_SKIP' "$combo_out" 2>/dev/null; then
    echo "| $name | $rmw | $localhost | $extra | SKIP |" >> "$OUT"
  else
    echo "| $name | $rmw | $localhost | $extra | FAIL |" >> "$OUT"
  fi
  return 0
}

{
  echo "# P1 DDS Matrix Test"
  echo
  echo "| combo | rmw | localhost | extra | result |"
  echo "|---|---|---|---|---|"
} > "$OUT"

run_combo fast_a rmw_fastrtps_cpp 1 none
run_combo fast_b rmw_fastrtps_cpp 0 none
run_combo fast_udp_local rmw_fastrtps_cpp 1 fast_udp
run_combo fast_udp_global rmw_fastrtps_cpp 0 fast_udp

if ros2 pkg list 2>/dev/null | grep -qx rmw_cyclonedds_cpp; then
  run_combo cyclone_c rmw_cyclonedds_cpp 1 none
  run_combo cyclone_d rmw_cyclonedds_cpp 0 none
else
  echo "| cyclone_c | rmw_cyclonedds_cpp | 1 | none | CYCLONEDDS_NOT_AVAILABLE_SUDO_BLOCKED |" >> "$OUT"
  echo "| cyclone_d | rmw_cyclonedds_cpp | 0 | none | CYCLONEDDS_NOT_AVAILABLE_SUDO_BLOCKED |" >> "$OUT"
fi

cat "$OUT"
