import readchar
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

while(1):
    key = readchar.readkey();
    print(key);

    # Determine what to do based on the key input

    # Numbered Keys
    if(key == "1" or key == "9"):
        # Dive Key
        print("Sinking");

    elif(key == "2"):
        # Down Key
        print("Backward");
	bytesToSend = ConvertStringToBytes("<B>");
        bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend);

    elif(key == "3"):
        # Toggle Light
        print("Toggled Light");

    elif(key == "4"):
        # Left Key
        print("Left");
        bytesToSend = ConvertStringToBytes("<L>");
        bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend);

    elif(key == "5"):
        # Stop Turning
        print("Stop Turning & Advancing");
	bytesToSend = ConvertStringToBytes("<S>");
	bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)
    elif(key == "6"):
        # Right Key
        print("Right");
	bytesToSend = ConvertStringToBytes("<R>");
        bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend);

    elif(key == "7"):
        # Rising Key
        print("Rising");

    elif(key == "8"):
        # Faster Key
        print("Forward");
        bytesToSend = ConvertStringToBytes("<F>");
        bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend);
        
    # Non-Numbering Keys
    elif(key == "e"):
        # Enable Key
        print("Endabled");

    elif(key == "q" or key == "c" or key == "x" or key == "z"):
        print("Execution Terminated by '"+key+"'");
        exit();
