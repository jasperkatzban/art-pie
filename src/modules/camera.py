from typing import DefaultDict
import cv2, imutils
import numpy as np
import logging
import sys

from collections import defaultdict

import matplotlib.pyplot as plt
from numpy.lib.function_base import average

from utils.constants import POLYFIT_DEG, THRESHOLD_LOWER, THRESHOLD_UPPER, LINE_RESOLUTION, X_CROP_PX

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

        self.kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
        self.kernel_close_sizes = [(3,3), (5,5), (7,7)]
        self.kernel_erode_sizes = [(3,3), (3,3)]

    def get_profile(self):
        """Returns current waveform"""
        self.generate_profile()
        return self.profile
    
    def erode_mask_slow(self, mask):
        """Clean up mask, connect lines, and remove noise"""
        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel_dilate)

        kernel_close_sizes = [(3,3), (3,3), (5,5), (7,7)]
        for kernel_size in kernel_close_sizes:
            kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
            
        kernel_erode_sizes = [(3,3), (3,3), (5,5)]
        for kernel_size in kernel_erode_sizes:
            kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
            mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel_erode)
        
        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (10,25))
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel_dilate)

        return mask

    def erode_mask(self, mask):
        """Clean up mask, connect lines, and remove noise"""
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, self.kernel_dilate)

        for kernel_size in self.kernel_close_sizes:
            kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
            
        for kernel_size in self.kernel_erode_sizes:
            kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
            mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel_erode)
        
        # kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (10,25))
        # mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel_dilate)

        return mask

    def generate_profile(self):
        """Generates a waveform based on laser image"""
        mask = self.mask_frame(self.current_frame_raw)
        eroded_mask = self.erode_mask(mask)

        # display frame
        self.current_frame = eroded_mask

        coords = self.generate_coordinates(eroded_mask)

        # if found coordinates, convert to wavetable
        if len(coords) > 0:
            # self.draw_coords(coords, (255, 0, 0))
            raw_profile = self.scale_coords_to_list(coords, self.profile_size)
            normalized_profile = self.normalize_profile(raw_profile)
            self.profile = normalized_profile
            # self.profile = raw_profile
        
        # otherwise return silence
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
        return mask

    def generate_coordinates(self, mask):
        """Generates profile from binary thresholded image"""
        contour_coords = self.generate_contour_coords(mask)
        return self.avg_along_x(contour_coords)

    def avg_along_x(self, cnt):
        """Averages x coordinates to find center of line"""
        d = DefaultDict(list)
        
        for c in cnt:
            x, y = c
            d[y].append(x)
            
        for y in d.keys():
            d[y] = np.average(d[y])
            # alternatively, just take the first element
            # d[y] = d[y][0]

        return np.array([[coord[1], coord[0]] for coord in d.items()])

    def generate_contour_coords(self, img):
        """Generate points with highest contour in given mask"""
        contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        self.current_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_GRAY2RGB)

        if len(contours) == 0:
            return []

        # find maximum contours
        min_contour_area = 0
        # print([cv2.contourArea(x) for x in contours])
        valid_contours = list(filter(lambda x: cv2.contourArea(x) > min_contour_area, contours))
        # print([cv2.contourArea(x) for x in valid_contours])
        
        # valid_contours = np.concatenate(valid_contours)
        valid_contours = np.concatenate(contours)

        # TODO: there's a cleaner way to do this
        return np.array([coord[0] for coord in valid_contours])

    # TODO: write other funcs to convert points to wavetable
    def map_poly(self, coords):
        """Uses polynomial line fitting to generate a list of coordinates based on the detected line"""
        x = coords[:, 0]
        y = coords[:, 1]

        poly = np.poly1d(np.polyfit(x, y, POLYFIT_DEG))
        coords = []
        for _x in range(min(x), max(x), LINE_RESOLUTION):
            y = np.max(int(poly(_x)), 0)
            coord = list((_x, y))
            coords.append(coord)
            
        return np.array(coords, dtype=float)

    def draw_coords(self, coords, color=(255, 255, 255)):
        """Draws coordinates for profile on image"""
        for coord in coords:
            cv2.circle(self.current_frame, (int(coord[0]), int(coord[1])), 5, color)

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
        _, frame = self.cap.read()
        if frame is not None:
            self.current_frame_raw = frame[:, X_CROP_PX:(int(self.width)-X_CROP_PX)]

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
