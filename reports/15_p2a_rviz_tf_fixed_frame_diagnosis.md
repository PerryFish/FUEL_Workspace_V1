# P2A RViz TF Fixed Frame Diagnosis

Date: 2026-06-21

Phase: `P2A_RVIZ_TF_FIXED_FRAME_VISUAL_FIX`

Workspace: `/home/nuaa/ZHY/FUEL_PLANNER_V3`

Source commit: `3b11fc50c0ab8e84f9093f084ce80f4d1af6088d`

## Symptom

The desktop RViz screenshot showed:

```text
Fixed Frame
No tf data. Actual error: Frame [map] does not exist.
```

P1 had already shown that FUEL headless planner, DDS discovery, goal publishing, planner topics, odom, and motion can work. Therefore this phase isolated RViz TF/fixed-frame readiness and display topic configuration.

## Diagnosis

The FUEL ROS2 port publishes most visualization messages in frame `map`, but RViz requires `map` to be present in TF. If RViz starts after the static TF is missed, or with a different ROS environment/domain, it can report `Frame [map] does not exist` even while marker/cloud topics exist.

Existing source also contains `p11_lite_frame_publisher.py`, which publishes `map -> odom`. For P2A, an independent RViz-safe static anchor was added:

```text
map -> fuel_rviz_anchor
```

This creates the `map` frame for RViz without changing planner, odom, controller, simulator, or algorithm behavior.

## Evidence

Key logs:

- `test-log/20260621_154328_p2a_rviz_tf_probe_2.md`
- `test-log/20260621_155151_p2a_visual_check_v3_fixed.md`

TF evidence:

```text
/tf_static [tf2_msgs/msg/TFMessage]
frame_id: map
child_frame_id: fuel_rviz_anchor
TF_STATIC_EXISTS=YES
MAP_FRAME_EXISTS=YES
FUEL_RVIZ_ANCHOR_FRAME_EXISTS=YES
RVIZ_FIXED_FRAME_READY=YES
P2A_TF_TREE_CHECK_PASS
```

`/tf` dynamic topic is not required for this fixed-frame repair:

```text
TF_TOPIC_EXISTS=NO
TF_STATIC_EXISTS=YES
```

`base_link` is not introduced in the default P2A static-anchor mode to avoid conflicting with future odom/simulator TF. RViz fixed frame only needs `map` to exist; the map, marker, path, cloud, and odom messages already use `frame=map`.

## Current Status

```text
tf_topic_exists=NO
tf_static_exists=YES
map_frame_exists=YES
odom_frame_exists=NO
base_link_frame_exists=NO
fuel_rviz_anchor_frame_exists=YES
rviz_fixed_frame_ready=YES
rviz_fixed_frame_error_fixed=YES_BY_TF_STATIC_ANCHOR
```

