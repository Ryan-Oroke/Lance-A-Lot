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

adj_A = 1.0
delay90 = 0.75

def convertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def sendMessage(msg):
    bytesToSend = convertStringToBytes(msg); 
    not_sent = True
    while(not_sent):
    	try:
    		bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend);
		not_sent = False
    	except:
		print("IO ERROR CAUGHT")
    
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
    
    if(letter == "A"):
	speed = speed * adj_A
        ##print("Correct!")
    
    if(letter != "A" and letter != "B"):
        print("ERROR: Bad Motor Command (" + letter + ")");
    else:
        if(speed != 0):
            #print(letter + direction + str(speed))
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

def turn90(i):
    if(i == 1):
        turnRobot(1, 110, delay90)
    elif(i == -1):
        turnRobot(-1, 110, delay90)
    else:
        print("turn90 input error!")
	exit(0)

def driveRobot(dir, speed):
    driveMotor("A", dir*speed)
    driveMotor("B", dir*speed)

def raiseLance():
    sendMessage("SV020")
    time.sleep(0.5)

def lowerLance():
    sendMessage("SV170")
    time.sleep(0.5)
