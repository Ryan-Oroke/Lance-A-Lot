import RPi.GPIO as GPIO
import multiprocessing as mp
import time
GPIO.setmode(GPIO.BCM)

button_pin = 21

GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def mptry():
    trig = False
    while True:
        press = GPIO.input(button_pin)
        if ((press == True) and (trig == False)):
            print("button triggered")
            trig = True
            q.put(press)
        elif press == False:
            trig = False
        time.sleep(0.05)

if __name__ == '__main__':
    mp.set_start_method('fork')
    q = mp.Queue()
    test = mp.Process(target = mptry)
    test.start()

count2 = 0
while True:
    if not q.empty():
        event = q.get()
        print(event)
    else:
        count2 = count2 + 1
        print("Main Process" + str(count2))
        time.sleep(5)
