# P2B Goal Frontier Trajectory Analysis

## Before Fix: Office 300s

Metrics directory: `reports/p2b_metrics/p2b_office_300s_20260621_162703`

```text
goal_msg_count=265
unique_goal_count=3
repeated_goal_count=262
goal_switch_count=2
average_goal_distance=0.014610
min_goal_distance=0.000000
max_goal_distance=2.132016
frontier_candidate_count_start=0
frontier_candidate_count_end=131
frontier_viewpoint_count_start=0
frontier_viewpoint_count_end=42
planner_pos_cmd_count=6000
trajectory_count=6436
trajectory_update_rate=21.129Hz
```

The frontier candidates and planner trajectories continued to publish. The low `unique_goal_count` and high repeated goal samples show that the manager was not effectively retiring or replacing goals after progress stopped.

## After Fix: Office 120s

Metrics directory: `reports/p2b_metrics/p2b_office_120s_20260621_163633`

```text
goal_msg_count=240
unique_goal_count=4
repeated_goal_count=236
goal_switch_count=3
average_goal_distance=0.042577
min_goal_distance=0.000000
max_goal_distance=4.599218
frontier_candidate_count_start=0
frontier_candidate_count_end=123
frontier_viewpoint_count_start=0
frontier_viewpoint_count_end=42
planner_pos_cmd_count=2399
trajectory_count=2537
trajectory_update_rate=20.361Hz
```

The post-fix run selected more unique goals in less time and produced a larger max goal transition distance. This is the expected effect of switching away from too-close active goals.

## Important Caveat

`repeated_goal_count` is inflated because `/fuel/p11_lite/exploration_goal` represents the current active exploration goal and is published repeatedly. It is still useful as a stall signal when combined with:

- low `unique_goal_count`
- no coverage growth
- no motion over a 20s window
- manager status showing `goal_too_close` or `goal_timeout`

## Conclusion

Planner output is healthy. Frontier output exists. The remaining bottleneck is robust goal lifecycle management under local-minimum conditions.
