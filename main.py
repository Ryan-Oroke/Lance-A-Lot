#Main file for robot control all other programs and functions will be run through here

# imports and set up
import RPi.GPIO as GPIO
import time
import multiprocessing as mp

#setup
GPIO.setmode(GPIO.BCM)

# function for starting camera background process
def Camera_Process():
    while True:
        #Insert code that calls the pixy to look for a balloon
        #Once balloon or robot detected set detect = True
        search = child_conn.recv()
        if search == True:
            # search for balloon
            # for loop to test code struct 
            for i in range(5):
                detect = True
            if detect == True:
               child_conn.send(detect)
               detect = False

# exception classes for interrupting loops
	# Technically exceptions are for error handling, but should work for our purposes
class Error(Exception):
    # Base Class for other exceptions
    pass

class Opponent_Detected(Error):
    # Raised when camera detects opponent
    pass

# Begin by starting camera fork
if __name__ == '__main__': #important syntax for using fork
   ################# set up for testing remove later #######################
    button_pin = 21
    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    ######################################################################### 
    parent_conn, child_conn = Pipe()
    mp.set_start_method('fork')
    q = mp.Queue()
    Camera = mp.Process(target = Camera_Process)
    Camera.start()

    mode = 1
    # Main operation loop
    while True:
        try:
	    # There are 4 modes the robot can be in:
	    #
	    # Mode 1:
		# is the mode where the robot will travel from one point on the graph to another
	    #
	    # Mode 2:
		# is when the robot is in front of a ballon it needs to pop
	    #
	    # Mode 3:
		# is the defense mode where the robot will attempt to defend itself and pop the opponent balloon
	    #
	    # Mode 4:
		# is when the robot sees the opponent and chases after it	

		# Will delete if not statement to replace with signal handler
            if not q.empty():
                event = q.get()
                print("opponent detected")
                time.sleep(1)
                raise Opponent_Detected
            elif mode == 1:
                print("traverse edge loop")
                time.sleep(1)
                mode = 2
            elif mode == 2:
                print("Balloon pop loop")
                time.sleep(1)
                mode = 3
            elif mode == 3:
                print("Defense loop")
                time.sleep(1)
                mode = 1
            elif mode == 4:
                print("Seek opponent")
                time.sleep(1)
        except Opponent_Detected:
            mode = 4

