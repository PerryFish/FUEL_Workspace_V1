# P1 DDS Discovery Diagnosis

Date: 2026-06-21

## Scope

Phase: `P1_DDS_GOAL_MOTION_FIX`

Workspace: `/home/nuaa/ZHY/FUEL_PLANNER_V3`

Source commit: `3b11fc50c0ab8e84f9093f084ce80f4d1af6088d`

## Root Cause

The earlier ROS2 CLI symptom, where `ros2 topic list` only showed `/rosout` and `/parameter_events`, was not a FUEL planner failure. The main root cause was environment and graph isolation:

- `scripts/env.sh` previously sourced the workspace setup in a way that inherited an unrelated underlay from `/home/nuaa/ZHY/A_DWA`.
- The ROS2 daemon could cache an incomplete graph.
- FUEL launch and CLI checks were not always using the same isolated `ROS_DOMAIN_ID`, `RMW_IMPLEMENTATION`, and `ROS_LOCALHOST_ONLY` values.

## Fix Applied

`scripts/env.sh` now:

- clears `AMENT_PREFIX_PATH`, `CMAKE_PREFIX_PATH`, and `COLCON_PREFIX_PATH` before sourcing ROS;
- sources `/opt/ros/humble/setup.bash`;
- prefers `install/local_setup.bash`;
- keeps `ROS_DOMAIN_ID`, `RMW_IMPLEMENTATION`, `ROS_LOCALHOST_ONLY`, and `FASTDDS_BUILTIN_TRANSPORTS` overrideable;
- writes ROS logs under the workspace.

For isolated P1 tests the working configuration is:

```text
ROS_DOMAIN_ID=88
RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ROS_LOCALHOST_ONLY=1
FASTDDS_BUILTIN_TRANSPORTS=UDPv4
```

## Evidence

Key logs:

- `test-log/20260621_144703_p1_baseline_env.md`
- `test-log/20260621_145634_p1_env_clean_check.md`
- `test-log/20260621_145506_p1_dds_minimal_clean.md`
- `test-log/20260621_145634_p1_dds_matrix.md`
- `test-log/20260621_151517_p1_smoke_v2_final.md`

DDS minimal test result:

```text
DDS_MINIMAL_TEST_PASS listener_received_chatter
```

DDS matrix result:

```text
fast_a: rmw_fastrtps_cpp, ROS_LOCALHOST_ONLY=1 -> PASS
fast_b: rmw_fastrtps_cpp, ROS_LOCALHOST_ONLY=0 -> PASS
fast_udp_local: rmw_fastrtps_cpp, ROS_LOCALHOST_ONLY=1, UDPv4 -> PASS
fast_udp_global: rmw_fastrtps_cpp, ROS_LOCALHOST_ONLY=0, UDPv4 -> PASS
cyclone_c: CYCLONEDDS_NOT_AVAILABLE_SUDO_BLOCKED
cyclone_d: CYCLONEDDS_NOT_AVAILABLE_SUDO_BLOCKED
```

Final smoke v2 confirmed ROS graph visibility:

```text
ros2 node list: PASS
ros2 topic list: PASS
/move_base_simple/goal visible: YES
/fuel/p11_lite/exploration_goal visible: YES
/planning/pos_cmd visible: YES
/planning/travel_traj visible: YES
/odom visible: YES
/state_ukf/odom visible: YES
```

## Current Diagnosis

```text
dds_discovery=PASS
ros2_node_list=PASS
ros2_topic_list=PASS
best_config=rmw_fastrtps_cpp + ROS_LOCALHOST_ONLY=1 + FASTDDS_BUILTIN_TRANSPORTS=UDPv4 + ROS_DOMAIN_ID=88
cyclonedds=CYCLONEDDS_NOT_AVAILABLE_SUDO_BLOCKED
```

