# P2A Manual Visual Demo Guide

Date: 2026-06-21

## Recommended One-Terminal Demo

Run:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2a_manual_visual ./scripts/run_manual_visual_demo_persistent.sh
```

The script:

1. cleans old FUEL/RViz processes;
2. uses the P1/P2A isolated DDS environment;
3. starts FUEL exploration;
4. starts `publish_rviz_map_tf.py --mode static_anchor`;
5. checks TF readiness;
6. starts RViz with `fuel_exploration_p2a_fixed_frame.rviz`;
7. publishes a goal;
8. starts `fuel_topic_probe.py`;
9. waits until you press Enter before cleanup.

Expected terminal text:

```text
MANUAL_VISUAL_DEMO_RUNNING
请在 RViz 中检查：
1. 是否不再出现 Frame [map] does not exist
2. 是否看到地图点云/障碍物
3. 是否看到 UAV marker
4. 是否看到轨迹
5. 是否看到 frontier/path/goal markers
确认完成后，在本终端按 Enter 清理退出。
```

Do not press Enter until you finish checking RViz.

## Multi-Terminal Manual Mode

Terminal 1:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export P2A_ROS_DOMAIN_ID=88
export P2A_ROS_LOCALHOST_ONLY=1
source scripts/env.sh
./scripts/run_exploration.sh
```

Terminal 2:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export P2A_ROS_DOMAIN_ID=88
export P2A_ROS_LOCALHOST_ONLY=1
source scripts/env.sh
python3 scripts/publish_rviz_map_tf.py --mode static_anchor
```

Terminal 3:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export P2A_ROS_DOMAIN_ID=88
export P2A_ROS_LOCALHOST_ONLY=1
source scripts/env.sh
rviz2 -d install/fuel_ros2/share/fuel_ros2/rviz/fuel_exploration_p2a_fixed_frame.rviz
```

Terminal 4:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
export P2A_ROS_DOMAIN_ID=88
export P2A_ROS_LOCALHOST_ONLY=1
source scripts/env.sh
./scripts/trigger_goal.sh --topic /fuel/p11_lite/exploration_goal --frame map --x 5.0 --y 0.0 --z 1.2
```

## Expected RViz Result

Check that:

```text
Frame [map] does not exist: should be gone
Map/obstacles: visible
UAV marker: visible
Travel trajectory/path markers: visible
Frontier/goal markers: visible
```

## Test Evidence

Automated non-interactive script test:

- `test-log/20260621_155800_p2a_manual_visual_demo_auto_enter.md`

Result:

```text
FUEL_MANUAL_VISUAL_DEMO_PERSISTENT_DONE
Exit Code 0
```

