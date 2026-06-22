# P2H Route Rationality Root Cause

- baseline_run_id: `p2h_route_300s_baseline_20260622_130557`
- duration_sec: 300.013
- odom_total_distance: 67.132m
- coverage_proxy_gain: 0.104918
- coverage_gain_per_meter: 0.001563
- selected_goal_unique_count: 18
- path_length_regret_avg: 1.744m
- path_length_regret_max: 13.402m
- nearest_frontier_ignored_count: 7
- near_high_gain_candidate_ignored_count: 0
- route_revisit_ratio: 0.892
- route_tortuosity: 6.760
- active_path_endpoint_to_goal_distance_avg: 0.251m
- active_path_endpoint_to_goal_distance_max: 17.545m
- main_route_issue: `PATH_COST_UNDERWEIGHTED`

## Diagnosis

The route baseline did not fail coverage, but it spent too much distance for the gained coverage. The selected goal path length was often longer than a nearer available frontier/viewpoint estimate, with a maximum regret above 13m. The route revisit ratio was also high, indicating repeated motion through already visited local regions.

The main cause is that `frontier_viewpoint_lite.py` scoring used a weak distance/path-cost term: distance was normalized by 30m and weighted only moderately, while information gain, inward direction, active-region preference, and density could dominate. This made farther viewpoints competitive even when nearer viewpoints still had reasonable gain.

The secondary cause is active-region stickiness. The previous scoring gave the preferred/active region a strong bonus, which helped exploration continuity but could preserve locally repetitive route choices after a region was already being revisited.
