
from statistics import mean, median, mode, stdev

def setVars(sensorList, stringFromSparki):
  # Store values... later we'll do analysis on them
  arrayOfValues = stringFromSparki.split(",")
  if len(arrayOfValues) > 2:  # Has to has more than two values
    sensorName = arrayOfValues[1]  # Sensor name is second value (elapsed is first)
    if sensorName not in sensorList:
      sensorList[sensorName] = {}  # create dictionary for this sensor
     
    idx = 4 # Have it represent where the value is not the label for it
    while idx <= len(arrayOfValues):
      sensorLabel = arrayOfValues[idx-2]
      sensorValue = float(arrayOfValues[idx-1])
      idx += 2
      if sensorLabel not in sensorList[sensorName]:
        sensorList[sensorName][sensorLabel] = []
      sensorList[sensorName][sensorLabel].append(sensorValue)

def getSummary(sensorList):
  rtnList = []
  rtnList.append("Sensor,Attribute,Mean,Median,Mode,StdDev,...")
  for sensorName in sensorList:
    theString = sensorName
    for sensorType in sensorList[sensorName]:
      try:
        theMean = mean(sensorList[sensorName][sensorType])
      except:
        theMean = sensorList[sensorName][sensorType][0]
      try:
        theMedian = median(sensorList[sensorName][sensorType])
      except:
        theMedian = sensorList[sensorName][sensorType][0]
      try:
        theMode = mode(sensorList[sensorName][sensorType])
      except:
        theMode = sensorList[sensorName][sensorType][0]
      try: 
        theStdDev = stdev(sensorList[sensorName][sensorType])
      except:
        theStdDev = 0.0
      theString += "," + sensorType + "," + str(theMean) + "," + \
                                  str(theMedian) + "," + \
                                  str(theMode) + ","  + \
                                  str(theStdDev) 
    rtnList.append(theString)
  return rtnList