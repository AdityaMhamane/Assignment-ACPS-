"""
Exercise 3 — figure_eight.py

Broadcasts odom → base_link at 50 Hz.
The robot traces a lemniscate (figure-eight):
    x(t) = A · sin(ωt)
    y(t) = A · sin(ωt) · cos(ωt)

with A = 2.0, ω = 0.5 rad/s.

The heading (yaw) is derived from the velocity vector so the robot
always faces its direction of travel.

Also publishes a nav_msgs/Path on /path so the trajectory can be
visualised easily in RViz2.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, PoseStamped
from nav_msgs.msg import Path
from tf2_ros import TransformBroadcaster


def euler_to_quaternion(roll, pitch, yaw):
    """Convert Euler angles (rad) → quaternion (x, y, z, w)."""
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


class FigureEightNode(Node):
    def __init__(self):
        super().__init__('figure_eight')

        # Lemniscate parameters
        self.A = 2.0        # amplitude  (metres)
        self.omega = 0.5    # angular speed (rad/s)

        # Dynamic TF broadcaster (NOT static — the transform changes every tick)
        self.tf_broadcaster = TransformBroadcaster(self)

        # Path publisher — so RViz2 can draw the trail
        self.path_pub = self.create_publisher(Path, 'path', 10)
        self.path_msg = Path()
        self.path_msg.header.frame_id = 'odom'

        # Record the start time so t begins at 0
        self.t0 = self.get_clock().now()

        # 50 Hz timer → 20 ms period
        self.timer = self.create_timer(1.0 / 50.0, self.timer_callback)

        self.get_logger().info(
            'figure_eight node started — broadcasting odom → base_link at 50 Hz')

    def timer_callback(self):
        now = self.get_clock().now()
        t = (now - self.t0).nanoseconds * 1e-9   # elapsed seconds

        A = self.A
        w = self.omega

        # ── Position ────────────────────────────────────────────
        x = A * math.sin(w * t)
        y = A * math.sin(w * t) * math.cos(w * t)
        # y can also be written as (A/2) * sin(2ωt)

        # ── Velocity (analytical derivatives) ───────────────────
        dx = A * w * math.cos(w * t)
        dy = A * w * (math.cos(w * t) * math.cos(w * t)
                      - math.sin(w * t) * math.sin(w * t))
        # dy simplifies to A * w * cos(2ωt)

        # ── Heading — face direction of travel ──────────────────
        yaw = math.atan2(dy, dx)

        # ── Build and send the TF transform ─────────────────────
        tf_msg = TransformStamped()
        tf_msg.header.stamp = now.to_msg()
        tf_msg.header.frame_id = 'odom'
        tf_msg.child_frame_id = 'base_link'

        tf_msg.transform.translation.x = x
        tf_msg.transform.translation.y = y
        tf_msg.transform.translation.z = 0.0

        qx, qy, qz, qw = euler_to_quaternion(0.0, 0.0, yaw)
        tf_msg.transform.rotation.x = qx
        tf_msg.transform.rotation.y = qy
        tf_msg.transform.rotation.z = qz
        tf_msg.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(tf_msg)

        # ── Append to path & publish ────────────────────────────
        pose = PoseStamped()
        pose.header.stamp = now.to_msg()
        pose.header.frame_id = 'odom'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = qx
        pose.pose.orientation.y = qy
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw

        self.path_msg.poses.append(pose)
        self.path_msg.header.stamp = now.to_msg()
        self.path_pub.publish(self.path_msg)


def main(args=None):
    rclpy.init(args=args)
    node = FigureEightNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
