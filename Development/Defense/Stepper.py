import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
A1pin = 12 #Pink
A2pin = 16 #Orange
A3pin = 20 #Blue
A4pin = 21 #Yellow

GPIO.setup(A1pin, GPIO.OUT)
GPIO.setup(A2pin, GPIO.OUT)
GPIO.setup(A3pin, GPIO.OUT)
GPIO.setup(A4pin, GPIO.OUT)

Seq = range(0,4)
Seq[0] = [0, 0, 1, 1]
Seq[1] = [0, 1, 1, 0]
Seq[2] = [1, 1, 0, 0]
Seq[3] = [1, 0, 0, 1]


CW(1024)

def Step(P1, P2, P3, P4)
    GPIO.output(A1pin, P1)
    GPIO.output(A2pin, P2)
    GPIO.output(A3pin, P3)
    GPIO.output(A4pin, P4)
    
def CW(steps)
    for i in range(steps)
        for j in range(4)
            Step(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])

def CCW(steps)
    for i in range(steps)
        for j in reversed(range(4))
            Step(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
      

                       
