#!/usr/bin/env bash
set -euo pipefail

cd /home/nuaa/ZHY/FUEL_PLANNER_V3

sudo apt update
sudo apt install -y \
  build-essential cmake git wget curl \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  python3-pip \
  libarmadillo-dev \
  libnlopt-dev \
  libeigen3-dev \
  libpcl-dev \
  libopencv-dev \
  ros-humble-rviz2 \
  ros-humble-tf2-ros \
  ros-humble-tf2-tools \
  ros-humble-tf2-geometry-msgs \
  ros-humble-pcl-ros \
  ros-humble-pcl-conversions \
  ros-humble-octomap \
  ros-humble-octomap-msgs \
  ros-humble-nav-msgs \
  ros-humble-geometry-msgs \
  ros-humble-sensor-msgs \
  ros-humble-visualization-msgs \
  ros-humble-message-filters

sudo rosdep init || true
rosdep update || true

set +u
source /opt/ros/humble/setup.bash
set -u
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
