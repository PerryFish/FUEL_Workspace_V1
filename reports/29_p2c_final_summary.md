# P2C Final Summary

## Result

P2C result: `PARTIAL_NOT_IMPROVED`

The workspace still builds and runs, and RViz topics were not changed, but P2C did not improve office 300s exploration coverage or motion over the P2B baseline.

## Final Metrics

Final P2C run:

```text
metrics_dir=reports/p2c_metrics/p2c_after_office_300s_20260621_173224
duration_sec=304.621
uav_total_distance=2.663m
uav_net_displacement=2.554m
raw_goal_msg_count=600
unique_goal_count_quantized_0p5m=4
unique_goal_count_quantized_1p0m=4
goal_switch_count=3
same_goal_max_duration_sec=238.998
goal_republish_count=596
true_repeated_goal_count=0
goal_retire_event_count=3
escape_goal_count=1
trajectory_count=6112
frontier_count_end=124
explored_grid_start=1363
explored_grid_end=1492
coverage_proxy_start=0.000000
coverage_proxy_end=0.109851
coverage_proxy_gain=0.109851
stuck_event_count=54
main_stuck_cause_after_fix=REPEATED_GOAL
main_goal_lifecycle_cause=SAME_GOAL_HELD_TOO_LONG
```

## Recommendation

Do not enter multi-map benchmark yet.

Keep:

- lifecycle recorder enhancements
- `analyze_goal_lifecycle.py`
- `/fuel/p11_lite/goal_lifecycle_status`

Do not rely on raw frontier-point escape yet. It needs path feasibility filtering before it can be used safely.

## Next Stage

The next stage should target:

```text
path_feasibility_issue=LIKELY
traj_server_stale_path_hold=LIKELY
active_goal_state_machine_still_has_limits=YES
frontier_scoring_issue=POSSIBLE
controller_or_sim_issue=LESS_LIKELY
```

Concrete next checks:

1. Record active goal to generated path endpoint distance.
2. Record traj_server stale path hold count as a metric.
3. Reject escape goals unless `goal_to_path_status` reports a feasible path.
4. Add a path-feasible candidate buffer instead of selecting raw frontier points.
5. Only then re-enable local-minimum escape.
