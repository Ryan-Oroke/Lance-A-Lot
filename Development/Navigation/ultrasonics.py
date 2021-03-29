#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
trig = 26
echo1 = 20 # right sensor
echo2 = 16 # left sensor
 
#set GPIO direction (IN / OUT)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)
GPIO.setup(echo2, GPIO.IN)

class UltrasonicSensors: 
    def Right_dis():
        # set Trigger to HIGH
        GPIO.output(trig, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trig, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(echo1) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(echo1) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

    def Left_dis():
        # set Trigger to HIGH
        GPIO.output(trig, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trig, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(echo2) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(echo2) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance
