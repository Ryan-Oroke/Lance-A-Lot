from __future__ import print_function
import pixy 
from ctypes import *
from pixy import *
import I2C_LIB as i2c
import os
import RPi.GPIO as GPIO
import time
import signal
import sys
import Sensors as sense
# Pixy2 Python SWIG get blocks example #

print("Pixy2 Python SWIG Example -- Get Blocks")

pixy.init ()
pixy.change_prog ("color_connected_components");

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
b = BlockArray(100)
frame = 0
min_balloon_height = 40

def balloonSeen(s):
	blocks = BlockArray(100)
	frame = 0
	count = pixy.ccc_get_blocks(100, blocks)
	if count > 0:
		frame += 1
	        for index in range (count+1):
			print("frame " + str(frame) + ": [" + str(blocks[index].m_signature) + "," + str(blocks[index].m_height) + "]")
			if(blocks[index].m_signature == s and blocks[index].m_height > min_balloon_height):
				print("Returned true")
				return True
	else:
		print("No frames found.")
	return False

def chaseBalloon(s):
	print("Chasing balloon!")
	timeout = 10
	i2c.raiseLance()
	start_time = time.time()
	x_center = 150
	while(time.time() - start_time < timeout):
		std_speed = 65
		adj_delay = 0.75
		ir = sense.IR_read()
		if(ir[0] == False):
			#adjustFromBumper(0)
			i2c.turnRobot(1, std_speed, adj_delay)
		elif(ir[2] == False):
			#adjustFromBumper(2)
			i2c.turnRobot(-1, std_speed, adj_delay)
		else:
			i2c.driveRobot(1, std_speed)
		            #print("Ultrasonics cannot see.")
		
		count = pixy.ccc_get_blocks(100, blocks)
		print(count)
		if(count > 0):
			for index in range(0, count):
				if(blocks[index].m_signature == s and blocks[index].m_height > min_balloon_height):
					print("S:" + str(blocks[index].m_signature) + " X:"+str(blocks[index].m_x))
					if(abs(blocks[index].m_x-x_center) > 15):
						print("Turning...")
						if(blocks[index].m_x-x_center < 0):
							i2c.turnRobot(1, 80, 0.1)
						else:
							i2c.turnRobot(-1, 80, 0.1)
					else:
						i2c.driveRobot(1, 70)
						time.sleep(0.03)
		else:
			break

	i2c.stopRobot()
	i2c.lowerLance()
"""
	#Camera Stuff

	IR_LEFT_PIN = 22
	IR_CENTER_PIN = 27
	IR_RIGHT_PIN = 17

	last_bump_right = True

	thr = 50
	x_center = 160

	#Setup for camera (for Red Recognition)
	blocks = BlockArray(100)
	b = BlockArray(100)
	frame = 0
"""
def checkForBalloon(s, w):
	print(4)
	c = pixy.ccc_get_blocks(100, b)
	print(5)
	for i in range(c):
        	if(b[i].m_signature == s and b[i].m_width >= w):
			print("I see a balloooooooon!!!")
            		return True
	print("This is boring, a balloon isn't even in sight...")
	return False

def huntBalloon(color):
	std_spd = 68
	thr = 10
	x_center = 150
	last_bump_right = False
	frame = 0
	time.sleep(1)
	big_delay = 0.5
	small_delay = 0.05
	swivel_delay = 0.5
	swivel_time_gap = 5 #seconds
	start_time = time.time()

	swivel_speed = 65
	i2c.driveMotor("A", 0)
	i2c.driveMotor("B", 0)

	i2c.lowerLance()

	try:
		while(True):

		    #Check for lines
            	    ir = sense.IR_read()
		    left_on = ir[0]
		    center_on = ir[1]
		    right_on = ir[2]

		    #False by default
		    tracking_balloon = False

		    #Capture Image and convert to HSV
		    count = pixy.ccc_get_blocks(100, blocks) 
		    if(count > 0):
		        #print('frame %3d:' % frame)
		        frame = frame + 1
		        for index in range(count):
		            #print('BLOCK: SIG=%d, X=%d, Y=%d, W=%d, H=%d' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height) )
		            if(blocks[index].m_width > 50 and blocks[index].m_signature == color):
		                #Balloon Seen
		        	i2c.raiseLance()
		                print("X Position:", blocks[index].m_x)
		                if(left_on and sense.center_line_detected() == "NONE"  and right_on):

		                    tracking_balloon = True;

		                    if(blocks[index].m_x - x_center > thr):
		                        #Turn Right
		                        i2c.turnRobot(-1, std_spd, 0.15)
		                        #time.sleep(0.15)

		                        #driveMotor("A", 50)
		                        #driveMotor("B", 50);
		                        #time.sleep(small_delay)

		                        #i2c.stopRobot()
		                        #time.sleep(small_delay)

		                    elif(blocks[index].m_x - x_center < -1*thr):
		                        i2c.turnRobot(1, std_spd, 0.15)
		                        #time.sleep(0.15)

		                        #driveMotor("A", 50)
		                        #driveMotor("B", 50);
		                        #time.sleep(small_delay)

		                        #i2c.stopRobot()
		                        #time.sleep(small_delay)

		                    else:
		                        #Drive Straight at It!
		                        i2c.driveRobot(1, std_spd)
		                        time.sleep(0.15)

		    #time.sleep()
		    if(tracking_balloon == False):
		        #print(GPIO.input(IR_PIN))
		        
		        #print(left_on, center_on, right_on)
		        if(sense.center_line_detected() == "NONE"):
		            print("Hit Left")
		            
		    	    start_time = time.time()

		            i2c.stopRobot()
		            time.sleep(small_delay)
		            
		            i2c.driveRobot(-1, std_spd)
		            time.sleep(big_delay)
		            time.sleep(big_delay)

		            i2c.stopRobot
		            time.sleep(small_delay)
		            
		            if(last_bump_right == False):
		                i2c.driveRobot(1, std_spd)
		                time.sleep(big_delay)
		            else:
		                i2c.turnRobot(-1, std_spd, big_delay)

		        	#i2c.driveMotor("A", 50)
		        	#i2c.driveMotor("B", 50)
		        	#time.sleep(big_delay)

		    	    i2c. stopRobot()

		    	elif(left_on == False):
				start_time = time.time()

				print("Hit Left")
				last_bump_right = True;

				i2c.stopRobot()
				time.sleep(small_delay)

				i2c.turnRobot(-1, std_spd, big_delay)

				i2c.stopRobot()
				time.sleep(small_delay)
			
			elif(right_on == False):
				start_time = time.time()

				print("Hit Left")
				last_bump_right = False

				i2c.stopRobot()
				time.sleep(small_delay)

				i2c.turnRobot(1, std_spd, big_delay)

				i2c.stopRobot()
				time.sleep(small_delay)

			i2c.driveMotor("A", 70)
			i2c.driveMotor("B", 70)
			time.sleep(0.01)

			if(time.time() - start_time > swivel_time_gap and tracking_balloon == False):
				    #print(1)
				    i2c.driveMotor("A", swivel_speed)
				    i2c.driveMotor("B", -1*swivel_speed)
				    time.sleep(swivel_delay)
				    i2c.stopRobot()
				    #time.sleep(0.5)
				    #print(2)

			    #Check to see if a pixy object is not visible
		    	if(checkForBalloon(1, 100) == False):
	            	    print(3)
		            #Turn the other way
		            i2c.turnRobot(-1, swivel_speed, swivel_delay*2)
		            i2c.stopRobot()
			    #print(1)
		            #time.sleep(0.9)

                #Check again for the balloon
                if(checkForBalloon(1, 100) == False):
		    print(2)
                    i2c.driveMotor("A", swivel_speed)
                    i2c.driveMotor("B", -1*swivel_speed)
                    time.sleep(swivel_delay)
		    start_time = time.time()

	except:
		print("Reached Error: ", sys.exc_info()[1:-1])
		i2c.driveMotor("A", 0)
		i2c.driveMotor("B", 0)
		GPIO.cleanup()
