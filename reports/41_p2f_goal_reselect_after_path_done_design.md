# P2F Goal Reselect After Path Done Design

## Design

- Keep the existing active goal lifecycle and topic interfaces.
- Detect path completion through recorder evidence: UAV close to active path endpoint and active path hash no longer changing.
- Prefer existing `goal_reached_switch`, `coverage_stall`, and `no_progress` paths in `exploration_manager_lite.py`.
- Use frontier point escape only when normal pending goal selection is insufficient.

## Conservative Changes

- Enable `enable_frontier_point_escape` by default.
- Reduce `escape_cooldown_sec` from 25s to 15s.
- Allow `coverage_stall` and `no_progress` escape to bypass global goal switch rate limiting, while still respecting escape cooldown and candidate filtering.

## Non-goals

- No map/world geometry changes.
- No disabling obstacles.
- No disabling local sensing.
- No random walk fallback.
