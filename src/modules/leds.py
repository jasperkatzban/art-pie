from .opc import Client
import logging
import numpy as np 
from utils.constants import LED_HUE_THRESHOLD_LOWER, LED_HUE_THRESHOLD_UPPER

logger = logging.getLogger(__name__)

class Leds:
    """
    LED control
    """

    def __init__(self, env_raspi=True):
        self.numLED = 33

        try:
            self.client = Client('localhost:7890')
        except Exception as e:
            logger.warn('Could not find fadecandy!')
            logger.warn(e)

        # colors
        self.black = [ (0,0,0) ] * self.numLED
        self.white = [ (0,0,255) ] * self.numLED
        self.purple = [ (102, 0, 204) ] * self.numLED
        self.pink = [ (255, 0, 255) ] * self.numLED
        self.blue = [ (51, 255, 255) ] * self.numLED
        self.green = [ (0, 255, 0) ] * self.numLED

        self.top_thresh = LED_HUE_THRESHOLD_UPPER    
        self.bot_thresh = LED_HUE_THRESHOLD_LOWER

    def set_hue(self, profile_avg):
        if profile_avg <= self.bot_thresh:
            color = self.pink
            logger.debug('Color: Pink')
        elif profile_avg > self.bot_thresh and profile_avg < self.top_thresh:
            color = self.purple
            logger.debug('Color: Purple')
        elif profile_avg >= self.top_thresh:
            color = self.blue
            logger.debug('Color: Blue')
        else:
            color = self.green
            logger.debug('Color: Green')

        logger.debug('Profile Avg: %s' %profile_avg)
        return self.client.put_pixels(color)

    def update(self, profile):
        profile_avg = np.average(profile)
        return self.set_hue(profile_avg)
