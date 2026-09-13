from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            # Launching turtle sim node
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        
        Node(
            # Launching static transform publisher 
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '3', '--y', '3', '--z', '0',
                '--yaw', '0.785398', '--pitch', '0', '--roll', '0',
                '--frame-id', 'world', '--child-frame-id', 'checkpoint'
            ]
        ),

    ])