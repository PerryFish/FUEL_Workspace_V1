# P2D Position Command vs Odom Analysis

## Baseline

```text
position_cmd_update_count=1
position_cmd_total_variation=0.0
position_cmd_same_pose_max_duration_sec=299.960
position_cmd_to_odom_distance_avg=0.000285
odom_total_distance=0.101m
```

## After Fix

```text
position_cmd_update_count=1
position_cmd_total_variation=0.0
position_cmd_same_pose_max_duration_sec=299.929
position_cmd_to_odom_distance_avg=0.000119
odom_total_distance=0.065m
```

## Interpretation

The simulator is not ignoring a changing command. The command itself is stale and nearly equal to odom, so the UAV has no motion target.

This is not currently classified as `SIM_TRACKING_FAIL`.
