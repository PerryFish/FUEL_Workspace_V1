# P2A Final Summary

Date: 2026-06-21

Phase: `P2A_RVIZ_TF_FIXED_FRAME_VISUAL_FIX`

Workspace: `/home/nuaa/ZHY/FUEL_PLANNER_V3`

Source commit: `3b11fc50c0ab8e84f9093f084ce80f4d1af6088d`

## Root Cause

```text
root_cause=RViz fixed frame map was not reliably present in TF when RViz opened. Planner topics, map clouds, odom, trajectory, and marker topics were already publishing in frame=map, but RViz needs a TF frame named map before it can render them under Fixed Frame=map.
```

## Fix

```text
fix=Add a RViz-only static TF anchor map -> fuel_rviz_anchor, add a fixed-frame RViz config that uses actual ROS2 port topics, and add persistent manual demo plus v3 data-readiness validation.
```

The static anchor does not alter algorithm behavior, odom integration, controller output, or simulator motion.

## Verification

```text
colcon_build=PASS
tf_static_exists=YES
map_frame_exists=YES
rviz_fixed_frame_ready=YES
rviz_config_created=YES
rviz_config_installed=YES
manual_visual_demo_script=PASS
visual_check_v3=PASS_DATA_READY_MANUAL_CONFIRM_REQUIRED
```

Important logs:

- `test-log/20260621_154456_p2a_build_check.md`
- `test-log/20260621_154328_p2a_rviz_tf_probe_2.md`
- `test-log/20260621_155151_p2a_visual_check_v3_fixed.md`
- `test-log/20260621_155800_p2a_manual_visual_demo_auto_enter.md`

## Headless V2 Note

`run_headless_smoke_test_v2.sh` was rerun twice in P2A:

- `test-log/20260621_154632_p2a_headless_smoke_v2.md`
- `test-log/20260621_155533_p2a_headless_smoke_v2_retry.md`

Both runs had planner, map, marker, trajectory, goal, and odom data, but failed the old motion threshold in that sampling window:

```text
FUEL_HEADLESS_SMOKE_TEST_V2_FAIL
reason=motion_threshold_only
planner_traj_count=1182
map_cloud_count=238
goal_msg_count=120
odom_msg_count=7127
```

This is not the P2A RViz fixed-frame root cause. In the P2A visual v3 run, the probe measured:

```text
uav_distance_moved=4.221
planner_traj_count=607
map_cloud_count=104
FUEL_VISUAL_CHECK_V3_PASS_DATA_READY_MANUAL_CONFIRM_REQUIRED
```

## Final Commands

Recommended manual visual validation:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2a_manual_visual ./scripts/run_manual_visual_demo_persistent.sh
```

Automated data readiness check:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2a_visual_v3 ./scripts/run_visual_check_v3.sh
```

TF-only check:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2a_tf ./scripts/run_rviz_tf_probe.sh
```

## Remaining Manual Confirmation

The automated check can prove TF and data readiness, and it verifies RViz starts without detecting `Frame [map] does not exist` in the RViz log. It cannot prove what the human eye sees in the RViz canvas. The final visual confirmation should be done with:

```bash
./scripts/run_with_log.sh p2a_manual_visual ./scripts/run_manual_visual_demo_persistent.sh
```

