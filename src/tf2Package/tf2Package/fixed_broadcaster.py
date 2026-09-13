"""
Exercise 8 — fixed_broadcaster.py

This is the corrected version of broken.py with all 4 bugs fixed.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class FixedBroadcaster(Node):
    def __init__(self):
        super().__init__('fixed_broadcaster')
        self.br = TransformBroadcaster(self)
        self.t0 = self.get_clock().now()

        self.msg = TransformStamped()
        
        # BUG 2 FIXED: Removed the leading slash. TF2 strictly forbids leading slashes.
        self.msg.header.frame_id = 'odom'
        self.msg.child_frame_id = 'base_link'
        
        # BUG 3 FIXED: Changed 0 to 0.0. ROS 2 strictly enforces float types.
        self.msg.transform.translation.z = 0.0
        
        # BUG 4 FIXED: Changed w=0.0 to w=1.0. An all-zero quaternion is invalid.
        self.msg.transform.rotation.w = 1.0

        self.create_timer(0.05, self.tick)

    def tick(self):
        # BUG 1 FIXED: Moved the timestamp update into the timer loop!
        # It must be updated every tick, otherwise the transform is stuck in the past.
        self.msg.header.stamp = self.get_clock().now().to_msg()
        
        el = (self.get_clock().now() - self.t0).nanoseconds * 1e-9
        self.msg.transform.translation.x = 2.0 * math.cos(0.4 * el)
        self.msg.transform.translation.y = 2.0 * math.sin(0.4 * el)
        self.br.sendTransform(self.msg)


def main():
    rclpy.init()
    rclpy.spin(FixedBroadcaster())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
