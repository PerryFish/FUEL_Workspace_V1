# P2G Full Run Log System Fix

## Root Cause

The previous logging system produced a raw log and a structured summary, but not a single comprehensive Markdown artifact containing raw command output, runtime snapshots, metrics content, and re-run commands. P2E also used a single-purpose runner that bypassed `run_with_log.sh`, so `test-log-summary/` could appear incomplete.

## Summary Log vs Full Log

- `*_summary.md`: compact structured status, metrics, diagnosis, generated files, and next action.
- `*_full_log.md`: complete debugging artifact with environment, git/process/ROS snapshots, raw log content, matched metrics files, generated reports, debug package paths, and visual re-run commands.

## New Script

- `scripts/generate_full_run_log.py`

## Modified Scripts

- `scripts/generate_unified_summary_log.py`
- `scripts/run_with_log.sh`

## Test Command

```bash
./scripts/run_with_log.sh summary_full_log_system_test bash -lc 'echo SUMMARY_AND_FULL_LOG_TEST_PASS'
```

## Generated Logs

- summary_log: `test-log-summary/20260622_114156_summary_full_log_system_test_summary.md`
- full_log: `test-log-summary/20260622_114201_summary_full_log_system_test_full_log.md`

## Acceptance Result

- terminal output contains `UNIFIED_SUMMARY_LOG_CREATED=...`: YES
- terminal output contains `FULL_RUN_LOG_CREATED=...`: YES
- raw log contains both markers: YES
- full log contains raw command output: YES
- full log contains visual re-run commands: YES
- summary metrics_source for clean command is NONE: YES
