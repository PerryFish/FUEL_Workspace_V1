#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="reports/FUEL_PLANNER_V3_P2H_DEBUG_PACKAGE_${STAMP}.tar.gz"
tar -czf "$OUT" \
  reports/54_p2h_route_rationality_root_cause.md \
  reports/55_p2h_official_fuel_reference_analysis.md \
  reports/56_p2h_path_aware_scoring_design.md \
  reports/57_p2h_route_rationality_fix_report.md \
  reports/58_p2h_300s_validation.md \
  reports/59_p2h_visual_route_review.md \
  reports/60_p2h_final_summary.md \
  reports/p2h_metrics \
  test-log-summary \
  test-log \
  reports/*p2h* \
  scripts/fuel_route_rationality_recorder.py \
  scripts/analyze_route_rationality.py \
  scripts/run_p2h_route_300s_baseline.sh \
  scripts/run_p2h_route_300s_after_fix.sh \
  scripts/run_p2h_visual_route_300s.sh 2>/dev/null || true
cp "$OUT" reports/latest_p2h_debug_package.tar.gz
echo "P2H_DEBUG_PACKAGE=$OUT"
