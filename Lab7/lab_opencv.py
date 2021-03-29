import time
import os
import i2c_woot as i2c
import RPi.GPIO as GPIO
import time
import signal
import sys

#Camera Stuff
import cv2
import numpy as np
import RPi.GPIO as gpio
import time
import scipy_com as COM

def signal_handler(sig, frame):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    cv2.destroyAllWindows()
    cap.release()
    GPIO.cleanup();
    sys.exit(0)



IR_LEFT_PIN = 22
IR_CENTER_PIN = 27
IR_RIGHT_PIN = 17

last_bump_right = True

#Setup for camera (for Red Recognition)
cap = cv2.VideoCapture(0)
lower_bound = np.array([160, 50, 50])
upper_bound = np.array([180, 255, 255])
balloon_mass_threshold = 3000

#set the gpio pinouts with BCM numbering
GPIO.setmode(GPIO.BCM)

#setup the button pins
GPIO.setup(IR_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_CENTER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

signal.signal(signal.SIGINT, signal_handler)

time.sleep(1)
big_delay = 0.5
small_delay = 0.05

i2c.driveMotor("A", 0)
i2c.driveMotor("B", 0)

while(True):
    
    #Capture Image and convert to HSV
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    
    masked_pixels = np.count_nonzero(mask)
    if(masked_pixels > balloon_mass_threshold):
        print("Balloon Spotted!")
        i2c.driveMotor("A", 0)
        i2c.driveMotor("B", 0)
        #time.sleep(small_delay)
        
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
            time.sleep(big_delay)
                    
            #balloon_pos = x_sum/x_center
            print(balloon_pos)
            time.sleep(big_delay)
            
            if(balloon_pos > 30):
                #Turn 
                i2c.driveMotor("A", 50)
                i2c.driveMotor("B", -50)
                time.sleep(0.25)
                
                #driveMotor("A", 50)
                #driveMotor("B", 50);
                #time.sleep(small_delay)
                
                i2c.driveMotor("A", 0)
                i2c.driveMotor("B", 0)
                time.sleep(small_delay)
                
            elif(balloon_pos < -30):
                #Turn Left
                i2c.driveMotor("A", -50)
                i2c.driveMotor("B", 50)
                time.sleep(0.25)
                
                #driveMotor("A", 50)
                #driveMotor("B", 50);
                #time.sleep(small_delay)
                
                i2c.driveMotor("A", 0)
                i2c.driveMotor("B", 0)
                time.sleep(small_delay)
            else:
                i2c.driveMotor("A", 50)
                i2c.driveMotor("B", 50)
                time.sleep(1)
    else:
        #Cannot see balloon
        left_on = GPIO.input(IR_LEFT_PIN)
        center_on = GPIO.input(IR_CENTER_PIN)
        right_on = GPIO.input(IR_RIGHT_PIN)

        #print(GPIO.input(IR_PIN))
        
        #print(left_on, center_on, right_on)
        if(center_on == False):
            print("Hit Left")
            
            i2c.driveMotor("A", 0)
            i2c.driveMotor("B", 0)
            time.sleep(small_delay)
            
            i2c.driveMotor("A", -50)
            i2c.driveMotor("B", -50)
            time.sleep(big_delay)
            time.sleep(big_delay)

            i2c.driveMotor("A", 0)
            i2c.driveMotor("B", 0)
            time.sleep(small_delay)
            
            if(last_bump_right == False):
                i2c.driveMotor("A", 50)
                i2c.driveMotor("B", -50)
                time.sleep(big_delay)
            else:
                i2c.driveMotor("A", -50)
                i2c.driveMotor("B", 50)
                time.sleep(big_delay)
                
                
        elif(left_on == False):
            print("Hit Left")
            last_bump_right = True;
            
            i2c.driveMotor("A", 0)
            i2c.driveMotor("B", 0)
            time.sleep(small_delay)
            
            i2c.driveMotor("A", -50)
            i2c.driveMotor("B", 50)
            time.sleep(big_delay)

            i2c.driveMotor("A", 0)
            i2c.driveMotor("B", 0)
            time.sleep(small_delay)
        elif(right_on == False):
            print("Hit Left")
            last_bump_right = False
            
            i2c.driveMotor("A", 0)
            i2c.driveMotor("B", 0)
            time.sleep(small_delay)
            
            i2c.driveMotor("A", 50)
            i2c.driveMotor("B", -50)
            time.sleep(big_delay)

            i2c.driveMotor("A", 0)
            i2c.driveMotor("B", 0)
            time.sleep(small_delay)
        
            
        i2c.driveMotor("A", 50)
        i2c.driveMotor("B", 50)
        time.sleep(small_delay)

    



