# P2H Route Rationality Fix Report

## Modified Files

- `src/FUEL/scripts/frontier_viewpoint_lite.py`
- `scripts/fuel_route_rationality_recorder.py`
- `scripts/analyze_route_rationality.py`
- `scripts/run_p2h_route_common.sh`
- `scripts/run_p2h_route_300s_baseline.sh`
- `scripts/run_p2h_route_300s_after_fix.sh`
- `scripts/run_p2h_visual_route_300s.sh`
- `scripts/export_p2h_debug_package.sh`

## Code Logic

The route fix changes only frontier/viewpoint scoring. It increases path/distance cost, reduces active-region stickiness, adds a small nearby-frontier bonus, and adds a new-region bonus. This targets the baseline root cause where path cost was underweighted and route tortuosity was high.

## Interface Impact

No ROS topic type or topic name changed. Additional frontier status fields are diagnostic only.

## Verification

- syntax check: PASS
- colcon build: PASS
- baseline 300s route recorder: PASS, main issue `PATH_COST_UNDERWEIGHTED`
- after-fix 300s route recorder: PASS with improved coverage gain, path regret average, and route tortuosity
