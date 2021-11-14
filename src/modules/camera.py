from picamera import PiCamera
import cv2, imutils
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Camera:
    """Handle laser tracking via camera"""

    def __init__(self):
        logger.info('Initializing camera module!')
        self.camera = PiCamera()
