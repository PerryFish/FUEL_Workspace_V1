# P2B Continuous Exploration Diagnosis

## Scope

Phase: `P2B_CONTINUOUS_EXPLORATION_COVERAGE_AND_STUCK_DIAGNOSIS`

Workspace: `/home/nuaa/ZHY/FUEL_PLANNER_V3`

Source commit: `3b11fc50c0ab8e84f9093f084ce80f4d1af6088d`

This phase did not redeploy or reclone FUEL. It focused on the office map continuous exploration behavior after P2A confirmed RViz visualization.

## Benchmark Commands

Primary 300s diagnostic run:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2b_office_300s ./scripts/run_p2b_office_300s_benchmark.sh
```

Post-fix 120s validation run:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2b_after_fix_office_120s ./scripts/run_continuous_exploration_benchmark.sh --map office --duration 120
```

## Key Logs

- `test-log/20260621_162703_p2b_office_300s.md`
- `test-log/20260621_163632_p2b_after_fix_office_120s.md`
- `test-log/20260621_163519_p2b_after_fix_build.md`
- `test-log/20260621_164031_p2b_smoke_v2_after_partial_fix.md`

## Metrics Directories

- Before fix 300s: `reports/p2b_metrics/p2b_office_300s_20260621_162703`
- After fix 120s: `reports/p2b_metrics/p2b_office_120s_20260621_163633`

## 300s Diagnosis Result

Result: `PARTIAL`

The exploration stack stayed alive and published odom, map clouds, local clouds, planner commands, and trajectories. Coverage increased initially, but the run then entered long periods where motion and coverage stalled even though planner outputs continued.

Key 300s metrics:

```text
duration_sec=304.609
odom_msg_count=26997
uav_total_distance=9.701m
uav_net_displacement=6.659m
planner_pos_cmd_count=6000
trajectory_count=6436
goal_msg_count=265
unique_goal_count=3
repeated_goal_count=262
frontier_candidate_count_last=131
explored_grid_start=1034
explored_grid_end=1565
coverage_proxy_gain=0.115226
stuck_event_count=51
max_no_motion_duration_sec=153.135
```

## Root Cause Evidence

The main stuck cause from `stuck_analysis.md` is `REPEATED_GOAL`.

At the end of the 300s run, the exploration manager status showed an invalid/aged active goal:

```text
active_goal_valid=false
goal_age=157
goal_distance=1.725
goal_timeout=true
switch_reason=goal_too_close_reselect
reason=goal_too_close_reselect
min_goal_distance=2.500
```

This means the active goal was too close/invalid and timed out, but the manager remained in a too-close reselection path instead of retiring the active goal and switching to a usable pending goal. Frontier candidates were still present, so the stall was not primarily caused by frontier exhaustion.

## Post-Fix Validation

After the minimal manager fix, the 120s run remained `PARTIAL` but improved early exploration:

```text
duration_sec=124.600
uav_total_distance=8.351m
uav_net_displacement=5.860m
goal_msg_count=240
unique_goal_count=4
repeated_goal_count=236
trajectory_count=2537
explored_grid_start=1359
explored_grid_end=1705
coverage_proxy_gain=0.125534
stuck_event_count=17
```

The fix improved goal switching and short-run coverage/motion, but it did not make the office exploration fully continuous. The repeated goal metric remains high partly because `/fuel/p11_lite/exploration_goal` republishes the active goal at runtime frequency; it should not be interpreted as 236 separate goal selection decisions.

## Conclusion

Current state: `PARTIAL`.

The system is not blocked by ROS2 discovery, RViz, odom, controller, or planner topic publication. The strongest evidence points to exploration manager goal retirement/switching behavior: repeated active goal publication and too-close invalid goals can leave the UAV in long coverage stalls even while trajectories are still being produced.
