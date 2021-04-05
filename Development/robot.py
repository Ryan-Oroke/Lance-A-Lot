import time
import I2C_LIB as i2c
import Sensors as sense

sight_threshold = 22

def traverseEdge():
    print("Driving Forward...")
    while(sense.all_IR_False() and sense.Left_dis() < sight_threshold and sense.Right_dis() < sight_threshold):
        i2c.driveRobot(1, 50)
        #time.sleep(0.25)
    print("Reached tape!")
    time.sleep(0.25)

def changeOrientation(current, new):

    diff = new - current
    for i in range(abs(diff)):
        #turnRobot90()
        if(diff > 0):
            print("Turning 90 deg cw ("+str(current)+"->"+str(new)+")")
            i2c.turn90(1)
        elif(diff < 0):
            print("Turning 90 deg ccw ("+str(current)+"->"+str(new)+")")
            i2c.turn90(-1)
    
    return new

