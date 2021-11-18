# import system libs
import os
import sys
import argparse
import logging
import numpy as np
from cv2 import waitKey

# import modules
from modules.audio import Audio
from modules.camera import Camera
from modules.laser import Laser
from modules.motor import Motor

def main(arguments):

    # parse arguments
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-l", "--local", help="specify local environment (not Raspberry Pi)",
                    action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    args = parser.parse_args(arguments)

    # specify if not running on raspberry pi, defaults to true
    ENV_RASPI = False if args.local else True

    # setup logger
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger = logging.getLogger(__name__)

    # intialize camera module, capture and show a single frame
    camera = Camera(env_raspi=ENV_RASPI)
    camera.capture_frame()
    camera.show_frame()

    # initialize audio module, plays noise when you click start
    audio = Audio(env_raspi=ENV_RASPI)
    audio.view_table()
    audio.open_gui()

    # main loop
    while True:
        # escape while running using cv2 interrupt
        if waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))