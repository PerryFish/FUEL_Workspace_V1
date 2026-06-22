# P2H Path-Aware Scoring Design

## Scoring Change

The P2H fix keeps the existing scoring structure in `frontier_viewpoint_lite.py`, but makes path cost visible at the same scale as gain and novelty:

```text
score =
  unknown_gain_weight * information_gain
+ frontier_density_weight * local_density
+ novelty_weight * novelty
+ inward_direction_weight * inward_score
+ near_frontier_bonus
+ new_region_bonus
+ local_gain_bonus
- distance_cost_weight * (distance / path_cost_normalizer)
- revisit_penalty
```

## New / Adjusted Weights

- `distance_cost_weight`: 0.8 -> 1.35
- `path_cost_normalizer`: 8.0m
- `near_frontier_bonus`: 0.25 for useful frontiers within 4m
- `new_region_bonus`: 0.35 for unvisited 2m regions
- `active_region_score_bonus`: 1.0 -> 0.35
- `non_preferred_region_penalty`: 0.25 -> 0.10
- `best_max_hold_sec`: 45s -> 25s
- `switch_score_margin`: 2.5 -> 1.4

## Why This Is Minimal

No topic interfaces changed. No map, RViz, DDS, odom, actuator, or trajectory-server behavior changed. The patch changes only viewpoint selection pressure and status fields, so it is easy to revert and compare.
