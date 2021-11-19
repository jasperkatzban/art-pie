import cv2, imutils
import numpy as np
import logging
import sys

logger = logging.getLogger(__name__)

class Camera:
    """Handle laser tracking via camera"""

    def __init__(self, env_raspi=True, filename=None):
        """Initializes camera module"""
        logger.info('Initializing camera module!')
        if filename:
            self.current_frame = cv2.imread(filename)
            if self.current_frame is None:
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
            self.current_frame = None
            self.hsv = None

        self.profile = None
        self.profile_size = -1
        self.windowName = 'Surface Player'

    def get_profile(self):
        """Returns current waveform"""
        self.generate_profile()
        return self.profile
    
    def generate_profile(self):
        """Generates a waveform based on laser image"""
        thresh = self.threshold_frame(self.current_frame)
        coords = self.generate_coordinates(thresh)
        raw_profile = self.scale_coords_to_list(coords, self.profile_size)
        normalized_profile = self.normalize_profile(raw_profile)
        self.profile = normalized_profile

    # TODO: implement this for our laser
    def threshold_frame(self, img):
        """Thresholds image to isolate laser line"""
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(imgray, 127, 255, 0)
        return thresh

    def generate_coordinates(self, img):
        """Generates profile from binary thresholded image"""
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        target = max(contours, key=lambda x: cv2.contourArea(x))
        x = target[:, :, 0].flatten()
        y = target[:, :, 1].flatten()
        poly = np.poly1d(np.polyfit(x, y, 10)) # make polyfit degree into a var
        coords = []
        for _x in range(min(x), max(x), 5):
            coord = list((_x, int(poly(_x))))
            cv2.circle(self.current_frame, coord, 3, [0, 255, 0])
            coords.append(coord)

        return np.array(coords, dtype=float)

    def scale_coords_to_list(self, coords, size):
        """Scales profile to specified size"""
        ref_scale = np.linspace(0, size-1, size)
        coord_len = np.shape(coords)[0]
        xp = np.linspace(0, coord_len-1, coord_len)
        fp = list(coords[:, 1])
        scaled = np.interp(ref_scale, xp, fp)
        return scaled

    def normalize_profile(self, profile):
        """Scales profile values from 0 to 1"""
        # return profile/np.linalg.norm(profile)
        return (profile - np.min(profile)) / (np.max(profile) - np.min(profile))

    def show_image(self, image):
        """Shows an image"""
        cv2.imshow(self.windowName, image)

    def capture_frame(self):
        """Capture current frame"""
        _, self.current_frame = self.cap.read()

    def show_frame(self):
        """Display current camera frame"""
        cv2.imshow(self.windowName, self.current_frame)

    def get_current_frame(self):
        """Return most recent frame"""
        return self.current_frame

    def set_profile_size(self, profile_size):
        """Sets target profile size to generate"""
        self.profile_size = profile_size
        
    def close(self):
        """Closes camera stream and gui windows"""
        self.cap.release()
        cv2.destroyAllWindows()
