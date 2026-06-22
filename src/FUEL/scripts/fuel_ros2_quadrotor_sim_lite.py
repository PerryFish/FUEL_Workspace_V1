#!/usr/bin/env python3
import math
from typing import Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


Vector3 = Tuple[float, float, float]


def clamp_norm(vec: Vector3, limit: float) -> Vector3:
    norm = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])
    if norm <= limit or norm <= 1e-9:
        return vec
    scale = limit / norm
    return vec[0] * scale, vec[1] * scale, vec[2] * scale


class FuelRos2QuadrotorSimLite(Node):
    def __init__(self):
        super().__init__("fuel_ros2_quadrotor_sim_lite")
        self.max_speed = max(0.05, float(self.declare_parameter("max_speed", 1.0).value))
        self.max_accel = max(0.05, float(self.declare_parameter("max_accel", 0.8).value))
        self.update_rate = max(1.0, float(self.declare_parameter("update_rate", 30.0).value))
        self.publish_state_estimation = bool(self.declare_parameter("publish_state_estimation", True).value)
        self.frame_id = str(self.declare_parameter("frame_id", "map").value)
        self.child_frame_id = str(self.declare_parameter("child_frame_id", "base_link").value)

        self.position = (
            float(self.declare_parameter("initial_x", 0.0).value),
            float(self.declare_parameter("initial_y", -12.0).value),
            float(self.declare_parameter("initial_z", 1.2).value),
        )
        self.target = self.position
        self.velocity: Vector3 = (0.0, 0.0, 0.0)
        self.last_update_sec = self._now_sec()

        self.create_subscription(PoseStamped, "/fuel/p10_lite/position_cmd", self._target_cb, 10)
        self.odom_pub = self.create_publisher(Odometry, "/odom", 20)
        self.state_estimation_pub = self.create_publisher(Odometry, "/state_estimation", 20)
        self.status_pub = self.create_publisher(String, "/fuel/p10_lite/quadrotor_sim_status", 10)
        self.timer = self.create_timer(1.0 / self.update_rate, self._tick)
        self.get_logger().info(
            "P10_LITE_QUADROTOR_SIM_RUNNING REAL_FLIGHT_COMMAND=false "
            "sim_model=point_mass_lite blocked_real_flight_topics=true"
        )

    def _now_sec(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    def _target_cb(self, msg: PoseStamped) -> None:
        self.target = (
            float(msg.pose.position.x),
            float(msg.pose.position.y),
            float(msg.pose.position.z),
        )

    def _tick(self) -> None:
        now = self._now_sec()
        dt = max(1.0 / self.update_rate, min(0.2, now - self.last_update_sec))
        self.last_update_sec = now

        error = (
            self.target[0] - self.position[0],
            self.target[1] - self.position[1],
            self.target[2] - self.position[2],
        )
        desired_velocity = clamp_norm((error[0] * 1.2, error[1] * 1.2, error[2] * 1.2), self.max_speed)
        accel = (
            (desired_velocity[0] - self.velocity[0]) / dt,
            (desired_velocity[1] - self.velocity[1]) / dt,
            (desired_velocity[2] - self.velocity[2]) / dt,
        )
        accel = clamp_norm(accel, self.max_accel)
        self.velocity = clamp_norm(
            (
                self.velocity[0] + accel[0] * dt,
                self.velocity[1] + accel[1] * dt,
                self.velocity[2] + accel[2] * dt,
            ),
            self.max_speed,
        )
        self.position = (
            self.position[0] + self.velocity[0] * dt,
            self.position[1] + self.velocity[1] * dt,
            self.position[2] + self.velocity[2] * dt,
        )

        odom = self._make_odom()
        self.odom_pub.publish(odom)
        if self.publish_state_estimation:
            self.state_estimation_pub.publish(odom)
        self._publish_status()

    def _make_odom(self) -> Odometry:
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = self.frame_id
        odom.child_frame_id = self.child_frame_id
        odom.pose.pose.position.x = self.position[0]
        odom.pose.pose.position.y = self.position[1]
        odom.pose.pose.position.z = self.position[2]
        odom.pose.pose.orientation.w = 1.0
        odom.twist.twist.linear.x = self.velocity[0]
        odom.twist.twist.linear.y = self.velocity[1]
        odom.twist.twist.linear.z = self.velocity[2]
        return odom

    def _publish_status(self) -> None:
        msg = String()
        msg.data = (
            "REAL_FLIGHT_COMMAND=false "
            "sim_model=point_mass_lite "
            f"position=({self.position[0]:.3f},{self.position[1]:.3f},{self.position[2]:.3f}) "
            f"target=({self.target[0]:.3f},{self.target[1]:.3f},{self.target[2]:.3f}) "
            f"velocity=({self.velocity[0]:.3f},{self.velocity[1]:.3f},{self.velocity[2]:.3f}) "
            f"max_speed={self.max_speed:.3f} "
            f"max_accel={self.max_accel:.3f} "
            "blocked_real_flight_topics=true"
        )
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FuelRos2QuadrotorSimLite()
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
