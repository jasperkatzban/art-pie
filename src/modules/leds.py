from opc import Client
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
    
    def set_hue(self, profile, profile_size):
        """
        Make the profile divisible by three an then divide it. Average each of the three sections and use 
        those averages for and rgb value to be sent to the LEDs.

        Args:
            profile: Int array. profile from camera.
            profile_size: Int. length of the profile.
        
        Return:
            rgb_array: a 9 digit rgb list in an array.
        """
        profile_remain = profile_size % 3
        if profile_remain != 0:
            new_profile_length = profile_size - profile_remain
            profile = profile[0:new_profile_length]
        
        trip = len(profile) / 3
        
        red_val = profile[0:trip+1]
        green_val = profile[trip+1:trip*2+1]
        blue_val = profile[trip*2+1:]
        
        red_avg = np.average(red_val)
        green_avg = np.average(green_val)
        blue_avg = np.average(blue_val)

        rgb_array = (red_avg, green_avg, blue_avg) 

        return rgb_array

    # def set_hue_avg(self, profile_avg):
    #     if profile_avg <= self.bot_thresh:
    #         color = self.pink
    #         logger.debug('Color: Pink')
    #     elif profile_avg > self.bot_thresh and profile_avg < self.top_thresh:
    #         color = self.purple
    #         logger.bedug('Color: Purple')
    #     elif profile_avg >= self.top_thresh:
    #         color = self.blue
    #         logger.debug('Color: Blue')
    #     else:
    #         color = self.green
    #         logger.debug('Color: Green')

    #     logger.debug('Profile Avg: %s' %profile_avg)
    #     return self.client.put_pixels(color)

    def update(self, profile, profile_size):
        color = [self.set_hue(profile, profile_size)] * self.numLED
        return self.client.put_pixels(color)