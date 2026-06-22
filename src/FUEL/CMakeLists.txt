cmake_minimum_required(VERSION 3.8)
project(fuel_ros2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(Eigen3 REQUIRED)
if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
endif()

include_directories(include)

add_library(fuel_plan_env_adapter
  src/plan_env/fuel_plan_env_adapter.cpp
)
target_include_directories(fuel_plan_env_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIRS}
)
ament_target_dependencies(
  fuel_plan_env_adapter
  rclcpp
  sensor_msgs
  nav_msgs
  visualization_msgs
)

add_library(fuel_frontier_fis_adapter
  src/frontier_fis/fuel_frontier_fis_adapter.cpp
)
target_include_directories(fuel_frontier_fis_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIRS}
)
target_link_libraries(fuel_frontier_fis_adapter fuel_plan_env_adapter)
ament_target_dependencies(
  fuel_frontier_fis_adapter
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
  tf2
)

add_library(fuel_exploration_fsm_adapter
  src/exploration_fsm/fuel_exploration_fsm_adapter.cpp
)
target_include_directories(fuel_exploration_fsm_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIRS}
)
ament_target_dependencies(
  fuel_exploration_fsm_adapter
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
)

add_library(fuel_path_searching_adapter
  src/path_searching/fuel_grid_astar3d.cpp
  src/path_searching/fuel_path_searching_adapter.cpp
)
target_include_directories(fuel_path_searching_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIRS}
)
target_link_libraries(fuel_path_searching_adapter fuel_plan_env_adapter)
ament_target_dependencies(
  fuel_path_searching_adapter
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
)

add_library(fuel_bspline_traj_adapter
  src/bspline_traj/fuel_bspline_traj_adapter.cpp
)
target_include_directories(fuel_bspline_traj_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIRS}
)
target_link_libraries(fuel_bspline_traj_adapter fuel_plan_env_adapter)
ament_target_dependencies(
  fuel_bspline_traj_adapter
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
)

add_library(fuel_plan_manager_adapter
  src/plan_manager/fuel_plan_manager_adapter.cpp
)
target_include_directories(fuel_plan_manager_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${EIGEN3_INCLUDE_DIRS}
)
ament_target_dependencies(
  fuel_plan_manager_adapter
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
)

add_library(fuel_real_interface_adapter
  src/real_interface/fuel_real_interface_adapter.cpp
)
target_include_directories(fuel_real_interface_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(
  fuel_real_interface_adapter
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
)

add_library(fuel_safety_gate_adapter
  src/safety_gate/fuel_safety_gate_adapter.cpp
)
target_include_directories(fuel_safety_gate_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(
  fuel_safety_gate_adapter
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
)

add_library(fuel_onboard_preflight_adapter
  src/onboard_preflight/fuel_onboard_preflight_adapter.cpp
)
target_include_directories(fuel_onboard_preflight_adapter PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(
  fuel_onboard_preflight_adapter
  rclcpp
  std_msgs
  visualization_msgs
)

add_executable(fuel_mvp_node src/mvp/fuel_mvp_node.cpp)
target_link_libraries(
  fuel_mvp_node
  fuel_plan_env_adapter
  fuel_frontier_fis_adapter
  fuel_exploration_fsm_adapter
  fuel_path_searching_adapter
  fuel_bspline_traj_adapter
  fuel_plan_manager_adapter
  fuel_real_interface_adapter
)
ament_target_dependencies(
  fuel_mvp_node
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
  tf2
  tf2_ros
)

add_executable(fake_real_interface_publisher src/real_interface/fake_real_interface_publisher.cpp)
ament_target_dependencies(
  fake_real_interface_publisher
  rclcpp
  sensor_msgs
  nav_msgs
  tf2
)

add_executable(fuel_control_bridge_node src/real_interface/fuel_control_bridge_node.cpp)
ament_target_dependencies(
  fuel_control_bridge_node
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
)

add_executable(fuel_safety_gate_node src/safety_gate/fuel_safety_gate_node.cpp)
target_link_libraries(fuel_safety_gate_node fuel_safety_gate_adapter)
ament_target_dependencies(
  fuel_safety_gate_node
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
)

add_executable(closed_loop_fake_follower src/safety_gate/closed_loop_fake_follower.cpp)
ament_target_dependencies(
  closed_loop_fake_follower
  rclcpp
  std_msgs
  geometry_msgs
  nav_msgs
)

add_executable(fuel_onboard_preflight_node src/onboard_preflight/fuel_onboard_preflight_node.cpp)
target_link_libraries(fuel_onboard_preflight_node fuel_onboard_preflight_adapter)
ament_target_dependencies(
  fuel_onboard_preflight_node
  rclcpp
  std_msgs
  visualization_msgs
)

install(TARGETS
  fuel_mvp_node
  fake_real_interface_publisher
  fuel_control_bridge_node
  fuel_safety_gate_node
  closed_loop_fake_follower
  fuel_onboard_preflight_node
  fuel_plan_env_adapter
  fuel_frontier_fis_adapter
  fuel_exploration_fsm_adapter
  fuel_path_searching_adapter
  fuel_bspline_traj_adapter
  fuel_plan_manager_adapter
  fuel_real_interface_adapter
  fuel_safety_gate_adapter
  fuel_onboard_preflight_adapter
  EXPORT export_fuel_plan_env_adapter
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include
)

install(DIRECTORY launch config rviz worlds models maps
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/fuel_world_cloud_publisher.py
  scripts/gazebo_uav_trajectory_follower.py
  scripts/fuel_ros2_traj_server_lite.py
  scripts/fuel_ros2_quadrotor_sim_lite.py
  scripts/world_collision_checker.py
  scripts/p11_lite_utils.py
  scripts/p11_lite_collision_utils.py
  scripts/p11_lite_frame_publisher.py
  scripts/local_sensing_lite.py
  scripts/occupancy_grid_lite.py
  scripts/frontier_viewpoint_lite.py
  scripts/exploration_manager_lite.py
  scripts/p11_lite_goal_to_path_bridge.py
  scripts/p11_lite_visual_markers.py
  scripts/p11_lite_complex_environment_adapter.py
  scripts/fuel_topic_compat_bridge.py
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/fuel_ros2_traj_server_lite.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME fuel_ros2_traj_server_lite
)

install(PROGRAMS
  scripts/fuel_ros2_quadrotor_sim_lite.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME fuel_ros2_quadrotor_sim_lite
)

install(PROGRAMS
  scripts/local_sensing_lite.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME local_sensing_lite
)

install(PROGRAMS
  scripts/occupancy_grid_lite.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME occupancy_grid_lite
)

install(PROGRAMS
  scripts/frontier_viewpoint_lite.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME frontier_viewpoint_lite
)

install(PROGRAMS
  scripts/exploration_manager_lite.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME exploration_manager_lite
)

install(PROGRAMS
  scripts/p11_lite_goal_to_path_bridge.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME p11_lite_goal_to_path_bridge
)

install(PROGRAMS
  scripts/p11_lite_visual_markers.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME p11_lite_visual_markers
)

install(PROGRAMS
  scripts/p11_lite_complex_environment_adapter.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME p11_lite_complex_environment_adapter
)

install(PROGRAMS
  scripts/p11_lite_frame_publisher.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME p11_lite_frame_publisher
)

if(BUILD_TESTING)
  ament_add_gtest(fuel_grid_astar3d_test test/test_grid_astar3d.cpp)
  target_include_directories(fuel_grid_astar3d_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    ${EIGEN3_INCLUDE_DIRS}
  )
  target_link_libraries(fuel_grid_astar3d_test fuel_path_searching_adapter)

  ament_add_gtest(fuel_bspline_traj_adapter_test test/test_bspline_traj_adapter.cpp)
  target_include_directories(fuel_bspline_traj_adapter_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    ${EIGEN3_INCLUDE_DIRS}
  )
  target_link_libraries(fuel_bspline_traj_adapter_test fuel_bspline_traj_adapter)

  ament_add_gtest(fuel_plan_manager_adapter_test test/test_plan_manager_adapter.cpp)
  target_include_directories(fuel_plan_manager_adapter_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    ${EIGEN3_INCLUDE_DIRS}
  )
  ament_target_dependencies(
    fuel_plan_manager_adapter_test
    geometry_msgs
    nav_msgs
  )
  target_link_libraries(fuel_plan_manager_adapter_test fuel_plan_manager_adapter)

  ament_add_gtest(fuel_real_interface_adapter_test test/test_real_interface_adapter.cpp)
  target_include_directories(fuel_real_interface_adapter_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  )
  ament_target_dependencies(
    fuel_real_interface_adapter_test
    rclcpp
    sensor_msgs
    geometry_msgs
    nav_msgs
  )
  target_link_libraries(fuel_real_interface_adapter_test fuel_real_interface_adapter)

  ament_add_gtest(fuel_safety_gate_adapter_test test/test_safety_gate_adapter.cpp)
  target_include_directories(fuel_safety_gate_adapter_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  )
  ament_target_dependencies(
    fuel_safety_gate_adapter_test
    rclcpp
    geometry_msgs
    nav_msgs
  )
  target_link_libraries(fuel_safety_gate_adapter_test fuel_safety_gate_adapter)

  ament_add_gtest(fuel_onboard_preflight_adapter_test test/test_onboard_preflight_adapter.cpp)
  target_include_directories(fuel_onboard_preflight_adapter_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  )
  ament_target_dependencies(
    fuel_onboard_preflight_adapter_test
    rclcpp
    std_msgs
    visualization_msgs
  )
  target_link_libraries(fuel_onboard_preflight_adapter_test fuel_onboard_preflight_adapter)
endif()

ament_package()
