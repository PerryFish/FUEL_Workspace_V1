#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p reports
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="reports/FUEL_PLANNER_V3_P2I_DEBUG_PACKAGE_${STAMP}.tar.gz"
tar -czf "$OUT" \
  reports/61_p2i_run_command_system_fix.md \
  reports/62_p2i_summary_metrics_matching_fix.md \
  reports/63_p2i_rviz_crash_detection_fix.md \
  reports/64_p2i_endpoint_outlier_route_revisit_fix.md \
  reports/65_p2i_300s_validation.md \
  reports/66_p2i_900s_validation.md \
  reports/67_p2i_final_summary.md \
  reports/68_p2i_goal_without_path_diagnosis_and_fix.md \
  reports/p2i_metrics \
  test-log-summary/*p2i* \
  test-log/*p2i* \
  reports/*p2i* \
  scripts/run_p2i_route_300s_after_fix.sh \
  scripts/run_p2i_visual_route_300s.sh \
  scripts/run_p2i_route_900s_after_fix.sh \
  scripts/run_p2i_visual_route_full.sh \
  scripts/run_p2i_route_full.sh \
  scripts/print_fuel_run_commands.sh 2>/dev/null || true
cp "$OUT" reports/latest_p2i_debug_package.tar.gz
echo "P2I_DEBUG_PACKAGE=$OUT"
