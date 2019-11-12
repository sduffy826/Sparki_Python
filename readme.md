## Note
---
A lot of the code is really 'play' code used to learn... The items of interest are identified below.  These are specific to work done with sparki although they can be used for other projects (i.e. if you need mapping, path planning, serial communication)


## Path planning
---
**GetPathClass.py** - File that has the class (DijkstraPathPlanning) to do path traversing, give it starting point and goal and it'll return the path to get there (get back array's of points to traverse - an array for x positions and one for y positions - use zip() to merge into tuple if you want).  Obviously by the name of the class this is using the dijkstra algorithm... builds a cost to get from a->b and then takes the path with lowest cost.

**GetPathTester.py** - Little test program to demonstrate above


## Mapping world
---
**MapWorldClass.py** - Class for mapping the world, currently really geared toward reading a file with startX, startY, angleInDegrees, distanceToObstacle.  It generates a grid of the robots world and marks each point within it as (obstacle (value 1.0), clear (value 0.0), or unchecked (value 0.5).  To use this you need a file of values where each record is in the format: x,y,angleInDegrees,distanceToObj.  Once you have the data you can use it by sample stub below:
```
  gridPointsPerXYValue = 4.0                                      # number of grid points per x/y cell 
  fileWithPointsAnglesDistances = "xPosYPosAngleDistance.csv"     # the input file with data

  mapperObj = MapWorldClass.MapWorld((1.0/gridPointsPerXYValue))  # instantiate the object (I have import MapWorldClass at top of code)
  mapperObj.generateMap(fileWithPointsAnglesDistances)            # this creates the map of data, note you can use 'getPointMap() afterward 
                                                                  #   too (0.0 is free, 1.0 is obstacle and 0.5 is unvisitied)
  mapperObj.plotMaps(True,True)                                   # this plots the grid, the args show the grid map and the lines 
                                                                  *   representing the vectors in input file
```
**MapWorldTester.py** - Code to test the code above

## Miscelaneous
---
**readSerialPort.py** - Like name suggests; for reading serial port - the information from the sparki