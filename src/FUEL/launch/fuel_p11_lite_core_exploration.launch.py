from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world_config = LaunchConfiguration("world_config")
    use_rviz = LaunchConfiguration("use_rviz")
    enable_visual_markers = LaunchConfiguration("enable_visual_markers")
    enable_frame_publisher = LaunchConfiguration("enable_frame_publisher")
    environment_mode = LaunchConfiguration("environment_mode")
    complex_env_config = LaunchConfiguration("complex_env_config")
    enable_complex_env_adapter = LaunchConfiguration("enable_complex_env_adapter")
    visual_profile = LaunchConfiguration("visual_profile")
    execution_source_lock = LaunchConfiguration("execution_source_lock")

    nodes = [
        Node(
            package="fuel_ros2",
            executable="p11_lite_frame_publisher",
            name="p11_lite_frame_publisher",
            output="screen",
            condition=IfCondition(enable_frame_publisher),
        ),
        Node(
            package="fuel_ros2",
            executable="p11_lite_complex_environment_adapter",
            name="p11_lite_complex_environment_adapter",
            output="screen",
            condition=IfCondition(enable_complex_env_adapter),
            parameters=[
                complex_env_config,
                {
                    "world_config": world_config,
                    "environment_mode": environment_mode,
                },
            ],
        ),
        Node(
            package="fuel_ros2",
            executable="fuel_ros2_quadrotor_sim_lite",
            name="fuel_ros2_quadrotor_sim_lite",
            output="screen",
            parameters=[{"max_speed": 1.2, "max_accel": 0.9, "publish_state_estimation": True}],
        ),
        Node(
            package="fuel_ros2",
            executable="local_sensing_lite",
            name="local_sensing_lite",
            output="screen",
            parameters=[
                complex_env_config,
                {
                    "world_config": world_config,
                    "environment_mode": environment_mode,
                },
            ],
        ),
        Node(
            package="fuel_ros2",
            executable="occupancy_grid_lite",
            name="occupancy_grid_lite",
            output="screen",
            parameters=[{"world_config": world_config}],
        ),
        Node(
            package="fuel_ros2",
            executable="frontier_viewpoint_lite",
            name="frontier_viewpoint_lite",
            output="screen",
            parameters=[
                complex_env_config,
                {
                    "world_config": world_config,
                    "environment_mode": environment_mode,
                },
            ],
        ),
        Node(
            package="fuel_ros2",
            executable="exploration_manager_lite",
            name="exploration_manager_lite",
            output="screen",
        ),
        Node(
            package="fuel_ros2",
            executable="p11_lite_goal_to_path_bridge",
            name="p11_lite_goal_to_path_bridge",
            output="screen",
            parameters=[
                complex_env_config,
                {
                    "world_config": world_config,
                    "environment_mode": environment_mode,
                },
            ],
        ),
        Node(
            package="fuel_ros2",
            executable="fuel_ros2_traj_server_lite",
            name="fuel_ros2_traj_server_lite",
            output="screen",
            parameters=[
                {
                    "execution_source_lock": execution_source_lock,
                    "execution_source_priority": "managed_trajectory,local_trajectory,global_path",
                }
            ],
        ),
        Node(
            package="fuel_ros2",
            executable="p11_lite_visual_markers",
            name="p11_lite_visual_markers",
            output="screen",
            condition=IfCondition(enable_visual_markers),
            parameters=[
                complex_env_config,
                {
                    "world_config": world_config,
                    "environment_mode": environment_mode,
                    "visual_profile": visual_profile,
                },
            ],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2_p11_lite",
            output="screen",
            condition=IfCondition(use_rviz),
            arguments=[
                "-d",
                PathJoinSubstitution([FindPackageShare("fuel_ros2"), "rviz", "fuel_exploration_large_demo_readable.rviz"]),
            ],
        ),
    ]

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "world_config",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("fuel_ros2"), "config", "fuel_visual_world_exploration.yaml"]
                ),
            ),
            DeclareLaunchArgument("use_rviz", default_value="false"),
            DeclareLaunchArgument("enable_visual_markers", default_value="true"),
            DeclareLaunchArgument("enable_frame_publisher", default_value="true"),
            DeclareLaunchArgument("environment_mode", default_value="simple"),
            DeclareLaunchArgument(
                "complex_env_config",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("fuel_ros2"), "config", "p11_lite_complex_env.yaml"]
                ),
            ),
            DeclareLaunchArgument("enable_complex_env_adapter", default_value="false"),
            DeclareLaunchArgument("visual_profile", default_value="acceptance"),
            DeclareLaunchArgument("execution_source_lock", default_value=""),
            *nodes,
        ]
    )
