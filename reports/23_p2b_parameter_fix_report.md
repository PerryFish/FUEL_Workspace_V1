# P2B Parameter and Fix Report

## Fix Applied

`fix_applied=YES`

Modified file:

- `src/FUEL/scripts/exploration_manager_lite.py`

Related smoke-test robustness update:

- `scripts/run_headless_smoke_test_v2.sh`

New diagnostic tools:

- `scripts/fuel_continuous_exploration_recorder.py`
- `scripts/run_continuous_exploration_benchmark.sh`
- `scripts/run_p2b_office_300s_benchmark.sh`
- `scripts/run_p2b_visual_300s_demo.sh`
- `scripts/analyze_p2b_stuck_events.py`
- `scripts/export_p2b_debug_package.sh`

## Root Cause

The 300s benchmark showed the active goal could become too close/invalid while timed out. The `_tick()` decision order handled `too_close` before `timeout`, and the too-close branch held the active goal instead of switching to a usable pending candidate. This allowed long stalls with planner output still present.

## Code Change

In `ExplorationManagerLite._tick()`, the `too_close` branch now switches to a pending usable goal when the rate limit allows:

```text
reason=goal_too_close_switch
```

If a pending usable goal exists but the rate limit blocks switching, it reports:

```text
reason=goal_too_close_rate_limited
```

If there is no distinct pending viewpoint, it reports:

```text
reason=goal_too_close_waiting_for_distinct_viewpoint
```

This is a minimal goal-retirement fix. It does not change the map, local sensing, obstacle handling, collision assumptions, or core planner fake any success topic.

## Diff Files

- Before fix: `reports/p2b_before_fix_diff_20260621_162318.patch`
- After fix: `reports/p2b_after_fix_diff_20260621_164449.patch`
- Added recorder patch: `reports/p2b_added_recorder_20260621_164449.patch`
- Added analyzer patch: `reports/p2b_added_analyzer_20260621_164449.patch`

## Verification

Syntax:

```text
test-log/20260621_163519_p2b_after_fix_syntax.md PASS
test-log/20260621_164030_p2b_final_syntax.md PASS
```

Build:

```text
test-log/20260621_163519_p2b_after_fix_build.md PASS
```

Smoke v2:

```text
test-log/20260621_164031_p2b_smoke_v2_after_partial_fix.md PASS
```

## Before vs After

Before fix, office 300s:

```text
result=PARTIAL
uav_total_distance=9.701m
coverage_proxy_gain=0.115226
unique_goal_count=3
stuck_event_count=51
max_no_motion_duration_sec=153.135
```

After fix, office 120s:

```text
result=PARTIAL
uav_total_distance=8.351m
coverage_proxy_gain=0.125534
unique_goal_count=4
stuck_event_count=17
max_no_motion_duration_sec=83.464
```

## Recommendation

Keep this fix. It addresses a real goal lifecycle bug and improves early exploration. Do not treat it as a complete continuous-exploration solution yet. The next minimal work should add a more explicit local-minimum escape policy based on coverage stall plus distance from recent goals.
