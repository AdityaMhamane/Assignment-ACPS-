"""
Exercise 6 — obstacle_mapper.py

The laser reports a hit at (1.5, 0.0, 0.0) in the 'laser' frame.
This node transforms that point into the 'odom' frame and prints it.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros import TransformException

# Required to use tf2_geometry_msgs.do_transform_point or buffer.transform
import tf2_geometry_msgs


class ObstacleMapperNode(Node):
    def __init__(self):
        super().__init__('obstacle_mapper')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # 1 Hz timer
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('obstacle_mapper started — projecting laser hit to odom')

    def timer_callback(self):
        # 1. Define the obstacle in the laser frame
        pt_laser = PointStamped()
        pt_laser.header.frame_id = 'laser'
        pt_laser.header.stamp = rclpy.time.Time().to_msg()
        
        pt_laser.point.x = 1.5
        pt_laser.point.y = 0.0
        pt_laser.point.z = 0.0

        try:
            # 2. Look up the transform from laser -> odom
            transform = self.tf_buffer.lookup_transform(
                'odom',
                'laser',
                rclpy.time.Time()
            )
            
            # 3. Apply the transform to our point
            pt_odom = tf2_geometry_msgs.do_transform_point(pt_laser, transform)

            self.get_logger().info(
                f"Obstacle in odom  |  "
                f"x: {pt_odom.point.x:.2f}, y: {pt_odom.point.y:.2f}, z: {pt_odom.point.z:.2f}"
            )

        except TransformException as ex:
            self.get_logger().warn(f'Could not transform point: {ex}')


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleMapperNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
