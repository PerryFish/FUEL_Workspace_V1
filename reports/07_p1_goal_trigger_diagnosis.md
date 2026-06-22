# P1 Goal Trigger Diagnosis

Date: 2026-06-21

## Source-Level Topic Findings

The ROS2 port does not use the original ROS1 `/move_base_simple/goal` as the only internal trigger. The source and launch graph show:

- primary internal goal topic: `/fuel/p11_lite/exploration_goal`
- compatibility RViz/CLI topic: `/move_base_simple/goal`
- message type: `geometry_msgs/msg/PoseStamped`
- frame: `map`
- relevant launch: `src/FUEL/launch/fuel_p11_lite_core_exploration.launch.py`
- relevant bridge: `src/FUEL/scripts/p11_lite_goal_to_path_bridge.py`
- RViz fixed frame: `map`

The final smoke test showed both goal topics visible:

```text
/fuel/p11_lite/exploration_goal [geometry_msgs/msg/PoseStamped]
/move_base_simple/goal [geometry_msgs/msg/PoseStamped]
```

## Trigger Fix

`scripts/trigger_goal.sh` was enhanced to:

- source `scripts/env.sh`;
- detect visible goal topics;
- fall back to source-confirmed `/fuel/p11_lite/exploration_goal`;
- support `--topic`, `--frame`, `--x`, `--y`, `--z`, `--repeat`, and `--rate`;
- call `scripts/publish_goal_once.py` instead of a one-shot CLI publish.

`scripts/publish_goal_once.py` was added as an `rclpy` publisher. It publishes repeated `PoseStamped` goals with current ROS time by default.

Default command:

```bash
./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --x 5.0 --y 0.0 --z 1.2 --frame map --repeat 8 --rate 2.0
```

## Evidence

Key logs:

- `test-log/20260621_150355_p1_smoke_v2.md`
- `test-log/20260621_151517_p1_smoke_v2_final.md`

Final smoke v2 goal topic info showed subscribers:

```text
Topic type: geometry_msgs/msg/PoseStamped
Subscription count: 2
Node name: p11_lite_goal_to_path_bridge
Node name: p11_lite_visual_markers
```

The publisher emitted:

```text
GOAL_PUBLISHED topic=/fuel/p11_lite/exploration_goal frame=map x=5.000 y=0.000 z=1.200 seq=1/8
...
GOAL_PUBLISHED topic=/fuel/p11_lite/exploration_goal frame=map x=5.000 y=0.000 z=1.200 seq=8/8
```

## Current Diagnosis

```text
goal_topic_detected=PASS
goal_topic=/fuel/p11_lite/exploration_goal
compat_goal_topic=/move_base_simple/goal
goal_type=geometry_msgs/msg/PoseStamped
goal_frame=map
goal_publish=PASS
goal_received_by_planner=PASS_BY_SUBSCRIBER_GRAPH_AND_RELIABLE_REPEAT_PUBLISH
```

Note: FUEL also publishes autonomous exploration goals on `/fuel/p11_lite/exploration_goal`, so a post-publish probe can contain both manual and planner-generated goals. The reliable repeated publisher and subscriber graph are the current acceptance evidence for command-line goal delivery.

