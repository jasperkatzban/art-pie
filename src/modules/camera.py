import cv2, imutils
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Camera:
    """Handle laser tracking via camera"""

    def __init__(self, env_raspi=True):
        """Initializes camera module"""
        logger.info('Initializing camera module!')
        if env_raspi:
            from picamera import PiCamera
            from picamera.array import PiRGBArray
            camera = PiCamera()
            self.cap = PiRGBArray(camera)
        else:
            self.cap = cv2.VideoCapture(0)

        # derive camera frame dimensions
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.windowName = 'Surface Player'

        # frame buffers
        self.frame = None
        self.hsv = None

    def capture_frame(self):
        """Capture current frame"""
        ret, self.frame = self.cap.read()

    def show_frame(self):
        """Display current camera frame"""
        cv2.imshow(self.windowName, self.frame)        

    def get_frame(self):
        """Return most recent frame"""
        return self.frame

    def close(self):
        """Closes camera stream and gui windows"""
        self.cap.release()
        cv2.destroyAllWindows()