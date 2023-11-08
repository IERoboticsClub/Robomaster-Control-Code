from Robot import Robot, RobotCommand, RobotComponents, RobotCommands
import time


# Create a robot object and connect to the robot
# robot = Robot()
# arm = robot.arm

move_command = RobotCommand(RobotComponents.ARM, RobotCommands.MOVE, {"x": 0.1})

# Send a command to the robot
print(move_command)
