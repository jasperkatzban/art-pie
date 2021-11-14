from gpiozero import LED
from utils.constants import GPIO_LASER
import logging

logger = logging.getLogger(__name__)

class Laser:
    """Handles turning laser on and off"""

    def __init__(self):
        """Creates laser object"""
        logger.info('Initializing laser module!')
        self.laser = LED(GPIO_LASER)

    def on(self):
        """Turns on laser"""
        logger.info('Turning laser on!')
        self.laser.on()

    def off(self):
        """Turns off laser"""
        logger.info('Turning laser off!')
        self.laser.off()

    def is_lit(self):
        """Check if power to laser is on"""
        return self.laser.is_lit