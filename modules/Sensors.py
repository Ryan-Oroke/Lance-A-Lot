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

# IR pin assignments
IR_LEFT_PIN = 22
IR_CENTER_PIN = 27
IR_RIGHT_PIN = 17

#setup the button pins
GPIO.setup(IR_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_CENTER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)



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
       
      def centering()
        center = 0
        for i in range(3)
             r_dist = UltrasonicSensors.Left_dis()
             l_dist = UltrasonicSensors.Right_dis()
             center = center + r_dist - l_dist
         center = center/3 
         
         return center


def IR_read()
    #Check for lines
    left_on = GPIO.input(IR_LEFT_PIN)
    center_on = GPIO.input(IR_CENTER_PIN)
    right_on = GPIO.input(IR_RIGHT_PIN)
    return left_on, center_on, right_on
