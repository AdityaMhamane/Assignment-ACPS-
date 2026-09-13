"""
Exercise 9 — rendezvous.py

At 2 Hz, reports:
  1. Range and bearing from robot_a to robot_b
  2. Whether robot_b is within robot_a's 60° forward field of view (±30°)
  3. Where robot_b was 1.5 s ago, expressed in robot_a's CURRENT frame
     (using tf2 advanced time travel: lookup_transform_full)
"""

import math
import rclpy
from rclpy.node import Node
import rclpy.duration
import rclpy.time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class RendezvousNode(Node):
    def __init__(self):
        super().__init__('rendezvous')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 2 Hz timer (period = 0.5 s)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('rendezvous node started — monitoring at 2 Hz')

    def timer_callback(self):
        # -------------------------------------------------------------
        # 1. Range & Bearing from robot_a to robot_b (NOW)
        # -------------------------------------------------------------
        try:
            t_curr = self.tf_buffer.lookup_transform(
                'robot_a',
                'robot_b',
                rclpy.time.Time()  # Latest available transform
            )
        except TransformException as ex:
            self.get_logger().warn(f"Waiting for robot_a → robot_b transform: {ex}")
            return

        dx = t_curr.transform.translation.x
        dy = t_curr.transform.translation.y
        range_m = math.sqrt(dx * dx + dy * dy)
        bearing_rad = math.atan2(dy, dx)
        bearing_deg = math.degrees(bearing_rad)

        # -------------------------------------------------------------
        # 2. 60° forward FOV check: [-30°, +30°]
        # -------------------------------------------------------------
        in_fov = abs(bearing_deg) <= 30.0
        fov_status = "INSIDE (YES)" if in_fov else "OUTSIDE (NO)"

        self.get_logger().info(
            f"Range: {range_m:.2f} m | "
            f"Bearing: {bearing_deg:+.1f}° | "
            f"60° FOV: {fov_status}"
        )

        # -------------------------------------------------------------
        # 3. Where robot_b was 1.5 s ago, in robot_a's CURRENT frame
        # -------------------------------------------------------------
        # Advanced Time Travel using lookup_transform_full:
        #   target_frame: 'robot_a' at target_time (NOW)
        #   source_frame: 'robot_b' at source_time (NOW - 1.5s)
        #   fixed_frame:  'world' (stationary reference frame connecting them)
        time_now = rclpy.time.Time.from_msg(t_curr.header.stamp)
        time_past = time_now - rclpy.duration.Duration(seconds=1.5)

        try:
            t_past = self.tf_buffer.lookup_transform_full(
                target_frame='robot_a',
                target_time=time_now,
                source_frame='robot_b',
                source_time=time_past,
                fixed_frame='world'
            )
            px_past = t_past.transform.translation.x
            py_past = t_past.transform.translation.y
            self.get_logger().info(
                f"↳ robot_b 1.5s ago in robot_a's current frame: (x: {px_past:.2f}, y: {py_past:.2f})"
            )
        except TransformException as ex:
            self.get_logger().warn(
                f"↳ Waiting for 1.5s of history in buffer: {ex}"
            )


def main(args=None):
    rclpy.init(args=args)
    node = RendezvousNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
