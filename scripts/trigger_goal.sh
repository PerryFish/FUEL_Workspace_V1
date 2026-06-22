#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
source scripts/env.sh >/dev/null

TOPIC="${GOAL_TOPIC:-}"
FRAME_ID="${FRAME_ID:-map}"
X="${GOAL_X:-5.0}"
Y="${GOAL_Y:-0.0}"
Z="${GOAL_Z:-1.2}"
REPEAT="${GOAL_REPEAT:-5}"
RATE="${GOAL_RATE:-2.0}"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --topic) TOPIC="$2"; shift 2 ;;
    --frame) FRAME_ID="$2"; shift 2 ;;
    --x) X="$2"; shift 2 ;;
    --y) Y="$2"; shift 2 ;;
    --z) Z="$2"; shift 2 ;;
    --repeat) REPEAT="$2"; shift 2 ;;
    --rate) RATE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--topic TOPIC] [--frame map] [--x 5.0] [--y 0.0] [--z 1.2] [--repeat 5] [--rate 2.0]"
      exit 0
      ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$TOPIC" ]; then
  CANDIDATES=(
    /move_base_simple/goal
    move_base_simple/goal
    /goal
    /waypoint_generator/goal
    /planning/goal
    /fuel/p11_lite/exploration_goal
  )
  VISIBLE="$(timeout 8 ros2 topic list --no-daemon --spin-time 4 2>/dev/null || true)"
  for candidate in "${CANDIDATES[@]}"; do
    if echo "$VISIBLE" | grep -qx "$candidate"; then
      TOPIC="$candidate"
      break
    fi
  done
fi

if [ -z "$TOPIC" ]; then
  TOPIC="/fuel/p11_lite/exploration_goal"
  echo "[trigger_goal] no visible goal topic; using source-confirmed internal topic $TOPIC"
fi

echo "[trigger_goal] topic=$TOPIC type=geometry_msgs/msg/PoseStamped frame=$FRAME_ID xyz=($X,$Y,$Z) repeat=$REPEAT rate=$RATE"
timeout 8 ros2 topic info -v "$TOPIC" --no-daemon || true
exec python3 scripts/publish_goal_once.py --topic "$TOPIC" --frame "$FRAME_ID" --x "$X" --y "$Y" --z "$Z" --repeat "$REPEAT" --rate "$RATE"
