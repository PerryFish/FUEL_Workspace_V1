# P2F Unified Summary Log Fix Report

- root_cause_of_no_summary_log: Previous P2E single-md runner intentionally bypassed `scripts/run_with_log.sh`, and `generate_unified_summary_log.py` also reused old metrics when no current-run metrics existed, which made summary status misleading.
- modified_scripts:
  - `scripts/generate_unified_summary_log.py`
  - `scripts/run_with_log.sh`
- test_command: `./scripts/run_with_log.sh summary_system_test bash -lc 'echo SUMMARY_SYSTEM_TEST_PASS'`
- raw_log_path: `test-log/20260622_104637_summary_system_test.md`
- summary_log_path: `test-log-summary/20260622_104638_summary_system_test_summary.md`
- test_result: PASS

## Verification

- `test-log-summary/` exists.
- `UNIFIED_SUMMARY_LOG_CREATED=/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log-summary/20260622_104638_summary_system_test_summary.md` was printed.
- Raw log contains `## Unified Summary Log`.
- Raw log contains P2F visual re-run commands.
- Summary file contains required Basic Info, Environment, Git / Source State, Key Runtime Evidence, Metrics Summary, Generated Files, Diagnosis, Visual Re-run Commands, and Next Action sections.
- Missing metrics are written as `UNAVAILABLE`.

## Notes

- Git status is scoped to `/home/nuaa/ZHY/FUEL_PLANNER_V3` with `git -C <workspace> status --short -- .`.
- The workspace still inherits a parent Git repository rooted at `/home/nuaa`; this report does not change Git configuration or push to GitHub.
