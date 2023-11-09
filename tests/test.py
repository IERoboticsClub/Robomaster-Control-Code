# get path from ../sdk
import sys
sys.path.append('../sdk')
from Robot import Robot, RobotCommand, RobotComponents, RobotCommands
import unittest

class TestRobotCommand(unittest.TestCase):
    def test_str(self):
        """
        Test the __str__ method of RobotCommand
        """
        move_command = RobotCommand(RobotComponents.ARM, RobotCommands.MOVE, {"x": 0.1})
        self.assertEqual(str(move_command), "robotic_arm move x 0.1;")
        move_command = RobotCommand(RobotComponents.CHASSIS, RobotCommands.MOVE, {"x": 0.1, "y": 0.1})
        self.assertEqual(str(move_command), "chassis move x 0.1 y 0.1;")
        move_command = RobotCommand(RobotComponents.CHASSIS, RobotCommands.MOVE, {"x": 0.1, "y": 0.1, "z": 0.1})
        self.assertEqual(str(move_command), "chassis move x 0.1 y 0.1 z 0.1;")
        move_command = RobotCommand(RobotComponents.ARM, RobotCommands.MOVE_TO, {"x": 0.1, "y": 0.1})
        self.assertEqual(str(move_command), "robotic_arm moveto x 0.1 y 0.1;")
        move_command = RobotCommand(RobotComponents.ARM, RobotCommands.RECENTER)
        self.assertEqual(str(move_command), "robotic_arm recenter;")


    def test_calculate_sleep_time(self):
        """
        Test the calculate_sleep_time method of RobotCommand
        """
        move_command = RobotCommand(RobotComponents.CHASSIS, RobotCommands.MOVE, {"x": 2})
        self.assertEqual(move_command.calculate_sleep_time(), 2)
        # TODO What we move in x and y
        move_command = RobotCommand(RobotComponents.CHASSIS, RobotCommands.MOVE, {"x": 2, "y": 2})
        self.assertEqual(move_command.calculate_sleep_time(), 2) # DOES IT REALLY?


if __name__ == '__main__':
    unittest.main()
