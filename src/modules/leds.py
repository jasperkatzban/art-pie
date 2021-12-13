from .opc import Client
import logging
import numpy as np 

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

        self.bot_thresh = 0.3
        self.top_thresh = 0.7    

    ## CALL INSIDE OF MAIN UPDATE FUNCTION

    def set_hue(self, profile_avg):
        if profile_avg <= self.bot_thresh:
            color = self.pink
        elif profile_avg > self.bot_thresh and profile_avg < self.top_thresh:
            color = self.purple
        elif profile_avg >= self.top_thresh:
            color = self.blue
        else:
            color = self.green
        
        return self.client.put_pixels(color)

    def update(self, profile):
        profile_avg = np.average(profile)
        return self.set_hue(profile_avg)
