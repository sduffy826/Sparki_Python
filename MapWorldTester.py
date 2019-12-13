"""
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
"""
import MapWorldClass

"""
Mainline
"""
def main():
  print(__file__, "start")
  gridPointsPerXYValue = 1.0
  fileWithPointsAnglesDistances = "xPosYPosAngleDistance.csv"

  mapperObj = MapWorldClass.MapWorld((1.0/gridPointsPerXYValue))
  mapperObj.generateMap(fileWithPointsAnglesDistances)
  mapperObj.plotMaps(True,True)

        
if __name__ == '__main__':
  main()       
