import networkx as nx
#import matplotlib.pyplot as plt
import robot
import sys
import signal
import I2C_LIB as i2c
import time
import Sensors as sense
import random
import pixy_module as pix

def signal_handler(sig, frame_sig):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    #cv2.destroyAllWindows()
    #cap.release()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
#dir = 1
#color = 2

def randControl(dir, color, time_remaining):
	start_time = time.time()
	random.seed(time.time())
	i2c.sendMessage("SV170")
	#dir = robot.traverseEdge3(0, 1)
	#dir = robot.changeOrientation(0, 1, newDir(1, False))
	#dir = robot.traverseEdge3(1, 2)
	while(time_remaining > time.time() - start_time):
		robot.traverseEdge3(1, 2)
		#i2c.driveRobot(1, 80)
		#time.sleep(0.25)
		#i2c.stopRobot()
		if(sense.center_line_detected() == "PURPLE"):
			#Intersection
			print("Hit purple line.")
			#scanForBalloon(color)
			i2c.driveRobot(1, 60)
			time.sleep(0.5)
			dir = robot.intersectionTurn(0, dir, newDir(dir, False), color)
			scanForBalloon(color)
		else:
			#(sense.center_line_detected() == "YELLOW"):
			#i2c.sendMessage("SV170")
			print("Hit yellow line.")
			i2c.driveRobot(-1, 60)
			time.sleep(1)
			scanForBalloon(color)
			i2c.driveRobot(1, 60)
			time.sleep(1)
			same_not_possible = False;
			#dir = changeOrientation(0, dir, newDir(dir, same_not_possible))
			new_d = random.randint(1, 3) - 2
			if(new_d != 0):
				i2c.turn90(new_d)
			#i2c.sendMessage("SV000")

def newDir(d, can_be_same):
	try:
		r = random.randint(1,5)
		while(r != d):
			rev_dir = d - 2
			if(rev_dir < 1):
				rev_dir = 4 -  rev_dir 
			r = random.randint(1,5)
		print("debug1")
		if(can_be_same == False and r == dir):
			r = r - 1
			if(r == 0):
				r = 4
		return r
	except:
		return 4

def scanForBalloon(color):
	i2c.lowerLance
	i2c.turnRobot(-1, 97, 0.5)
	for i in range(9):
		i2c.turnRobot(1, 97, 0.5)
		i2c.stopRobot()
		#time.sleep(0.25)
		if(pix.balloonSeen(color) == True):
			pix.chaseBalloon(color)
			i2c.raiseLance()
			break
	i2c.lowerLance()
	i2c.driveRobot(-1, 80)
	time.sleep(2)


"""
if __name__ == '__main__':
	main()
"""
