import matplotlib.pyplot as plt
import math

show_animation = True

class Dijkstra:

    def __init__(self, obstacleXPositions, obstacleYPositions, gridResolution, robotRadius):
      """
      Initialize map for a star planning

      obstacleXPositions: x position list of Obstacles [m]
      obstacleYPositions: y position list of Obstacles [m]
      gridResolution:     grid resolution [m]
      robotRadius:        robot radius[m]
      """
      self.gridResolution = gridResolution
      self.robotRadius    = robotRadius
      self.calc_obstacle_map(obstacleXPositions, obstacleYPositions)
      self.motion = self.get_motion_model()

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
    Calculate the final path, we will return it backwards from the goal to the start
    """
    def calc_final_path(self, goalNode, alreadyVisitedNodeDict):
      # generate final course, return array of x and y positions
      xPositionsGoalToStart, yPositionsGoalToStart = [self.calc_position(goalNode.x, self.minx)], [self.calc_position(goalNode.y, self.miny)]
      priIndex = goalNode.priorIndex
      while priIndex != -1:
        theNode = alreadyVisitedNodeDict[priIndex]
        xPositionsGoalToStart.append(self.calc_position(theNode.x, self.minx))
        yPositionsGoalToStart.append(self.calc_position(theNode.y, self.miny))
        priIndex = theNode.priorIndex

      return xPositionsGoalToStart, yPositionsGoalToStart


    """
    Calculate the heuristic... it's basically the hypotenuse
    """
    def calc_heuristic(self, node1, node2):
      weight = 1.0  # weight of heuristic
      heuristicValue = weight * math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
      return heuristicValue


    """
    This takes a given node and translates it's x and y values into a single index position, it's used to get
    the index of the dictionary item for visitied/unvisited nodes... this basically translates a two dimensional
    array into a long one dimesional one
    """
    def calc_index(self, node):
        return (node.y - self.miny) * self.xwidth + (node.x - self.minx)


    """
    Calculate the obstacle map
    """
    def calc_obstacle_map(self, obstacleXPositions, obstacleYPositions):
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
        x = self.calc_position(ix, self.minx)
        for iy in range(self.ywidth):
          y = self.calc_position(iy, self.miny)
          for iobstacleXPositions, iobstacleYPositions in zip(obstacleXPositions, obstacleYPositions):
            d = math.sqrt((iobstacleXPositions - x)**2 + (iobstacleYPositions - y)**2)
            if d <= self.robotRadius:
              self.obmap[ix][iy] = True
              break


    """
    Calculate the position... it's (indexPosition * gridResolution) + minPositionValue
    """
    def calc_position(self, index, minp):
      pos = index*self.gridResolution+minp
      return pos

    
    """
    This calculates the xyindex position for the arguments passed in... it basically maps the world position
    to the grid position... logic used is (axisValue - minAxisValue)/gridResolution
    """
    def calc_xyindex(self, position, minp):
      return round((position - minp)/self.gridResolution)


    """
    Returns an array that has the motions to take and their associated cost.  The
    array has the x, y offset and it's cost, makes sense if u look below.
    NOTE: The cost is really the distance taken; when only moving in x or y the
          cost is 1, when moving both then it's sqrt(xDelta**2 + yDelta**2), since
          ?Delta**2 is 1 it's the sqrt(1+1) or sqrt(2).
    """
    def get_motion_model(self):
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
    Returns all the nodes to get from the starting position to a goal position, if there isn't a
    path then empty array's are returned.  This uses dijkstra path alogorith.
    The inputs are the x,y of the starting position and the x,y of the goal position.
    The output is arrayX, arrayY of the nodes to get from goal to start (yes it's returned in order
    from goal to start)
    """
    def getPath(self, startingXPosition, startingYPosition, goalXPosition, goalYPosition):
      # Define the start and goal nodes
      startNode = self.Node(self.calc_xyindex(startingXPosition, self.minx), 
                            self.calc_xyindex(startingYPosition, self.miny), 
                            0.0, 
                            -1)
      goalNode = self.Node(self.calc_xyindex(goalXPosition, self.minx), 
                            self.calc_xyindex(goalYPosition, self.miny), 
                            0.0, 
                            -1)

      # We store the visited and unvisited nodes in dictionaries where the key to the dictionary
      # is the index position
      unvisitedNodeDict, alreadyVisitedNodeDict = dict(), dict()
      # Add the starting node to the list of unvisited nodes
      unvisitedNodeDict[self.calc_index(startNode)] = startNode

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
        if show_animation:  # pragma: no cover
          plt.plot(self.calc_position(current.x, self.minx),
                    self.calc_position(current.y, self.miny), "xc")
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
          adjacentNodeIndex = self.calc_index(adjacentNode)

          # Already visited so skip to next one
          if adjacentNodeIndex in alreadyVisitedNodeDict:
            continue

          if not self.verify_node(adjacentNode):
            continue

          # Not in list of open nodes then add it
          if adjacentNodeIndex not in unvisitedNodeDict:
            unvisitedNodeDict[adjacentNodeIndex] = adjacentNode  # Discover a new node
          else:
            if unvisitedNodeDict[adjacentNodeIndex].cost >= adjacentNode.cost:
              # The cost of this one is better than the one we had so replace it
              unvisitedNodeDict[adjacentNodeIndex] = adjacentNode

      # Return array's with the x and y positions to get from goal back to start (yes we give it reverse)
      rx, ry = self.calc_final_path(goalNode, alreadyVisitedNodeDict)

      return rx, ry


    """
    Verify that the node is good
    """
    def verify_node(self, node):
      px = self.calc_position(node.x, self.minx)
      py = self.calc_position(node.y, self.miny)

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
