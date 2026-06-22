#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="reports/FUEL_PLANNER_V3_P2C_DEBUG_PACKAGE_${STAMP}.tar.gz"
tar -czf "$OUT" \
  reports/25_p2c_goal_lifecycle_root_cause.md \
  reports/26_p2c_local_minimum_escape_design.md \
  reports/27_p2c_fix_implementation_report.md \
  reports/28_p2c_before_after_300s_comparison.md \
  reports/29_p2c_final_summary.md \
  reports/p2c_metrics \
  test-log/*p2c* \
  reports/*p2c* 2>/tmp/p2c_tar_warnings.txt || {
    cat /tmp/p2c_tar_warnings.txt >&2
    exit 1
  }
ln -sf "$(basename "$OUT")" reports/latest_p2c_debug_package.tar.gz
echo "P2C_DEBUG_PACKAGE_CREATED"
echo "$OUT"
echo "reports/latest_p2c_debug_package.tar.gz"
