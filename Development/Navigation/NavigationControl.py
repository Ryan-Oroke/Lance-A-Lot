import smbus
import sys
import time
import os
from ultrasonics import UltrasonicSensors
from i2c_commands import i2c_control
sys.path.append("../modules/")
import I2C_LIB

std_spd = 100

try:
    while True:
        #Beginning of navigation loop will always be to go forward
        driverobot("F"
        center = centering()
        
            if center < 1 # if center is less than one then left distance was larger on average
                # twist left and continue forward
                i2c_control.Send_Command("AF100")
                i2c_control.Send_Command("BR100")
                time.sleep(0.5)
                i2c_control.Send_Command("AF100")
                i2c_control.Send_Command("BF100")
            if center > 1 # if center is > 1 right distance was larger
                # twist right and continue forward
    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
