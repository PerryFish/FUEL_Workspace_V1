# 05 Final Usage Guide

Build:

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh build ./scripts/build.sh
```

Start exploration:

```bash
./scripts/run_with_log.sh exploration ./scripts/run_exploration.sh office
```

Start RViz2:

```bash
./scripts/run_with_log.sh rviz ./scripts/run_rviz.sh
```

Trigger goal:

```bash
./scripts/trigger_goal.sh
```

Map names:

```bash
./scripts/run_exploration.sh office
./scripts/run_exploration.sh office2
./scripts/run_exploration.sh office3
./scripts/run_exploration.sh pillar
```

Headless test:

```bash
./scripts/run_with_log.sh headless ./scripts/run_headless_smoke_test.sh
```

Visual check:

```bash
./scripts/run_with_log.sh visual ./scripts/run_visual_check.sh
```

Logs to send to ChatGPT if debugging continues:
- Latest `test-log/*build*.md`
- Latest `test-log/*headless*.md`
- Matching `test-log/headless_smoke_runtime_*.txt`
- Matching `test-log/headless_smoke_runtime_*.txt.launch`
- Latest `test-log/*visual*.md`
- All files in `reports/`

Current known blocker:
- The workspace builds and launch logs show planner activity, but ROS2 CLI discovery from this managed environment fails to see running FUEL topics. Verify from a normal host terminal before changing planner code.
