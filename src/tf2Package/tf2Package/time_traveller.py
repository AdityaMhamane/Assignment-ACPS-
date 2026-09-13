"""
Exercise 7 — time_traveller.py

Demonstrates time-indexed TF2 buffer lookups and hitting the buffer cache limit.
Once per second, this node:
  1. Looks up the robot's position *now* (latest available transform).
  2. Looks up the robot's position *2 seconds ago*.
  3. Computes the straight-line distance between the two.
  4. Attempts a lookup *30 seconds ago* and cleanly catches/reports the exception.
"""

import math
import rclpy
from rclpy.node import Node
import rclpy.duration
import rclpy.time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class TimeTravellerNode(Node):
    def __init__(self):
        super().__init__('time_traveller')

        # The TF2 Buffer stores transforms in a time-indexed circular cache (default: 10 seconds)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Run lookup once per second
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('time_traveller node started — querying past transforms at 1 Hz')

    def timer_callback(self):
        # -------------------------------------------------------------
        # 1. Robot position NOW (latest available transform)
        # -------------------------------------------------------------
        try:
            t_now = self.tf_buffer.lookup_transform(
                'odom',
                'base_link',
                rclpy.time.Time()  # Time() = latest available
            )
        except TransformException as ex:
            self.get_logger().warn(f"odom → base_link not yet available: {ex}")
            return

        x_now = t_now.transform.translation.x
        y_now = t_now.transform.translation.y
        z_now = t_now.transform.translation.z
        self.get_logger().info(f"1. Position NOW: ({x_now:.2f}, {y_now:.2f}, {z_now:.2f})")

        # Use the timestamp of the latest transform as our time reference
        stamp_now = rclpy.time.Time.from_msg(t_now.header.stamp)

        # -------------------------------------------------------------
        # 2. Robot position 2 SECONDS AGO
        # -------------------------------------------------------------
        time_2s_ago = stamp_now - rclpy.duration.Duration(seconds=2.0)
        try:
            t_2s = self.tf_buffer.lookup_transform(
                'odom',
                'base_link',
                time_2s_ago
            )
            x_2s = t_2s.transform.translation.x
            y_2s = t_2s.transform.translation.y
            z_2s = t_2s.transform.translation.z
            self.get_logger().info(f"2. Position 2s AGO: ({x_2s:.2f}, {y_2s:.2f}, {z_2s:.2f})")

            # ---------------------------------------------------------
            # 3. Distance between NOW and 2 SECONDS AGO
            # ---------------------------------------------------------
            distance = math.sqrt(
                (x_now - x_2s) ** 2 +
                (y_now - y_2s) ** 2 +
                (z_now - z_2s) ** 2
            )
            self.get_logger().info(f"3. Distance between the two: {distance:.2f} m")

        except TransformException as ex:
            self.get_logger().warn(f"2/3. 2s ago lookup failed (less than 2s elapsed): {ex}")

        # -------------------------------------------------------------
        # 4. Attempt lookup 30 SECONDS in the past (Clean exception report)
        # -------------------------------------------------------------
        time_30s_ago = stamp_now - rclpy.duration.Duration(seconds=30.0)
        try:
            t_30s = self.tf_buffer.lookup_transform(
                'odom',
                'base_link',
                time_30s_ago
            )
            self.get_logger().info(
                f"4. 30s AGO unexpectedly succeeded: ({t_30s.transform.translation.x:.2f}, {t_30s.transform.translation.y:.2f})"
            )
        except TransformException as ex:
            # Expected because default tf2 Buffer cache size is 10.0 seconds
            self.get_logger().warn(
                f"4. 30s AGO lookup failed as expected (buffer cache limit exceeded): {ex}"
            )


def main(args=None):
    rclpy.init(args=args)
    node = TimeTravellerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
