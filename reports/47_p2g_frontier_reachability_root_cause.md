# P2G Frontier Reachability Root Cause

- Baseline run_id: `p2g_frontier_300s_baseline_20260622_114700`
- Duration: 300.013s
- Odom total distance: 1.405m
- Coverage proxy: 0.079591 -> 0.085923, gain 0.006332
- Coverage stall max duration: 239.972s
- Frontier candidates end: 105
- Frontier viewpoints end: 44
- Selected goal unique count: 4
- Selected goal region count: 4
- Active path update count: 2
- Active path endpoint to selected goal avg/max: 0.000m / 0.000m
- Active path endpoint to best viewpoint avg: 5.609m
- Unreachable goal ratio: 0.993
- Reachability reject count: 298
- Goal blacklist count observed by recorder: 0
- Main frontier blocker: `PATH_ENDPOINT_FAR_FROM_GOAL`

## Diagnosis

Frontiers and viewpoints were still present at the end of the baseline, so exploration was not complete. The selected active path endpoint was close to the currently published exploration goal, but the best viewpoint stream had drifted far away from that active path endpoint. The system repeatedly selected or retained frontier/viewpoint targets that the goal-to-path bridge reported as invalid or infeasible.

The root cause is missing feedback from path feasibility into frontier/viewpoint scoring. `frontier_viewpoint_lite.py` did not blacklist or penalize a region after `/fuel/p11_lite/goal_to_path_status` reported repeated infeasible paths. As a result, the manager retired active goals, but the upstream best_viewpoint/frontier_viewpoints source could keep offering the same unreachable local regions. This produced high frontier counts with almost no movement and very low coverage gain.

The immediate blocker is `PATH_ENDPOINT_FAR_FROM_GOAL` / unreachable frontier selection. The next blocker after reachability improves is likely residual low-gain or score-plateau frontier selection.
