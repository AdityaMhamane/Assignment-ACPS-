"""Launch file for Exercise 3.

Runs:
  1. figure_eight  — broadcasts dynamic odom → base_link (50 Hz)
  2. sensor_mounts — broadcasts static  base_link → laser  &  base_link → camera_link

Together these give a full TF tree:
    odom → base_link → laser
                     → camera_link
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2Package',
            executable='figure_eight',
            name='figure_eight',
            output='screen',
        ),
        Node(
            package='tf2Package',
            executable='sensor_mounts',
            name='sensor_mounts',
            output='screen',
        ),
    ])
