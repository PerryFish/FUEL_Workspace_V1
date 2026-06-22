# P2F Coverage 600s Validation

- status: NOT_RUN
- reason: Final 300s after-fix validation did not show stable improvement over baseline. Per P2F instructions, 600s validation was skipped to avoid spending time on a longer run before addressing the remaining blocker.
- next_required_condition_for_600s: A 300s after-fix run should show `coverage_stall_max_duration_sec < 90`, `odom_total_distance >= 25m`, and `main_coverage_blocker=COVERAGE_GROWING` or `COVERAGE_SATURATED`.
