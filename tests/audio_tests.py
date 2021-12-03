from pyo import *
s = Server().boot()
mod = Sine(freq=200, mul=50)
a = Sine(freq=mod + 440, mul=0.1).out()
s.gui(locals())