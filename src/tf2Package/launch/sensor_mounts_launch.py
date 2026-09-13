from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2Package',
            executable='sensor_mounts',
            name='sensor_mounts_node'
        )
    ])