# P2A RViz Visual Display Fix

Date: 2026-06-21

## Files Added Or Changed

New scripts:

- `scripts/check_tf_tree.sh`
- `scripts/run_rviz_tf_probe.sh`
- `scripts/publish_rviz_map_tf.py`
- `scripts/run_manual_visual_demo_persistent.sh`
- `scripts/run_visual_check_v3.sh`
- `scripts/run_rviz_only_with_correct_env.sh`

Modified script:

- `scripts/fuel_topic_probe.py`

New RViz config:

- `src/FUEL/rviz/fuel_exploration_p2a_fixed_frame.rviz`
- installed as `install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz`

## Display Configuration

The new RViz config uses:

```text
Fixed Frame: map
```

It includes visible displays for:

```text
/map_generator/global_cloud
/global_cloud
/fuel/p11_lite/occupancy_grid
/fuel/p11_lite/explored_grid
/fuel/p11_lite/local_free_points
/fuel/p11_lite/local_occupied_points
/fuel/p11_lite/frontier_candidates_raw
/fuel/p11_lite/frontier_viewpoints
/fuel/p11_lite/visual/all_markers
/fuel/p11_lite/visual/uav_marker
/fuel/p11_lite/visual/uav_trail
/fuel/p11_lite/visual/path_markers
/fuel/p11_lite/visual/frontier_markers
/fuel/p11_lite/visual/current_goal_marker
/fuel/visual/world_bounds
/fuel/visual/world_obstacles
/planning/travel_traj
/fuel/plan_manager/managed_trajectory
/odom
```

Colors were chosen so the map, occupied/free local sensing, frontier candidates, UAV marker, and trajectories do not all collapse into a white/grey view.

## Data Readiness Evidence

Key log:

- `test-log/20260621_155151_p2a_visual_check_v3_fixed.md`

The v3 visual check recorded:

```text
RVIZ_STARTED=YES
TF_CHECK_OK=1
uav_marker_count=50
all_markers_count=51
path_markers_count=50
map_cloud_count=104
planner_traj_count=607
odom_msg_count=3045
FUEL_VISUAL_CHECK_V3_PASS_DATA_READY_MANUAL_CONFIRM_REQUIRED
```

Probe samples confirmed all major display sources are in `frame=map`:

```text
/fuel/p11_lite/visual/uav_marker frame=map
/fuel/p11_lite/visual/path_markers markers=7
/map_generator/global_cloud points=13582 frame=map
/planning/travel_traj poses=69 frame=map
/odom frame=map
```

## Build Status

Key log:

- `test-log/20260621_154456_p2a_build_check.md`

Result:

```text
colcon_build=PASS
2 packages finished
```

Only existing C++ warnings were present in `fuel_plan_manager_adapter.cpp`.

