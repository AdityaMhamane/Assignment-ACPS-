from setuptools import find_packages, setup

package_name = 'tf2Package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/assign1_launch.py',
            'launch/sensor_mounts_launch.py',
            'launch/figure_eight_launch.py',
            'launch/rendezvous_launch.py',
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aditya3a',
    maintainer_email='aditya3a@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tf2IntroNode = tf2Package.tf2IntroNode:main',
            'sensor_mounts = tf2Package.sensor_mounts:main',
            'figure_eight = tf2Package.figure_eight:main',
            'odometer = tf2Package.odometer:main',
            'chain_demo = tf2Package.chain_demo:main',
            'obstacle_mapper = tf2Package.obstacle_mapper:main',
            'fixed_broadcaster = tf2Package.fixed_broadcaster:main',
            'time_traveller = tf2Package.time_traveller:main',
            'two_robots_broadcaster = tf2Package.two_robots_broadcaster:main',
            'rendezvous = tf2Package.rendezvous:main',
        ],
    },
)
