# still is

import cv2
import numpy as np
import RPi.GPIO as gpio
import time

# Set the GPIO
triggered = False
trigger_pin = 16
gpio.setmode(gpio.BCM)
gpio.setup(trigger_pin, gpio.OUT)
gpio.output(trigger_pin, gpio.HIGH)
threshold = 4000

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Yellow
    #lower_bound = np.array([15, 40, 40])
    #upper_bound = np.array([40, 215, 215])

    #Purple
    lower_bound = np.array([150, 0, 0])
    upper_bound = np.array([255, 255, 255])
    #Red Balloon
    #lower_bound = np.array([160, 50, 50])
    #upper_bound = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    res = cv2.bitwise_and(frame, frame, mask = mask)

    masked_pixels = np.count_nonzero(mask)
    if(triggered == False and masked_pixels >= threshold):
        #The trigger should be on
        gpio.output(trigger_pin, gpio.LOW)
        print("Triggered:", masked_pixels)
        triggered = True;
    if(triggered == True and masked_pixels < threshold):
        #The Trigger should be set to off
        gpio.output(trigger_pin, gpio.HIGH)
        print("Detriggered:", masked_pixels)
        triggered = False;

    cv2.imshow('frame', frame)    #cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    s = mask.shape
        
    #Compute the center of mass of the 1s
    x_center = int(s[0]/2)
    y_center = int(s[1]/2)
    x_sum = 0
    y_sum = 0
    num_ones = 0
    for i in range(s[0]):
        if(mask[x_center][i] != 0):
            num_ones += 1
            y_sum += (i-y_center)
    
    if(num_ones != 0 and num_ones > 100):
        balloon_pos = y_sum/num_ones 
        print(balloon_pos)
        time.sleep(0.5)

    k = cv2.waitKey(5) & 0xFF
    if k == ord("q"):
        break

print(masked_pixels)
cv2.destroyAllWindows()
cap.release()
gpio.output(trigger_pin, gpio.LOW)

