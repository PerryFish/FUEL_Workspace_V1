#!/usr/bin/env python3
import argparse
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node


class GoalPublisher(Node):
    def __init__(self, args):
        super().__init__("fuel_goal_publisher_once")
        self.args = args
        self.pub = self.create_publisher(PoseStamped, args.topic, 10)

    def make_msg(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg() if self.args.current_time else msg.header.stamp
        msg.header.frame_id = self.args.frame
        msg.pose.position.x = float(self.args.x)
        msg.pose.position.y = float(self.args.y)
        msg.pose.position.z = float(self.args.z)
        msg.pose.orientation.w = 1.0
        return msg

    def run(self):
        delay = 1.0 / max(0.1, float(self.args.rate))
        for i in range(int(self.args.repeat)):
            msg = self.make_msg()
            self.pub.publish(msg)
            self.get_logger().info(
                f"GOAL_PUBLISHED topic={self.args.topic} frame={self.args.frame} "
                f"x={self.args.x:.3f} y={self.args.y:.3f} z={self.args.z:.3f} seq={i + 1}/{self.args.repeat}"
            )
            rclpy.spin_once(self, timeout_sec=0.05)
            time.sleep(delay)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="/fuel/p11_lite/exploration_goal")
    parser.add_argument("--frame", default="map")
    parser.add_argument("--x", type=float, default=5.0)
    parser.add_argument("--y", type=float, default=0.0)
    parser.add_argument("--z", type=float, default=1.2)
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--rate", type=float, default=2.0)
    parser.add_argument("--current-time", action="store_true", default=True)
    return parser.parse_args()


def main():
    args = parse_args()
    rclpy.init()
    node = GoalPublisher(args)
    try:
      node.run()
    finally:
      node.destroy_node()
      rclpy.shutdown()


if __name__ == "__main__":
    main()
