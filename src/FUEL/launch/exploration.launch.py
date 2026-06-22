from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    map_name = LaunchConfiguration("map_name")
    world_config = PathJoinSubstitution([FindPackageShare("fuel_ros2"), "config", "fuel_visual_world_exploration.yaml"])
    base_launch = PathJoinSubstitution([FindPackageShare("fuel_ros2"), "launch", "fuel_p11_lite_core_exploration.launch.py"])
    return LaunchDescription(
        [
            DeclareLaunchArgument("map_name", default_value="office"),
            DeclareLaunchArgument("environment_mode", default_value="complex"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(base_launch),
                launch_arguments={
                    "world_config": world_config,
                    "use_rviz": "false",
                    "environment_mode": LaunchConfiguration("environment_mode"),
                    "enable_complex_env_adapter": "true",
                    "visual_profile": "acceptance",
                }.items(),
            ),
            Node(
                package="fuel_ros2",
                executable="fuel_world_cloud_publisher.py",
                name="map_pub",
                output="screen",
                parameters=[
                    {
                        "config_path": world_config,
                        "qos_mode": "rviz_compatible",
                        "map_name": map_name,
                    }
                ],
            ),
            Node(
                package="fuel_ros2",
                executable="fuel_topic_compat_bridge.py",
                name="fuel_topic_compat_bridge",
                output="screen",
            ),
        ]
    )
