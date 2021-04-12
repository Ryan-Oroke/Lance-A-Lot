import time
import I2C_LIB as i2c
import Sensors as sense
from simple_pid import PID

sight_threshold = 100

pid = PID(4, 0, 0, setpoint=8) #One sided
#pid = PID(8, 0, 0, setpoint = 0) #Two-Sided

pid.output_limits = (-50, 50)

pid_max_time_step = 0.125

min_drive_speed = 80
max_ultrasonic_reading = 50

control = 0

def traverseEdge2():
    print("Driving Forward...")
    scalar = 1

    line_status = sense.center_line_detected()
    last_pid_time = time.time()
    while( line_status == "NONE"):
	
        ir = sense.IR_read()
        if(ir[0] == False):
            i2c.turnRobot(-1, 80, 0.25)
        elif(ir[2] == False):
            i2c.turnRobot(1, 80, 0.25)

        left_us = sense.Left_dis()
        right_us = sense.Right_dis()
	print(left_us, right_us)
        if(left_us < sight_threshold and right_us < sight_threshold):
		t = time.time()
		if((t - last_pid_time) > pid_max_time_step):
            		mean_us = (left_us + right_us)/2;
            		control = pid(mean_us)
            		i2c.driveMotor("A", min_drive_speed + scalar*control)
	    		i2c.driveMotor("B", min_drive_speed - scalar*control)
	    		print("Using US:", left_us, right_us, control)
	    		last_pid_time = time.time()
		else:
			print("PID out of time")
	    	time.sleep(0.05)
        elif(left_us < sight_threshold and right_us >= sight_threshold):
		i2c.turnRobot(1, 70, 0.1)
	elif(left_us >= sight_threshold and right_us < sight_threshold):
		i2c.turnRobot(-1, 70, 0.1)
	else:
            i2c.driveRobot(1, 80)
            time.sleep(0.05)

        line_status = sense.center_line_detected()


    if(line_status == "PURPLE"):
        i2c.driveRobot(1, 50)
        time.sleep(1)
	i2c.stopRobot()
    else:
	i2c.driveRobot(-1, 50)
	time.sleep(1)
	i2c.stopRobot()
    print("Line Visible: ", line_status)


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
	i2c.driveRobot(1, 30)
	status_line = sense.center_line_detected()
	print(status_line)
	if(status_line != "NONE"):
		print("Line Seen: ", status_line)
		break
	i2c.driveRobot(1, 50)
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

    while(sense.center_line_detected() == "NONE"):
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
    time.sleep(10.01)

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

