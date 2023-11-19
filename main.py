from Robot import Robot, RobotCommand, RobotComponents, RobotCommands
import time


# Create a robot object and connect to the robot
robot = Robot()
arm = robot.arm

recenter_arm = RobotCommand(RobotComponents.ARM, RobotCommands.RECENTER)

movements = [
    #x, y, z
#     [4, 0, 0],
#     [0, 0.5, 0],
#     [3, 0, 0],
    [0,-0.2,0],
]

commands = [
    RobotCommand(RobotComponents.CHASSIS, RobotCommands.MOVE, {"x": m[0], "y": m[1], "z": m[2]})
    for m in movements
]



for command in commands:
    print(">>>>>>>>>>>>>>>>>")
    robot.execute_command(command)
    print("<<<<<<<<<<<<<<<<<")
    time.sleep(2)
