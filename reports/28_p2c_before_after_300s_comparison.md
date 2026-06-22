# P2C Before After 300s Comparison

## Summary

P2C did not improve over the P2B 300s baseline. It generated better lifecycle diagnostics and showed that aggressive escape can hurt motion. The final conservative fix still stalled.

| metric | P2B_before_300s | P2C_after_300s | change | result |
|---|---:|---:|---:|---|
| uav_total_distance | 9.701m | 2.663m | -7.038m | worse |
| uav_net_displacement | 6.659m | 2.554m | -4.105m | worse |
| raw_goal_msg_count | not measured | 600 | n/a | measured |
| unique_goal_count_quantized_1p0m | not measured | 4 | n/a | below target |
| goal_switch_count | 2 legacy | 3 lifecycle | +1 | insufficient |
| same_goal_max_duration_sec | not measured | 238.998 | n/a | fail |
| true_repeated_goal_count | not measured | 0 | n/a | improved metric only |
| goal_republish_count | not measured | 596 | n/a | high |
| goal_retire_event_count | not measured | 3 | n/a | low |
| escape_goal_count | 0 | 1 | +1 | insufficient |
| stuck_event_count | 51 | 54 | +3 | worse |
| coverage_proxy_gain | 0.115226 | 0.109851 | -0.005375 | worse |
| trajectory_count | 6436 | 6112 | -324 | acceptable |
| frontier_count_end | 131 | 124 | -7 | acceptable |
| fatal_crash | NO | NO | none | pass |

## P2C Attempted Run: Aggressive Escape

Run:

```text
reports/p2c_metrics/p2c_after_office_300s_20260621_171817
```

It produced:

```text
uav_total_distance=1.179m
unique_goal_count_quantized_1p0m=12
goal_switch_count=53
escape_goal_count=50
true_repeated_goal_count=40
```

This proves goal diversity alone does not guarantee movement. It likely selected path-infeasible or poor local-minimum escape goals.

## Final P2C Run

Run:

```text
reports/p2c_metrics/p2c_after_office_300s_20260621_173224
```

Result:

```text
office_300s_after_fix=PARTIAL
main_goal_lifecycle_cause=SAME_GOAL_HELD_TOO_LONG
main_stuck_cause=REPEATED_GOAL
```

## Conclusion

`P2C_PARTIAL_NOT_IMPROVED`

The current minimum safe changes did not meet the target thresholds:

```text
uav_total_distance > 10m: FAIL
coverage_proxy_gain >= 0.12: FAIL
goal_switch_count >= 5: FAIL
unique_goal_count_quantized_1p0m >= 5: FAIL
stuck_event_count < P2B baseline: FAIL
```
