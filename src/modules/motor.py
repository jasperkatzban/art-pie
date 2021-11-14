from gpiozero import Motor as m
from utils.constants import GPIO_MOTOR_FORWARD, GPIO_MOTOR_BACKWARD, MOTOR_SPEED
import logging

logger = logging.getLogger(__name__)

class Motor:
    """Handle controlling motor to turn turnable"""

    def __init__(self):
        logger.info('Initializing motor module!')
        self.motor = m(forward=GPIO_MOTOR_FORWARD, backward=GPIO_MOTOR_BACKWARD, pwm=True)

    def start(self):
        """Start turntable motor"""
        # TODO: smooth ramp up speed
        logger.info('Turning motor on!')
        self.motor.forward(MOTOR_SPEED)

    def stop(self):
        """Start turntable motor"""
        # TODO: smooth ramp down speed
        logger.info('Stopping motor!')
        self.motor.stop()
        

    def is_active(self):
        """Check if motor is active"""
        return self.motor.is_active