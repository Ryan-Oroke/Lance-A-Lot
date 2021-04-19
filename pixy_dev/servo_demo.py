import I2C_LIB as i2c
import time

i2c.sendMessage("SV000")
time.sleep(1)
i2c.sendMessage("SV180")

