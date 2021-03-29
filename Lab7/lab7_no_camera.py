import time
import os
import i2c_woot as i2c
import RPi.GPIO as GPIO
import time
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    sys.exit(0)


IR_LEFT_PIN = 22
IR_CENTER_PIN = 27
IR_RIGHT_PIN = 17

last_bump_right = True

#set the gpio pinouts with BCM numbering
GPIO.setmode(GPIO.BCM)

#setup the button pins
GPIO.setup(IR_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_CENTER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

signal.signal(signal.SIGINT, signal_handler)

time.sleep(1)
big_delay = 0.75
small_delay = 0.05

i2c.driveMotor("A", 0)
i2c.driveMotor("B", 0)

while(True):
    
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
	    time.sleep(big_delay)
        else:
            i2c.driveMotor("A", -50)
            i2c.driveMotor("B", 50)
            time.sleep(big_delay)
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
    
        
    i2c.driveMotor("A",50)
    i2c.driveMotor("B", 50)
    time.sleep(small_delay)

    

GPIO.cleanup();

