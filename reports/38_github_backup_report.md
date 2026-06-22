# GitHub Backup Report

- backup_time: 2026-06-22T10:35:00+08:00
- workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- remote_repo: https://github.com/PerryFish/FUEL_Workspace_V1
- branch: main
- commit_hash: 11bfc13ad46106eedb5a35c2a26e28ac98c3667c
- tag: v0.1.0-fuel-planner-v3-stable
- files_added_count: 298
- files_changed_count: 0
- files_ignored_summary: build/, install/, log/, logs/, test-log/, .ros/, pycache, archives, rosbag files, local backup dirs, agent metadata
- push_result: PASS
- clone_test_result: PASS
- clone_test_path: /tmp/fuel_workspace_v1_clone_test/FUEL_Workspace_V1

## Notes

- The workspace `.git` directory is read-only in this managed environment, so backup Git metadata was created under `/tmp/fuel_workspace_v1_git` with `/home/nuaa/ZHY/FUEL_PLANNER_V3` as the work tree.
- Source RViz configs are present under `src/FUEL/rviz`, so `install/` is not required for backup.
- `test-log-summary/` was empty at backup time.
- Ordinary `git push -u origin main` and `git push origin --tags` succeeded; no force push was used.
- Clone verification confirmed `src/`, `scripts/`, `reports/`, `scripts/env.sh`, `scripts/run_with_log.sh`, and `scripts/run_manual_visual_demo_persistent.sh`.
- Clone verification confirmed excluded build outputs: `build/`, `install/`, and `log/` were not present.

## Recommended Clone Commands

```bash
git clone https://github.com/PerryFish/FUEL_Workspace_V1.git
cd FUEL_Workspace_V1
```

## Recommended Build Commands

```bash
source /opt/ros/humble/setup.bash
./scripts/build.sh
```

## Recommended Visual Run Command

```bash
./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh
```
