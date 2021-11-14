# import system libs
import os
import sys
import argparse
import logging

# import modules
from modules.audio import Audio
from modules.camera import Camera
from modules.laser import Laser
from modules.motor import Motor

# TODO: setup logging level as argument
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    args = parser.parse_args(arguments)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))