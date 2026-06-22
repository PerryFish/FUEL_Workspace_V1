# P2G Final Summary

## Logging

- Summary metric scoping fix: PASS
- Full run log system: PASS
- Summary and full logs are generated under `test-log-summary/` for each `run_with_log.sh` task.
- Clean summary test result: PASS, `metrics_source=NONE`.

## Frontier Baseline

- run_id: `p2g_frontier_300s_baseline_20260622_114700`
- coverage gain: 0.006332
- odom distance: 1.405m
- selected goal unique count: 4
- coverage stall max: 239.972s
- main blocker: `PATH_ENDPOINT_FAR_FROM_GOAL`

## 300s After Fix

- run_id: `p2g_coverage_300s_after_fix_20260622_115723`
- coverage gain: 0.101900
- odom distance: 50.235m
- selected goal unique count: 29
- selected goal region count: 27
- active path updates: 155
- coverage stall max: 0.000s
- main blocker: residual `PATH_ENDPOINT_FAR_FROM_GOAL`
- result: PASS for 300s office coverage continuity

## 600s After Fix

- run_id: `p2g_coverage_600s_after_fix_20260622_120315`
- coverage gain: 0.072817
- odom distance: 41.137m
- selected goal unique count: 11
- coverage stall max: 389.957s
- main blocker: `PATH_ENDPOINT_FAR_FROM_GOAL`
- status: STALLED

## Conclusion

P2G fixed the immediate 300s failure mode by feeding path reachability failures back into frontier viewpoint selection. UAV movement and coverage improved substantially over P2F/P2G baseline. The system still does not complete coverage in a 600s run because residual frontiers after the reachable high-gain regions are consumed remain mostly infeasible.

Do not move to multi-map benchmark yet. The next minimal action is to make frontier generation/scoring path-aware before best_viewpoint publication, or to add a stronger frontier-region quarantine when a region repeatedly produces infeasible paths across multiple candidate points.
