from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "mvp_params.yaml",
    ])
    plan_env_params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "fuel_plan_env.yaml",
    ])
    frontier_fis_params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "fuel_frontier_fis.yaml",
    ])
    exploration_fsm_params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "fuel_exploration_fsm.yaml",
    ])
    path_searching_params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "fuel_path_searching.yaml",
    ])
    bspline_traj_params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "fuel_bspline_traj.yaml",
    ])
    plan_manager_params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "fuel_plan_manager.yaml",
    ])
    rviz_config = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "rviz",
        "fuel_exploration_large_demo_readable.rviz",
    ])

    start_rviz = LaunchConfiguration("start_rviz")
    planner_backend = LaunchConfiguration("planner_backend")

    return LaunchDescription([
        DeclareLaunchArgument("start_rviz", default_value="false"),
        DeclareLaunchArgument("planner_backend", default_value="fuel_plan_manager"),
        DeclareLaunchArgument("real_flight_command", default_value="false"),
        Node(
            package="fuel_ros2",
            executable="fuel_mvp_node",
            name="fuel_mvp_node",
            output="screen",
            parameters=[
                params,
                plan_env_params,
                frontier_fis_params,
                exploration_fsm_params,
                path_searching_params,
                bspline_traj_params,
                plan_manager_params,
                {
                    "planner_backend": planner_backend,
                    "frontier_fis.enable_frontier_fis": False,
                    "frontier_fis.use_frontier_goal_source": False,
                    "real_interface.enable_real_interface_mode": False,
                },
            ],
        ),
        Node(
            package="fuel_ros2",
            executable="fuel_ros2_traj_server_lite",
            name="fuel_ros2_traj_server_lite",
            output="screen",
            parameters=[{"loop_trajectory": False}],
        ),
        Node(
            package="fuel_ros2",
            executable="fuel_ros2_quadrotor_sim_lite",
            name="fuel_ros2_quadrotor_sim_lite",
            output="screen",
            parameters=[{"publish_state_estimation": True}],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config],
            condition=IfCondition(start_rviz),
            output="screen",
        ),
    ])
