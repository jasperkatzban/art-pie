# motor config
MOTOR_NUM_STEPS_REVOLUTION = 200

# laser pin definition
GPIO_LASER = 14 # pin 8 (GPIO14) on raspberry pi 2B V1.1

# camera & cv macros
# vals when swapping red and blue
# in a dark room on a white object, detects the area outside of the bright center beam
min_hue, max_hue = 130, 180
min_sat, max_sat = 50, 255
min_val, max_val = 100, 255

from numpy import array
THRESHOLD_LOWER = array([min_hue, min_sat, min_val])
THRESHOLD_UPPER = array([max_hue, max_sat, max_val])

POLYFIT_DEG = 5
LINE_RESOLUTION = 5
X_CROP_PX = 150
MIN_CONTOUR_AREA = 0

# led control
LED_HUE_THRESHOLD_LOWER = 0.3
LED_HUE_THRESHOLD_UPPER = 0.7