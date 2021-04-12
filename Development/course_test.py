import networkx as nx
#import matplotlib.pyplot as plt
import robot
import sys
import signal
import I2C_LIB as i2c
import time
def signal_handler(sig, frame_sig):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    #cv2.destroyAllWindows()
    #cap.release()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


N = 1
E = 2
S = 3
W = 4

G = nx.DiGraph()

nodes = [1, 2, 3]
G.add_nodes_from(nodes)

edges = [(1,2,N), (2,3,E), (3,4,E), (4,5,N)]

G.add_weighted_edges_from(edges)


#Can't do this on the Pi
#plt.plot()
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()

path = nx.shortest_path(G, source=1, target=5)
path_edges = []
path_edges_orientation = []
print(path_edges)

#Get edges for traversal
for i in range(len(path)-1):
    path_edges.append((path[i], path[i+1]))
    path_edges_orientation.append(G[path[i]][path[i+1]]['weight'])

print(path)
print(path_edges)
print(path_edges_orientation)

current_orientation = 1

#Now let's drive it!
for i in range(len(path_edges)-1):
    robot.traverseEdge2()
    current_orientation = robot.changeOrientation(current_orientation, path_edges_orientation[i+1])
    i2c.sendMessage("SV000")
    time.sleep(1)
    i2c.sendMessage("SV140")

robot.traverseEdge2()





