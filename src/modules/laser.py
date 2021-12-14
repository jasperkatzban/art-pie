from utils.constants import GPIO_LASER
import logging

logger = logging.getLogger(__name__)

try:
    from gpiozero import LED
except:
    logger.warning('Unable to import gpiozero module! Assuming program is not running on a Raspberry Pi.')

class Laser:
    """Handles turning laser on and off"""

    def __init__(self, env_raspi):
        """Creates laser object"""

        self.env_raspi = env_raspi

        logger.info('Initializing laser module!')
        if self.env_raspi:
            self.laser = LED(GPIO_LASER)

    def on(self):
        """Turns on laser"""
        logger.info('Turning laser on!')
        if self.env_raspi:
            self.laser.on()

    def off(self):
        """Turns off laser"""
        logger.info('Turning laser off!')
        if self.env_raspi:
            self.laser.off()

    def is_lit(self):
        """Check if power to laser is on"""
        if self.env_raspi:
            return self.laser.is_lit
    
    def toggle(self):
        """Toggles laser state"""
        logger.info('Toggling laser!')
        if self.env_raspi:
            self.laser.toggle()