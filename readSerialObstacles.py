import serial
import time
from datetime import datetime
import sparkiStats

useBluetooth = False
isIBMMacBook = True

outputFile   = "obstacleReadings.csv"

if useBluetooth == False:
  if isIBMMacBook:
    ser = serial.Serial(port='/dev/cu.usbmodem14601', baudrate=19200)
  else:
    ser = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600)

readLines = 0
runTime   = 60          # Only runs for 2 minutes
startTime = time.time()  # Returns time in seconds since epoch
ser.write(b' ')    # Push something on the serial port, this will activate it

fileHandle = open(outputFile,"at") # Append and text file
currTime   = time.time() - startTime
leaveLoop  = False
# -----------------------------------------------------------------------
def processObstacle(insFromSparki):
  theArray = insFromSparki.split(',')
  if len(theArray) > 8 and theArray[0] == "DO":
    fileHandle.write(theArray[2]) # x value
    fileHandle.write(",")
    fileHandle.write(theArray[4]) # y value
    fileHandle.write(",")
    fileHandle.write(theArray[6]) # angle
    fileHandle.write(",")
    fileHandle.write(theArray[8]) # distance
    fileHandle.write("\n")
    fileHandle.flush()
  return

# -----------------------------------------------------------------------
while ((currTime) < runTime) and (leaveLoop == False):
  try:
    stringFromSparki = ser.readline().decode('ascii').strip()  
    if stringFromSparki == "DONE":
      leaveLoop = True
    else:
      processObstacle(stringFromSparki)      
  except:
    pass
  readLines += 1
  currTime = time.time() - startTime

ser.flush() #flush the buffer

print("Read {0} lines".format(readLines))
fileHandle.close()  