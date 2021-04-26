import I2C_LIB as i2c
import time

i2c.driveRobot(1, 100)
time.sleep(2)
i2c.driveRobot(-1, 100)
time.sleep(2)
i2c.stopRobot()
