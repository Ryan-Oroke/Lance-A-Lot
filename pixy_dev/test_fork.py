import RPi.GPIO as GPIO
import os, signal
import time
import subprocess
import I2C_LIB as i2c

color_pin = 1
start_stop_pin = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(start_stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.add_event_detect(start_stop_pin, GPIO.RISING, callback=startRun())
# GPIO.add_event_detect(start_stop_pin, GPIO.RISING, callback=stopRun())

running = False
pid = 9999
off_state = 1
on_state = 0
while(True and pid > 0):
    #RUN BY THE PARENT ONLY

    #IF NOT RUNNING 
    if(running == False and GPIO.input(start_stop_pin) == on_state):
        time.sleep(0.2)
	#Check for debouncing
        if(GPIO.input(start_stop_pin) == 0):
            time.sleep(0.5)
            running = True
		
	    #Start the new subprocess child! (Start traversal)
            print("Process Starting")
	    devnull = open('/dev/null', 'w')
	    p = subprocess.Popen(["python", "course_test.py"])

	    #Store the pid for later, this will allow for killing the traversal mid-drive	
	    pid = p.pid 
	    print("Child PID: " + str(pid))
        else:
            print("False positive recieved.")

    #IF ALREADY RUNNING 
    elif(running == True and GPIO.input(start_stop_pin) == off_state):
        time.sleep(0.2)
	
	#Check for debounce
        if(GPIO.input(start_stop_pin) == off_state):
		
	    #Kill and reap the child
	    print("Killing child process: " + str(pid))
	    while p.poll() is None:
	    	os.kill(pid, 9)
	    running = False
	    i2c.stopRobot()
        else:
            print("False negative received.")

    #Wait for the switch to flip and for the program to fork
    elif(running == False and GPIO.input(start_stop_pin) == off_state):
	#print("Waiting for input to start run.")
	time.sleep(1)

#The child's code. THIS IS OUTDATED AND WAS USED FOR THE FORK() METHOD. 
if(pid == 0):
    pass
    #os.system("python turn_test.py")
    #while(True):
    #    print("Hello from the child process!")
    #    time.sleep(1)

print("The top-level process has terminated!!!")
