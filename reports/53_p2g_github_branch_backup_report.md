# P2G GitHub Branch Backup Report

- backup_time: 2026-06-22T12:56:00+08:00
- workspace: `/home/nuaa/ZHY/FUEL_PLANNER_V3`
- remote_repo: `https://github.com/PerryFish/FUEL_Workspace_V1`
- branch: `backup/p2g-coverage-route-stable-20260622`
- commit_hash: `43fdf845085177b6a3acf5b05158ea9540fd454e` initial backup commit; final branch HEAD is reported after this report commit.
- tag: `v0.2.0-p2g-coverage-route-stable`
- push_result: PASS
- clone_test_result: PASS
- clone_test_path: `/tmp/fuel_workspace_v1_branch_clone_test/FUEL_Workspace_V1`
- test_log_summary_included: YES
- summary_md_count: 19
- full_log_md_count: 10
- excluded_large_files_summary: `build/`, `install/`, `log/`, `.ros/`, `*.tar.gz`, `*.zip`, `*.bag`, `*.db3`, and `*.mcap` are excluded by `.gitignore` or temporary Git metadata exclude rules.

## Clone Test Evidence

```text
SRC_EXISTS=YES
SCRIPTS_EXISTS=YES
REPORTS_EXISTS=YES
TEST_LOG_SUMMARY_EXISTS=YES
RUN_WITH_LOG_EXISTS=YES
VISUAL_SCRIPT_EXISTS=YES
P2G_VISUAL_SCRIPT_EXISTS=YES
SUMMARY_MD_COUNT=19
FULL_LOG_MD_COUNT=10
TAR_GZ_TRACKED_COUNT=0
BUILD_TRACKED_COUNT=0
```

## Recommended Clone Command

```bash
git clone --branch backup/p2g-coverage-route-stable-20260622 https://github.com/PerryFish/FUEL_Workspace_V1.git
cd FUEL_Workspace_V1
```

## Recommended Build Command

```bash
source /opt/ros/humble/setup.bash
./scripts/build.sh
```

## Recommended Visual Command

```bash
./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh
```

## Recommended Coverage Visual Command

```bash
cd /home/nuaa/ZHY/FUEL_PLANNER_V3
./scripts/run_with_log.sh p2g_visual_coverage_300s ./scripts/run_p2g_visual_coverage_300s.sh
```
