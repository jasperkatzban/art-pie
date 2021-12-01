GPIO_MOTOR_FORWARD = -1
GPIO_MOTOR_BACKWARD = -1
MOTOR_SPEED = 0.5

GPIO_LASER = 14 # pin 8 (GPIO14) on raspberry pi 2B V1.1

POLYFIT_DEG = 5
LINE_RESOLUTION = 5

# vals working in a dark room kinda
# vals if treating red normally
# min_hue, max_hue = 170, 180
# min_hue, max_hue = 0, 10

# vals when swapping red and blue
# in a dark room
min_hue, max_hue = 130, 180
min_sat, max_sat = 0, 255
min_val, max_val = 180, 255

from numpy import array
THRESHOLD_LOWER = array([min_hue, min_sat, min_val])
THRESHOLD_UPPER = array([max_hue, max_sat, max_val])