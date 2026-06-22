# P2H 300s Validation

| metric | baseline | after_fix | change | result |
|---|---:|---:|---:|---|
| coverage_proxy_gain | 0.104918 | 0.159034 | +0.054116 | improved |
| coverage_gain_per_meter | 0.001563 | 0.002142 | +0.000579 | improved |
| odom_total_distance | 67.132m | 74.239m | +7.107m | acceptable; more coverage gained |
| path_length_regret_avg | 1.744m | -0.024m | -1.768m | improved |
| path_length_regret_max | 13.402m | 14.884m | +1.482m | residual outlier |
| near_high_gain_candidate_ignored_count | 0 | 0 | 0 | unchanged |
| route_revisit_ratio | 0.892 | 0.877 | -0.015 | slight improvement |
| route_tortuosity | 6.760 | 3.770 | -2.990 | improved |
| selected_goal_unique_count | 18 | 31 | +13 | improved |
| active_path_endpoint_to_goal_distance_avg | 0.251m | 0.297m | +0.046m | acceptable |
| main_route_issue | PATH_COST_UNDERWEIGHTED | PATH_COST_UNDERWEIGHTED | residual heuristic outlier | partial |

## Result

The 300s after-fix route is better by the metrics that match the user-visible issue: higher coverage, higher coverage per meter, much lower average path regret, more unique goals, and lower route tortuosity. The remaining issue is occasional outlier path regret / endpoint mismatch, so P2H is marked `PASS` for the route-cost fix and `PARTIAL` for complete route rationality.
