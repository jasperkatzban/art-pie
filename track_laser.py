import cv2
import numpy as np
import mido
import sys

# enables sliders to set threshold values
DEBUG_THRESHOLD = False

# create video capture object
cap = cv2.VideoCapture(0)
windowName = 'Laser Finder'

# derive camera frame dimensions
CAM_WIDTH_PX = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
CAM_HEIGHT_PX = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# set midi cc channel
MIDI_CC_CHAN = 14

# set target virtual midi device name
target_output_name = 'IAC Driver Virtual Midi Cable'

# get midi output names and set to target
output_names = mido.get_output_names()
if target_output_name in output_names:
    outport = mido.open_output(target_output_name)
else:
    print(f'Error: Could not find {target_output_name} in the midi devices:')
    print(output_names)
    sys.exit(-1)



# These defaults work nicely with a macbook pro camera on a piece of white paper
# These thresholds rely on the fact that the laser pointer is usually the brightest thing in the 
# frame, so it may not work in other environments
min_hue, max_hue = 0, 6
min_sat, max_sat = 0, 163
min_val, max_val = 245, 255

# pack into a np array
lower_threshold = np.array([min_hue, min_sat, min_val])
upper_threshold = np.array([max_hue, max_sat, max_val])

# placeholder callback func for trackbars
def trackbar_callback(val):
    print(f'Setting value:\t{val}')

# run a continuous loop
while True:

    # Capture each frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    if DEBUG_THRESHOLD:
        # create sliders
        # TODO: cleanup this a bit

        cv2.createTrackbar('min_hue', windowName, 0, 255, trackbar_callback)
        cv2.createTrackbar('max_hue', windowName, 0, 255, trackbar_callback)
        cv2.createTrackbar('min_sat', windowName, 0, 255, trackbar_callback)
        cv2.createTrackbar('max_sat', windowName, 0, 255, trackbar_callback)
        cv2.createTrackbar('min_val', windowName, 0, 255, trackbar_callback)
        cv2.createTrackbar('max_val', windowName, 0, 255, trackbar_callback)

        # set threshold values from slider positions
        min_hue = cv2.getTrackbarPos('min_hue', windowName)
        max_hue = cv2.getTrackbarPos('max_hue', windowName)
        min_sat = cv2.getTrackbarPos('min_sat', windowName)
        max_sat = cv2.getTrackbarPos('max_sat', windowName)
        min_val = cv2.getTrackbarPos('min_val', windowName)
        max_val = cv2.getTrackbarPos('max_val', windowName)

        # set threshold values 
        lower_threshold = np.array([min_hue, min_sat, min_val])
        upper_threshold = np.array([max_hue, max_sat, max_val])

    # create a mask with specified threshold vals and extract minmax locations
    # TODO: explore shape masks to identify the laser pointer as separate from
    # other valid thresholded values
    mask = cv2.inRange(hsv, lower_threshold, upper_threshold)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

    # draw a circle around the estimated laser position
    cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)

    # show the current frame
    cv2.imshow(windowName, mask)

    # map laser point location to note values and a midi control change
    note = int((maxLoc[0] / CAM_WIDTH_PX) * 127)
    value = int((maxLoc[1] / CAM_HEIGHT_PX) * 127)

    # create and send midi messages
    print(f'Sending midi: Note: {note}\tCC: {value}')
    msg1 = mido.Message('note_on', note=note, velocity=100)
    # msg1 = mido.Message('note_off', note=note, velocity=100)
    msg2 = mido.Message('control_change', channel=MIDI_CC_CHAN, value=value)
    outport.send(msg1)
    outport.send(msg2)

    # quit by pressing CTRL/CMD + Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()