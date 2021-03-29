import readchar
import time
import os
import i2c_woot as woot

time.sleep(1)
woot.driveMotor("A", 150)
time.sleep(1)
woot.SendI2CMessage("AF100")
woot.SendI2CMessage("BF100")
time.sleep(0.5)
woot.SendI2CMessage("AF000")
woot.SendI2CMessage("BF000")
time.sleep(0.5)
woot.SendI2CMessage("AR050")
woot.SendI2CMessage("BR050")
time.sleep(0.5)
woot.SendI2CMessage("AF000")
woot.SendI2CMessage("BF000")
time.sleep(0.5)
woot.SendI2CMessage("AF200")
woot.SendI2CMessage("BR200")
time.sleep(0.5)
woot.SendI2CMessage("AF000")
woot.SendI2CMessage("BF000")
time.sleep(0.5)

# Servo Control
woot.SendI2CMessage("SV020")
time.sleep(1)
woot.SendI2CMessage("SV150")
time.sleep(1)
woot.SendI2CMessage("SV035");
