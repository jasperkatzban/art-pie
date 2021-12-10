#!/user/bin/env python

import opc, time

numLED = 32 # Total num of LEDs


client = opc.Client('localhost:7890')

black = [ (0,0,0), (0,0,0) ] * numLED
white = [ (255,255,255), (0,0,0) ] * numLED

client.put_pixels(white)
