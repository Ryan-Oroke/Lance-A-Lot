#Ryan Oroke
#Adapted from Lab 3

import RPi.GPIO as GPIO
import time

IR_PIN = 24
IR_TRIGGERED = False

#set the gpio pinouts with BCM numbering
GPIO.setmode(GPIO.BCM)

#setup the button pins
GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(True):

	time.sleep(0.25)
	#print(GPIO.input(IR_PIN))
	if(GPIO.input(IR_PIN) == 0 and IR_TRIGGERED==False):
		print("IR Sensor has been triggered.")
		IR_TRIGGERED = True
	elif(GPIO.input(IR_PIN) == 1 and IR_TRIGGERED==True):
		print("IR Sensor has bee untriggered.")
		IR_TRIGGERED = False

	time.sleep(0.1)

GPIO.cleanup();

