# import system libs
import os
import sys
import argparse

# import modules
from modules.audio import Audio
from modules.camera import Camera
from modules.laser import Laser
from modules.motor import Motor

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    args = parser.parse_args(arguments)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))