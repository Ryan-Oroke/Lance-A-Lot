import time
import I2C_LIB as i2c
import Sensors as sense
from simple_pid import PID
import sys
import signal
import numpy

def signal_handler(sig, frame_sig):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    #cv2.destroyAllWindows()
    #cap.release()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

scalar = -1

pid = PID(2, 0.25, 0, setpoint=1) #One sided
#pid = PID(8, 0, 0, setpoint = 0) #Two-Sided

pid.output_limits = (-50, 50)

min_drive_speed = 50
max_ultrasonic_reading = 30

control = 0

while(True):
	x = (sense.Left_dis()+sense.Right_dis())/2 #One-Sided
	l = sense.Left_dis()
	r = sense.Right_dis()
	#x = (l-r)/2
	a=0
	if(abs(x) < 30):

		d = numpy.sqrt( (r-l)**2 + 16**2 )
		a = 90 - 180/3.14259 * numpy.arccos( ((16**2) + d**2 - (r-l)**2)/(2*16*d))

		if(x > max_ultrasonic_reading):
			x = 100
		elif(x < -1*max_ultrasonic_reading):
			x = -100

		if(l > r):
			x = x * -1

		control = pid(x)

		i2c.driveMotor("A", min_drive_speed + scalar*control)
		i2c.driveMotor("B", min_drive_speed - scalar*control)
		time.sleep(0.05)

		print(control)

	ir = sense.IR_read()
	print(ir)
	if(ir[1] == False):
		i2c.driveRobot(-50, 0.5)
		i2c.turnRobot(-1, 90, 1)

	print("Ultrasonic: ", x, min_drive_speed + scalar*control)

	#time.sleep(0.1)
