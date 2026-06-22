# P2D Motion Chain Root Cause

## Baseline Run

```text
run_id=p2d_motion_chain_300s_20260622_090829
metrics_dir=reports/p2d_metrics/p2d_motion_chain_300s_20260622_090829
```

## Key Evidence

```text
odom_total_distance=0.101m
goal_switch_count=2
active_path_update_count=1
active_path_same_hash_max_duration_sec=299.875
active_path_endpoint_to_goal_distance_avg=7.051
active_path_endpoint_to_goal_distance_max=7.806
travel_traj_update_count=47
travel_traj_same_hash_max_duration_sec=277.562
position_cmd_update_count=1
position_cmd_total_variation=0.0
position_cmd_same_pose_max_duration_sec=299.960
traj_server_stale_path_hold_count=38
quadrotor_sim_motion_blocked_count=8999
main_chain_break=PATH_FEASIBILITY
```

## Root Cause

The active goal continued to change or remain far away, but `/fuel/p10_lite/active_path` stayed effectively unchanged and its endpoint was about 7m from the active goal. Therefore the downstream traj server was executing or holding a stale managed trajectory, and position command stayed fixed.

The main break is before traj server command sampling:

```text
active goal -> active path = BROKEN
active path -> travel trajectory = stale downstream consequence
travel trajectory -> position_cmd = stale downstream consequence
position_cmd -> odom = no motion because command target equals current pose
```

## Runtime Status Evidence

`/fuel/p10_lite/traj_server_status` ended with:

```text
active_source=managed_trajectory
active_points=15
target_index=14
hold_position=true
stale_path_hold_count=38
```

This means the traj server reached the end of its selected path and held position.

## Conclusion

`main_chain_break=PATH_FEASIBILITY`
