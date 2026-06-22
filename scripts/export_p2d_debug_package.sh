#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="reports/FUEL_PLANNER_V3_P2D_DEBUG_PACKAGE_${STAMP}.tar.gz"
tar -czf "$OUT" \
  reports/30_p2d_motion_chain_root_cause.md \
  reports/31_p2d_path_feasibility_analysis.md \
  reports/32_p2d_traj_server_stale_path_analysis.md \
  reports/33_p2d_position_cmd_vs_odom_analysis.md \
  reports/34_p2d_fix_implementation_report.md \
  reports/35_p2d_before_after_300s_comparison.md \
  reports/36_p2d_final_summary.md \
  reports/37_unified_summary_log_system.md \
  reports/p2d_metrics \
  test-log/*p2d* \
  test-log-summary/*p2d* \
  reports/*p2d* 2>/tmp/p2d_tar_warnings.txt || {
    cat /tmp/p2d_tar_warnings.txt >&2
    exit 1
  }
ln -sf "$(basename "$OUT")" reports/latest_p2d_debug_package.tar.gz
echo "P2D_DEBUG_PACKAGE_CREATED"
echo "$OUT"
echo "reports/latest_p2d_debug_package.tar.gz"
