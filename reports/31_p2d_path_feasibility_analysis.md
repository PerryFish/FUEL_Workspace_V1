# P2D Path Feasibility Analysis

## Baseline

```text
active_path_msg_count=3000
active_path_update_count=1
active_path_endpoint_to_goal_distance_avg=7.050957763302419
active_path_endpoint_to_goal_distance_max=7.805698684593535
active_path_same_hash_max_duration_sec=299.8745274543762
path_feasibility_break=True
```

## Source Finding

The relevant source is:

```text
src/FUEL/scripts/p11_lite_goal_to_path_bridge.py
```

The bridge could keep `last_valid_path_active_reselect` when a new active goal had no executable path. That allowed an old path to remain active while the current goal was elsewhere.

## Fix Attempt

P2D changed fallback behavior so a previous path can only be reused for the same rounded goal key. Cross-goal stale fallback was disabled.

## After Fix

```text
run_id=p2d_motion_chain_300s_20260622_091639
active_path_msg_count=2991
active_path_update_count=1
active_path_endpoint_to_goal_distance_avg=6.865569898280451
active_path_endpoint_to_goal_distance_max=7.805698684593535
active_path_same_hash_max_duration_sec=299.0344657897949
path_feasibility_break=True
```

The attempt did not fix the path-feasibility break.

## Next Target

The next fix should make the path bridge publish explicit infeasible status and prevent the exploration manager from holding a goal unless `active_path_endpoint_to_goal_distance <= 1.5m`.
