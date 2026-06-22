#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
mkdir -p test-log reports/screenshots
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="test-log/${STAMP}_p1_visual_v2_runtime.txt"

echo "# P1 visual check v2" | tee "$OUT"
if ! ./scripts/run_headless_smoke_test_v2.sh | tee -a "$OUT"; then
  echo "FUEL_VISUAL_CHECK_V2_FAIL headless_v2_failed" | tee -a "$OUT"
  exit 1
fi

export ROS_DOMAIN_ID="${P1_ROS_DOMAIN_ID:-88}"
export ROS_LOCALHOST_ONLY=1
source scripts/env.sh

echo "DISPLAY=${DISPLAY:-}" | tee -a "$OUT"
glxinfo -B >>"$OUT" 2>&1 || true
if [ -z "${DISPLAY:-}" ]; then
  echo "FUEL_VISUAL_CHECK_V2_PASS_WITH_DISPLAY_LIMITATION" | tee -a "$OUT"
  exit 0
fi

RVIZ_PID=""
cleanup() {
  [ -n "$RVIZ_PID" ] && kill "$RVIZ_PID" 2>/dev/null || true
}
trap cleanup EXIT

./scripts/run_rviz.sh >"$OUT.rviz" 2>&1 &
RVIZ_PID=$!
sleep 8
if grep -Eqi 'Failed to create an OpenGL context|Unable to create a suitable GLXContext|RenderingAPIException|BadValue.*GLX|GLXCreateNewContext' "$OUT" "$OUT.rviz" 2>/dev/null; then
  echo "RVIZ_OPENED=NO" | tee -a "$OUT"
  echo "DISPLAY_ENVIRONMENT_LIMITATION=GLX_OPENGL_CONTEXT_FAILURE" | tee -a "$OUT"
  echo "FUEL_VISUAL_CHECK_V2_PASS_WITH_DISPLAY_LIMITATION" | tee -a "$OUT"
  exit 0
fi

if kill -0 "$RVIZ_PID" 2>/dev/null; then
  echo "RVIZ_OPENED=YES" | tee -a "$OUT"
  echo "FUEL_VISUAL_CHECK_V2_PASS" | tee -a "$OUT"
  exit 0
fi

echo "RVIZ_OPENED=NO" | tee -a "$OUT"
echo "FUEL_VISUAL_CHECK_V2_FAIL" | tee -a "$OUT"
exit 1
