# P2D Before After 300s Comparison

| metric | baseline | after_fix | result |
|---|---:|---:|---|
| odom_total_distance | 0.101m | 0.065m | worse |
| goal_switch_count | 2 | 2 | same |
| active_path_update_count | 1 | 1 | same |
| active_path_same_hash_max_duration_sec | 299.875 | 299.034 | same |
| active_path_endpoint_to_goal_distance_avg | 7.051 | 6.866 | slight better but still fail |
| active_path_endpoint_to_goal_distance_max | 7.806 | 7.806 | same |
| travel_traj_update_count | 47 | 99 | higher |
| travel_traj_same_hash_max_duration_sec | 277.562 | 251.831 | still fail |
| position_cmd_update_count | 1 | 1 | same |
| position_cmd_total_variation | 0.0 | 0.0 | same |
| position_cmd_same_pose_max_duration_sec | 299.960 | 299.929 | same |
| position_cmd_to_odom_distance_avg | 0.000285 | 0.000119 | command equals odom |
| traj_server_stale_path_hold_count | 38 | 64 | worse |
| quadrotor_sim_motion_blocked_count | 8999 | 8971 | same |
| main_chain_break | PATH_FEASIBILITY | PATH_FEASIBILITY | unchanged |

## Conclusion

The P2D fix attempt did not improve the 300s motion-chain result.

```text
after_fix_result=PARTIAL_NOT_IMPROVED
```
