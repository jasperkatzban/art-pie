# import stepper motor libs
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import logging
import time

from utils.constants import MOTOR_NUM_STEPS_REVOLUTION

logger = logging.getLogger(__name__)

class Motor:
    """Handle controlling motor to turn turnable"""

    def __init__(self):
        """Initializes motor object on motor shield"""
        logger.info('Initializing motor module!')
        self.kit = MotorKit()

    def step(self, num_steps=1, backwards=False):
        """Move the motor a specified number of steps"""
        for _ in range(num_steps):
            logger.debug('Steping Motor!')
            if backwards:
                self.kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
            else:
                self.kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        
    def full_turn(self, backwards=False):
        """Moves the motor one revolution. Set `backwards` flag to change direction"""
        logger.debug('Starting full revolution of motor!')
        self.step(num_steps=MOTOR_NUM_STEPS_REVOLUTION, backwards=backwards)
        logger.debug('Motor revolution complete!')

    def release(self):
        """Release motor hold"""
        logger.debug('Releasing motor hold!')
        self.kit.stepper1.release()