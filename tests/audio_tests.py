from pyo import *
s = Server(duplex=0, audio='jack').boot()
mod = Sine(freq=200, mul=50)
a = Sine(freq=mod + 440, mul=0.1).out()
s.gui(locals())