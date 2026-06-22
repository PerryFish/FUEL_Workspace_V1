# P2C Local Minimum Escape Design

## Design Constraints

- Do not modify maps.
- Do not disable obstacles, local sensing, or collision assumptions.
- Do not touch RViz topics.
- Do not publish real flight-controller commands.
- Keep changes localized to `exploration_manager_lite.py` and diagnostic scripts.

## Implemented Design

P2C added goal lifecycle instrumentation and a conservative escape framework:

- recent goal memory:
  - `recent_goal_memory_size=10`
  - `recent_goal_quantization=0.5`
  - `recent_goal_ttl_sec=120`
- lifecycle status topic:
  - `/fuel/p11_lite/goal_lifecycle_status`
  - type `std_msgs/msg/String`
- goal lifecycle events:
  - `NEW_GOAL`
  - `KEEP_GOAL`
  - `RETIRE_GOAL`
  - `ESCAPE_GOAL`
- coverage/motion stall inputs:
  - `/fuel/p11_lite/explored_grid`
  - `/map_generator/global_cloud`
  - `/fuel/p11_lite/frontier_candidates_raw`
  - `/fuel/p11_lite/frontier_viewpoints`
  - `/odom`

## Attempt 1: Raw Frontier Point Escape

The first P2C attempt selected escape candidates from `/fuel/p11_lite/frontier_viewpoints` when coverage and motion stalled.

Result:

```text
escape_goal_count=50
goal_switch_count=53
uav_total_distance=1.179m
coverage_proxy_gain=0.083935
```

Conclusion: too aggressive. It increased goal churn and did not improve motion.

## Attempt 2: Conservative Best-Viewpoint Escape and Threshold Fix

The final code keeps raw frontier-point escape disabled by default:

```text
enable_frontier_point_escape=false
```

It also changes goal lifecycle defaults to align with the P2C design:

```text
min_goal_separation=1.0
min_goal_distance=1.0
min_new_goal_separation=1.0
goal_timeout_sec=25.0
escape_cooldown_sec=25.0
```

Result:

```text
escape_goal_count=1
goal_switch_count=3
same_goal_max_duration_sec=238.998
uav_total_distance=2.663m
coverage_proxy_gain=0.109851
```

Conclusion: safer than raw point escape, but not sufficient to improve over P2B baseline.

## Final Design Assessment

The lifecycle instrumentation should be kept. The raw frontier-point escape should remain disabled until path feasibility checks are added. The threshold reduction is reasonable but did not solve the long-run stall by itself.
