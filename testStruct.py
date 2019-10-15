
import sparkiStats

sensorList = {}
sparkiStats.setVars(sensorList,"67,BOTTOMINFRARED,edgeLeft,591,lineLeft,655,lineCenter,773,lineRight,675,edgeRight,555")
sparkiStats.setVars(sensorList,"67,BOTTOMINFRARED,edgeLeft,591,lineLeft,655,lineCenter,773,lineRight,675,edgeRight,555")
sparkiStats.setVars(sensorList,"67,BOTTOMINFRARED,edgeLeft,493,lineLeft,657,lineCenter,775,lineRight,677,edgeRight,557")

theSummary = sparkiStats.getSummary(sensorList)
for aLine in theSummary:
  print(aLine)





  # print("SensorName: {0}".format(sensorName))

  #  print("mean is {0}".format(theMean))
  #  print("median is {0}".format(theMedian))    
  #  print("mode is {0}".format(theMode))  
  #  print("stdev is {0}".format(theStdDev))  