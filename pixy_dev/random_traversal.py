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
dir = 1

def newDir(d, can_be_same):
	r = random.randint(1,5)
	while(r != d):
		rev_dir = d - 2
		if(rev_dir < 1):
			rev_dir = 4 -  rev_dir 
		r = random.randint(1,5)
	if(can_be_same == False and r == dir):
		r = r - 1
		if(r == 0):
			r = 4
	return r

def scanForBalloon():
	i2c.sendMessage("SV170")
	for i in range(5):
		i2c.turnRobot(1, 100, 0.5)
		i2c.stopRobot()
		if(pix.balloonSeen(1)):
			pix.chaseBalloon(1)
			break
	i2c.sendMessage("SV000")


def main():
	dir = 1
	random.seed(time.time())
	i2c.sendMessage("SV170")
	dir = robot.traverseEdge3(0, 1)
	dir = robot.changeOrientation(0, 1, 2)
	dir = robot.traverseEdge3(1, 2)
	while(True):
		robot.traverseEdge3(1, 2)
		if(sense.center_line_detected() == "PURPLE"):
			print("Hit purple line.")
			same_possible = True
			scanForBalloon()
			dir = robot.intersectionTurn(0, dir, newDir(dir, True))
		else:
			#(sense.center_line_detected() == "YELLOW"):
			#i2c.sendMessage("SV170")
			print("Hit yellow line.")
			i2c.driveRobot(-1, 60)
			time.sleep(1)
			scanForBalloon()
			same_not_possible = False;
			#dir = changeOrientation(0, dir, newDir(dir, same_not_possible))
			new_d = random.randint(1, 3) - 2
			if(new_d != 0):
				i2c.turn90(new_d)
			#i2c.sendMessage("SV000")
			

if __name__ == '__main__':
	main()
