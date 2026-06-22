#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="reports/FUEL_PLANNER_V3_P2G_DEBUG_PACKAGE_${STAMP}.tar.gz"
tar -czf "$OUT" \
  reports/46_p2g_summary_metric_scoping_fix.md \
  reports/46a_p2g_full_run_log_system_fix.md \
  reports/47_p2g_frontier_reachability_root_cause.md \
  reports/48_p2g_frontier_scoring_design.md \
  reports/49_p2g_reachability_filter_fix_report.md \
  reports/50_p2g_coverage_300s_validation.md \
  reports/51_p2g_coverage_600s_validation.md \
  reports/52_p2g_final_summary.md \
  reports/p2g_metrics \
  test-log-summary \
  test-log \
  scripts/fuel_frontier_reachability_recorder.py \
  scripts/analyze_frontier_scoring_and_reachability.py \
  scripts/run_p2g_frontier_300s_baseline.sh \
  scripts/run_p2g_coverage_300s_after_fix.sh \
  scripts/run_p2g_coverage_600s_after_fix.sh \
  scripts/run_p2g_visual_coverage_300s.sh 2>/dev/null || true
cp "$OUT" reports/latest_p2g_debug_package.tar.gz
echo "P2G_DEBUG_PACKAGE=$OUT"
