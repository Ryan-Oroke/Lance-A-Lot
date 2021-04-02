import time
import I2C_LIB as i2c
import Sensors as sense
from simple_pid import PID
import sys
import signal

def signal_handler(sig, frame_sig):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    #cv2.destroyAllWindows()
    #cap.release()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

scalar = 2

pid = PID(0.125, 0, 0, setpoint=0)
pid.output_limits = (-100, 100)
pid.sample_time = 0.1

min_drive_speed = 50

while(True):
	x = sense.centering()
	if(x > 5):
		x = 100
	elif(x < -5):
		x = -100
	control = pid(x)

	i2c.driveMotor("A", -1*min_drive_speed + scalar*control)
	i2c.driveMotor("B", -1*min_drive_speed - scalar*control)

	print(control)
