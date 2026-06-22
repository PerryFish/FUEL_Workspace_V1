# P1 UAV Motion Validation

Date: 2026-06-21

## Validation Method

`scripts/fuel_topic_probe.py` was added to avoid relying only on `ros2 topic echo`. It subscribes directly with `rclpy` and records:

- odometry counts and start/end position;
- UAV distance moved;
- planner command count;
- trajectory count;
- map/global cloud count;
- local sensing cloud count;
- goal count.

Main observed topics:

```text
/odom
/state_ukf/odom
/visual_slam/odom
/planning/pos_cmd
/planning/travel_traj
/map_generator/global_cloud
/pcl_render_node/cloud
/fuel/p11_lite/visual/all_markers
```

## Evidence

Key logs:

- `test-log/20260621_150355_p1_smoke_v2.md`
- `test-log/20260621_150654_p1_visual_v2.md`
- `test-log/20260621_151122_p1_visual_v2_fixed.md`
- `test-log/20260621_151517_p1_smoke_v2_final.md`

Strongest motion evidence:

```text
test-log/20260621_150355_p1_smoke_v2.md
uav_distance_moved=3.926
planner_pos_cmd_count=1200
planner_traj_count=1378
map_cloud_count=240
goal_msg_count=107
FUEL_HEADLESS_SMOKE_TEST_V2_PASS
```

Visual v2 internal headless evidence:

```text
test-log/20260621_150654_p1_visual_v2.md
uav_distance_moved=5.529
planner_pos_cmd_count=1200
planner_traj_count=1332
map_cloud_count=240
FUEL_HEADLESS_SMOKE_TEST_V2_PASS
```

Final post-build smoke v2:

```text
test-log/20260621_151517_p1_smoke_v2_final.md
UAV_DISTANCE_MOVED_BEFORE_GOAL=0.598
UAV_DISTANCE_MOVED_AFTER_GOAL=0
UAV_DISTANCE_MOVED=0.598
PLANNER_POS_CMD_COUNT=1191
PLANNER_TRAJ_COUNT=1191
MAP_CLOUD_COUNT=240
GOAL_MSG_COUNT=120
FUEL_HEADLESS_SMOKE_TEST_V2_PASS
```

## Interpretation

The planner and simulator chain is active:

- odometry publishes continuously;
- planner command and trajectory topics publish continuously;
- map and local sensing clouds publish continuously;
- UAV motion is measurable in odom.

The final post-build run measured motion before the manual goal window and no additional displacement after the manual goal window. Earlier P1 smoke/visual runs measured larger displacement after goal. This is consistent with the autonomous exploration loop already moving or reaching a local target before the manual goal observation window. It is not a DDS or topic visibility failure.

## Current Diagnosis

```text
odom_topic=/odom
compat_odom_topics=/state_ukf/odom,/visual_slam/odom
odom_topic=PASS
planner_output_topic=PASS
uav_motion=PASS
best_observed_uav_distance_moved=5.529 m
final_post_build_uav_distance_moved=0.598 m
headless_smoke_test_v2=PASS
```

