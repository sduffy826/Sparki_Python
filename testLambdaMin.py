import math
import random

class Node:
  def __init__(self, x, y, cost, pind):
    self.x = x  # index of grid
    self.y = y  # index of grid
    self.cost = cost
    self.pind = pind

def printNode(theNodeToPrint):
  print("x: {0} y: {1} cost: {2} pind: {3}".format(theNodeToPrint.x,theNodeToPrint.y,theNodeToPrint.cost,theNodeToPrint.pind))

dictOfObj = dict()
listOfObj = []
for i in range(5):
  aNode = Node(i,i*2,round(10 * random.random(),2),-1)
  dictOfObj[i] = aNode
  listOfObj.append(aNode)
  printNode(aNode)

print(type(dictOfObj))
print(type(listOfObj))
for theNode in listOfObj:
  printNode(theNode)

# Get the index of the record with min value
indexOfMin = min(dictOfObj, key=lambda o: dictOfObj[o].cost)
print("Getting min value based on cost, index of min: {0}".format(indexOfMin))
printNode(dictOfObj[indexOfMin])

# Get max value
indexOfMax = max(dictOfObj, key=lambda o: dictOfObj[o].cost)
print("Getting max value based on cost, the record is at {0}".format(indexOfMax))
printNode(dictOfObj[indexOfMax])