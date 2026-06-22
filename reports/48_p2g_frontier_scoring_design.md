# P2G Frontier Scoring Design

## Current Problem

The P2F/P2G baseline showed that goal lifecycle and trajectory execution can work, but frontier scoring lacked reachability memory. When a selected frontier/viewpoint region failed path feasibility, the failure stayed downstream in the bridge/manager and did not suppress the upstream candidate source.

## Reachability Gate

- Subscribe `frontier_viewpoint_lite.py` to `/fuel/p11_lite/goal_to_path_status`.
- Parse `goal_key`, `path_feasible`, `path_valid`, `request_reselect`, `endpoint_to_goal_distance`, and reject reason.
- Treat a goal as unreachable if path is infeasible/invalid, reselect is requested, or endpoint distance is above 1.5m.
- Require two consecutive failures before blacklisting to avoid one-frame transient rejects.

## Region Penalty / Blacklist

- Convert unreachable goal coordinates into a 2.0m grid region.
- Blacklist that region for 90s.
- Exclude blacklisted regions from preferred region selection.
- Skip candidate viewpoints whose final inward-shifted goal falls inside a blacklisted unreachable region.

## Low-Gain / Saturated Handling

This patch does not implement a new low-gain blacklist. The 300s after-fix result showed enough improvement from the reachability gate alone. The 600s run still stalls later, so low-gain residual frontier scoring remains the next minimal target.

## Status Additions

The frontier status now includes:

- `unreachable_blacklisted_region_count`
- `unreachable_blacklist_event_count`
- `reachability_reject_count`
- `last_reachability_reject_goal`
- `last_reachability_reject_reason`

No existing topic names or message types were changed.
