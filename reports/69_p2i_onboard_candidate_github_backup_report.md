# P2I Onboard Candidate GitHub Backup Report

- backup_time: 2026-06-22T14:58:00+08:00
- workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- remote_repo: https://github.com/PerryFish/FUEL_Workspace_V1
- branch: backup/p2i-onboard-candidate-20260622
- commit_hash: 6094405c7b54682e2317bac341bf4a7284b29f01
- tag: v0.3.0-p2i-onboard-candidate
- push_branch_result: PASS
- push_tags_result: PASS
- clone_test_result: PASS
- clone_test_path: /tmp/fuel_workspace_v1_p2i_onboard_clone_test/FUEL_Workspace_V1
- test_log_summary_included: YES
- summary_md_count: 42
- full_log_md_count: 33
- src_exists: YES
- scripts_exists: YES
- reports_exists: YES
- build_install_log_excluded: YES
- debug_tar_excluded: YES

## Recommended Clone Command

```bash
git clone --branch backup/p2i-onboard-candidate-20260622 https://github.com/PerryFish/FUEL_Workspace_V1.git
cd FUEL_Workspace_V1
```

## Recommended Build Command

```bash
source /opt/ros/humble/setup.bash
./scripts/build.sh
```

## Recommended Full Visual Run Command

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_visual_route_full ./scripts/run_p2i_visual_route_full.sh
```

## Recommended 300s Visual Run Command

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_visual_route_300s ./scripts/run_p2i_visual_route_300s.sh
```

## Recommended 300s Headless Run Command

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_route_300s_after_fix ./scripts/run_p2i_route_300s_after_fix.sh
```

## Recommended 900s Headless Run Command

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2i_route_900s_after_fix ./scripts/run_p2i_route_900s_after_fix.sh
```

## Clean Command

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/kill_fuel.sh
```

## Known Limitations

- 300s headless route validation PASS.
- Visual route 300s is PARTIAL_WITH_RVIZ_CRASH because RViz may core dump in current desktop environment.
- 900s long-run validation currently FAIL / early stopped due to long-run no-path watchdog recovery not fully solved.
- This branch is an onboard-candidate backup, not final onboard release.
- Do not connect to real flight controller until real localization/mapping/control interface tests are completed.

