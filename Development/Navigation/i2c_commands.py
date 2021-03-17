import smbus
import time
import os

class i2c_control:
  def ConvertStringToBytes(src):
      converted = []
      for b in src:
          converted.append(ord(b))
      return converted

  def Send_Command(cmd):
    bus = smbus.SMBus(1)
    #Arduino i2c addres
    i2c_address = 0x36
    i2c_cmd = 0x01
    bytesToSend = ConvertStringToBytes(cmd)
    bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)
