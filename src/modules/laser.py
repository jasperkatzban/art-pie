from gpiozero import LED
from utils.constants import GPIO_LASER

class Laser:
    """Handles turning laser on and off"""

    def __init__(self):
        """Creates laser object"""
        self.laser = LED(GPIO_LASER)

    def on(self):
        """Turns on laser"""
        self.laser.on()

    def off(self):
        """Turns off laser"""
        self.laser.off()