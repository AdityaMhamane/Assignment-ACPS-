"""
Launch file for Exercise 9: Two-Robot Rendezvous Mini-Project

Launches:
  1. two_robots_broadcaster: publishes world -> robot_a, world -> robot_b, and static front_sensors
  2. rendezvous: monitors range, bearing, 60° FOV, and time-travel position at 2 Hz
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2Package',
            executable='two_robots_broadcaster',
            name='two_robots_broadcaster',
            output='screen',
        ),
        Node(
            package='tf2Package',
            executable='rendezvous',
            name='rendezvous',
            output='screen',
        ),
    ])
