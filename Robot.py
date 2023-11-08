"""
Using this file, you can control the robot.
"""
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
    """
    With this class, you can create a command to send to the robot.
    """
    def __init__(self, component:RobotComponents, command:RobotCommands, args:dict={}):
        """
        Initializes a new instance of the RobotCommand class.

        :param component: The component to which the command should be sent.
        :param command: The command to send to the component.
        :param args: A dictionary of arguments to send with the command. (optional)

        Example usage:
        move_command = RobotCommand(RobotComponents.ARM, RobotCommands.MOVE, {"x": 0.1})

        """
        self.component = component
        self.command = command
        self.args = args
        self.VX = 1.0
        self.VY = 1.0
        self.VZ = 100.0

    def __process_args(self):
        """
        Processes the args dict into a string for the command
        """
        if self.args == {}:
            return ""
        structure = ROBOT[self.component.value][self.command.value]
        argsString = ""
        for key in structure.keys():
            if key in self.args.keys():
                argsString += f"{key} {self.args[key]} "
        return argsString

    def __str__(self):
        command = f"{self.component.value} {self.command.value} {self.__process_args().strip()}"
        return command.strip() + ";"

    def calculate_sleep_time(self):
        """
        Calculates the time to sleep for the command
        """
        time_to_sleep = 0.0
        # kinematics
        if self.component == RobotComponents.CHASSIS:
            if self.command == RobotCommands.MOVE:
                # compute vector x,y
                x = self.args["x"] if "x" in self.args.keys() else 0.0
                y = self.args["y"] if "y" in self.args.keys() else 0.0
                time_x = abs(x/self.VX)
                time_y = abs(y/self.VY)
                time_to_sleep = max(time_x, time_y) * 1.5
                if 'z' in self.args.keys() and self.args['z'] != 0:
                    time_to_sleep = self.args['z'] / self.VZ
        print(time_to_sleep)
        return time_to_sleep


class Robot:
    """
    A class for controlling the robot.
    """
    def __init__(self, host: str = "192.168.2.1"):
        self.host = host
        self.arm = Arm(self)
        self.port = 40923
        self.connect()

    def connect(self, host: str = None, port: int = None) -> bool:
        """
        Connects to the robot
        """
        if host is None:
            host = self.host
        if port is None:
            port = self.port
        address = (host, int(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Connecting...")
            s.connect(address)
            s.send("command;".encode('utf-8'))
            out = s.recv(1024)
            print(out.decode('utf-8'))
            print("Connected!")
            self.s = s
            return True
        except Exception as e:
            print(e)
            return False

    def set_speed(self, x: float = 1.0, y: float =1.0, z: float = 100.0) -> str:
        """
        Sets the speed of the robot
        """
        self.v_x = x
        self.v_y = y
        self.v_z = z
        self.s.send(f"speed x {x} y {y} z {z}".encode('utf-8'))
        res = self.s.recv(1024)
        return res.decode('utf-8')

    def _send(self, cmd: str):
        _sm = "" if ";" in cmd else ";"
        cmd += _sm
        print(cmd)
        self.s.send(cmd.encode('utf-8'))
        out = self.s.recv(1024)
        print(out.decode('utf-8'))

    def __is_moving(self) -> bool:
        """
        Tells use if the chassis is moving
        """
        self.s.send("chassis status ?;".encode('utf-8'))
        out = self.s.recv(1024).decode('utf-8')
        return int(out.split(" ")[0]) == 0



    def execute_command(self, command: RobotCommand, sleep: bool = True):
        """
        Executes a single command on the robot
        """
        print(command)
        self._send(str(command))
        time.sleep(1)
        status = True # have to set to true, sometimes will overlap with non movement
        while status:
            # so we check if the thing is moving
            # this means command is not yet done
            status = self.__is_moving() # I think this only works for things like chassis
            # to get around this we can pass the command to the is_moving
            # then create separate logic for other parts
            print("moving")

        print("Done")

    def chain_commands(self, commands: list[RobotCommand]):
        """
        Chains a list of commands together
        """
        for command in commands:
            self.execute_command(command)
