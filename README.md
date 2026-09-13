# ROS 2 TF2 Assignments

This repository contains solutions for nine ROS 2 TF2 assignments.

- `Assignment Sol/` contains one Markdown solution guide for each assignment.
- `src/` contains the ROS 2 Python package used by the solutions.
- The solution guides include the terminal commands, expected output, screenshots, and TF tree files where applicable. Open the `READMEassign*.md` file inside an assignment folder to follow that assignment and view its results directly on GitHub.

## Prerequisites

Install and source a supported ROS 2 distribution on Ubuntu. The examples use ROS 2 packages including `rclpy`, `tf2_ros`, `tf2_geometry_msgs`, `geometry_msgs`, `nav_msgs`, `turtlesim`, `launch`, `launch_ros`, and RViz2.

You will also need:

- `colcon`
- `rosdep`
- the ROS 2 TF2 and turtlesim packages for your distribution

## Setup

### Option 1: Clone this repository

Create a new ROS 2 workspace and copy this package into its `src` directory:

```bash
git clone https://github.com/AdityaMhamane/Assignment-ACPS-.git
mkdir -p ~/tf2_ws/src
cp -r <repository-directory>/src/tf2Package ~/tf2_ws/src/
cd ~/tf2_ws
```

Replace `<repository-url>` and `<repository-directory>` with the values for your checkout.

### Option 2: Copy the `src` folder manually

If this repository is already downloaded, run:

```bash
mkdir -p ~/tf2_ws/src
cp -r /path/to/this/repository/src/tf2Package ~/tf2_ws/src/
cd ~/tf2_ws
```

### Build the workspace

Source ROS 2 first, then install package dependencies and build:

```bash
source /opt/ros/<ros-distro>/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Replace `<ros-distro>` with the ROS 2 distribution installed on your system, such as `humble` or `jazzy`.

## Running the assignments

Each assignment has its own instructions and evidence:

| Assignment | Solution guide |
| --- | --- |
| 1 | [Exercise 1: Turtlesim and TF2](Assignment%20Sol/Excercise1_Solutions/READMEassign1.md) |
| 2 | [Exercise 2: Sensor mounts](Assignment%20Sol/Excercise2_Solutions/READMEassign2.md) |
| 3 | [Exercise 3](Assignment%20Sol/Excercise3_Solutions/READMEassign3.md) |
| 4 | [Exercise 4](Assignment%20Sol/Excercise4_Solutions/READMEassign4.md) |
| 5 | [Exercise 5](Assignment%20Sol/Excercise5_Solutions/READMEassign5.md) |
| 6 | [Exercise 6](Assignment%20Sol/Excercise6_Solutions/READMEassign6.md) |
| 7 | [Exercise 7: Time travel](Assignment%20Sol/Excercise7_Solutions/READMEassign7.md) |
| 8 | [Exercise 8](Assignment%20Sol/Excercise8_Solutions/READMEassign8.md) |
| 9 | [Exercise 9: Two-robot rendezvous](Assignment%20Sol/Excercise9_Solutions/READMEassign9.md) |

Before running a command in a new terminal, source both the system ROS 2 installation and this workspace:

```bash
source /opt/ros/<ros-distro>/setup.bash
source ~/tf2_ws/install/setup.bash
```

The workspace command is `source install/setup.bash`; there is no `install.sh` file in this repository. Keep the nodes that belong to the same exercise running in separate terminals, and source the workspace in every terminal.

Most package commands follow this form:

```bash
ros2 launch tf2Package <launch-file>.py
ros2 run tf2Package <node-name>
```

Use the exact launch files, node names, terminal arrangement, and verification commands shown in the relevant assignment guide.

## Repository layout

```text
.
├── Assignment Sol/
│   ├── Excercise1_Solutions/
│   ├── Excercise2_Solutions/
│   ├── Excercise3_Solutions/
│   ├── Excercise4_Solutions/
│   ├── Excercise5_Solutions/
│   ├── Excercise6_Solutions/
│   ├── Excercise7_Solutions/
│   ├── Excercise8_Solutions/
│   └── Excercise9_Solutions/
├── src/
│   └── tf2Package/
│       ├── launch/
│       ├── resource/
│       ├── test/
│       └── tf2Package/
└── README.md
```
