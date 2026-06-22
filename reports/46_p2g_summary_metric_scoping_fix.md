# P2G Summary Metric Scoping Fix

- root_cause: `generate_unified_summary_log.py` previously searched recent metrics broadly and could bind old P2B/P2D/P2F metrics to a simple command.
- fix:
  - Metrics are only loaded if generated after the raw log start timestamp.
  - Metrics must match `run_id=` found in raw log, or the current task name in the metrics path.
  - If no current-run metrics match, `metrics_source=NONE` and all metric values remain `UNAVAILABLE`.
- modified_scripts:
  - `scripts/generate_unified_summary_log.py`
  - `scripts/run_with_log.sh`
- test_command: `./scripts/run_with_log.sh summary_system_test_clean bash -lc 'echo SUMMARY_SYSTEM_TEST_CLEAN_PASS'`
- raw_log: `test-log/20260622_114256_summary_system_test_clean.md`
- summary_log: `test-log-summary/20260622_114257_summary_system_test_clean_summary.md`
- full_log: `test-log-summary/20260622_114303_summary_system_test_clean_full_log.md`
- result: PASS
- metrics_source: NONE
- duration_sec: UNAVAILABLE
- main_chain_break: UNAVAILABLE
