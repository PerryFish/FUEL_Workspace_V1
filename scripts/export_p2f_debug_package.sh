#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="reports/FUEL_PLANNER_V3_P2F_DEBUG_PACKAGE_${STAMP}.tar.gz"
tar -czf "$OUT" \
  reports/39_p2f_unified_summary_log_fix_report.md \
  reports/40_p2f_coverage_completion_root_cause.md \
  reports/41_p2f_goal_reselect_after_path_done_design.md \
  reports/42_p2f_coverage_stall_recovery_fix_report.md \
  reports/43_p2f_coverage_300s_validation.md \
  reports/44_p2f_coverage_600s_validation.md \
  reports/45_p2f_final_summary.md \
  reports/p2f_metrics \
  test-log-summary \
  test-log \
  scripts/fuel_coverage_completion_recorder.py \
  scripts/run_p2f_coverage_300s_baseline.sh \
  scripts/run_p2f_coverage_300s_after_fix.sh \
  scripts/run_p2f_coverage_600s_after_fix.sh \
  scripts/run_p2f_visual_coverage_300s.sh \
  scripts/analyze_coverage_stall_and_goal_reselect.py 2>/dev/null || true
cp "$OUT" reports/latest_p2f_debug_package.tar.gz
echo "P2F_DEBUG_PACKAGE=$OUT"
