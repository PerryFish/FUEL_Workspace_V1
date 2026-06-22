# 00 Environment Audit

- Workspace: `/home/nuaa/ZHY/FUEL_PLANNER_V3`
- OS: Ubuntu 22.04.5 LTS (jammy)
- ROS2: Humble, `/opt/ros/humble`
- colcon: `python3-colcon-core 0.20.1`
- gcc/g++: 11.4.0
- Python: 3.10.12
- DISPLAY: `:0`
- RViz2: `/opt/ros/humble/bin/rviz2`
- GPU: `nvidia-smi` failed to communicate with the NVIDIA driver
- ROS logs redirected to: `/home/nuaa/ZHY/FUEL_PLANNER_V3/test-log/ros`
- RMW: `rmw_fastrtps_cpp`
- FastDDS transport override: `FASTDDS_BUILTIN_TRANSPORTS=UDPv4`

Dependency state:
- Core packages such as `python3-colcon-common-extensions`, `python3-rosdep`, `libarmadillo-dev`, `libnlopt-dev`, `libpcl-dev`, `libopencv-dev`, and RViz2 were present.
- `scripts/install_deps.sh` could not use `sudo` in this managed execution environment: `no new privileges` blocked sudo. See `test-log/20260621_134919_install_deps.md`.

Source:
- Selected source commit: `3b11fc50c0ab8e84f9093f084ce80f4d1af6088d`
- Selected branch: `master`

Primary audit logs:
- `test-log/20260621_134324_phase0_audit_local.md`
- `test-log/20260621_134919_install_deps.md`
