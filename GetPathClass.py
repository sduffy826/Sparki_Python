import matplotlib.pyplot as plt
import math

class DijkstraPathPlanning:

    def __init__(self, obstacleXPositions, obstacleYPositions, gridResolution, robotRadius, show_animation):
      """
      Initialize map for a star planning

      obstacleXPositions: x position list of Obstacles [m]
      obstacleYPositions: y position list of Obstacles [m]
      gridResolution:     grid resolution [m]
      robotRadius:        robot radius[m]
      """
      self.gridResolution = gridResolution
      self.robotRadius    = robotRadius
      self.showAnimation  = show_animation
      self.calculateObstacleMap(obstacleXPositions, obstacleYPositions)
      self.motion         = self.getMotionsAndCost()

    """
    Inner class to represent a node in the grid
    """
    class Node:
      def __init__(self, x, y, cost, priorIndex):
        self.x          = x  # index of grid
        self.y          = y  # index of grid
        self.cost       = cost
        self.priorIndex = priorIndex

      def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.cost) + "," + str(self.priorIndex)


    """
    This takes a given node and translates it's x and y values into a single index position, it's used to get
    the index of the dictionary item for visitied/unvisited nodes... this basically translates a two dimensional
    array into a long one dimesional one
    """
    def calculateNodeIndex(self, node):
        return (node.y - self.miny) * self.xwidth + (node.x - self.minx)


    """
    Calculate the obstacle map
    """
    def calculateObstacleMap(self, obstacleXPositions, obstacleYPositions):
      self.minx = round(min(obstacleXPositions))
      self.miny = round(min(obstacleYPositions))
      self.maxx = round(max(obstacleXPositions))
      self.maxy = round(max(obstacleYPositions))
      print("minX: {0} minY: {1} maxX: {2} maxY: {3}".format(self.minx,self.miny,self.maxx,self.maxy))

      self.xwidth = round((self.maxx - self.minx)/self.gridResolution)
      self.ywidth = round((self.maxy - self.miny)/self.gridResolution)
      print("xWidth: {0} yWidth: {1}".format(self.xwidth,self.ywidth))
      
      # obstacle map generation
      self.obmap = [[False for i in range(self.ywidth)]
                    for i in range(self.xwidth)]
      for ix in range(self.xwidth):
        x = self.calculatePosition(ix, self.minx)
        for iy in range(self.ywidth):
          y = self.calculatePosition(iy, self.miny)
          for iobstacleXPositions, iobstacleYPositions in zip(obstacleXPositions, obstacleYPositions):
            d = math.sqrt((iobstacleXPositions - x)**2 + (iobstacleYPositions - y)**2)
            if d <= self.robotRadius:
              self.obmap[ix][iy] = True
              break


    """
    Calculate the position... it's (indexPosition * gridResolution) + minPositionValue
    """
    def calculatePosition(self, index, minp):
      pos = index*self.gridResolution+minp
      return pos

    
    """
    This calculates the xyindex position for the arguments passed in... it basically maps the world position
    to the grid position... logic used is (axisValue - minAxisValue)/gridResolution
    """
    def calculateXYindex(self, position, minp):
      return round((position - minp)/self.gridResolution)


    """
    Returns an array that has the motions to take and their associated cost.  The
    array has the x, y offset and it's cost, makes sense if u look below.
    NOTE: The cost is really the distance taken; when only moving in x or y the
          cost is 1, when moving both then it's sqrt(xDelta**2 + yDelta**2), since
          ?Delta**2 is 1 it's the sqrt(1+1) or sqrt(2).
    """
    def getMotionsAndCost(self):
      motion = [[1, 0, 1],              # x+1, y,   cost=1
                [0, 1, 1],              # x,   y+1, cost=1
                [-1, 0, 1],             # x-1. y,   cost=1
                [0, -1, 1],             # x,   y-1, cost=1
                [-1, -1, math.sqrt(2)], # x-1, y-1, cost=1.41
                [-1, 1, math.sqrt(2)],  # x-1, y+1, cost=1.41
                [1, -1, math.sqrt(2)],  # x+1, y-1, cost=1.41
                [1, 1, math.sqrt(2)]]   # x+1, y+1, cost=1.41

      return motion

    
    """
    Calculate the final path, we will return it backwards from the goal to the start
    """
    def getFinalPath(self, goalNode, alreadyVisitedNodeDict):
      # generate final course, return array of x and y positions
      xPositionsGoalToStart, yPositionsGoalToStart = [self.calculatePosition(goalNode.x, self.minx)], [self.calculatePosition(goalNode.y, self.miny)]
      priIndex = goalNode.priorIndex
      while priIndex != -1:
        theNode = alreadyVisitedNodeDict[priIndex]
        xPositionsGoalToStart.append(self.calculatePosition(theNode.x, self.minx))
        yPositionsGoalToStart.append(self.calculatePosition(theNode.y, self.miny))
        priIndex = theNode.priorIndex

      return xPositionsGoalToStart, yPositionsGoalToStart

    
    """
    Returns all the nodes to get from the starting position to a goal position, if there isn't a
    path then empty array's are returned.  This uses dijkstra path alogorith.
    The inputs are the x,y of the starting position and the x,y of the goal position.
    The output is arrayX, arrayY of the nodes to get from goal to start (yes it's returned in order
    from goal to start)
    """
    def getPath(self, startingXPosition, startingYPosition, goalXPosition, goalYPosition):
      # Define the start and goal nodes
      startNode = self.Node(self.calculateXYindex(startingXPosition, self.minx), 
                            self.calculateXYindex(startingYPosition, self.miny), 
                            0.0, 
                            -1)
      goalNode = self.Node(self.calculateXYindex(goalXPosition, self.minx), 
                            self.calculateXYindex(goalYPosition, self.miny), 
                            0.0, 
                            -1)

      # We store the visited and unvisited nodes in dictionaries where the key to the dictionary
      # is the index position
      unvisitedNodeDict, alreadyVisitedNodeDict = dict(), dict()
      # Add the starting node to the list of unvisited nodes
      unvisitedNodeDict[self.calculateNodeIndex(startNode)] = startNode

      # Loop till done (or no solution)... note the no solution condition is when there are no
      # more nodes in unvisitedNodeDict
      while True:
        # Get the index position of the open node with the lowest cost
        if (len(unvisitedNodeDict) > 0):
          c_id = min(unvisitedNodeDict, key=lambda o: unvisitedNodeDict[o].cost)
        else:
          # No nodes in unvisitedNodeDict, no solution return empty arrays
          return [],[]

        # Set the current node to the one we got with the lowest cost
        current = unvisitedNodeDict[c_id]

        # show graph
        if self.showAnimation:  # pragma: no cover
          plt.plot(self.calculatePosition(current.x, self.minx),
                    self.calculatePosition(current.y, self.miny), "xc")
          if len(alreadyVisitedNodeDict.keys()) % 10 == 0:
            plt.pause(0.001)

        # See if we're at the goal
        if current.x == goalNode.x and current.y == goalNode.y:
          print("Find goal")
          goalNode.priorIndex = current.priorIndex
          goalNode.cost = current.cost
          break

        # Remove the item from the open set
        del unvisitedNodeDict[c_id]

        # Add it to the closed set
        alreadyVisitedNodeDict[c_id] = current

        # Expand search grid based on motion model
        for i, _ in enumerate(self.motion):
          # Get a node. set it's x,y,cost,priorIndex 
          adjacentNode = self.Node(current.x + self.motion[i][0],
                                    current.y + self.motion[i][1],
                                    current.cost + self.motion[i][2], 
                                    c_id)
          adjacentNodeIndex = self.calculateNodeIndex(adjacentNode)

          # Already visited so skip to next one
          if adjacentNodeIndex in alreadyVisitedNodeDict:
            continue

          if not self.isGoodNode(adjacentNode):
            continue

          # Not in list of open nodes then add it
          if adjacentNodeIndex not in unvisitedNodeDict:
            unvisitedNodeDict[adjacentNodeIndex] = adjacentNode  # Discover a new node
          else:
            if unvisitedNodeDict[adjacentNodeIndex].cost >= adjacentNode.cost:
              # The cost of this one is better than the one we had so replace it
              unvisitedNodeDict[adjacentNodeIndex] = adjacentNode

      # Return array's with the x and y positions to get from goal back to start (yes we give it reverse)
      rx, ry = self.getFinalPath(goalNode, alreadyVisitedNodeDict)

      return rx, ry

    
    """
    Little helper to return the slope between two points
    """
    def getSlope(self, x1, y1, x2, y2):
      dx = x2-x1
      if dx != 0:
        return ((y2-y1)/dx)
      else:
        return "INF"

    
    """
    Verify that the node is good; it's position has to be within min/max and not on an obstacle
    """
    def isGoodNode(self, node):
      px = self.calculatePosition(node.x, self.minx)
      py = self.calculatePosition(node.y, self.miny)

      if px < self.minx:
        return False
      elif py < self.miny:
        return False
      elif px >= self.maxx:
        return False
      elif py >= self.maxy:
        return False

      if self.obmap[node.x][node.y]:
        return False

      return True


    """
    This takes the points in the arrays which are a bunch of points and creates arrays with the points representing the line segments... i.e.
    where the slope between the points are the same... i.e. 1,1 2,2 3,3 4,4 5,4 is translated to 1,1 4,4 5,4 (slope between first 4 points
    are the same, it changed with the last point).
    NOTE: We do it in reverse order because it has fro the goal to the start and we want the other way around
    """
    def mergePointsWithSameSlope(self, arrayX, arrayY):
      newXArray = []
      newYArray = []
      
      firstPass = True
      idx       = len(arrayX) -1
      baseIdx   = idx
      while (idx >= 0):
      #for idx in range(len(arrayX)):
        if baseIdx != idx:  # we're not pointing to ourselves (only on first rec)   
          currSlope = self.getSlope(arrayX[baseIdx],arrayY[baseIdx],arrayX[idx],arrayY[idx])
          if firstPass:
            # On first pass we want to set the 'lastSlope' correctly
            lastSlope = currSlope
            firstPass = False

          if currSlope != lastSlope:
            # Slope changed append the prior record and set the base to be that prior record
            newXArray.append(arrayX[idx+1])
            newYArray.append(arrayY[idx+1])
            baseIdx   = idx+1
            lastSlope = self.getSlope(arrayX[baseIdx],arrayY[baseIdx],arrayX[idx],arrayY[idx])
        else:
          # Only true on the first iteration so add that record
          newXArray.append(arrayX[baseIdx])
          newYArray.append(arrayY[baseIdx])

        idx -= 1
      
      if (len(arrayX) > 1):
        # We need to write out the last record (if we have more than one record in the array)
        newXArray.append(arrayX[0])
        newYArray.append(arrayY[0])

      return newXArray, newYArray
