# P2I Summary Metrics Matching Fix

- result: PASS

## Root Cause
P2H/P2I route metrics are stored under `reports/p2h_metrics/<run_id>/route_rationality.json` and `reports/p2i_metrics/<run_id>/route_rationality.json`. The summary generator did not reliably resolve those route metrics from the raw log `run_id`, so some summaries showed `metrics_source=NONE`.

## Fix
- `scripts/generate_unified_summary_log.py` now searches `route_rationality.json`.
- It first parses `run_id=...` from the raw log and matches metrics by run_id.
- It falls back to recorder result blocks only when no current-run metrics file exists.
- `scripts/generate_full_run_log.py` includes route metrics and the common run command block.

## Evidence
- final 300s summary: `test-log-summary/20260622_143658_p2i_route_300s_after_fix_summary.md`
- metrics_source: CURRENT_RUN
- metrics_source_path: `reports/p2i_metrics/p2i_route_300s_after_fix_20260622_143133/route_rationality.json`
- matched_by: run_id

