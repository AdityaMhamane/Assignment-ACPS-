"""
Exercise 5 — chain_demo.py

Demonstrates tf2 automatic frame chaining.

Nobody publishes odom → camera_link directly, but tf2 knows:
    odom → base_link        (from figure_eight.py,  Exercise 3)
    base_link → camera_link (from sensor_mounts.py, Exercise 2)

so it walks the tree and composes them for us:
    odom → base_link → camera_link
"""

import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


def quaternion_to_yaw(q):
    """Extract yaw (rotation about Z) from a quaternion."""
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class ChainDemoNode(Node):
    def __init__(self):
        super().__init__('chain_demo')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 1 Hz timer
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info(
            'chain_demo started — looking up odom → camera_link (chained)')

    def timer_callback(self):
        try:
            # Ask tf2 for odom → camera_link.
            # Nobody broadcasts this directly — tf2 chains:
            #   odom → base_link → camera_link
            t = self.tf_buffer.lookup_transform(
                'odom',
                'camera_link',
                rclpy.time.Time())

        except TransformException as ex:
            self.get_logger().warn(
                f'Could not get odom → camera_link: {ex}')
            return

        x = t.transform.translation.x
        y = t.transform.translation.y
        z = t.transform.translation.z
        yaw_deg = math.degrees(quaternion_to_yaw(t.transform.rotation))

        self.get_logger().info(
            f'odom → camera_link  |  '
            f'Position: ({x:.2f}, {y:.2f}, {z:.2f})  |  '
            f'Yaw: {yaw_deg:.1f}°')


def main(args=None):
    rclpy.init(args=args)
    node = ChainDemoNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
