from pyo import *
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Audio:
    """Handle audio generation"""

    def __init__(self, env_raspi=True):
        logger.info('Initializing audio module!')

        # Initialize audio server
        self.s = Server().boot()

        # Get the length of an audio block.
        self.bs = self.s.getBufferSize()

        # Create a table of length `buffer size` and read it in loop.
        self.t = DataTable(size=self.bs)
        self.osc = TableRead(self.t, freq=self.t.getRate(), loop=True, mul=.1).out()

        # Share the table's memory with a numpy array.
        self.arr = np.asarray(self.t.getBuffer())

        # Make empty array of samples, which we update with time
        self.curr_samples = []

        # Register the `set_waveform` function to be called at the beginning
        # of every processing loop.
        self.s.setCallback(self.set_waveform)

    def view_table(self):
        """Opens a window to view the current waveform."""
        # table = AtanTable(slope=0.5, size=512)
        # table.view()
        self.t.view()
        print(self.t.getTable())

    def open_gui(self):
        """Initializes gui."""
        self.s.gui(locals())
        
    def set_samples_from_noise(self):
        """Generates white noise."""
        self.curr_samples = self.generate_noise(size=self.bs)

    def generate_noise(self, size):
        """Generates array of noise of specified size"""
        return np.random.normal(0.0, 1, size=size)

    def set_samples_from_profile(self, profile):
        """Generates sound based on a list of values"""
        self.curr_samples = profile

    def set_waveform(self):
        """Sets current sample array to list of values."""
        self.arr[:] = self.curr_samples

    def get_buffer_size(self):
        """Returns current buffer size."""
        return self.bs

    def start(self):
        self.s.start()