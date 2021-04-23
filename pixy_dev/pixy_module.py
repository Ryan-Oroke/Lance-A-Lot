from __future__ import print_function
import pixy 
from ctypes import *
from pixy import *
import I2C_LIB as i2c
import time
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
frame = 0
min_balloon_height = 60

def balloonSeen(s):
	frame = 0
	count = pixy.ccc_get_blocks (100, blocks)
	if count > 0:
	        print('frame %3d:' % (frame))
	        frame = frame + 1
		for index in range (0, count):
	                print('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height))
			if(blocks[index].m_signature == s and blocks[index].m_height > min_balloon_height):
				return True
	else:
		print("No frames found.")
	return False

def chaseBalloon(s):
	timeout = 10
	i2c.sendMessage("SV000")
	start_time = time.time()
	while(time.time() - start_time < timeout):
		count = pixy.ccc_get_blocks(100, blocks)	
		if(count > 0):
			for index in range(0, count):
				if(blocks[index].m_signature == s and blocks[index].m_height > min_balloon_height):
					if(abs(blocks[index].m_x) < 30):
						if(blocks[index].m_x < 0):
							i2c.turnRobot(-1, 80, 0.1)
						else:
							i2c.turnRobot(1, 80, 0.1)
					else:
						i2c.driveRobot(1, 70)
						time.sleep(0.03)
		else:
			break


		

