import Sensors as sense
import time

while True:
	print("L:"+format(sense.Left_dis(), '03f')+ "R:" + format(sense.Right_dis(), '03f'))
	time.sleep(0.25)
