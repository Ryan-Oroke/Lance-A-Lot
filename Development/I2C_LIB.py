#convertStringToBytes(String)
#sendMessage(String)
#driveMotor(Motor Letter, Motor Speed/Direction)
#stopRobot()
#turnRobot(direction, speed, delay time)
#driveRobot(direction, speed, delay time)

import smbus
import os
import time

bus = smbus.SMBus(1)

#Arduino i2c address
i2c_address = 0x36
i2c_cmd = 0x01

def convertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def sendMessage(msg):
    bytesToSend = convertStringToBytes(msg); 
    bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend);
    
def driveMotor(letter, speed):
    if(speed >= 0):
        direction = "F"
    elif(speed < 0):
        direction = "R"
        
    if(abs(speed) > 255):
        if(speed > 0):
            speed = 255
        else:
            speed = -255
    elif(abs(speed) < 0):
        speed = 0
    
    #if(letter == "A"):
        ##print("Correct!")
    
    if(letter != "A" and letter != "B"):
        print("ERROR: Bad Motor Command (" + letter + ")");
    else:
        if(speed != 0):
            print(letter + direction + str(speed))
            sendMessage(letter + direction + str(format(abs(speed), "3.0f")))
        else:
            sendMessage(letter + direction + "000")

def stopRobot():
    driveMotor("A", 0)
    driveMotor("B", 0)
            
def turnRobot(dir, speed, delay):
    driveMotor("A", dir*speed)
    driveMotor("B", -1*dir*speed)
    time.sleep(delay)
    stopRobot()
    
def driveRobot(dir, speed):
    driveMotor("A", dir*speed)
    driveMotor("B", dir*speed)
    
