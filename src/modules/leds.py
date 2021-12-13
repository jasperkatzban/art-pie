# !/usr/bin/env python

from modules.opc import *
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

        self.counter = 0
        self.color_state = 0

        self.color_state_map = [self.pink, self.purple, self.blue]
    
    def update(self):
        if self.counter % 100 == 0:

            if self.color_state >= 2:
                self.color_state = 0
            else:
                logger.debug('Changing led color!')
                self.color_state += 1

            self.client.put_pixels(self.color_state_map[self.color_state])
        
        self.counter += 1

    def set_color_blue(self):
        """Set leds to specific color"""
        self.client.put_pixels(self.blue)
