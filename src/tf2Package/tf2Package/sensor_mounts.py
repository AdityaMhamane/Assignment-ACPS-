import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

def euler_to_quaternion(roll, pitch, yaw):
    """Converts Euler angles (in radians) to Quaternions"""
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

class SensorMountsNode(Node):
    def __init__(self):
        super().__init__('sensor_mounts')
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        self.publish_transforms()

    def publish_transforms(self):
        # 1. Transform: base_link -> laser
        t_laser = TransformStamped()
        t_laser.header.stamp = self.get_clock().now().to_msg()
        t_laser.header.frame_id = 'base_link'
        t_laser.child_frame_id = 'laser'
        
        t_laser.transform.translation.x = 0.20
        t_laser.transform.translation.y = 0.00
        t_laser.transform.translation.z = 0.15
        
        # Yaw is 0° (0 radians)
        q_laser = euler_to_quaternion(0, 0, 0)
        t_laser.transform.rotation.x = q_laser[0]
        t_laser.transform.rotation.y = q_laser[1]
        t_laser.transform.rotation.z = q_laser[2]
        t_laser.transform.rotation.w = q_laser[3]

        # 2. Transform: base_link -> camera_link
        t_cam = TransformStamped()
        t_cam.header.stamp = self.get_clock().now().to_msg()
        t_cam.header.frame_id = 'base_link'
        t_cam.child_frame_id = 'camera_link'
        
        t_cam.transform.translation.x = 0.10
        t_cam.transform.translation.y = 0.00
        t_cam.transform.translation.z = 0.40
        
        # Yaw is 90° (π/2 radians)
        q_cam = euler_to_quaternion(0, 0, math.pi / 2.0)
        t_cam.transform.rotation.x = q_cam[0]
        t_cam.transform.rotation.y = q_cam[1]
        t_cam.transform.rotation.z = q_cam[2]
        t_cam.transform.rotation.w = q_cam[3]

        # Publish both transforms at once via a list
        self.tf_static_broadcaster.sendTransform([t_laser, t_cam])

def main(args=None):
    rclpy.init(args=args)
    node = SensorMountsNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()