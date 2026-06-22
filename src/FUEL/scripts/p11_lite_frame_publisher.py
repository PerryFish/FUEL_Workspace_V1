#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster


class P11LiteFramePublisher(Node):
    def __init__(self):
        super().__init__("p11_lite_frame_publisher")
        self.broadcaster = StaticTransformBroadcaster(self)
        self._publish_static_map_to_odom()
        self.get_logger().info("P11_LITE_FRAME_PUBLISHER_READY map->odom REAL_FLIGHT_COMMAND=false")

    def _publish_static_map_to_odom(self) -> None:
        tf = TransformStamped()
        tf.header.stamp = self.get_clock().now().to_msg()
        tf.header.frame_id = "map"
        tf.child_frame_id = "odom"
        tf.transform.translation.x = 0.0
        tf.transform.translation.y = 0.0
        tf.transform.translation.z = 0.0
        tf.transform.rotation.x = 0.0
        tf.transform.rotation.y = 0.0
        tf.transform.rotation.z = 0.0
        tf.transform.rotation.w = 1.0
        self.broadcaster.sendTransform(tf)


def main(args=None):
    rclpy.init(args=args)
    node = P11LiteFramePublisher()
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
