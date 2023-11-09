# Getting Started with Robomaster

The Robomaster S1 is a great robot for learning about robotics and programming. This repository contains a collection of resources to help you get started with the Robomaster S1. Our SDK implements a simple interface for controlling the robot and its components. We also provide a collection of examples to help you get started with your own projects.

## Connecting to the Robot
There are 3 ways to connect to the robot:
1. Robot as router
2. Robot as client
3. Robot via USB

### Robot as router
This is the most ideal method for connecting to the robot. The robot will act as a router and you can connect to it directly from your computer. This method is the most reliable and has the lowest latency. To connect to the robot as a router, follow these steps:
1. Turn on the robot and wait for it to boot up.
2. Look at the sticker attached to the conenection module on the robot. It should look something like this:
![Connection Module](images/connection_module.jpg)
3. Connect to the Wi-Fi network with the name and password shown on the sticker.


## Interfacing with the Robot
Once you are connected to the robots Wi-Fi network, you can start by connecting the the robots network socket, this is done automatically when you create the `Robot` object:

```python
from Robot import Robot
```

From here on out, you can use the `Robot` object to control the robot. The `Robot` object has a number of methods for controlling the robot.



## Commanding the Robot
The SDK provides a `RobotCommand` object that can be used to control any part of the robot. The `RobotCommand` object is a simple interface which takes at least 3 inputs: `RobotComponents`, `RobotCommands` and a dictionary of `arguments`.

### RobotComponents
Currently available components are:
- `CHASSIS`
- `ARM`
- `GRIPPER`

### RobotCommands
Currently available commands are:
- `MOVE`
- `MOVE_TO`
- `RECENTER`
- `STOP`
- `OPEN`
- `CLOSE`
- `STATUS`


### Arguments
The arguments dictionary is a collection of key-value pairs that are used to specify the command. The arguments dictionary is different for each command. For example, the `MOVE` command takes `x,y,z` coordinates as arguments, while the `RECENTER` command takes no arguments.
