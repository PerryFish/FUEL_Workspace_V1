# P2I Endpoint Outlier And Route Revisit Fix

- result: PARTIAL

## Changes
- `src/FUEL/scripts/frontier_viewpoint_lite.py`
  - `distance_cost_weight`: 1.35 -> 1.45
  - `recent_revisit_penalty_weight`: 3.0 -> 3.5
  - `new_region_bonus`: 0.35 -> 0.45
  - endpoint outliers above 2.0m are blacklisted faster through reachability feedback; above 5.0m is treated as a hard outlier.

## Validation
Final headless 300s:
- `path_length_regret_avg=-2.448`
- `path_length_regret_max=4.819`
- `active_path_endpoint_to_goal_distance_avg=0.000`
- `active_path_endpoint_to_goal_distance_max=0.000`
- `route_revisit_ratio=0.868`
- `route_tortuosity=6.108`

## Remaining Issue
Endpoint and path-regret outliers improved in the headless run, but route revisit remains high and visual mode still had endpoint outliers. Further route shaping should be separate from the no-path watchdog fix.

