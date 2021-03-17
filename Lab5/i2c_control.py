import smbus
import time
import os

bus = smbus.SMBus(1)

#Arduino i2c addres
i2c_address = 0x36
i2c_cmd = 0x01

def ConvertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

# send welcome message at start-up
bytesToSend = ConvertStringToBytes("Hello Uno")
bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)

# loop to send message
exit = False
while not exit:
    r = raw_input('Enter something, "q" to quit"')
    print(r)
    
    bytesToSend = ConvertStringToBytes(r)
    bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)
    
    if r=='q':
        exit=True
