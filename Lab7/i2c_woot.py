import smbus
import os

bus = smbus.SMBus(1)

#Arduino i2c address
i2c_address = 0x36
i2c_cmd = 0x01

def ConvertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def SendI2CMessage(msg):
    bytesToSend = ConvertStringToBytes(msg); 
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
            SendI2CMessage(letter + direction + str(format(abs(speed), "3.0f")))
        else:
            SendI2CMessage(letter + direction + "000")
        
        
    
    
    
    
    
    
    
    