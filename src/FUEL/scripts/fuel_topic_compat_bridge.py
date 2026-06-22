#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import String


class FuelTopicCompatBridge(Node):
    def __init__(self):
        super().__init__("fuel_topic_compat_bridge")
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.goal_pub = self.create_publisher(PoseStamped, "/fuel/p11_lite/exploration_goal", 10)
        self.global_cloud_pub = self.create_publisher(PointCloud2, "/map_generator/global_cloud", 10)
        self.depth_pub = self.create_publisher(PointCloud2, "/pcl_render_node/depth", 10)
        self.cloud_pub = self.create_publisher(PointCloud2, "/pcl_render_node/cloud", 10)
        self.sensor_pose_pub = self.create_publisher(PoseStamped, "/pcl_render_node/sensor_pose", 10)
        self.visual_slam_odom_pub = self.create_publisher(Odometry, "/visual_slam/odom", 20)
        self.state_ukf_odom_pub = self.create_publisher(Odometry, "/state_ukf/odom", 20)
        self.pos_cmd_pub = self.create_publisher(PoseStamped, "/planning/pos_cmd", 10)
        self.travel_traj_pub = self.create_publisher(Path, "/planning/travel_traj", 10)
        self.status_pub = self.create_publisher(String, "/fuel/compat/status", 10)

        self.create_subscription(PoseStamped, "/move_base_simple/goal", self._goal_cb, 10)
        self.create_subscription(PointCloud2, "/global_cloud", self._global_cloud_cb, 10)
        self.create_subscription(PointCloud2, "/map_cloud", self._global_cloud_cb, 10)
        self.create_subscription(PointCloud2, "/fuel/p11_lite/local_occupied_points", self._local_cloud_cb, 10)
        self.create_subscription(Odometry, "/odom", self._odom_cb, 20)
        self.create_subscription(PoseStamped, "/fuel/p10_lite/position_cmd", self._pos_cmd_cb, 10)
        self.create_subscription(Path, "/fuel/p10_lite/active_path", self._travel_traj_cb, 10)
        self.create_subscription(Path, "/fuel/plan_manager/managed_trajectory", self._travel_traj_cb, 10)
        self.timer = self.create_timer(1.0, self._publish_status)
        self.goal_count = 0
        self.cloud_count = 0
        self.odom_count = 0
        self.cmd_count = 0
        self.traj_count = 0
        self.get_logger().info("FUEL_TOPIC_COMPAT_BRIDGE_READY forwards_only=true real_flight_command=false")

    def _stamp_frame(self, msg):
        msg.header.stamp = self.get_clock().now().to_msg()
        if not msg.header.frame_id:
            msg.header.frame_id = self.frame_id
        return msg

    def _goal_cb(self, msg: PoseStamped) -> None:
        self.goal_count += 1
        self.goal_pub.publish(self._stamp_frame(msg))

    def _global_cloud_cb(self, msg: PointCloud2) -> None:
        self.cloud_count += 1
        self.global_cloud_pub.publish(msg)

    def _local_cloud_cb(self, msg: PointCloud2) -> None:
        self.depth_pub.publish(msg)
        self.cloud_pub.publish(msg)

    def _odom_cb(self, msg: Odometry) -> None:
        self.odom_count += 1
        self.visual_slam_odom_pub.publish(msg)
        self.state_ukf_odom_pub.publish(msg)
        pose = PoseStamped()
        pose.header = msg.header
        pose.pose = msg.pose.pose
        self.sensor_pose_pub.publish(pose)

    def _pos_cmd_cb(self, msg: PoseStamped) -> None:
        self.cmd_count += 1
        self.pos_cmd_pub.publish(msg)

    def _travel_traj_cb(self, msg: Path) -> None:
        self.traj_count += 1
        self.travel_traj_pub.publish(msg)

    def _publish_status(self) -> None:
        msg = String()
        msg.data = (
            f"goals={self.goal_count} clouds={self.cloud_count} odom={self.odom_count} "
            f"pos_cmd={self.cmd_count} travel_traj={self.traj_count} real_flight_command=false"
        )
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FuelTopicCompatBridge()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
