"""
Exercise 9 — two_robots_broadcaster.py

Publishes:
  1. Dynamic transforms under 'world':
     - world → robot_a: Circle of radius 3.0 at 0.3 rad/s (counter-clockwise)
     - world → robot_b: Circle of radius 1.5 at 0.7 rad/s (clockwise / opposite direction)
  2. Static transforms:
     - robot_a → robot_a/front_sensor: +0.25 m forward (x = 0.25)
     - robot_b → robot_b/front_sensor: +0.25 m forward (x = 0.25)
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


def euler_to_quaternion(roll, pitch, yaw):
    """Convert Euler angles (rad) to quaternion (qx, qy, qz, qw)."""
    cr = math.cos(roll / 2.0)
    sr = math.sin(roll / 2.0)
    cp = math.cos(pitch / 2.0)
    sp = math.sin(pitch / 2.0)
    cy = math.cos(yaw / 2.0)
    sy = math.sin(yaw / 2.0)

    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    qw = cr * cp * cy + sr * sp * sy
    return qx, qy, qz, qw


class TwoRobotsBroadcaster(Node):
    def __init__(self):
        super().__init__('two_robots_broadcaster')

        # TF broadcasters
        self.dynamic_broadcaster = TransformBroadcaster(self)
        self.static_broadcaster = StaticTransformBroadcaster(self)

        # Kinematic parameters
        # Robot A: R = 3.0 m, omega = 0.3 rad/s (counter-clockwise)
        self.r_a = 3.0
        self.w_a = 0.3

        # Robot B: R = 1.5 m, omega = -0.7 rad/s (clockwise / opposite direction)
        self.r_b = 1.5
        self.w_b = -0.7

        # Start time anchor
        self.t0 = self.get_clock().now()

        # Publish static front sensors once at startup
        self.publish_static_sensors()

        # 50 Hz timer for dynamic broadcasts (20 ms)
        self.timer = self.create_timer(0.02, self.timer_callback)
        self.get_logger().info('two_robots_broadcaster running at 50 Hz')

    def publish_static_sensors(self):
        now_msg = self.get_clock().now().to_msg()
        static_transforms = []

        # Sensor for Robot A: mounted 0.25 m forward (+x)
        t_sa = TransformStamped()
        t_sa.header.stamp = now_msg
        t_sa.header.frame_id = 'robot_a'
        t_sa.child_frame_id = 'robot_a/front_sensor'
        t_sa.transform.translation.x = 0.25
        t_sa.transform.translation.y = 0.0
        t_sa.transform.translation.z = 0.0
        t_sa.transform.rotation.w = 1.0
        static_transforms.append(t_sa)

        # Sensor for Robot B: mounted 0.25 m forward (+x)
        t_sb = TransformStamped()
        t_sb.header.stamp = now_msg
        t_sb.header.frame_id = 'robot_b'
        t_sb.child_frame_id = 'robot_b/front_sensor'
        t_sb.transform.translation.x = 0.25
        t_sb.transform.translation.y = 0.0
        t_sb.transform.translation.z = 0.0
        t_sb.transform.rotation.w = 1.0
        static_transforms.append(t_sb)

        self.static_broadcaster.sendTransform(static_transforms)

    def timer_callback(self):
        now = self.get_clock().now()
        now_msg = now.to_msg()
        t = (now - self.t0).nanoseconds * 1e-9

        # ---------------- Robot A ----------------
        theta_a = self.w_a * t
        xa = self.r_a * math.cos(theta_a)
        ya = self.r_a * math.sin(theta_a)
        yaw_a = theta_a + (math.pi / 2.0)  # tangent to counter-clockwise circle

        msg_a = TransformStamped()
        msg_a.header.stamp = now_msg
        msg_a.header.frame_id = 'world'
        msg_a.child_frame_id = 'robot_a'
        msg_a.transform.translation.x = xa
        msg_a.transform.translation.y = ya
        msg_a.transform.translation.z = 0.0
        qa = euler_to_quaternion(0.0, 0.0, yaw_a)
        msg_a.transform.rotation.x = qa[0]
        msg_a.transform.rotation.y = qa[1]
        msg_a.transform.rotation.z = qa[2]
        msg_a.transform.rotation.w = qa[3]

        # ---------------- Robot B ----------------
        theta_b = self.w_b * t
        xb = self.r_b * math.cos(theta_b)
        yb = self.r_b * math.sin(theta_b)
        yaw_b = theta_b - (math.pi / 2.0)  # tangent to clockwise circle

        msg_b = TransformStamped()
        msg_b.header.stamp = now_msg
        msg_b.header.frame_id = 'world'
        msg_b.child_frame_id = 'robot_b'
        msg_b.transform.translation.x = xb
        msg_b.transform.translation.y = yb
        msg_b.transform.translation.z = 0.0
        qb = euler_to_quaternion(0.0, 0.0, yaw_b)
        msg_b.transform.rotation.x = qb[0]
        msg_b.transform.rotation.y = qb[1]
        msg_b.transform.rotation.z = qb[2]
        msg_b.transform.rotation.w = qb[3]

        # Broadcast both transforms
        self.dynamic_broadcaster.sendTransform([msg_a, msg_b])


def main(args=None):
    rclpy.init(args=args)
    node = TwoRobotsBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
