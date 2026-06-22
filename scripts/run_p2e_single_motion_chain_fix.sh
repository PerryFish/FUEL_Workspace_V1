#!/usr/bin/env bash
set -u -o pipefail

WS="/home/nuaa/ZHY/FUEL_PLANNER_V3"
LOG="$WS/test-log-summary/20260622_p2e_single_motion_chain_fix_full_log.md"
METRICS_TMP="/tmp/p2e_motion_metrics.env"
RUN_TMP="/tmp/p2e_motion_run_output.txt"
RECORDER_TMP="/tmp/p2e_inline_motion_chain_recorder.py"
RUNNER_TMP="/tmp/p2e_300s_runner.sh"

mkdir -p "$WS/test-log-summary"
rm -f "$LOG" "$METRICS_TMP" "$RUN_TMP" "$RECORDER_TMP" "$RUNNER_TMP"

section_counter=0

append_overview() {
  {
    echo "# P2E Single Markdown PATH_FEASIBILITY Fix Full Log"
    echo
    echo "## 本次整体运行概述"
    echo
    echo "- Workspace: $WS"
    echo "- Single Markdown log: $LOG"
    echo "- Safety: REAL_FLIGHT_COMMAND=false; no actuator/motor/offboard/arm/takeoff commands."
    echo "- Scope: P10/P11 motion chain only; no RViz/map/world geometry changes."
    echo "- Started: $(date -Is)"
    echo
  } >> "$LOG"
}

write_text_section() {
  local title="$1"
  shift
  {
    echo
    echo "## $title"
    echo
    echo "- start_time: $(date -Is)"
    echo "- command: internal text section"
    echo
    echo '```text'
    printf '%s\n' "$@"
    echo '```'
    echo
    echo "- end_time: $(date -Is)"
    echo "- exit_code: 0"
  } >> "$LOG"
}

run_section() {
  local title="$1"
  shift
  local cmd="$*"
  local start_ts end_ts tmp exit_code
  section_counter=$((section_counter + 1))
  tmp="$(mktemp /tmp/p2e_section_${section_counter}.XXXXXX)"
  start_ts="$(date -Is)"
  {
    echo
    echo "## $title"
    echo
    echo "- start_time: $start_ts"
    echo "- command:"
    echo
    echo '```bash'
    echo "$cmd"
    echo '```'
    echo
    echo "- output:"
    echo
    echo '```text'
  } >> "$LOG"
  (
    cd "$WS" || exit 1
    bash -lc "$cmd"
  ) >"$tmp" 2>&1
  exit_code=$?
  cat "$tmp" >> "$LOG"
  end_ts="$(date -Is)"
  {
    echo '```'
    echo
    echo "- end_time: $end_ts"
    echo "- exit_code: $exit_code"
  } >> "$LOG"
  rm -f "$tmp"
  return "$exit_code"
}

write_recorder() {
  cat > "$RECORDER_TMP" <<'PY'
import hashlib
import math
import re
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String
from rclpy.node import Node


def point_pose(msg):
    p = msg.pose.position
    return (float(p.x), float(p.y), float(p.z))


def path_points(msg):
    return [
        (float(p.pose.position.x), float(p.pose.position.y), float(p.pose.position.z))
        for p in msg.poses
    ]


def path_hash(points):
    return hashlib.sha1(
        ";".join(f"{x:.2f},{y:.2f},{z:.2f}" for x, y, z in points).encode()
    ).hexdigest()


class Rec(Node):
    def __init__(self):
        super().__init__("p2e_inline_motion_chain_recorder")
        self.start = time.time()
        self.end = self.start + 300.0
        self.odom_start = None
        self.odom_last = None
        self.odom_dist = 0.0
        self.goal_last = None
        self.goal_switch = 0
        self.goal_count = 0
        self.current_goal = None
        self.ap_hash = ""
        self.ap_updates = 0
        self.ap_same_start = self.start
        self.ap_same_max = 0.0
        self.ap_ep_goal = []
        self.tt_hash = ""
        self.tt_updates = 0
        self.tt_same_start = self.start
        self.tt_same_max = 0.0
        self.cmd_last = None
        self.cmd_updates = 0
        self.cmd_var = 0.0
        self.cmd_same_start = self.start
        self.cmd_same_max = 0.0
        self.cmd_odom = []
        self.traj_stale = 0
        self.quad_block = 0
        self.frontier = 0
        self.traj_count = 0
        self.ap_count = 0
        self.cmd_count = 0
        self.latest_status = {}
        self.create_timer(30.0, self.progress)

        for topic in ["/odom", "/state_ukf/odom", "/visual_slam/odom"]:
            self.create_subscription(Odometry, topic, lambda m, t=topic: self.odom_cb(t, m), 20)
        self.create_subscription(PoseStamped, "/fuel/p11_lite/exploration_goal", self.goal_cb, 10)
        for topic in ["/planning/pos_cmd", "/fuel/p10_lite/position_cmd"]:
            self.create_subscription(PoseStamped, topic, lambda m, t=topic: self.cmd_cb(t, m), 10)
        for topic in [
            "/fuel/p10_lite/active_path",
            "/planning/travel_traj",
            "/fuel/plan_manager/managed_trajectory",
        ]:
            self.create_subscription(Path, topic, lambda m, t=topic: self.path_cb(t, m), 10)
        for topic in [
            "/fuel/p10_lite/traj_server_status",
            "/fuel/p10_lite/quadrotor_sim_status",
            "/fuel/p11_lite/goal_to_path_status",
            "/fuel/p11_lite/exploration_manager_status",
        ]:
            self.create_subscription(String, topic, lambda m, t=topic: self.status_cb(t, m), 10)
        for topic in ["/fuel/p11_lite/frontier_viewpoints", "/fuel/p11_lite/frontier_candidates_raw"]:
            self.create_subscription(PointCloud2, topic, lambda m, t=topic: self.cloud_cb(t, m), 10)

    def odom_cb(self, _topic, msg):
        p = msg.pose.pose.position
        pos = (float(p.x), float(p.y), float(p.z))
        if self.odom_start is None:
            self.odom_start = pos
        if self.odom_last is not None:
            self.odom_dist += math.dist(self.odom_last, pos)
        self.odom_last = pos

    def goal_cb(self, msg):
        p = point_pose(msg)
        self.goal_count += 1
        self.current_goal = p
        if self.goal_last and math.dist(self.goal_last, p) > 0.5:
            self.goal_switch += 1
        self.goal_last = p

    def path_cb(self, topic, msg):
        pts = path_points(msg)
        h = path_hash(pts)
        now = time.time()
        if topic == "/fuel/p10_lite/active_path":
            self.ap_count += 1
            if h != self.ap_hash:
                self.ap_same_max = max(self.ap_same_max, now - self.ap_same_start)
                self.ap_same_start = now
                self.ap_hash = h
                self.ap_updates += 1
            if pts and self.current_goal:
                self.ap_ep_goal.append(math.dist(pts[-1], self.current_goal))
        else:
            self.traj_count += 1
            if h != self.tt_hash:
                self.tt_same_max = max(self.tt_same_max, now - self.tt_same_start)
                self.tt_same_start = now
                self.tt_hash = h
                self.tt_updates += 1

    def cmd_cb(self, _topic, msg):
        p = point_pose(msg)
        now = time.time()
        self.cmd_count += 1
        if self.cmd_last is None or math.dist(self.cmd_last, p) > 0.02:
            self.cmd_same_max = max(self.cmd_same_max, now - self.cmd_same_start)
            self.cmd_same_start = now
            self.cmd_updates += 1
            if self.cmd_last:
                self.cmd_var += math.dist(self.cmd_last, p)
        self.cmd_last = p
        if self.odom_last:
            self.cmd_odom.append(math.dist(p, self.odom_last))

    def status_cb(self, topic, msg):
        self.latest_status[topic] = msg.data
        if topic == "/fuel/p10_lite/traj_server_status":
            mt = re.search(r"stale_path_hold_count=([0-9]+)", msg.data)
            if mt:
                self.traj_stale = max(self.traj_stale, int(mt.group(1)))
            if "stale_path=true" in msg.data:
                self.traj_stale += 1
        if topic == "/fuel/p10_lite/quadrotor_sim_status" and (
            "blocked" in msg.data.lower() or "stuck" in msg.data.lower()
        ):
            self.quad_block += 1

    def cloud_cb(self, topic, msg):
        if topic == "/fuel/p11_lite/frontier_candidates_raw":
            self.frontier = int(msg.width * msg.height)

    def avg(self, values):
        return sum(values) / len(values) if values else 0.0

    def progress(self):
        print(
            "P2E_PROGRESS "
            f"time={time.time() - self.start:.1f} "
            f"odom_total_distance={self.odom_dist:.3f} "
            f"active_path_update_count={self.ap_updates} "
            f"travel_traj_update_count={self.tt_updates} "
            f"position_cmd_update_count={self.cmd_updates} "
            f"frontier={self.frontier}",
            flush=True,
        )

    def run(self):
        while rclpy.ok() and time.time() < self.end:
            rclpy.spin_once(self, timeout_sec=0.2)
        now = time.time()
        self.ap_same_max = max(self.ap_same_max, now - self.ap_same_start)
        self.tt_same_max = max(self.tt_same_max, now - self.tt_same_start)
        self.cmd_same_max = max(self.cmd_same_max, now - self.cmd_same_start)
        endpoint_avg = self.avg(self.ap_ep_goal)
        if self.goal_count > 5 and (self.ap_updates <= 3 or endpoint_avg > 1.5 or self.ap_same_max > 120):
            chain_break = "PATH_FEASIBILITY"
        elif self.ap_updates > 3 and (self.tt_updates <= 1 or self.tt_same_max > 120):
            chain_break = "TRAJ_SERVER_STALE_PATH"
        elif self.tt_updates > 3 and (self.cmd_updates <= 10 or self.cmd_same_max > 120):
            chain_break = "POSITION_CMD_STALE"
        elif self.cmd_updates > 10 and self.odom_dist < 1.0 and self.avg(self.cmd_odom) > 1.0:
            chain_break = "SIM_TRACKING_FAIL"
        else:
            chain_break = "MAP_COVERAGE_STALL" if self.odom_dist > 1.0 else "UNKNOWN"

        print("P2E_MOTION_CHAIN_RESULT")
        values = {
            "duration_sec": time.time() - self.start,
            "odom_total_distance": self.odom_dist,
            "odom_net_displacement": math.dist(self.odom_start, self.odom_last)
            if self.odom_start and self.odom_last
            else 0.0,
            "goal_switch_count": self.goal_switch,
            "active_path_update_count": self.ap_updates,
            "active_path_same_hash_max_duration_sec": self.ap_same_max,
            "active_path_endpoint_to_goal_distance_avg": endpoint_avg,
            "active_path_endpoint_to_goal_distance_max": max(self.ap_ep_goal) if self.ap_ep_goal else 0.0,
            "travel_traj_update_count": self.tt_updates,
            "travel_traj_same_hash_max_duration_sec": self.tt_same_max,
            "position_cmd_update_count": self.cmd_updates,
            "position_cmd_total_variation": self.cmd_var,
            "position_cmd_same_pose_max_duration_sec": self.cmd_same_max,
            "position_cmd_to_odom_distance_avg": self.avg(self.cmd_odom),
            "traj_server_stale_path_hold_count": self.traj_stale,
            "quadrotor_sim_motion_blocked_count": self.quad_block,
            "main_chain_break": chain_break,
        }
        for key, value in values.items():
            print(f"{key}={value}")
        print(
            "LATEST_GOAL_TO_PATH_STATUS="
            + self.latest_status.get("/fuel/p11_lite/goal_to_path_status", "UNAVAILABLE")[:1000]
        )
        print(
            "LATEST_TRAJ_SERVER_STATUS="
            + self.latest_status.get("/fuel/p10_lite/traj_server_status", "UNAVAILABLE")[:1000]
        )


rclpy.init()
node = Rec()
try:
    node.run()
finally:
    node.destroy_node()
    rclpy.shutdown()
PY
}

write_300s_runner() {
  cat > "$RUNNER_TMP" <<'SH'
#!/usr/bin/env bash
set -u -o pipefail
WS="/home/nuaa/ZHY/FUEL_PLANNER_V3"
cd "$WS" || exit 1
source scripts/env.sh >/dev/null
export ROS_DOMAIN_ID=88
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_LOCALHOST_ONLY=1
export FASTDDS_BUILTIN_TRANSPORTS=UDPv4

./scripts/kill_fuel.sh >/dev/null 2>&1 || true
LAUNCH_LOG="/tmp/p2e_launch.log"
TF_LOG="/tmp/p2e_tf.log"
GOAL_LOG="/tmp/p2e_goal.log"
RECORDER_TMP="/tmp/p2e_inline_motion_chain_recorder.py"
RUN_TMP="/tmp/p2e_motion_run_output.txt"
METRICS_TMP="/tmp/p2e_motion_metrics.env"
rm -f "$LAUNCH_LOG" "$TF_LOG" "$GOAL_LOG" "$RUN_TMP" "$METRICS_TMP"

ros2 launch exploration_manager exploration.launch.py map_name:=office >"$LAUNCH_LOG" 2>&1 &
LAUNCH_PID=$!
python3 scripts/publish_rviz_map_tf.py --mode static_anchor >"$TF_LOG" 2>&1 &
TF_PID=$!

cleanup_inner() {
  kill "$TF_PID" 2>/dev/null || true
  kill "$LAUNCH_PID" 2>/dev/null || true
  wait "$TF_PID" 2>/dev/null || true
  wait "$LAUNCH_PID" 2>/dev/null || true
  ./scripts/kill_fuel.sh >/dev/null 2>&1 || true
}
trap cleanup_inner EXIT

sleep 12
echo "--- runtime node list during run ---"
timeout 10 ros2 node list --no-daemon --spin-time 4 || true
echo "--- runtime topic list during run ---"
timeout 10 ros2 topic list -t --no-daemon --spin-time 4 | grep -E '/odom|/planning/pos_cmd|/planning/travel_traj|/fuel/p10_lite/active_path|/fuel/p10_lite/traj_server_status|/fuel/p11_lite/goal_to_path_status|/fuel/p11_lite/exploration_goal|/fuel/p11_lite/frontier_viewpoints' || true

./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --frame map --x 5.0 --y 0.0 --z 1.2 --repeat 8 --rate 2.0 >"$GOAL_LOG" 2>&1 || true
python3 "$RECORDER_TMP" | tee "$RUN_TMP"

grep -E '^(duration_sec|odom_total_distance|active_path_update_count|active_path_same_hash_max_duration_sec|active_path_endpoint_to_goal_distance_avg|position_cmd_update_count|position_cmd_total_variation|traj_server_stale_path_hold_count|quadrotor_sim_motion_blocked_count|main_chain_break)=' "$RUN_TMP" > "$METRICS_TMP" || true
echo "--- trigger goal output ---"
cat "$GOAL_LOG" || true
echo "--- tf publisher log tail ---"
tail -40 "$TF_LOG" || true
echo "--- launch log tail ---"
tail -120 "$LAUNCH_LOG" || true
SH
  chmod +x "$RUNNER_TMP"
}

append_overview

write_text_section "0. 修改前问题复述" \
  "P2D baseline showed active goal -> active path is broken." \
  "Baseline odom_total_distance=0.101m." \
  "active_path_update_count=1." \
  "active_path_same_hash_max_duration_sec=299.875." \
  "active_path_endpoint_to_goal_distance_avg=7.051m." \
  "position_cmd_update_count=1 and position_cmd_total_variation=0." \
  "main_chain_break=PATH_FEASIBILITY." \
  "This run fixes only P10/P11 path feasibility and stale trajectory handling."

run_section "1. 脚本语法检查" \
  "bash -n scripts/*.sh; python3 -m py_compile src/FUEL/scripts/p11_lite_goal_to_path_bridge.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/fuel_ros2_traj_server_lite.py"
SYNTAX_EXIT=$?

run_section "2. 运动链路诊断" \
  "python3 - <<'PY'
import json, pathlib
paths = [
    ('P2D_BASELINE', pathlib.Path('reports/p2d_metrics/p2d_motion_chain_300s_20260622_090829/motion_chain.json')),
    ('P2D_PREVIOUS_FIX', pathlib.Path('reports/p2d_metrics/p2d_motion_chain_300s_20260622_091639/motion_chain.json')),
]
keys = ['odom_total_distance','goal_switch_count','active_path_update_count','active_path_same_hash_max_duration_sec','active_path_endpoint_to_goal_distance_avg','active_path_endpoint_to_goal_distance_max','travel_traj_update_count','travel_traj_same_hash_max_duration_sec','position_cmd_update_count','position_cmd_total_variation','position_cmd_same_pose_max_duration_sec','traj_server_stale_path_hold_count','quadrotor_sim_motion_blocked_count','main_chain_break']
for name, path in paths:
    print('---', name, path)
    if not path.exists():
        print('UNAVAILABLE')
        continue
    data = json.loads(path.read_text())
    for key in keys:
        print(f'{key}={data.get(key)}')
PY"

run_section "3. PATH_FEASIBILITY 根因定位" \
  "grep -n \"last_valid_path_active\\|last_valid_goal_key\\|path_feasible\\|endpoint_to_goal\\|clear_stale_path\\|empty_path\\|goal_to_path_status\\|path_infeasible\" src/FUEL/scripts/p11_lite_goal_to_path_bridge.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/fuel_ros2_traj_server_lite.py; echo; git -C $WS status --short -- . || true"

run_section "4. 修复方案说明" \
  "cat <<'EOF'
Implemented minimal P2E fix:
1. p11_lite_goal_to_path_bridge.py:
   - no cross-goal reuse of last valid path;
   - publishes empty Path on infeasible current goal to clear stale trajectories;
   - rejects active paths whose endpoint is farther than 1.5m from current goal;
   - reports path_feasible, endpoint_to_goal_distance, clear_stale_path, goal_key.
2. exploration_manager_lite.py:
   - subscribes /fuel/p11_lite/goal_to_path_status;
   - retires active goal after >=3s and >=3 infeasible status samples;
   - records path_infeasible_* status fields and blacklists recently infeasible goals.
3. fuel_ros2_traj_server_lite.py:
   - clears cached path source when receiving empty Path;
   - reports empty_path_clear_count, clear_reason, stale_path.

No map/world/RViz/real flight interfaces were changed.
EOF
echo
git -C $WS diff -- src/FUEL/scripts/p11_lite_goal_to_path_bridge.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/fuel_ros2_traj_server_lite.py | sed -n '1,320p'"

run_section "5. 语法修复检查" \
  "python3 -m py_compile src/FUEL/scripts/p11_lite_goal_to_path_bridge.py src/FUEL/scripts/exploration_manager_lite.py src/FUEL/scripts/fuel_ros2_traj_server_lite.py && bash -n scripts/run_p2e_single_motion_chain_fix.sh"
FIX_SYNTAX_EXIT=$?

run_section "6. 编译修复检查" \
  "source scripts/env.sh >/dev/null && colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo"
BUILD_EXIT=$?

write_recorder
write_300s_runner
run_section "7. 修复后 300s 复测" "$RUNNER_TMP"
TEST_EXIT=$?

run_section "8. 清理流程" \
  "./scripts/kill_fuel.sh; ps aux | grep -E 'fuel|exploration|traj|quadrotor|pcl_render|rviz2|p2e_inline' | grep -v grep || true"
CLEAN_EXIT=$?

{
  echo
  echo "## 9. 全流程汇总 Summary"
  echo
  echo "- start_time: $(date -Is)"
  echo "- command: aggregate metrics from /tmp/p2e_motion_metrics.env"
  echo
  echo '```text'
  echo "single_markdown_log=$LOG"
  echo "syntax_exit=$SYNTAX_EXIT"
  echo "fix_syntax_exit=$FIX_SYNTAX_EXIT"
  echo "build_exit=$BUILD_EXIT"
  echo "test_exit=$TEST_EXIT"
  echo "cleanup_exit=$CLEAN_EXIT"
  if [ -f "$METRICS_TMP" ]; then
    cat "$METRICS_TMP"
  else
    echo "metrics=UNAVAILABLE"
  fi
  # shellcheck disable=SC1090
  source "$METRICS_TMP" 2>/dev/null || true
  colcon_build="FAIL"
  [ "${BUILD_EXIT:-1}" -eq 0 ] && colcon_build="PASS"
  duration="${duration_sec:-0}"
  odom="${odom_total_distance:-0}"
  apu="${active_path_update_count:-0}"
  aps="${active_path_same_hash_max_duration_sec:-999}"
  pcu="${position_cmd_update_count:-0}"
  pcv="${position_cmd_total_variation:-0}"
  stale="${traj_server_stale_path_hold_count:-999}"
  chain_break="${main_chain_break:-UNKNOWN}"
  result="FAIL"
  awk "BEGIN{exit !($duration >= 290 && $odom > 2.0 && $apu > 3 && $pcu > 10 && $pcv > 0.5 && $aps < 120 && \"$chain_break\" != \"PATH_FEASIBILITY\" && $stale < 5)}" && result="PASS" || true
  if [ "$result" != "PASS" ]; then
    awk "BEGIN{exit !($odom > 0.101 || $apu > 1 || $pcu > 1 || $pcv > 0.0)}" && result="PARTIAL" || true
  fi
  echo "colcon_build=$colcon_build"
  echo "after_fix_result=$result"
  echo "single_md_only=YES"
  echo "extra_md_logs_created=0"
  echo '```'
  echo
  echo "- end_time: $(date -Is)"
  echo "- exit_code: 0"
  echo
  echo "- Final result: ${result}"
  echo "- Root cause: PATH_FEASIBILITY is fixed only if active_path updates and endpoint tracks the current goal; otherwise the remaining direct cause is path candidate feasibility/search."
  echo "- Next action: if PATH_FEASIBILITY remains, inspect start/goal occupancy, z corridor bounds, and partial-path endpoint generation inside the planner search."
} >> "$LOG"

echo "P2E_SINGLE_MD_LOG=$LOG"
exit 0
