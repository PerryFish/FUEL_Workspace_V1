# P2B Stuck Event Analysis

## Detection Rules

The recorder marks:

- `MOTION_STUCK`: 20s displacement below 0.2m while planner output continues.
- `COVERAGE_STALL`: frontier count stable and coverage proxy gain below 0.01 over the stall window.
- `REPEATED_GOAL`: consecutive goal samples within 0.5m.
- `PLANNER_STALL`: trajectory count does not advance.
- `FRONTIER_EMPTY`: frontier count stays at zero long enough to block exploration.

## Before Fix: Office 300s

Analyzer output: `reports/p2b_metrics/p2b_office_300s_20260621_162703/stuck_analysis.md`

```text
main_stuck_cause=REPEATED_GOAL
stuck_event_count=51
event_counts={'COVERAGE_STALL': 12, 'MOTION_STUCK': 51, 'REPEATED_GOAL': 25}
max_no_motion_duration_sec=153.135
uav_total_distance=9.701m
trajectory_count=6436
coverage_proxy_gain=0.115226
```

Representative event sequence:

- Early repeated-goal events appeared around `t=1.8s` to `t=113.3s`.
- Motion improved briefly around `t=119s` to `t=129s`.
- A long late stall started around `t=146s` and continued to the end of the run.
- During the late stall, frontier candidates remained available, ending at 131 candidates.

Most likely cause: the active goal became too close/invalid and timed out, but goal retirement did not switch to a fresh usable viewpoint.

## After Fix: Office 120s

Analyzer output: `reports/p2b_metrics/p2b_office_120s_20260621_163633/stuck_analysis.md`

```text
main_stuck_cause=REPEATED_GOAL
stuck_event_count=17
event_counts={'COVERAGE_STALL': 4, 'MOTION_STUCK': 17, 'REPEATED_GOAL': 22}
max_no_motion_duration_sec=83.464
uav_total_distance=8.351m
trajectory_count=2537
coverage_proxy_gain=0.125534
```

The post-fix run still detects repeated goal samples and motion-stuck windows, but it covers more area and travels farther during a shorter test. This supports the fix as an improvement, not a full solution.

## Cause Classification

```text
REPEATED_GOAL=YES
GOAL_TOO_CLOSE=YES
FRONTIER_EMPTY=NO
FRONTIER_NOT_UPDATED=PARTIAL
PLANNER_STALL=NO
CONTROLLER_OR_SIM_STALL=NO
COVERAGE_SATURATED=NO
LOCAL_MINIMUM=LIKELY
UNKNOWN=NO
```

Planner and controller topics were active throughout the runs. The core issue is goal selection/retirement behavior under local minima, not a broken simulation command chain.
