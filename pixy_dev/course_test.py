#course_test.py
#Used too test-run the network graph generated for navigation. 

import networkx as nx
#import matplotlib.pyplot as plt
import robot
import sys
import signal
import I2C_LIB as i2c
import time

#Signal handler function. This will catch the signal for CTRL+C and stop the robot/exit execution. 
def signal_handler(sig, frame_sig):
    print('You pressed CTRL+C...Terminating Operation')
    i2c.driveMotor("A", 0)
    i2c.driveMotor("B", 0)
    #cv2.destroyAllWindows()
    #cap.release()
    sys.exit(0)

#INstantiate the predefined signal handler function
signal.signal(signal.SIGINT, signal_handler)

#Establish the starting orientation of the robot.
start_dir = 1

def main():
	#Calls the traverseGraph function to travel between nodes. Also raises and lowers servo when needed with i2c. 
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
	#Called with a starting orientation, start node, and end node. Traverses the graph from s to t. (I know rebuilding the graph everytime is bad but oh well.)

	#Establish weights for directions (direction of edge is stored in each edges weight)
	N = 1
	E = 2
	S = 3
	W = 4

	#Create the graph object
	G = nx.DiGraph()

	#Node lists used to build the graph
	starting_nodes = [1, 2]
	corner_nodes = [31, 32]
	intersection_nodes = [11, 21]
        blank_intersection_nodes = [12]
	balloon_corners = [41, 42]
	balloon_nodes = [81, 82, 83]

	#Add nodes to the graph
	G.add_nodes_from(starting_nodes)
	G.add_nodes_from(corner_nodes)
	G.add_nodes_from(intersection_nodes)
	G.add_nodes_from(blank_intersection_nodes)
	G.add_nodes_from(balloon_nodes)

	#Edges used to connected the nodes (starting_node, end_node, weight/direction)
	edges = [(1,31,N),(31,1,S), (31,11,E),(11,31,W), (11,21,N),(21,11,S), (21,41,W),(41,21,E),\
            (41,81,S),(81,41,N), (21,42,E),(42,21,W), (42,82,S),(82,42,N), (11,83,S),(83,11,N),\
            (11,12,E),(12,11,W), (12,63,S),(63,12,N), (63,92,W),(92,63,E)]

	#Connect the graph
	G.add_weighted_edges_from(edges)

	#Can't do this on the Pi over SSH
	#plt.plot()
	#nx.draw(G, with_labels=True, font_weight='bold')
	#plt.show()

	#Compute the shortest path between the source and target nodes (the only path). Then generated a traversal list to instruct robot how to move. 
	path = nx.shortest_path(G, source=s, target=t)
	path_edges = []
	path_edges_orientation = []
	print(path_edges)

	#Get edges for traversal
	for i in range(len(path)-1):
	    path_edges.append((path[i], path[i+1]))
	    path_edges_orientation.append(G[path[i]][path[i+1]]['weight'])

	#Print the path so it can be verified. 
	print(path)
	print(path_edges)
	print(path_edges_orientation)

	#Use a variable which is more understandable for direction
	current_orientation = bearing

	#Now let's drive it!

	#Adjust initial orientation if different than first edge traversal
	if(current_orientation != path_edges_orientation[0]):
		current_orientation = robot.changeOrientation(path[0], current_orientation, path_edges_orientation[0])

	#Traverse all of the edges in the pre-planned path
	for i in range(len(path_edges)-1):

	    #Traverse the edge
	    robot.traverseEdge3(path[i], path[i+1])

	    #Sometimes we need to do special things after edge traversal, do those here:
	    if(path[i+1] in intersection_nodes):
		#Perform and intersection specific turn
		current_orientation = robot.intersectionTurn(path[i+1], current_orientation, path_edges_orientation[i+1])

	    elif(path[i+1] in balloon_nodes):
		#Attack the balloon! (This is not working yet...)
		print("Time to look for the balloon!")
		for i in range(5):
			i2c.driveRobot(-1, 60)
			time.sleep(1.25)
			i2c.driveRobot(1, 60)
			time.sleep(1.25)

	    elif(path[i+1] in blank_intersection_nodes):
		#Used for finding "blank" or "hidden" intersections since they lack tape across the path near them.

		#YET TO BE INSTANTIATED (CODE WRITTEN THOUGH)
 
		print("Backing away from balloon")
		i2c.driveRobot(-1, 60)
		time.sleep(2)
	    else:
		#If none of these happen, we have reached a yellow corner. Therein use the standard turning package. 
	    	current_orientation = robot.changeOrientation(path[i+1], current_orientation, path_edges_orientation[i+1])

	#End of FOR loop

	#We have to add a final traverse edge since we only do up to path[end-1] in the FOR loop
	robot.traverseEdge3(path[i], path[i+1])

	#Return the new orientation of the robot to keep track of things for successive calls. 
	return current_orientation




#Allows for a main() loop to be placed above everything else
if __name__ == '__main__':
	main()



