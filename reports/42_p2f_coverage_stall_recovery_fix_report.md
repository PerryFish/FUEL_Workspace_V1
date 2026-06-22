# P2F Coverage Stall Recovery Fix Report

## Modified Files

- `scripts/generate_unified_summary_log.py`
- `scripts/run_with_log.sh`
- `scripts/fuel_coverage_completion_recorder.py`
- `scripts/run_p2f_coverage_300s_baseline.sh`
- `scripts/run_p2f_coverage_common.sh`
- `scripts/run_p2f_coverage_300s_after_fix.sh`
- `scripts/run_p2f_coverage_600s_after_fix.sh`
- `scripts/run_p2f_visual_coverage_300s.sh`
- `scripts/analyze_coverage_stall_and_goal_reselect.py`
- `scripts/export_p2f_debug_package.sh`
- `src/FUEL/scripts/exploration_manager_lite.py`

## Fix Summary

- Unified summary logs now generate under `test-log-summary/` for every `run_with_log.sh` execution.
- Coverage recorder now uses `/map_generator/global_cloud` as the stable denominator for coverage proxy.
- Coverage recorder no longer imports old metrics when the current run has no metrics.
- Frontier point escape is enabled by default.
- Coverage-stall/no-progress escape can bypass global switch rate limiting, while still using cooldown and candidate filtering.

## Result

The fix improves instrumentation and keeps the motion chain alive in some runs, but final 300s validation remained PARTIAL due run-to-run variability and a likely frontier scoring/reachability limitation.
