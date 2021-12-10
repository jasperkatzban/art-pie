# !/usr/bin/env python

from modules.opc import *
import logging

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

"""
    for i in range(0, 17):
        pink = [ (255, 0, 255) ] * i
        client.put_pixels(pink)
        time.sleep(1)
        blue = [ (51, 255, 255) ] * i
        client.put_pixels(blue)
        time.sleep(1)
    for range(17,34):
        blue = [ (51, 255, 255) ] * i
        client.put_pixels(blue)
        time.sleep(1)
        pink = [ (255, 0, 255) ] * i
        client.put_pixels(pink)
        time.sleep(1)
"""