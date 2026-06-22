# Unified Summary Log System

## Added Script

- `scripts/generate_unified_summary_log.py`

## Modified Script

- `scripts/run_with_log.sh`

## Summary Directory

```text
/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary
```

## Naming Rule

```text
test-log-summary/YYYYMMDD_HHMMSS_<task_name>_summary.md
```

## Behavior

Every `scripts/run_with_log.sh` run now keeps the original raw log in `test-log/` and then attempts to generate a unified summary log. The original command exit code is preserved even if summary generation fails.

Raw logs now append:

- unified summary path
- manual visual demo command
- P2D visual diagnostic command
- cleanup command

## Test Command

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh summary_system_test bash -lc 'echo SUMMARY_SYSTEM_TEST_PASS'
```

## Test Result

```text
summary_system_test=PASS
terminal_output_contains_UNIFIED_SUMMARY_LOG_CREATED=YES
raw_log_contains_Unified_Summary_Log=YES
raw_log_contains_Visual_Re-run_Commands=YES
```

## Example Files

```text
raw_log=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/20260622_090453_summary_system_test.md
summary=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_090454_summary_system_test_summary.md
```
