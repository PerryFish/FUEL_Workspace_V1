# GitHub Backup Report

- backup_time: pending
- workspace: /home/nuaa/ZHY/FUEL_PLANNER_V3
- remote_repo: https://github.com/PerryFish/FUEL_Workspace_V1
- branch: main
- commit_hash: pending
- tag: pending
- files_added_count: pending
- files_changed_count: pending
- files_ignored_summary: build/, install/, log/, logs/, test-log/, .ros/, pycache, archives, rosbag files, local backup dirs, agent metadata
- push_result: pending
- clone_test_result: pending
- clone_test_path: /tmp/fuel_workspace_v1_clone_test/FUEL_Workspace_V1

## Notes

- The workspace `.git` directory is read-only in this managed environment, so backup Git metadata was created under `/tmp/fuel_workspace_v1_git` with `/home/nuaa/ZHY/FUEL_PLANNER_V3` as the work tree.
- Source RViz configs are present under `src/FUEL/rviz`, so `install/` is not required for backup.
- `test-log-summary/` was empty at backup time.

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
