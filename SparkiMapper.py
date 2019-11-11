import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

EXTENDED_AREA = 6.0
DEBUGIT = True

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
def getGridMapConfig(startValuesForX, startValuesForY, endValuesForX, endValuesForY, xyResolution):
  """
  Calculates the min, max values for the arrays (that's the math.min(npArray1.min(),nparray2.min())
  """
  minX = round(min(startValuesForX.min(),endValuesForX.min()) - EXTENDED_AREA / 2)
  maxX = round(max(startValuesForX.max(),endValuesForX.max()) + EXTENDED_AREA / 2)

  minY = round(min(startValuesForY.min(),endValuesForY.min()) - EXTENDED_AREA / 2)
  maxY = round(max(startValuesForY.max(),endValuesForY.max()) + EXTENDED_AREA / 2)
  
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
def initFromFile(inputFile):
  inputData    = [line.strip().split(",") for line in open(inputFile)]
  np_startXpos = []
  np_startYpos = []
  np_angles    = []
  np_distances = []
  for poseWithDistance in inputData:  
    if len(poseWithDistance) == 4:
      np_startXpos.append(float(poseWithDistance[0].strip()))
      np_startYpos.append(float(poseWithDistance[1].strip()))
      np_angles.append(float(poseWithDistance[2].strip()))
      np_distances.append(float(poseWithDistance[3].strip()))
    else:
      print("Bad record in input file: " + list(poseWithDistance))
     
  np_startXpos = np.array(np_startXpos)
  np_startYpos = np.array(np_startYpos)
  np_angles    = np.array(np_angles)
  np_distances = np.array(np_distances)
  return np_startXpos, np_startYpos, np_angles, np_distances


"""
Fill the grid map with values
"""
def fillGridMap(startValuesForX, startValuesForY, endValuesForX, endValuesForY, xyResolution):
  minX, minY, maxX, maxY, xGridSize, yGridSize = getGridMapConfig(startValuesForX, startValuesForY, endValuesForX, endValuesForY, xyResolution)

  pointMap = np.ones((xGridSize,yGridSize))/2.0  # Give everything default value of .5 (not reviewed)
  # Get a zip with start and ending values (x1, y1, x2, y2)
  startAndEndValues = zip(startValuesForX,startValuesForY,endValuesForX,endValuesForY)
  for startingEndingTuple in startAndEndValues:  # Len of this same as the array of tuples
    x1, y1, x2, y2 = startingEndingTuple # Get values out of tuple

    if DEBUGIT:
      print("In fillGridMap  world line:({0},{1})->*({2},{3})".format(x1,y1,x2,y2))

    # Convert values to values to grid values
    x1, y1 = mapXYToGrid(x1, y1, minX, minY, xyResolution)
    x2, y2 = mapXYToGrid(x2, y2, minX, minY, xyResolution)

    if DEBUGIT:
      print("In fillGridMap  grid line:({0},{1})->*({2},{3})".format(x1,y1,x2,y2))


    # Get all the points that make up the line from (x1,y1)->(x2,y2)
    pointsOnLine = returnAllPointsBetweenTwoPoints(x1, y1, x2, y2)

    # NOTE: You may want to extend the cells marked as cleared by using the helper too :)
    for aPointOnLine in pointsOnLine:
      pointMap[aPointOnLine[0]][aPointOnLine[1]] = 0.0  # Mark this point as free
    # Mark the ending points as 1.0 (we extend it a little 2 cells either side), the
    # routine below is a little helper to do that
    fillGridMapHelper(pointMap, aPointOnLine[0], aPointOnLine[1], -1, 1, 1.0)
  return pointMap, minX, minY, maxX, maxY

def fillGridMapHelper(pointMapToUpdate, xPos, yPos, rangeLow, rangeHigh, value2Use):
  for xOffset in range(rangeLow,rangeHigh+1):
    for yOffset in range(rangeLow,rangeHigh+1):
      pointMapToUpdate[xPos+xOffset][yPos+yOffset] = value2Use
  return

# This takes in a point in the world and converts it to a point in the grid
def mapTupleToGrid(thePoint, minX, minY, xyResolution):
  xInGrid = int(round((thePoint[0] - minX)/xyResolution))
  yInGrid = int(round((thePoint[1] - minY)/xyResolution))
  return (xInGrid,yInGrid)

# Note this doesn't return the 'real' value, that's lost due to rounding, but should be close enough
def mapGridToWorld(thePoint, minX, minY, xyResolution):
  xInWorld = (thePoint[0]*xyResolution) + minX
  yInWorld = (thePoint[1]*xyResolution) + minY
  return (xInWorld, yInWorld)

"""
Helper routine, convert the x and y values to the grid values
"""
def mapXYToGrid(xValue, yValue, minX, minY, xyResolution):
  theXValue = int(round(xValue - minX) / xyResolution)
  theYValue = int(round(yValue - minY) / xyResolution)
  return theXValue, theYValue

"""
Return an array that contains a tuple for each point between the starting
position and the ending position.  This uses the Bresenham's line drawing 
algorithm
Input args: the starting position x1, y1 and ending position x2, y2 
"""
def returnAllPointsBetweenTwoPoints(x1, y1, x2, y2):
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

"""
Mainline
"""
def main():
  print(__file__, "start")
  
  xyResolutionToUse = 1.0  # 2 grid points per x/y value
  
  startXPosArray, startYPosArray, anglesArray, distancesArray = initFromFile("xPosYPosAngleDistance.csv")
  print("length of startXPosArray: {0}".format(len(startYPosArray)))

  # Convert angles in degrees to radians
  radiansArray = np.radians(anglesArray)

  # Calculate the endpoints for x and y (NOTE: the x is based on cos not sin like some do... doesn't matter as
  # long as your consistemt... and other sparki code is based on x/cos)
  endXPosArray = (np.cos(radiansArray) * distancesArray) + startXPosArray
  endYPosArray = (np.sin(radiansArray) * distancesArray) + startYPosArray
  
  for i in range(2,4):
    print("Starting point ({0:.2f},{1:.2f}) angle: {2} distance: {3:.2f}".format(startXPosArray[i],startYPosArray[i],anglesArray[i],distancesArray[i]))
    print("     end point ({0:.2f},{1:.2f})".format(endXPosArray[i],endYPosArray[i]))
    
  pointMap, minX, minY, maxX, maxY = fillGridMap(startXPosArray, startYPosArray, endXPosArray, endYPosArray, xyResolutionToUse)

  # Get the number of rows and columns in the point array
  xyres = np.array(pointMap).shape
  plt.figure(1, figsize=(10,4))
  plt.subplot(122)
  plt.imshow(pointMap, cmap="PiYG_r") # cmap = "binary" "PiYG_r" "PiYG_r" "bone" "bone_r" "RdYlGn_r"
  plt.clim(-0.4, 1.4)
  plt.gca().set_xticks(np.arange(-.5, xyres[1], 1), minor=True)
  plt.gca().set_yticks(np.arange(-.5, xyres[0], 1), minor=True)
  plt.grid(True, which="minor", color="w", linewidth=0.6, alpha=0.5)
  plt.colorbar()

  plt.subplot(121)
  # plt.plot([endYPosArray, np.zeros(np.size(endYPosArray))], [endXPosArray, np.zeros(np.size(endXPosArray))], "ro-")

  for i in range(len(startXPosArray)):
    xArray = [startXPosArray[i], endXPosArray[i]]
    yArray = [startYPosArray[i], endYPosArray[i]]
    plt.plot(xArray, yArray, 'm')

  #plt.plot([startXPosArray, endXPosArray], [startYPosArray, endYPosArray] , "ro-")
  plt.axis("equal")
  plt.plot(0.0, 0.0, "ob")
  plt.gca().set_aspect("equal", "box")
  bottom, top = plt.ylim()  # return the current ylim
  plt.ylim((top, bottom)) # rescale y axis, to match the grid orientation
  plt.grid(True)
  plt.show()




        
if __name__ == '__main__':
    #seanTest(-4,12, -2, -1)
    main()       