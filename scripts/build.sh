#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3
source scripts/env.sh

rm -rf build install log

set +e
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
CODE=$?
set -e

if [ "$CODE" -ne 0 ]; then
  echo
  echo "[build.sh] Build failed. Diagnostic checklist:"
  echo "- Missing package: run rosdep install and inspect CMake find_package errors."
  echo "- Missing header: check package.xml/CMakeLists dependencies and include paths."
  echo "- ROS1 API remnants: look for roscpp, catkin, ros::, NodeHandle, tf instead of rclcpp/tf2."
  echo "- Message/service generation: check rosidl_generate_interfaces dependencies."
  echo "- PCL/Eigen/OpenCV/Armadillo/NLopt: check target_link_libraries and ament dependencies."
  echo "- Launch paths: check install(DIRECTORY launch config rviz DESTINATION share/\${PROJECT_NAME})."
fi

exit "$CODE"
