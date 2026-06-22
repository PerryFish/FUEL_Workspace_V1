# 03 Runtime Smoke Test Report

Headless smoke test result: FAIL

Command:

```bash
./scripts/run_with_log.sh headless_smoke_test ./scripts/run_headless_smoke_test.sh
```

Important logs:
- `test-log/20260621_141949_headless_smoke_test_udp.md`
- `test-log/headless_smoke_runtime_20260621_141950.txt`
- `test-log/headless_smoke_runtime_20260621_141950.txt.launch`

What passed:
- `ros2 launch exploration_manager exploration.launch.py` starts the FUEL ROS2 node graph.
- Launch log confirms these nodes started: frame publisher, complex environment adapter, quadrotor simulator, local sensing, occupancy grid, frontier viewpoint, exploration manager, goal-to-path bridge, trajectory server, visual markers, world cloud publisher, topic compatibility bridge.
- Launch log confirms planner output: `P10_LITE_TRAJECTORY_SOURCE_UPDATED source=global_path/local_trajectory/managed_trajectory`.
- No real flight/actuator command path is used; logs explicitly show `REAL_FLIGHT_COMMAND=false`.

What failed:
- ROS2 CLI discovery in this managed environment only saw `/parameter_events` and `/rosout`.
- As a result, `ros2 topic echo`, `/move_base_simple/goal` publish, odom sampling, and planner topic sampling failed from the smoke script.

Likely cause:
- Current sandbox/process environment has DDS discovery limitations. FastDDS UDPv4 was tried and did not restore CLI discovery.

Next action:
- Run the same commands in a normal terminal on the host, outside the managed execution sandbox.
- If the host terminal still only sees `/rosout`, install/test CycloneDDS (`ros-humble-rmw-cyclonedds-cpp`) and set `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`.
