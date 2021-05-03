# Lance-A-Lot
## University of Colorado Boulder MCEN 4115/5115: Mechatronics

For all of the final code used during runoff, visit the 'pixy_dev' folder. 
The following files are the most relevant to our final project's software:
 - test_fork.py
 - course_test.py
 - random_traversal.py
 - robot.py
 - Sensors.py
 - I2C_LIB.py
 - pixy_module.py
 - camera.py

*The following has been copied from our final project report.*

Software Design
===============

In order to adeptly navigate the course, we developed a series of
different algorithms which were used to traverse the course in different
manners. To simplify the complexity of our software, as well as improve
its readability, these function calls were broken down into several
different Python modules. The contents and core functions of these
modules have been broken down below. Note that most of the robot’s
software has not been included in the appendix of the report, as our
team wrote roughly 2,000 lines of code. For the vehicle’s complete code
database, please visit the *raspberrypi* branch of our team’s repository
at <https://github.com/Ryan-Oroke/Lance-A-Lot>.

Subprocess Routine *(test\_fork.py)*
------------------------------------

As the top level process for Lance-A-Lot, the subprocess python routine
controlled the start of the vehicle’s navigation as well as its
termination. Control of upper level processes were done by watching a
switch on the robot, and then forking the process using the
*subprocess.Popen()* fucntion call to begin course traversal in a child
process. The PID of the child was then stored by the parent, which
allowed for the parent (the original process) to send *os.kill(PID, 9)*
to the child when the same switch was turn off. (Note that signal number
nine is SIGINT, the same as a CTRL+C key press.) The parent process then
reaped the child and waited for the switch to flip on and repeat the
process. The beauty of this process was that it allowed the team to
start and kill our robot with a single switch, making the overall
competition work-flow much simpler and robust.

Course Traversal Routine *(course\_test.py)*
--------------------------------------------

This module contained the most significant software relevant to course
navigation and the robot’s ability to make decisions regarding course
traversal. Additionally, this module was called during the
*suprocess.Popen()* described previously.

In order to robustly navigate the course, a graph was employed to
describe the relationships between locations on the course. The
*networkx* library in Python was employed to do this, and easily allowed
for path finding within our set of defined vertices. Below in figure
[fig:map] is an image representing the robot’s understanding of the
course layout. Notice that the entire graph has not been mapped into the
robot’s memory, this is because traversal became unreliable beyond more
than a few balloon, usually due to the stack up of multiple, small
location offsets.

The main function of the *course\_test.py* module performed the
high-level function of dictating where the robot should traverse on the
course network, which was in turn computed and executed by
*traverseGraph()*. This process was broken down into the following
series of steps for the traversal from one node to a balloon:

1.  Compute a path list from Node $s$ to Node $t$

2.  Convert the path list from a list of nodes to a list of directions

3.  Execute traversal along this path. Nodes are considered reached when
    the IR sensor and ArduCam detect a line in front of the robot
    (regardless of color).

4.  Traverse the span of the newly reached node with either
    *changeOrientation()* or *intersectionTurn()* (depending on whether
    the new node is a purple or yellow intersection).

5.  Repeat until a \`\`decision node\`\` is reached. Then turn to face
    the would-be location of the balloon.

6.  If a balloon exists and the Pixy determines it to have the correct
    signature, then rush and pop the balloon. Otherwise skip.

This process was then repeated for each set of traversals along the
course, and as a result the target nodes of each run were hard coded
(although the path was recomputed each time). Further, the *main()*
function also used *I2C\_LIB* to control the actuation of the lance
during each of the*balloonDecision()* function calls.

General Robot Functionality *(robot.py)*
----------------------------------------

The *robot.py* Python module was used to make the majority of
Lance-A-Lot’s main functionality more modular. As a result, this chunk
of software contained the following critical functions:

-   *lineBasedOrient()*: Corrects the bearing of the robot after its
    random starting orientation using only the IR sensors. Initial
    design plans included the use of ultrasonics for this purpose, but
    they proved to be unreliable.

-   *traverseEdge3()*: Used to travel from one node to another while
    watching various sensors, such as the infrared sesnors and Pi
    Camera.

-   *intersectionTurn()*: Took the current and future bearings as
    inputs, and then crossed through purple tape intersections and
    reoriented the robot accordingly.

-   *changeOrientation()*: Simply rotated the robot in steps of
    90$\degree$ to align with the desired orientation of the platform.

All of the above functions were dependent on and I2C module which we had
written to make controlling the robot easier using functions such as
*driveRobot()*,*turnRobot()*, and *stopRobot()*. The use of these
abstraction was a fantastic investment as it made our code easier to
understand and saved time. As a result, we strongly recommend the use of
such a module to future teams.

Collecting Data from the Couse
------------------------------

Similar to the I2C module detailed above, the measurement of sensor data
on the Raspebrry Pi was also abstracted to separate files.

### Sensors *(Sensors.py)*

The *Sensors.py* module, written in Python, was responsible to reading
the infrared and ultrasonic sensors, as well as the color and process
switches. In most cases, the function calls within the module simply
returned the values output by the sensors allowing for the process of
physically reading the data to exist separately from their repeated
areas of need. In some cases, functions were to created to evaluate the
state of multiple sensors to make upper-level decision making simpler.

### Utilizing OpenCV with the Pi Camera *(camera.py)*

Data from the PiCam (or ‘ArduCam’) was processed within the *camera.py*
module using *OpenCV2*. Since the PiCam was only used detection of the
line color directly in front of the robot, the implementation of *cv2*
was somewhat simple. Essentially, an image with 64x64 pixel resolution
was taken and passed through a yellow and purple HSV color filter,
resulting in respective masks for each color. The total number of pixels
in each mask were then counted to give the total magnitude of their
respective colors within the frame. We initially had issues with mask
effectiveness due to we overcast and sunny conditions outside the ITLL
had significant effects on the mask. To combat this, we added a white
LED to stabilize HSV readings across different times and weather. This
method of determining line color proved to very robust and became the
foundation for the navigation of our vehicle.

### Pixy2 Camera *(pixy\_module.py)*

After significant testing we determined that the Pi Camera would be too
slow for our team to use its vision capabilities for tracking balloons,
thus we were compelled to use the Pixy for recognizing targets. For the
purpose of simplifying the wiring layout of Lance-A-Lot, we chose to
connect the Pixy using one of the Pi’s four USB connections. As a
result, the helper files generated by the *python\_exmaples* folder in
the *pixy2* repository were copied over into the *pixy\_dev* folder of
our own repository. In fact, only after reinstalling the repo and
copying the entire *python\_exmaples* folder into our working directory
were we able to effectively communicate with the Pixy. This could be
very helpful information for future teams. With the exception of this
workaround, much of the Pixy’s utilization was fairly boilerplate (it
was basically the same as the provided examples). The only exception to
this was the addition of some extra logic operations we implemented to
make upper-level code cleaner, such as a function which adjusted robot
orientation to *chase* a balloon.
