# still is

import cv2
import numpy as np
import time

# Set the GPIO
triggered = False
yellow_threshold = 100000
purple_threshold = 4000

def get_line_status():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Yellow
    yellow_lower_bound = np.array([15, 40, 40])
    yellow_upper_bound = np.array([40, 215, 215])

    #Purple
    purple_lower_bound = np.array([150, 50, 50])
    purple_upper_bound = np.array([180, 255, 255])
 
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

    if(yellow_masked_pixels > yellow_threshold and purple_masked_pixels > purple_threshold):
        return "BOTH"
    elif(yellow_masked_pixels > yellow_threshold):
	print(yellow_masked_pixels)
        return "YELLOW"
    elif(purple_masked_pixels > purple_threshold):
        return "PURPLE"
    else:
        return "NONE"
