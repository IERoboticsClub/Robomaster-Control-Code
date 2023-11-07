from Robot import Robot, RobotCommand, RobotComponents, RobotCommands
import time


# Create a robot object and connect to the robot
# robot = Robot()
# arm = robot.arm

move_command = RobotCommand(RobotComponents.CHASSIS, RobotCommands.MOVE, {"x": 0.1, "y": 0.1})

# Send a command to the robot
# use __str__ to get the command string # returns <Robot.RobotCommand object at 0x7faa8ffb0dd0>
# so does setting __repr__ to __str__
print(move_command)
