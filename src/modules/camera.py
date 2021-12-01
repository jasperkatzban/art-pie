import cv2, imutils
import numpy as np
import logging
import sys

from numpy.core.fromnumeric import shape

from utils.constants import POLYFIT_DEG, THRESHOLD_LOWER, THRESHOLD_UPPER, LINE_RESOLUTION

logger = logging.getLogger(__name__)

class Camera:
    """Handle laser tracking via camera"""

    def __init__(self, env_raspi=True, filename=None):
        """Initializes camera module"""
        logger.info('Initializing camera module!')
        if filename:
            self.current_frame_raw = cv2.imread(filename)
            if self.current_frame_raw is None:
                logger.error('Invalid test image file path encountered! Please check the path and try again')
                sys.exit()
        else:
            if env_raspi:
                cv2.destroyAllWindows
                self.cap = cv2.VideoCapture('/dev/video0')
            else:
                self.cap = cv2.VideoCapture(0)

            # derive camera frame dimensions
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            # frame buffers
            self.current_frame_raw = None
            self.current_frame = None
            self.hsv = None

        self.profile = None
        self.profile_size = -1
        self.windowName = 'Video Preview'

        self.lower_threshold = THRESHOLD_LOWER
        self.upper_threshold = THRESHOLD_UPPER

    def get_profile(self):
        """Returns current waveform"""
        self.generate_profile()
        return self.profile
    
    def generate_profile(self):
        """Generates a waveform based on laser image"""
        mask = self.mask_frame(self.current_frame_raw)
        coords = self.generate_coordinates(mask)
        if len(coords) > 0:
            self.draw_coords(coords)
            raw_profile = self.scale_coords_to_list(coords, self.profile_size)
            normalized_profile = self.normalize_profile(raw_profile)
            self.profile = normalized_profile
        else:
            self.profile = np.zeros(self.profile_size)

    # TODO: implement this for our laser
    def mask_frame(self, img):
        """Thresholds image to isolate laser line"""
        # purposely swap BRG with RGB, meaning the red channel is actually
        # read into HSV as the blue channel and avoids the target hue range being 
        # spread across the 170 to 10 range (hue goes from 0-180 where min, max are red)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, self.lower_threshold, self.upper_threshold)
        # mask = cv2.bitwise_not(mask)
        self.current_frame = mask
        # self.show_image(thresh)
        return mask

    def generate_coordinates(self, img):
        """Generates profile from binary thresholded image"""
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self.current_frame, contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        if len(contours) == 0:
            return []
        target = max(contours, key=lambda x: cv2.contourArea(x))
        x = target[:, :, 0].flatten()
        y = target[:, :, 1].flatten()
        
        return self.map_poly(x, y)

    def map_poly(self, x, y):
        """Uses polynomial line fitting to generate a list of coordinates based on the detected line"""
        poly = np.poly1d(np.polyfit(x, y, POLYFIT_DEG))
        coords = []
        for _x in range(min(x), max(x), LINE_RESOLUTION):
            y = np.max(int(poly(_x)), 0)
            coord = list((_x, y))
            coords.append(coord)
            
        return np.array(coords, dtype=float)


    def draw_coords(self, coords):
        """Draws coordinates for profile on image"""
        for coord in coords:
            cv2.circle(self.current_frame, (int(coord[0]), int(coord[1])), 3, (0, 0, 255), -1)

    def scale_coords_to_list(self, coords, size):
        """Scales profile to specified size"""
        ref_scale = np.linspace(0, size-1, size)
        coords_len = np.shape(coords)[0]
        xp = np.linspace(0, coords_len-1, coords_len)
        fp = list(coords[:, 1])
        scaled = np.interp(ref_scale, xp, fp)
        return scaled

    def normalize_profile(self, profile):
        """Scales profile values from 0 to 1"""
        range = np.max(profile) - np.min(profile)
        return (profile - np.min(profile)) / max(range, 1)

    def show_image(self, image):
        """Shows an image"""
        cv2.imshow(self.windowName, image)

    def capture_frame(self):
        """Capture current frame"""
        _, self.current_frame_raw = self.cap.read()

    def show_frame(self):
        """Display current camera frame"""
        cv2.imshow(self.windowName, self.current_frame)

    def get_current_frame(self):
        """Return most recent frame"""
        return self.current_frame

    def get_current_frame_raw(self):
        """Return most recent unprocessed frame"""
        return self.current_frame_raw

    def set_profile_size(self, profile_size):
        """Sets target profile size to generate"""
        self.profile_size = profile_size
        
    def close(self):
        """Closes camera stream and gui windows"""
        self.cap.release()
        cv2.destroyAllWindows()
