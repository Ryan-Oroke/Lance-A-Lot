import time
import I2C_LIB as i2c
import Sensors as sense
#from simple_pid import PID

#std_speed = 65
std_speed = 67

sight_threshold = 45

#pid = PID(16, 0, 0, setpoint=13) #One sided
#pid = PID(8, 0, 0, setpoint = 0) #Two-Sided

#pid.output_limits = (-50, 50)

#pid_max_time_step = 0.125

min_drive_speed = std_speed
max_ultrasonic_reading = 50

control = 0

intersection_delay = 2.45
line_crossing_delay = 0.625
backup_delay= 0.64
short_backup_delay = 0.2
#driving_timeout = 12
driving_timeout = 9

blank_intersection_search_delay = 3
blank_intersection_adj_delay = 0.5

turn_bumper_delay = 1.2
turn90_time = 1.0

def adjustFromBumper(bumper_num):
	print("Bumper " + str(bumper_num) + "hit, checking status...")
	if(bumper_num == 0):
		dir = -1
	elif(bumper_num == 2):
		dir = 1
	#The Adjustment process
	i2c.turnRobot(dir, std_speed, turn_bumper_delay)
	if(sense.center_line_detected() == "YELLOW"):
		i2c.turnRobot(-1*dir, std_speed, turn_bumper_delay + 0.25)
	elif(sense.center_line_detected() != "PURPLE"):
		i2c.turnRobot(-1*dir, std_speed, 0.25)

def traverseEdge3(start_node, end_node):
	print("Travelling from Node #" + str(start_node))
	#IR Only!
	starting_drive_time = time.time()
	while(sense.center_line_detected() == "NONE" and time.time() - starting_drive_time < driving_timeout):
		i2c.driveRobot(1, std_speed)
		ir = sense.IR_read()
		if(ir[0] == False):
			#adjustFromBumper(0)
			i2c.turnRobot(1, std_speed, 0.25)
		elif(ir[2] == False):
			#adjustFromBumper(2)
			i2c.turnRobot(-1, std_speed, 0.25)
		else:
			i2c.driveRobot(1, std_speed)
            		#print("Ultrasonics cannot see.")

	center_status = sense.center_line_detected()
	print(center_status)
	if(center_status == "YELLOW" or time.time()-starting_drive_time >= driving_timeout ):
		i2c.driveRobot(-1, 70)
		if(end_node == 41 or end_node == 42):
			time.sleep(short_backup_delay)
		else:
			time.sleep(backup_delay)
		i2c.stopRobot()
	#elif(center_status == "PURPLE"):
	#	i2c.driveRobot(1, 70)
	#	time.sleep(1)
	#	i2c.stopRobot()

	print("Reached Node #" + str(end_node))

def traverseToBlankNode(currNode, newNode, newBearing):
    d = 1
    opp_d = d*-1
    if(currNode == 11 and newNode == 12):
        i2c.driveRobot(1, std_speed)
        time.sleep(blank_intersection_search_delay)
        i2c.stopRobot
        for i in range(5):
            i2c.turn90(d)
            while(sense.center_line_detected() == "NONE"):
                i2c.driveRobot(1, std_speed)
                time.sleep(0.03)
            if(sense.center_line_detected() == "PURPLE"):
                break;
            else:
                i2c.driveRobot(-1, std_speed)
                i2c.turn90(opp_d)
                i2c.driveRobot(1, std_speed)
                time.sleep(blank_intersection_adj_delay)
                

def intersectionTurn(n, oldBearing, newBearing):
    start_time = time.time()
#    while(time.time() - start_time < intersection_delay):
#	ir = sense.IR_read()
#	if(False and ir[0] == False):
#	    i2c.turnRobot(1, 80, 0.25)
#	    start_time += 0.25
#	elif(False and ir[2] == False):
#	    i2c.turnRobot(-1, 80, 0.25)
#	    start_time += 0.25
#    	else:
#	    i2c.driveRobot(1, std_speed*0.8)
    i2c.driveRobot(1, std_speed)
    time.sleep(intersection_delay)
    i2c.stopRobot()
 
    diff = newBearing - oldBearing
    for i in range(abs(diff)):
        #turnRobot90()
        if(diff > 0):
            print("Turning 90 deg cw at intersection #" + str(n) + " ("+str(oldBearing)+"->"+str(newBearing)+")")
            i2c.turn90(-1)
        elif(diff < 0):
            print("Turning 90 deg ccw at intersection #" + str(n) + " ("+str(oldBearing)+"->"+str(newBearing)+")")
            i2c.turn90(1)

    i2c.driveRobot(-1, std_speed)
    time.sleep(0.4)

    #Advance until second purple line
    while(sense.center_line_detected() == "NONE"):
	ir = sense.IR_read()
	if(ir[0] == False):
		#adjustFromBumper(0)
		i2c.turnRobot(1, 80, 0.25)
	elif(ir[2] == False):
		#adjustFromBumper(2)
		i2c.turnRobot(-1, 80, 0.25)
        i2c.driveRobot(1, std_speed)
        time.sleep(0.01)

    i2c.driveRobot(1, std_speed)
    time.sleep(line_crossing_delay)
    i2c.stopRobot()

    return newBearing


def crossIntersection(old_dir, new_dir):
	print("crossIntersection()")
	if(old_dir == new_dir):
		start_time = time.time()
		print("OOPSIE")
		#i2c.driveRobot(1, std_speed*0.8)
		#time.sleep(0.5)
		while(sense.center_line_detected() == "NONE"):
			ir = sense.IR_read()
			if(ir[0] == False):
				i2c.turnRobot(-1, 80, 0.25)
			elif(ir[2] == False):
				i2c.turnRobot(1, 80, 0.25)
			else:
            			i2c.driveRobot(1, 60)
			time.sleep(0.05)
            		#print("Ultrasonics cannot see.")

	i2c.driveRobot(1, std_speed)
	time.sleep(0.8)
	i2c.turn90(-1)
	time.sleep(0.5)
	while(sense.center_line_detected() == "NONE"):
		i2c.driveRobot(1, 60)

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

	    print(x, control)

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

def changeOrientation(n, current, new):

    diff = new - current
    for i in range(abs(diff)):
        #turnRobot90()
        if(diff > 0):
            print("Turning 90 deg cw at #" + str(n) + " ("+str(current)+"->"+str(new)+")")
            i2c.turn90(-1)
        elif(diff < 0):
            print("Turning 90 deg ccw at #" + str(n) + " ("+str(current)+"->"+str(new)+")")
            i2c.turn90(1)
    
    l = sense.Left_dis()
    r = sense.Right_dis()
    x = l-r

    while(abs(x) > 5 and l < 15 and r < 15 and False):
	print("Fixing bearing...")
	if(x > 0):
	    i2c.turnRobot(1, std_speed, 0.5)
	else:
	    i2c.turnRobot(-1, std_speed, 0.5)
	
	

    return new

def traverseEdge2():
    print("Driving Forward...")
    scalar = -1

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
	#print(left_us, right_us)
        if(left_us < sight_threshold and right_us < sight_threshold):
		t = time.time()
		if((t - last_pid_time) > pid_max_time_step):
            		mean_us = (left_us + right_us)/2;
            		control = pid(mean_us)
            		i2c.driveMotor("A", min_drive_speed + scalar*control)
	    		i2c.driveMotor("B", min_drive_speed - scalar*control)
	    		print("Using US(L/B,R/F):", left_us, right_us, control)
	    		last_pid_time = time.time()
			time.sleep(0.05)
		else:
			#print("PID out of time")
			pass
	    	#time.sleep(0.05)
        elif(left_us < sight_threshold and right_us >= sight_threshold):
		i2c.turnRobot(1, 70, 0.1)
		#print("Adjusting course to left.")
		#i2c.driveMotor("A", std_speed)
		#i2c.driveMotor("B", 0.5*std_speed)
		#time.sleep(0.05)
	elif(left_us >= sight_threshold and right_us < sight_threshold):
		i2c.turnRobot(-1, 70, 0.1)
		#print("Adujsuting course to right.")
		#i2c.driveMotor("A", 0.5*std_speed)
		#i2c.driveMotor("B", std_speed)
		#time.sleep(0.5)
	else:
            i2c.driveRobot(1, std_speed)
            time.sleep(0.05)

        line_status = sense.center_line_detected()


    if(line_status == "PURPLE"):
        i2c.driveRobot(1, std_speed)
        time.sleep(1)
	i2c.stopRobot()
    else:
	i2c.driveRobot(-1, std_speed)
	time.sleep(1)
	i2c.stopRobot()
    print("Line Visible: ", line_status)

