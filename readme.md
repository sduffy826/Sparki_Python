**GetPath.py** - File that has the class (DijkstraPathPlanning) to do path traversing, give it starting point and goal and it'll return the path to get there (get back array's of points to traverse - an array for x positions and one for y positions - use zip() to merge into tuple if you want).  Obviously by the name of the class this is using the dijkstra algorithm... builds a cost to get from a->b and then takes the path with lowest cost.
**GetPathTester.py** - Little test program to demonstrate above


**MapWorldClass.py** - Class for mapping the world, currently really geared toward reading a file with startX, startY, angleInDegrees, distanceToObstacle.  It generates a grid of the robots world and marks each poing within it as (obstacle (value 1.0), clear (value 0.0), or unchecked (value 0.5).
**MapWorldTester.py** - Code to test the code above

**readSerialPort.py** - Like name suggests; for reading serial port - the information from the sparki