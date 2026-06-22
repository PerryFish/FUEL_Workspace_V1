# P2H Visual Route Review

Use this command:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2h_visual_route_300s ./scripts/run_p2h_visual_route_300s.sh
```

During RViz review, check:

1. Whether the UAV prefers nearby unexplored regions when they have visible frontier markers.
2. Whether obvious long detours are reduced compared with P2G.
3. Whether the path repeatedly revisits the same local area.
4. Whether goal switching is more diverse without becoming jittery.
5. Whether frontier, goal, active path, travel trajectory, and UAV trail remain visually consistent.

The route recorder prints every 30 seconds:

```text
coverage_proxy
odom_total_distance
coverage_gain_per_meter
path_length_regret_avg
near_high_gain_candidate_ignored_count
route_revisit_ratio
route_tortuosity
main_route_issue
```

## P2H Visual Run Result

- run_id: `p2h_visual_route_300s_20260622_132156`
- duration_sec: 300.027
- odom_total_distance: 48.384m
- coverage_proxy_gain: 0.146591
- coverage_gain_per_meter: 0.003030
- selected_goal_unique_count: 29
- path_length_regret_avg: -0.320m
- route_tortuosity: 3.187
- active_path_endpoint_to_goal_distance_avg: 0.154m
- recorder_result: PASS
- visual_result: PARTIAL

The recorder completed and produced valid metrics. The raw log contains an `rviz2` aborted/core-dump line near cleanup, so this visual run should be treated as PARTIAL for RViz process stability even though the route diagnostic itself completed.
