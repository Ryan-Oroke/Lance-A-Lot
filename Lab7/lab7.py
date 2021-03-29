from __future__ import print_function
import pixy
from ctypes import *
from pixy import *

import time
import os
import i2c_woot as i2c
import RPi.GPIO as GPIO
import time
import signal
import sys

#Camera Stuff


def signal_handler(sig, frame_sig):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    #cv2.destroyAllWindows()
    #cap.release()
    GPIO.cleanup();
    sys.exit(0)



IR_LEFT_PIN = 22
IR_CENTER_PIN = 27
IR_RIGHT_PIN = 17

last_bump_right = True

thr = 50
x_center = 160

#Setup for camera (for Red Recognition)
pixy.init()
pixy.change_prog("color_connected_components")
class Blocks (Structure):
    _fields_ = [ ("m_signature", c_uint),
                 ("m_x", c_uint),
                 ("m_y", c_uint),
                 ("m_width", c_uint),
                 ("m_height", c_uint),
                 ("m_angle", c_uint),
                 ("m_index", c_uint),
                 ("m_age", c_uint) ]
blocks = BlockArray(100)
frame = 0

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

try:
    while(True):

        #Check for lines
        left_on = GPIO.input(IR_LEFT_PIN)
        center_on = GPIO.input(IR_CENTER_PIN)
        right_on = GPIO.input(IR_RIGHT_PIN)

        #False by deaault
        tracking_balloon = False

        #Capture Image and convert to HSV
        count = pixy.ccc_get_blocks(100, blocks) 
        if(count > 0):
            #print('frame %3d:' % frame)
            frame = frame + 1
            for index in range(count):
                #print('BLOCK: SIG=%d, X=%d, Y=%d, W=%d, H=%d' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height) )
                if(blocks[index].m_width > 50 and blocks[index].m_signature == 1):
                    #Balloon Seen
                    print("X Position:", blocks[index].m_x)
                    if(left_on and center_on and right_on):

                        tracking_balloon = True;

                        if(blocks[index].m_x - x_center > thr):
                            #Turn Right
                            i2c.driveMotor("A", -50)
                            i2c.driveMotor("B", 50)
                            time.sleep(0.15)

                            #driveMotor("A", 50)
                            #driveMotor("B", 50);
                            #time.sleep(small_delay)

                            i2c.driveMotor("A", 0)
                            i2c.driveMotor("B", 0)
                            #time.sleep(small_delay)

                        elif(blocks[index].m_x - x_center < -1*thr):
                            i2c.driveMotor("A", 50)
                            i2c.driveMotor("B", -50)
                            time.sleep(0.15)

                            #driveMotor("A", 50)
                            #driveMotor("B", 50);
                            #time.sleep(small_delay)

                            i2c.driveMotor("A", 0)
                            i2c.driveMotor("B", 0)
                            #time.sleep(small_delay)
                        else:
                            #Drive Straight at It!
                            i2c.driveMotor("A", 50)
                            i2c.driveMotor("B", 50)
                            time.sleep(0.15)

        #time.sleep()
        if(tracking_balloon == False):

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

		i2c.driveMotor("A", 50)
		i2c.driveMotor("B", 50)
		time.sleep(big_delay)

		i2c.driveMotor("A", 0)
		i2c.driveMotor("B", 0)
                    
                    
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
except:
	print("Reached Error")
	i2c.driveMotor("A", 0)
	i2c.driveMotor("B", 0)
	GPIO.cleanup()


