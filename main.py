from Robot import Robot
import time


# Create a robot object and connect to the robot
robot = Robot()
arm = robot.arm
# arm.close_gripper(4)
# arm.open_gripper(4)
robot.move(-0.5,0,0)
