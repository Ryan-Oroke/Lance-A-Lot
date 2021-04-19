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
start_dir = 1
def main():
	dir = traverseGraph(start_dir, 1, 12)
	dir = traverseGraph(dir, 31, 11)
	dir = traverseGraph(dir, 11,21)
	dir = traverseGraph(dir, 21, 41)
	#i2c.sendMessage("SV170")
	#dir = traverseGraph(start_dir, 21, 42)
	#i2c.sendMessage("SV020")
	#dir = traverseGraph(dir, 42, 82)
	#dir = traverseGraph(start_dir, 82, 42)
	#i2c.sendMessage("SV170")
	#dir = traverseGraph(dir, 42, 41)
	#i2c.sendMessage("SV020")
	#dir = traverseGraph(dir, 41, 81)
	#i2c.sendMessage("SV170")
	#dir = traverseGraph(dir, 81, 11)


def traverseGraph(bearing, s, t):
	N = 1
	E = 2
	S = 3
	W = 4

	G = nx.DiGraph()

	starting_nodes = [1, 2]
	corner_nodes = [31, 32]
	intersection_nodes = [11, 21]
        blank_intersection_nodes = [12]
	balloon_corners = [41, 42]
	balloon_nodes = [81, 82, 83]

	G.add_nodes_from(starting_nodes)
	G.add_nodes_from(corner_nodes)
	G.add_nodes_from(intersection_nodes)
	G.add_nodes_from(blank_intersection_nodes)
	G.add_nodes_from(balloon_nodes)

	#edges = [(1,31,N), (31,11,E), (11,21,N), (21,41,W), (41,81,S), (81,41,N), (41,21,E), (21,42,E), (42,82,S)]
	#edges2 = [(82,42,N),(42,21,W),(21,11,S),(11,31,W),(31,1,S)]

	edges = [(1,31,N),(31,1,S), (31,11,E),(11,31,W), (11,21,N),(21,11,S), (21,41,W),(41,21,E),\
            (41,81,S),(81,41,N), (21,42,E),(42,21,W), (42,82,S),(82,42,N), (11,83,S),(83,11,N),\
            (11,12,E),(12,11,W), (12,63,S),(63,12,N), (63,92,W),(92,63,E)]


	G.add_weighted_edges_from(edges)
	#G.add_weighted_edges_from(edges2)

	#Can't do this on the Pi
	#plt.plot()
	#nx.draw(G, with_labels=True, font_weight='bold')
	#plt.show()

	path = nx.shortest_path(G, source=s, target=t)
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

	current_orientation = bearing

	#Now let's drive it!
	if(current_orientation != path_edges_orientation[0]):
		current_orientation = robot.changeOrientation(path[0], current_orientation, path_edges_orientation[0])
	for i in range(len(path_edges)-1):
	    robot.traverseEdge3(path[i], path[i+1])
	    if(path[i+1] in intersection_nodes):
		current_orientation = robot.intersectionTurn(path[i+1], current_orientation, path_edges_orientation[i+1])
	    elif(path[i+1] in balloon_nodes):
		print("Time to look for the balloon!")
		for i in range(5):
			i2c.driveRobot(-1, 60)
			time.sleep(1.25)
			i2c.driveRobot(1, 60)
			time.sleep(1.25)
	    elif(path[i+1] in blank_intersection_nodes):
		print("Backing away from balloon")
		i2c.driveRobot(-1, 60)
		time.sleep(2)
	    else:
	    	current_orientation = robot.changeOrientation(path[i+1], current_orientation, path_edges_orientation[i+1])

	robot.traverseEdge3(path[i], path[i+1])

	return current_orientation

if __name__ == '__main__':
	main()



