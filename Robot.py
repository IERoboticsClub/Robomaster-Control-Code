import sys
import socket
import time


class Arm:
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




class Robot:
    def __init__(self,host="192.168.2.1"):
        self.host = host
        self.VX = 1
        self.VY = 1
        self.VZ = 100
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



    def set_speed(self, x, y, z):
        self.VX = x
        self.VY = y
        self.VZ = z
        self.s.send(f"speed x {x} y {y} z {z}".encode('utf-8'))

    def time_to_sleep(self, x: float, y:float, z:float):
        """
        calculates the number of seconds for the command to run and sleeps
        """
        velocity = 0
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



    def move(self, x:float=0, y:float=0, z:float=0):
        """
        This function moves the robot in the x, y, and z directions
        Args:
            x (float): distance to move in the x direction
            y (float): distance to move in the y direction
            z (float): distance to move in the z direction
        """
        print(x,y,z)
        command = f"chassis move x {x} y {y} z {z}"
        self._send(command)
        time.sleep(self.time_to_sleep(x, y, z))

    def move_forward(self, distance:float):
        self.move(x=distance)
