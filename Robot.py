import sys
import socket
import time
from enum import Enum


class Arm:
    """
    I DID NOT WRITE THIS CLASS - CHAT GPT DID
    """
    def __init__(self, robot):
        """
        Initializes a new instance of the Arm class.

        :param robot: A reference to the parent Robot instance to which this arm is attached.
        """
        self.robot = robot

    def move(self, x_dist, y_dist):
        """
        Moves the arm a relative distance from its current position.

        :param x_dist: The distance to move along the x-axis, typically in mm or steps (range could be -500 to 500).
        :param y_dist: The distance to move along the y-axis, typically in mm or steps (range could be -500 to 500).
        """
        self.robot._send(f"robotic_arm move x {x_dist} y {y_dist}")

    def move_to(self, x_pos, y_pos):
        """
        Moves the arm to an absolute position within its range of motion.

        :param x_pos: The target x position, could be within the calibrated range of the arm (e.g., 0 to 1000 mm).
        :param y_pos: The target y position, could be within the calibrated range of the arm (e.g., 0 to 1000 mm).
        """
        self.robot._send(f"robotic_arm moveto x {x_pos} y {y_pos}")

    def recenter(self):
        """
        Recenters the arm to its default position, which is often the center of its range or a home position.
        """
        self.robot._send("robotic_arm recenter")

    def stop(self):
        """
        Stops all arm movement immediately. This is typically an emergency stop that halts all motors.
        """
        self.robot._send("robotic_arm stop")

    def query_position(self):
        """
        Queries the current position of the arm. The response should be parsed to extract the x and y position values.
        """
        self.robot._send("robotic_arm position ?")
        # Implementation for response parsing should be added here.

    def open_gripper(self, level_num):
        """
        Opens the gripper to a specified level. Levels can range from slightly open (1) to fully open (10).

        :param level_num: The level to which the gripper should be opened (e.g., 1 for minimum opening, 10 for maximum).
        """
        self.robot._send(f"robotic_gripper open {level_num}")

    def close_gripper(self, level_num):
        """
        Closes the gripper to a specified level. Levels can range from slightly closed (1) to fully closed (10).

        :param level_num: The level to which the gripper should be closed (e.g., 1 for minimum closing, 10 for maximum).
        """
        self.robot._send(f"robotic_gripper close {level_num}")

    def query_gripper_status(self):
        """
        Queries the current status of the gripper, such as its open/close level and whether it is holding an object.
        """
        self.robot._send("robotic_gripper status ?")


ROBOT = {
    "chassis": {
        "move": {
            "x": float,
            "y": float,
            "z": float
        },
    },
    "robotic_arm": {
        "move": {
            "x": float,
            "y": float
        },
        "moveto": {
            "x": float,
            "y": float
        },
        "recenter": None,
        "stop": None
    },
    "robotic_gripper": {
        "open": int,
        "close": int,
        "status": None
    }
}

class RobotComponents(Enum):
    CHASSIS = "chassis"
    ARM = "robotic_arm"
    GRIPPER = "robotic_gripper"

class RobotCommands(Enum):
    MOVE = "move"
    MOVE_TO = "moveto"
    RECENTER = "recenter"
    STOP = "stop"
    OPEN = "open"
    CLOSE = "close"
    STATUS = "status"


class RobotCommand:
    def __init__(self, component:RobotComponents, command:RobotCommands, args:dict):
        self.component = component
        self.command = command
        self.args = args

    def __process_args(self):
        """
        Processes the args dict into a string for the command
        """
        structure = ROBOT[self.component.value][self.command.value]
        argsString = ""
        for key in structure.keys():
            if key in self.args.keys():
                argsString += f"{key} {self.args[key]} "
        return argsString


    def __str__(self):
        return f"{self.component.value} {self.command.value} {self.__process_args().strip()};"

    def calculate_sleep_time(self):
        """
        Calculates the time to sleep for the command
        """
        pass # TODO: Implement this


class Robot:
    def __init__(self,host:str="192.168.2.1"):
        self.host = host
        self.VX = 1.0
        self.VY = 1.0
        self.VZ = 100.0
        self.arm = Arm(self)
        port = 40923
        self.port = port
        address = (host, int(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting...")
        s.connect(address)
        s.send("command;".encode('utf-8'))
        res = s.recv(1024)
        print(res.decode('utf-8'))
        time.sleep(2)
        print("Connected!")
        self.s = s



    def set_speed(self, x:float=1.0, y:float=1.0, z:float=100.0) -> str:
        self.VX = x
        self.VY = y
        self.VZ = z
        self.s.send(f"speed x {x} y {y} z {z}".encode('utf-8'))
        res = self.s.recv(1024)
        return res.decode('utf-8')

    def time_to_sleep(self, x: float=0.0, y: float=0.0, z: float=0.0) -> float:
        """
        calculates the number of seconds for the command to run and sleeps
        """
        velocity = 0.0
        x = abs(x)
        y = abs(y)
        z = abs(z)
        if x != 0:
            velocity = self.VX
        elif y != 0:
            velocity = self.VY
        elif z != 0:
            velocity = self.VZ
        time_to_sleep = max(x, y, z) / velocity
        return time_to_sleep


    def _send(self, cmd:str):
        sm = "" if ";" in cmd else ";"
        cmd += sm
        print(cmd)
        self.s.send(cmd.encode('utf-8'))
        out = self.s.recv(1024)
        print(out.decode('utf-8'))


    def execute_command(self, command:RobotCommand, sleep:bool=True):
        """
        Executes a single command on the robot
        """
        print(command)


    def chain_commands(self, commands:list[RobotCommand]):
        for command in commands:
            self.execute_command(command)
