# 04 Visual Demo Report

Visual check result: FAIL

Important logs:
- `test-log/20260621_142504_visual_check.md`
- `test-log/visual_check_runtime_20260621_142505.txt`
- `test-log/visual_check_runtime_20260621_142505.txt.rviz`
- `test-log/visual_check_runtime_20260621_142505.txt.exploration`

Checks:
- RViz2 process opened: YES
- Exploration launch started: launch log indicates YES
- Goal trigger: FAIL, `/move_base_simple/goal` was not discoverable by ROS2 CLI
- Map topic visible through CLI: NO
- UAV odom visible through CLI: NO
- Trajectory visible through CLI: NO
- Frontier/planning visualization visible through CLI: NO
- FOV/local sensing cloud visible through CLI: NO

Interpretation:
- RViz2 itself starts with DISPLAY `:0`.
- Algorithm launch logs show the simulation/planner nodes are running, but CLI/RViz discovery cannot be verified from this environment.
- This is not yet a confirmed visual reproduction of original FUEL.

Next action:
- Run `./scripts/run_rviz.sh` and `./scripts/run_exploration.sh office` in two normal host terminals.
- In a third host terminal, run `source scripts/env.sh && ros2 topic list`.
- If topics appear there, RViz should be checked manually for map, UAV, frontier, trajectory, FOV, and explored voxels.
