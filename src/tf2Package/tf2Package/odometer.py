"""
Exercise 4 — odometer.py

TF listener that, once per second, looks up the odom → base_link
transform and reports:
  • current (x, y) position in odom
  • straight-line distance from the origin
  • yaw in degrees

Gracefully handles the case where it is started BEFORE the
broadcaster — it warns instead of crashing.
"""

import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


def quaternion_to_yaw(q):
    """Extract yaw (rotation about Z) from a quaternion."""
    # yaw = atan2(2(wz + xy), 1 - 2(y² + z²))
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class OdometerNode(Node):
    def __init__(self):
        super().__init__('odometer')

        # TF2 buffer + listener — the listener subscribes to /tf and
        # /tf_static automatically and fills the buffer.
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 1 Hz timer
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('odometer node started — reporting at 1 Hz')

    def timer_callback(self):
        try:
            # Look up the latest available transform odom → base_link
            t = self.tf_buffer.lookup_transform(
                'odom',
                'base_link',
                rclpy.time.Time())       # Time(0) = latest available

        except TransformException as ex:
            # Covers LookupException, ConnectivityException,
            # ExtrapolationException — all subclasses of TransformException
            self.get_logger().warn(
                f'Could not get odom → base_link transform: {ex}')
            return

        # ── Extract position ────────────────────────────────────
        x = t.transform.translation.x
        y = t.transform.translation.y

        # ── Straight-line distance from origin ──────────────────
        distance = math.sqrt(x * x + y * y)

        # ── Yaw in degrees ──────────────────────────────────────
        yaw_rad = quaternion_to_yaw(t.transform.rotation)
        yaw_deg = math.degrees(yaw_rad)

        self.get_logger().info(
            f'Position: ({x:.2f}, {y:.2f})  |  '
            f'Distance: {distance:.2f} m  |  '
            f'Yaw: {yaw_deg:.1f}°')


def main(args=None):
    rclpy.init(args=args)
    node = OdometerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
