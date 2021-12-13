# import system libs
import os
import sys
import argparse
import logging
import numpy as np
from cv2 import waitKey
from timeit import default_timer as timer

# import modules
from modules.audio import Audio
from modules.camera import Camera
from modules.laser import Laser
from modules.motor import Motor
from modules.leds import Leds

def main(arguments):

    # parse arguments
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-l", "--local", help="specify local environment (not Raspberry Pi)",
                    action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("-i", "--image", help="specify path to input image for testing")
    parser.add_argument("-p", "--preview", help="preview camera image",
                    action="store_true")
    parser.add_argument("-m", "--use-morph", help="slower but more accurate profile generation using morphological transformations",
                    action="store_true")
    parser.add_argument("--volume", type=int, help="set volume to integer between 0 and 100")
    args = parser.parse_args(arguments)

    # specify if not running on raspberry pi, defaults to true
    ENV_RASPI = False if args.local else True

    # setup logger
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger = logging.getLogger(__name__)

    # intialize camera module, capture and show a single frame
    camera = Camera(env_raspi=ENV_RASPI, filename=args.image, use_morph=args.use_morph)
   
    # initialize audio module
    audio = Audio(env_raspi=ENV_RASPI, volume=args.volume)

    # initialize motor module
    motor = Motor(env_raspi=ENV_RASPI)

    # initialize laser module
    laser = Laser(env_raspi=ENV_RASPI)

    # initialize led strips
    leds = Leds(env_raspi=ENV_RASPI)

    # set profile array size
    profile_size = audio.get_buffer_size()
    camera.set_profile_size(profile_size)

    # start audio engine
    audio.start()

    # turn on laser
    laser.on()

    # begin spinning motor
    # motor.start_spin()

    # main loop, this iterates continuously forever
    while True:
        # timing the main loop for debugging purposes
        if args.verbose:
            start = timer()

        # take picture if not using a test image
        if not args.image:
            camera.capture_frame()

        # create profile and send to audio engine
        profile = camera.get_profile()
        audio.set_samples_from_profile(profile)

        # # move the motor by one step
        # motor.step(100)
        motor.start_spin()

        # led callback
        leds.update(profile)

        # draw coords on frame
        if args.preview:
            camera.show_frame()

        # escape while running using cv2 interrupt
        if waitKey(1) & 0xFF == ord('q'):
            break
        
        # calculate and print elapsed time for a single loop
        if args.verbose:
            end = timer()
            logger.debug(f'Current loop time: {end - start}')

    # turn everything off
    motor.stop_spin()
    motor.release()
    laser.off()

    logger.info('Exiting program!')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))