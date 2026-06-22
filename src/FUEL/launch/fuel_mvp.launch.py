from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


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
    real_interface_params = PathJoinSubstitution([
        FindPackageShare("fuel_ros2"),
        "config",
        "fuel_real_interface.yaml",
    ])
    planner_backend = LaunchConfiguration("planner_backend")
    enable_frontier_fis = LaunchConfiguration("enable_frontier_fis")
    use_frontier_goal_source = LaunchConfiguration("use_frontier_goal_source")
    enable_real_interface_mode = LaunchConfiguration("enable_real_interface_mode")
    robot_mode = LaunchConfiguration("robot_mode")

    return LaunchDescription([
        DeclareLaunchArgument("planner_backend", default_value="mvp"),
        DeclareLaunchArgument("enable_frontier_fis", default_value="false"),
        DeclareLaunchArgument("use_frontier_goal_source", default_value="false"),
        DeclareLaunchArgument("enable_real_interface_mode", default_value="false"),
        DeclareLaunchArgument("robot_mode", default_value="air"),
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
                real_interface_params,
                {
                    "planner_backend": planner_backend,
                    "frontier_fis.enable_frontier_fis": enable_frontier_fis,
                    "frontier_fis.use_frontier_goal_source": use_frontier_goal_source,
                    "real_interface.enable_real_interface_mode": enable_real_interface_mode,
                    "real_interface.mode.robot_mode": robot_mode,
                },
            ],
        ),
    ])
