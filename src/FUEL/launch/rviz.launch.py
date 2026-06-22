from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    rviz_config = PathJoinSubstitution(
        [FindPackageShare("fuel_ros2"), "rviz", "fuel_exploration_large_demo_readable.rviz"]
    )
    return LaunchDescription(
        [
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2_fuel",
                output="screen",
                arguments=["-d", rviz_config],
            )
        ]
    )
