# P2C Goal Lifecycle Root Cause

## Source Audit

File audited:

- `src/FUEL/scripts/exploration_manager_lite.py`

The manager sets `active_goal` from `/fuel/p11_lite/best_viewpoint`, publishes `/fuel/p11_lite/exploration_goal`, and reports `/fuel/p11_lite/exploration_manager_status`.

Relevant code paths after P2B:

- `_best_cb()` stores `pending_best`.
- `_pending_is_usable()` checks pending/active separation and distance from odom.
- `_switch_to_pending()` retires current active goal and activates the pending best viewpoint.
- `_tick()` decides between reached, too-close, timeout, better-pending, and hold states.

P2B root-cause evidence showed an active goal with:

```text
active_goal_valid=false
goal_age=157
goal_distance=1.725
goal_timeout=true
switch_reason=goal_too_close_reselect
min_goal_distance=2.500
```

The important detail is `goal_distance=1.725` while `min_goal_distance=2.500`. That goal was not within the reached radius of 0.8m, but it was considered too close/invalid and could stop being published. This explains why a goal could be neither reached nor useful.

## Runtime Evidence

P2B 300s baseline:

```text
uav_total_distance=9.701m
coverage_proxy_gain=0.115226
unique_goal_count=3
stuck_event_count=51
main_stuck_cause=REPEATED_GOAL
```

P2C aggressive escape attempt:

```text
run_id=p2c_after_office_300s_20260621_171817
uav_total_distance=1.179m
coverage_proxy_gain=0.083935
goal_switch_count=53
escape_goal_count=50
true_repeated_goal_count=40
```

This proved that simply switching goals more often is not enough. Raw frontier-point escape caused many goal switches but little motion.

P2C conservative threshold attempt:

```text
run_id=p2c_after_office_300s_20260621_173224
uav_total_distance=2.663m
coverage_proxy_gain=0.109851
goal_switch_count=3
same_goal_max_duration_sec=238.998
escape_goal_count=1
```

This reduced true repeated-goal churn, but the same active goal was held too long and exploration still stalled.

## Root Cause After P2C

The root cause is broader than active goal retirement alone:

```text
root_cause_after_p2c=goal lifecycle contributes to stalls, but after threshold fixes the dominant symptom is same-goal hold with continued trajectory publication and poor physical progress
```

The next investigation should focus on path feasibility and traj_server/controller acceptance of repeatedly updated trajectories near local minima.
