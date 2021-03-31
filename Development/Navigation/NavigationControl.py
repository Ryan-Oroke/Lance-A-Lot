import smbus
import sys
import time
import os
from ultrasonics import UltrasonicSensors
from i2c_commands import i2c_control
sys.path.append("../modules/")
import I2C_LIB

std_spd = 100
drive_delay = 2
turn_delay = 1
F = 1
L = 1
R = -1
B = -1

try:
    while True:
        #Beginning of navigation loop will always be to go forward
        driveRobot(F, std_spd)
        center = centering()  
        left_on, center_on, right_on = IR_read()
        if right_on == True
            turnRobot(L, std_spd, turn_delay)
            driveRobot(F, std_spd/2)
            rightLast = True
            leftLast = False
        else if left_on == True
            turnRobot(R, std_spd, turn_delay)
            driveRobot(F, std_spd/2)
            leftLast = True
            rightLast = False
        else if center_on == True
            stopRobot()
            driveRobot(B, std_spd)
            time.sleep(1)
            if leftLast == True
                turnRobot(R, std_spd, turn_delay)
                driveRobot(F, std_spd/2)
            else if rightLast == True
                turnRobot(L, std_spd, turn_delay)
                driveRobot(F, std_spd/2)
        else if center < 1 # if center is less than one then left distance was larger on average
            #turn left
            turnRobot(L, std_spd, turn_delay)
            driveRobot(F, std_spd)
        else if center > 1 # if center is > 1 right distance was larger
            #turn right
            turnRobot(R, std_spd, turn_delay)
            driveRobot(F, std_spd)
                
            turnRobot
    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
