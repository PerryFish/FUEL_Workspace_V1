# P2H Final Summary

## Branch

- base backup branch: `backup/p2g-coverage-route-stable-20260622`
- dev branch: `dev/p2h-route-rationality-frontier-cost`
- source_commit_before: `54bcdba23f71e202c0774ec1fce02df07eaff9fa`

## Baseline

- run_id: `p2h_route_300s_baseline_20260622_130557`
- coverage_proxy_gain: 0.104918
- coverage_gain_per_meter: 0.001563
- odom_total_distance: 67.132m
- selected_goal_unique_count: 18
- path_length_regret_avg: 1.744m
- route_tortuosity: 6.760
- main_route_issue: `PATH_COST_UNDERWEIGHTED`

## After Fix

- run_id: `p2h_route_300s_after_fix_20260622_131440`
- coverage_proxy_gain: 0.159034
- coverage_gain_per_meter: 0.002142
- odom_total_distance: 74.239m
- selected_goal_unique_count: 31
- path_length_regret_avg: -0.024m
- route_tortuosity: 3.770
- main_route_issue: residual `PATH_COST_UNDERWEIGHTED`

## Visual Route Run

- run_id: `p2h_visual_route_300s_20260622_132156`
- coverage gain: 0.146591
- coverage gain per meter: 0.003030
- selected goal unique count: 29
- route tortuosity: 3.187
- recorder result: PASS
- visual process result: PARTIAL due to an `rviz2` aborted/core-dump line in the raw log

## Conclusion

P2H improves the route rationality issue that was visible in the baseline: the system gains more coverage per meter and reduces average path regret and tortuosity. It does not fully eliminate all outliers; the next phase should focus on endpoint mismatch and local-region revisit suppression rather than more global lifecycle changes.
