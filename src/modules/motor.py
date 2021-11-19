from utils.constants import GPIO_MOTOR_FORWARD, GPIO_MOTOR_BACKWARD, MOTOR_SPEED
import logging

logger = logging.getLogger(__name__)

class Motor:
    """Handle controlling motor to turn turnable"""

    def __init__(self):
        logger.info('Initializing motor module!')
        pass

    def start(self):
        """Start turntable motor"""
        # TODO: smooth ramp up speed
        logger.info('Turning motor on!')
        pass

    def stop(self):
        """Start turntable motor"""
        # TODO: smooth ramp down speed
        logger.info('Stopping motor!')
        pass

    def is_active(self):
        """Check if motor is active"""
        pass