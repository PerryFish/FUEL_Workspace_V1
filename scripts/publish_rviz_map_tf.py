#!/usr/bin/env python3
import argparse
import sys

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster, TransformBroadcaster


class RvizMapTfPublisher(Node):
    def __init__(self, args):
        super().__init__("fuel_rviz_map_tf_publisher")
        self.args = args
        self.parent_frame = args.parent_frame
        self.child_frame = args.child_frame
        self.dynamic_broadcaster = None
        self.static_broadcaster = None
        self.odom_count = 0

        if args.mode == "static_anchor":
            self.static_broadcaster = StaticTransformBroadcaster(self)
            self.publish_static(self.parent_frame, self.child_frame)
        elif args.mode == "odom_to_tf":
            self.dynamic_broadcaster = TransformBroadcaster(self)
            self.create_subscription(Odometry, args.odom_topic, self.odom_cb, 20)
        else:
            raise ValueError(f"unsupported mode: {args.mode}")

        self.get_logger().info("RVIZ_MAP_TF_PUBLISHER_STARTED")
        self.get_logger().info(f"mode={args.mode}")
        self.get_logger().info(f"parent_frame={self.parent_frame}")
        self.get_logger().info(f"child_frame={self.child_frame}")
        print("RVIZ_MAP_TF_PUBLISHER_STARTED", flush=True)
        print(f"mode={args.mode}", flush=True)
        print(f"parent_frame={self.parent_frame}", flush=True)
        print(f"child_frame={self.child_frame}", flush=True)

    def make_identity_tf(self, parent: str, child: str) -> TransformStamped:
        tf = TransformStamped()
        tf.header.stamp = self.get_clock().now().to_msg()
        tf.header.frame_id = parent
        tf.child_frame_id = child
        tf.transform.translation.x = 0.0
        tf.transform.translation.y = 0.0
        tf.transform.translation.z = 0.0
        tf.transform.rotation.x = 0.0
        tf.transform.rotation.y = 0.0
        tf.transform.rotation.z = 0.0
        tf.transform.rotation.w = 1.0
        return tf

    def publish_static(self, parent: str, child: str) -> None:
        if parent == child:
            raise ValueError("parent_frame and child_frame must differ")
        self.static_broadcaster.sendTransform(self.make_identity_tf(parent, child))

    def odom_cb(self, msg: Odometry) -> None:
        parent = msg.header.frame_id or self.parent_frame
        child = msg.child_frame_id or self.child_frame
        if not parent or not child or parent == child:
            return
        tf = TransformStamped()
        tf.header.stamp = msg.header.stamp
        tf.header.frame_id = parent
        tf.child_frame_id = child
        tf.transform.translation.x = msg.pose.pose.position.x
        tf.transform.translation.y = msg.pose.pose.position.y
        tf.transform.translation.z = msg.pose.pose.position.z
        tf.transform.rotation = msg.pose.pose.orientation
        self.dynamic_broadcaster.sendTransform(tf)
        self.odom_count += 1
        if self.odom_count == 1 or self.odom_count % 100 == 0:
            self.get_logger().info(
                f"RVIZ_ODOM_TF_PUBLISHED count={self.odom_count} parent={parent} child={child}"
            )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["static_anchor", "odom_to_tf"], default="static_anchor")
    parser.add_argument("--parent-frame", default="map")
    parser.add_argument("--child-frame", default="fuel_rviz_anchor")
    parser.add_argument("--odom-topic", default="/odom")
    return parser.parse_args()


def main():
    args = parse_args()
    rclpy.init()
    node = RvizMapTfPublisher(args)
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
