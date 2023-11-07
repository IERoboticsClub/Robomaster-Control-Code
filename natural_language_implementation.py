from Robot import Robot, RobotCommand, RobotComponents, RobotCommands
import time


# Create a robot object and connect to the robot
# robot = Robot()
# arm = robot.arm

# Hey I would like to move the chassis forward by 0.1 meters and to the right by 0.1 meters
# Example usage

from transformers import pipeline
from enum import Enum
import re

# Your Robot and Enums setup

# ... (Your code for ROBOT, RobotComponents, RobotCommands, and RobotCommand classes)

# Instantiate a pipeline for intent classification and entity recognition
classifier = pipeline("zero-shot-classification")
ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Function to process natural language
def process_natural_language(sentence):
    # Define possible intents
    intents = ["move", "moveto", "recenter", "stop", "open", "close", "status"]

    # Classify the intent of the sentence
    intent_result = classifier(sentence, candidate_labels=intents)
    command = intent_result["labels"][0]

    # Extract entities
    entities = ner(sentence)
    patterns = {
        'x': r'(?:forward|forwards) by ([0-9]+\.?[0-9]*) meters?',
        'y': r'(?:right|to the right) by ([0-9]+\.?[0-9]*) meters?',
        'z': r'(?:upward|upwards) by ([0-9]+\.?[0-9]*) meters?'  # Example for z-axis
    }

    # Initialize args dictionary
    args = {}

    # Extract movements from the sentence
    for key, pattern in patterns.items():
        match = re.search(pattern, sentence, re.IGNORECASE)
        if match:
            # Convert matched strings to float
            args[key] = float(match.group(1))


    # Map the intent to RobotCommands
    command_enum = RobotCommands[command.upper()]

    # Determine the component based on the command
    if command_enum in [RobotCommands.MOVE, RobotCommands.MOVE_TO, RobotCommands.RECENTER, RobotCommands.STOP]:
        component = RobotComponents.CHASSIS
    elif command_enum in [RobotCommands.OPEN, RobotCommands.CLOSE, RobotCommands.STATUS]:
        component = RobotComponents.GRIPPER
    else:
        # Default to ARM for any other command
        component = RobotComponents.ARM

    # Create the RobotCommand
    robot_command = RobotCommand(component, command_enum, args)
    return robot_command

sentence = "Hey I would like to move the chassis forward by 0.1 meters and to the right by 0.1 meters"
command = process_natural_language(sentence)
print(command)

# Send a command to the robot
# use __str__ to get the command string # returns <Robot.RobotCommand object at 0x7faa8ffb0dd0>
