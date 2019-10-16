import serial
import time
from datetime import datetime
import sparkiStats

useBluetooth = False
isIBMMacBook = False

outputFile   = "sparkiLog." + datetime.now().isoformat(timespec='seconds').replace("-","").replace(":","") + ".csv"

if useBluetooth == False:
  if isIBMMacBook:
    ser = serial.Serial(port='/dev/cu.usbmodem14601', baudrate=9600)
  else:
    ser = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600)

readLines = 0
runTime   = 30          # Only runs for 2 minutes
startTime = time.time()  # Returns time in seconds since epoch
ser.write(b'Trigger')    # Push something on the serial port, this will activate it

sensorList = {}

fileHandle = open(outputFile,"at") # Append and text file
currTime   = time.time() - startTime

while (currTime) < runTime:
  try:
    stringFromSparki = ser.readline().decode('ascii').strip()  
    fileHandle.write(stringFromSparki + "\n")
    print("Time: {0} SerialFromSparki: {1}".format(currTime,stringFromSparki))
    
    sparkiStats.setVars(sensorList,stringFromSparki)
  except:
    pass
  readLines += 1
  currTime = time.time() - startTime

ser.flush() #flush the buffer

print("Read {0} lines".format(readLines))

summaryList = sparkiStats.getSummary(sensorList)
for aLine in summaryList:
  fileHandle.write(aLine + "\n")

fileHandle.close()  