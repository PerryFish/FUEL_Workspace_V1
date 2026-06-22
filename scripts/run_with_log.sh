#!/usr/bin/env bash
set -uo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <task_name> <command> [args...]" >&2
  exit 2
fi

TASK_NAME="$1"
shift
COMMAND_STRING="$*"

FUEL_WS="${FUEL_WS:-/home/nuaa/ZHY/FUEL_PLANNER_V3}"
LOG_DIR="$FUEL_WS/test-log"
mkdir -p "$LOG_DIR"

SAFE_TASK="$(echo "$TASK_NAME" | tr -cs 'A-Za-z0-9._-' '_' | sed 's/^_//;s/_$//')"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$LOG_DIR/${STAMP}_${SAFE_TASK}.md"
TMP_OUT="$(mktemp /tmp/fuel_run_log.XXXXXX)"

collect_metadata() {
  {
    echo "# FUEL Run Log"
    echo
    echo "## Metadata"
    echo "- Date: $(date -Is)"
    echo "- Host: $(hostname)"
    echo "- User: $(whoami)"
    echo "- Workspace: $FUEL_WS"
    echo "- Pwd: $(pwd)"
    echo "- Shell: ${SHELL:-unknown}"
    echo "- Command: $*"
    echo "- Log file: $LOG_FILE"
    echo
    echo "## Environment"
    echo '```bash'
    env | sort | grep -E '^(ROS|RMW|FUEL|AMENT|COLCON|DISPLAY|WAYLAND|LD_LIBRARY_PATH|PYTHONPATH)=' || true
    echo '```'
    echo
    echo "## Git"
    echo '```bash'
    if [ -d "$FUEL_WS/src/FUEL/.git" ]; then
      git -C "$FUEL_WS/src/FUEL" status --short || true
      echo "branch=$(git -C "$FUEL_WS/src/FUEL" branch --show-current 2>/dev/null || true)"
      echo "commit=$(git -C "$FUEL_WS/src/FUEL" rev-parse HEAD 2>/dev/null || true)"
    else
      echo "src/FUEL is not a git repository yet"
    fi
    echo '```'
    echo
    echo "## Colcon Packages"
    echo '```text'
    if command -v colcon >/dev/null 2>&1 && [ -d "$FUEL_WS/src" ]; then
      (cd "$FUEL_WS" && colcon list 2>&1) || true
    else
      echo "colcon unavailable or src missing"
    fi
    echo '```'
    echo
    echo "## Command Output"
    echo '```text'
  } > "$LOG_FILE"
}

collect_metadata "$@"

set +e
(
  cd "$FUEL_WS" || exit 1
  "$@"
) > >(tee "$TMP_OUT") 2>&1
EXIT_CODE=$?
set -e

cat "$TMP_OUT" >> "$LOG_FILE"
{
  echo '```'
  echo
  echo "## Exit Code"
  echo "$EXIT_CODE"
  echo
  echo "## Result"
  if [ "$EXIT_CODE" -eq 0 ]; then
    echo "PASS"
  else
    echo "FAIL"
  fi
  echo
  echo "## Next Action"
  if [ "$EXIT_CODE" -eq 0 ]; then
    echo "- Continue with the next deployment or verification phase."
  else
    echo "- Inspect the command output above."
    echo "- For build failures, check missing headers/packages, ROS1 API remnants, CMake/package.xml dependencies, and linker errors."
    echo "- For runtime failures, check node list, topic remaps, frame IDs, map file paths, and DISPLAY/GLX state."
  fi
} >> "$LOG_FILE"

SUMMARY_PATH=""
SUMMARY_STATUS=0
if [ -f "$FUEL_WS/scripts/generate_unified_summary_log.py" ]; then
  SUMMARY_OUTPUT="$(python3 "$FUEL_WS/scripts/generate_unified_summary_log.py" \
    --task-name "$TASK_NAME" \
    --command "$COMMAND_STRING" \
    --exit-code "$EXIT_CODE" \
    --raw-log "$LOG_FILE" \
    --workspace "$FUEL_WS" 2>&1)"
  SUMMARY_STATUS=$?
  echo "$SUMMARY_OUTPUT"
  if [ "$SUMMARY_STATUS" -eq 0 ]; then
    SUMMARY_PATH="$(printf '%s\n' "$SUMMARY_OUTPUT" | awk -F= '/^UNIFIED_SUMMARY_LOG_CREATED=/{print $2}' | tail -1)"
    {
      echo
      echo "## Unified Summary Log"
      echo
      echo '```text'
      echo "$SUMMARY_PATH"
      echo '```'
      echo
      echo "## Visual Re-run Commands"
      echo
      echo "Manual persistent visual demo:"
      echo
      echo '```bash'
      echo "cd /home/nuaa/ZHY/FUEL_PLANNER_V3"
      echo "./scripts/run_with_log.sh visual_manual ./scripts/run_manual_visual_demo_persistent.sh"
      echo '```'
      echo
      echo "300s visual diagnostic demo:"
      echo
      echo '```bash'
      echo "cd /home/nuaa/ZHY/FUEL_PLANNER_V3"
      echo "./scripts/run_with_log.sh p2d_visual_300s ./scripts/run_p2d_visual_300s_demo.sh"
      echo '```'
      echo
      echo "Clean all FUEL/RViz processes:"
      echo
      echo '```bash'
      echo "cd /home/nuaa/ZHY/FUEL_PLANNER_V3"
      echo "./scripts/kill_fuel.sh"
      echo '```'
    } >> "$LOG_FILE"
  else
    {
      echo
      echo "## Unified Summary Log"
      echo
      echo "UNIFIED_SUMMARY_LOG_FAILED=$SUMMARY_OUTPUT"
    } >> "$LOG_FILE"
  fi
else
  {
    echo
    echo "## Unified Summary Log"
    echo
    echo "UNIFIED_SUMMARY_LOG_FAILED=summary_generator_missing"
  } >> "$LOG_FILE"
fi

rm -f "$TMP_OUT"
echo "[run_with_log] log=$LOG_FILE"
exit "$EXIT_CODE"
