#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="reports/FUEL_PLANNER_V3_P2B_DEBUG_PACKAGE_${STAMP}.tar.gz"
tar -czf "$OUT" \
  reports/19_p2b_continuous_exploration_diagnosis.md \
  reports/20_p2b_coverage_metric_report.md \
  reports/21_p2b_stuck_event_analysis.md \
  reports/22_p2b_goal_frontier_trajectory_analysis.md \
  reports/23_p2b_parameter_fix_report.md \
  reports/24_p2b_final_summary.md \
  reports/p2b_metrics \
  test-log/*p2b* \
  reports/*p2b* 2>/tmp/p2b_tar_warnings.txt || {
    cat /tmp/p2b_tar_warnings.txt >&2
    exit 1
  }
ln -sf "$(basename "$OUT")" reports/latest_p2b_debug_package.tar.gz
echo "P2B_DEBUG_PACKAGE_CREATED"
echo "$OUT"
echo "reports/latest_p2b_debug_package.tar.gz"
