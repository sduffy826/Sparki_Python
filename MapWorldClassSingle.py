import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image, transforms
from collections import deque

EXTENDGRIDAREABY = 6  # Number of grid points to exted by (like a margin)
DEBUGIT = True

class MapWorld:
  # Constructor with args...  this one is for the future so it's commented now
  """
  def __init__(self, startXPosArray, startYPosArray, angleArray, distanceArray, gridResolution=0.5):
    self.startXPosArray    = startXPosArray
    self.startYPosArray    = startYPosArray
    self.angleArray        = angleArray
    self.distanceArray     = distanceArray
    self.xyResolutionToUse = gridResolution
  """

  # Initialization no args, nothing required
  def __init__(self, gridResolution=0.5):
    self.xyResolutionToUse = gridResolution
    self.minX, self.minY, self.maxX, self.maxY = 0,0,0,0
    self.havePointMap = False

  def generateMap(self, inputFile):
    # Read from the input file
    self.np_startXPosArray, self.np_startYPosArray, self.np_anglesArray, self.np_distancesArray = self.initFromFile(inputFile)
    
    if DEBUGIT:
      print("length of np_startXPosArray: {0}".format(len(self.np_startYPosArray)))

    # Convert angles in degrees to radians
    self.np_radiansArray = np.radians(self.np_anglesArray)

    # Calculate the endpoints for x and y (NOTE: the x is based on cos not sin like some do... doesn't matter as
    # long as your consistemt... and other sparki code is based on x/cos)
    self.np_endXPosArray = (np.cos(self.np_radiansArray) * self.np_distancesArray) + self.np_startXPosArray
    self.np_endYPosArray = (np.sin(self.np_radiansArray) * self.np_distancesArray) + self.np_startYPosArray
    
    if DEBUGIT:  # Sample some output
      for i in range(len(self.np_startXPosArray)):
        print("Starting point ({0:.2f},{1:.2f}) angle: {2} distance: {3:.2f}".format(self.np_startXPosArray[i],
                                                                                     self.np_startYPosArray[i],
                                                                                     self.np_anglesArray[i],
                                                                                     self.np_distancesArray[i]))
        print("     end point ({0:.2f},{1:.2f})".format(self.np_endXPosArray[i],self.np_endYPosArray[i]))
      
    # Fill the grid based on the lines we've seen
    self.np_pointMap, self.minX, self.minY, self.maxX, self.maxY = self.fillGridMap(self.np_startXPosArray, self.np_startYPosArray, 
                                                                   self.np_endXPosArray, self.np_endYPosArray, self.xyResolutionToUse)
    if (len(self.np_pointMap) > 0):
      self.havePointMap = True

  # Return the x/y min max values 
  def getMinMaxXYValues():
    return self.minX, self.minY, self.maxX, self.maxY

  # Return point mapping 
  def getPointMap():
    if (self.havePointMap):
      return []
    else:
      return self.np_pointMap

  def plotMaps(self, lineMap = True, pointMap = True):
    # Get the number of rows and columns in the point array
    outMap = self.np_pointMap.T # Transpose the array so values appear correct (otherwise x are on vertical axis)
    xyres = np.array(outMap).shape
    if lineMap and pointMap:
      plt.figure(1, figsize=(12,5))               # figsize is in inches
      print("two")
    else:
      plt.figure(1, figsize=(6,5))
      print("one")
    
    if pointMap:  # This shows each point, the open points are different color then obstacle
      plt.subplot(121)
      # tr = transforms.Affine2D().rotate_deg(270)  // This is to transform an image, didn't work with grid
      # Below we show all the points in the map (imshow is image show)
      # plt.imshow(self.np_pointMap, cmap="bone_r", transform=tr) # cmap = "binary" "PiYG_r" "bone" "bone_r" "RdYlGn_r"  // show format of transform
      # Use imshow to show the matrix, it uses the values (0.0, 0.5 and 1.0) to map to colors, the origin lower puts 0,0 in lower left corner
      plt.imshow(outMap, cmap="bone_r", origin="lower") # cmap = "binary" "PiYG_r" "bone" "bone_r" "RdYlGn_r"  the .T transposes the array
      #plt.clim(-0.4, 1.4)  
      plt.clim(0.0,1.0)
      plt.gca().set_xticks(np.arange(-.5, xyres[1], 1), minor=True)
      plt.gca().set_yticks(np.arange(-.5, xyres[0], 1), minor=True)
      #plt.gca().invert_yaxis()  // Another way to invert the axis... use the parm 
      plt.grid(True, which="minor", color="w", linewidth=1.0, alpha=0.5)  #color="#c8c9b3"
      plt.gca().set_title("Grid/Obstacle Map")      
      plt.colorbar()
    if lineMap:  # Show the lines that were taken from the sensor
      plt.subplot(122)
      # plt.plot([endYPosArray, np.zeros(np.size(endYPosArray))], [endXPosArray, np.zeros(np.size(endXPosArray))], "ro-")

      for i in range(len(self.np_startXPosArray)):
        xArray = [self.np_startXPosArray[i], self.np_endXPosArray[i]]
        yArray = [self.np_startYPosArray[i], self.np_endYPosArray[i]]
        #plt.plot(xArray, yArray, 'm')
        plt.plot(xArray,yArray,color="green",linewidth=1,marker='o',markersize=1)
        plt.scatter(self.np_endXPosArray[i],self.np_endYPosArray[i],marker='o',c='red')
        
      #plt.plot([np_startXPosArray, endXPosArray], [np_startYPosArray, endYPosArray] , "ro-")
      plt.axis("equal")
      plt.plot(0.0, 0.0, "ob")
      plt.gca().set_aspect("equal", "box")
      plt.gca().invert_yaxis()
      bottom, top = plt.ylim()  # return the current ylim
      plt.ylim((top, bottom)) # rescale y axis, to match the grid orientation
      plt.grid(True)
      plt.gca().set_title("Sensor Readings")
    
    plt.show()


  """
  Fill the grid map with values that are in the arrays
  """
  def fillGridMap(self, startValuesForX, startValuesForY, endValuesForX, endValuesForY, xyResolution):
    minX, minY, maxX, maxY, xGridSize, yGridSize = self.getGridMapConfig(startValuesForX, startValuesForY, endValuesForX, endValuesForY, xyResolution)

    pointMap = np.ones((xGridSize,yGridSize))/2.0  # Give everything default value of .5 (not reviewed)
    # Get a zip with start and ending values (x1, y1, x2, y2)
    startAndEndValues = zip(startValuesForX,startValuesForY,endValuesForX,endValuesForY)
    for startingEndingTuple in startAndEndValues:  # Len of this same as the array of tuples
      x1, y1, x2, y2 = startingEndingTuple # Get values out of tuple

      if DEBUGIT:
        print("In fillGridMap  world line:({0},{1})->*({2},{3})".format(x1,y1,x2,y2))

      # Convert values to values to grid values
      x1, y1 = self.mapXYToGrid(x1, y1, minX, minY, xyResolution)
      x2, y2 = self.mapXYToGrid(x2, y2, minX, minY, xyResolution)

      if DEBUGIT:
        print("In fillGridMap  grid line:({0},{1})->*({2},{3})".format(x1,y1,x2,y2))


      # Get all the points that make up the line from (x1,y1)->(x2,y2)
      pointsOnLine = self.returnAllPointsBetweenTwoPoints(x1, y1, x2, y2)
      if DEBUGIT:
        print("Points from ({0},{1})->({2}.{3})".format(x1,y1,x2,y2))
        tempString="  "
        for aPoint in pointsOnLine:
          tempString += " ({0},{1})".format(aPoint[0],aPoint[1])
          if len(tempString) > 120:
            print(tempString)
            tempString = "  "
        print(tempString)

      # NOTE: You may want to extend the cells marked as cleared by using the helper too :)
      for aPointOnLine in pointsOnLine:
        pointMap[aPointOnLine[0]][aPointOnLine[1]] = 0.0  # Mark this point as free
      # Mark the ending points as 1.0 (we extend it a little 2 cells either side), the
      # routine below is a little helper to do that
      # self.fillGridMapHelper(pointMap, aPointOnLine[0], aPointOnLine[1], -1, 1, 1.0)
      self.fillGridMapHelper(pointMap, aPointOnLine[0], aPointOnLine[1], 0, 0, 1.0)
    return pointMap, minX, minY, maxX, maxY


  """
  Little helper routine to fill the point (and range around it) with a value
  """
  def fillGridMapHelper(self, pointMapToUpdate, xPos, yPos, rangeLow, rangeHigh, value2Use):
    for xOffset in range(rangeLow,rangeHigh+1):
      for yOffset in range(rangeLow,rangeHigh+1):
        pointMapToUpdate[xPos+xOffset][yPos+yOffset] = value2Use
    return


  """
  This calculates the grid map configuration, the parms are
      startValuesForX - an np array of the x starting points
      startValuesForY - an np array of the y starting points
      endValuesForX - np array of the ending x xpoing
      endValuesForY - np array of the corresonding ending y point
        NOTE: startOfXPoint[0] is related to startValuesForY[0], and it's ending point is at endOfXPoint[0] and y is at endOfYPoint[0]
      xyResolution - the xy resolution, this is the number of grid spaces per point, so if you want 5 grid spaces per unit of x then it'd be .2
  fyi: EXTEMD+AREA - is the space you want to extend the grid space by
  It returns
    minX is minimum value found in x endpoint array
    minY is minimum y value found
    maxX is the max x value found
    maxY is the max y value found in the sample
    xGridSize is the number of x grid locations in the world
    yGridSize is the grid size for the y axis
  """
  def getGridMapConfig(self, startValuesForX, startValuesForY, endValuesForX, endValuesForY, xyResolution):
    """
    Calculates the min, max values for the arrays (that's the math.min(npArray1.min(),nparray2.min())
    """
    minX = round(min(startValuesForX.min(),endValuesForX.min()) - EXTENDGRIDAREABY / 2)
    maxX = round(max(startValuesForX.max(),endValuesForX.max()) + EXTENDGRIDAREABY / 2)

    minY = round(min(startValuesForY.min(),endValuesForY.min()) - EXTENDGRIDAREABY / 2)
    maxY = round(max(startValuesForY.max(),endValuesForY.max()) + EXTENDGRIDAREABY / 2)
    
    xGridSize = int(round((maxX - minX) / xyResolution))
    yGridSize = int(round((maxY - minY) / xyResolution))
    if DEBUGIT:
      print("The grid map is ", xGridSize, "x", yGridSize, ".")
      print("MinX: {0} MinY: {1}  MaxX: {2} MaxY: {3}".format(minX, minY, maxX, maxY))

    return minX, minY, maxX, maxY, xGridSize, yGridSize


  """
  This reads the input file passed in and returns numpy arrays that
  have the starting x position, starting y position, angles and
  distance traveled.
  This is really for testing
  """
  def initFromFile(self, inputFile):
    inputData = [line.strip().split(",") for line in open(inputFile)]
    startXpos = []
    startYpos = []
    angles    = []
    distances = []
    for poseWithDistance in inputData:  
      if len(poseWithDistance) == 4:
        startXpos.append(float(poseWithDistance[0].strip()))
        startYpos.append(float(poseWithDistance[1].strip()))
        angles.append(float(poseWithDistance[2].strip()))
        distances.append(float(poseWithDistance[3].strip()))
      else:
        print("Bad record in input file: " + list(poseWithDistance))
      
    np_startXpos = np.array(startXpos)
    np_startYpos = np.array(startYpos)
    np_angles    = np.array(angles)
    np_distances = np.array(distances)
    return np_startXpos, np_startYpos, np_angles, np_distances

  # This takes in a point in the world and converts it to a point in the grid
  def mapTupleToGrid(self, thePoint, minX, minY, xyResolution):
    xInGrid = int(round((thePoint[0] - minX)/xyResolution))
    yInGrid = int(round((thePoint[1] - minY)/xyResolution))
    return (xInGrid,yInGrid)

  # Note this doesn't return the 'real' value, that's lost due to rounding, but should be close enough
  def mapGridToWorld(self, thePoint, minX, minY, xyResolution):
    xInWorld = (thePoint[0]*xyResolution) + minX
    yInWorld = (thePoint[1]*xyResolution) + minY
    return (xInWorld, yInWorld)

  """
  Helper routine, convert the x and y values to the grid values
  """
  def mapXYToGrid(self, xValue, yValue, minX, minY, xyResolution):
    theXValue = int(round(xValue - minX) / xyResolution)
    theYValue = int(round(yValue - minY) / xyResolution)
    return theXValue, theYValue

  """
  Return an array that contains a tuple for each point between the starting
  position and the ending position.  This uses the Bresenham's line drawing 
  algorithm
  Input args: the starting position x1, y1 and ending position x2, y2 
  """
  def returnAllPointsBetweenTwoPoints(self, x1, y1, x2, y2):
    deltaX = x2 - x1
    deltaY = y2 - y1
    isSteep = abs(deltaY) > abs(deltaX) 
    if isSteep: # rotate line
      x1, y1 = y1, x1
      x2, y2 = y2, x2
    
    wasSwapped = False # swap start and end points if necessary and store swap state
    if x1 > x2:
      x1, x2 = x2, x1
      y1, y2 = y2, y1
      wasSwapped = True
    
    deltaX = x2 - x1 # recalculate deltas
    deltaY = y2 - y1 
    error = int(deltaX / 2.0) # calculate error
    ystep = 1 if y1 < y2 else -1
    # iterate over  points between start and end
    
    points = []
    y = y1
    for x in range(x1, x2 + 1):
      coordinate = (y, x) if isSteep else (x, y)
      points.append(coordinate)   
      error -= abs(deltaY)
      if error < 0:
        y += ystep
        error += deltaX
      
    if wasSwapped: # reverse the list if the coordinates were swapped
      points.reverse()

    npPoints = np.array(points)
    return npPoints

