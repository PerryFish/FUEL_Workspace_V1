# P2G Reachability Filter Fix Report

## Modified Files

- `src/FUEL/scripts/frontier_viewpoint_lite.py`

## Fix Logic

The frontier viewpoint selector now consumes goal-to-path feasibility feedback. Repeated infeasible goals are mapped to a temporary 2m region blacklist. Blacklisted regions are excluded before publishing `frontier_viewpoints` and `best_viewpoint`, so the manager receives fewer unreachable candidates during coverage stall recovery.

## Parameters

- `unreachable_blacklist_ttl_sec=90.0`
- `unreachable_region_resolution=2.0`
- `unreachable_path_fail_threshold=2`

## Interface Impact

No topic interfaces changed. The patch only adds one subscription and additional text fields in `/fuel/p11_lite/frontier_status`.

## Verification

- Syntax check: PASS
- Colcon build: PASS
- 300s after-fix validation: PASS by P2G recorder criteria
- 600s long validation: PARTIAL; stable run, but late coverage stall remains

## Diff

- `reports/p2g_before_frontier_fix_diff_20260622_115350.patch`
- `reports/p2g_after_frontier_fix_diff_20260622_115542.patch`
