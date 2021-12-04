#!/user/bin/env python

import opc, time

sideLEDs = 12
topLEDs = 20

client = opc.Client('localhost:7890')

black = [ (0,0,0) ] * topLEDs
white = [ (255,255,255) ] * topLEDs
black = [ (0,0,0) ] * sideLEDs
white = [ (255,255,255) ] * sideLEDs

client.put_pixels(black)
client.put_pixels(black)
time.sleep(0.5)
client.put_pixels(white)
