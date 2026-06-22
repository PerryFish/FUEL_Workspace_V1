# P2D Traj Server Stale Path Analysis

## Baseline

```text
active_path_update_count=1
travel_traj_update_count=47
travel_traj_same_hash_max_duration_sec=277.56186389923096
traj_server_stale_path_hold_count=38
traj_server_break=False
```

## After Fix

```text
active_path_update_count=1
travel_traj_update_count=99
travel_traj_same_hash_max_duration_sec=251.83116340637207
traj_server_stale_path_hold_count=64
traj_server_break=False
```

## Interpretation

The traj server is stale, but this is downstream of path feasibility. It receives an active path that does not correspond to the current active goal, reaches the end, then holds position.

Per P2D rules, because `main_chain_break=PATH_FEASIBILITY`, traj server was not modified.
