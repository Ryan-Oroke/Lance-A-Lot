import time
import I2C_LIB as i2c
import Sensors as sense
from simple_pid import PID

sight_threshold = 50

pid = PID(2, 0.25, 0, setpoint=10) #One sided
#pid = PID(8, 0, 0, setpoint = 0) #Two-Sided

pid.output_limits = (-50, 50)

min_drive_speed = 50
max_ultrasonic_reading = 30

control = 0

def traverseEdge():
    print("Driving Forward...")
    scalar = -1

    print("Initial loop without US.")
    while(sense.Left_dis() > sight_threshold or sense.Right_dis() > sight_threshold):
	ir = sense.IR_read()
	if(ir[0] == False):
		i2c.turnRobot(-1, 80, 0.25)
	elif(ir[2] == False):
		i2c.turnRobot(1, 80, 0.25)
	else:
            i2c.driveRobot(1, 50)
            #print("Ultrasonics cannot see.")
        time.sleep(0.01)

    print("Entering PID Loop:")
    while(sense.center_IR_False() and sense.Left_dis() < sight_threshold and sense.Right_dis() < sight_threshold):

        ir = sense.IR_read()
	if(ir[0] == False):
		i2c.turnRobot(-1, 80, 0.25)
		print("Altering course due to right bump.")
	elif(ir[2] == False):
                i2c.turnRobot(1, 80, 0.25)
   		print("Altering course due to left bump.")
        else:
            x = (sense.Left_dis()+sense.Right_dis())/2 #One-Sided

            control = pid(x)

	    i2c.driveMotor("A", min_drive_speed + scalar*control)
	    i2c.driveMotor("B", min_drive_speed - scalar*control)
	    time.sleep(0.01)

        #i2c.driveRobot(1, 50)
        #time.sleep(0.25)

    while(sense.center_IR_False()):
	ir = sense.IR_read()
	if(ir[0] == False):
		i2c.turnRobot(-1, 80, 0.25)
	if(ir[2] == False):
		i2c.turnRobot(1, 80, 0.25)
	else:
        	i2c.driveRobot(1, 50)
        time.sleep(0.05)

    print("Reached tape!")
    i2c.driveRobot(-70, 1 )
    time.sleep(0.01)

def changeOrientation(current, new):

    diff = new - current
    for i in range(abs(diff)):
        #turnRobot90()
        if(diff > 0):
            print("Turning 90 deg cw ("+str(current)+"->"+str(new)+")")
            i2c.turn90(-1)
        elif(diff < 0):
            print("Turning 90 deg ccw ("+str(current)+"->"+str(new)+")")
            i2c.turn90(1)
    
    return new

