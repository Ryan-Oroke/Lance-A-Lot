# HOSTS OPENCV MODULE AND HANDLES LINE DETECTION COMPUTATIONS (CALLED FROM SENSORS.PY)
# Honestly this is very straightforward if ever worked with cv2 and camera, so uncommented.

import cv2
import numpy as np
import time

# Set the GPIO
triggered = False
yellow_threshold = 600
purple_threshold = 600

def get_line_status():
    cap = cv2.VideoCapture(0)
    cap.set(3, 64)
    cap.set(4, 64)
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #White -- FOr home testing ONLY
    #yellow_threshold = 7000
    #yellow_lower_bound = np.array([0, 20, 80])
    #yellow_upper_bound = np.array([255, 255, 255])
    #purple_lower_bound = np.array([150, 255, 255])
    #purple_upper_bound = np.array([151, 255, 255])

    #Yellow
    yellow_lower_bound = np.array([15, 80, 80])
    yellow_upper_bound = np.array([60, 255, 255])

    #Purple
    purple_lower_bound = np.array([110, 10, 10])
    purple_upper_bound = np.array([255, 255, 255])
 
    #Red Balloon
    #lower_bound = np.array([160, 50, 50])
    #upper_bound = np.array([180, 255, 255])

    yellow_mask = cv2.inRange(hsv, yellow_lower_bound, yellow_upper_bound)
    purple_mask = cv2.inRange(hsv, purple_lower_bound, purple_upper_bound)
    #res = cv2.bitwise_and(frame, frame, mask = mask)

    yellow_maksed_pixels = 0
    yellow_masked_pixels = np.count_nonzero(yellow_mask)
    purple_masked_pixels = np.count_nonzero(purple_mask)

    # cv2.imshow('frame', frame)    #cv2.imshow('mask', mask)
    # cv2.imshow('res', res)

    # k = cv2.waitKey(5) & 0xFF
    # if k == ord("q"):
    #     break

    # print(masked_pixels)
    # cv2.destroyAllWindows()
    #cap.release()

    print("Yellow, Purple:", yellow_masked_pixels, purple_masked_pixels)

    if(yellow_masked_pixels > yellow_threshold and purple_masked_pixels > purple_threshold):
        return "BOTH"
    elif(yellow_masked_pixels > yellow_threshold):
	#print(yellow_masked_pixels)
        return "YELLOW"
    elif(purple_masked_pixels > purple_threshold):
        return "PURPLE"
    else:
        return "NONE"
