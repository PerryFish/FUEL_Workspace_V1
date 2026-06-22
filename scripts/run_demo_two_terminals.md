# FUEL ROS2 Demo In Two Terminals

Terminal 1:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh exploration ./scripts/run_exploration.sh office
```

Terminal 2:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh rviz ./scripts/run_rviz.sh
./scripts/trigger_goal.sh
```

Map choices: `office`, `office2`, `office3`, `pillar`.
