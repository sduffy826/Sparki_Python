import numpy as np

# Create array with 3 zeros, the zeros are floating point 0
zeros = np.zeros(3)
print(type(zeros))
print(list(zeros))

print(zeros.shape)
zeros.shape = (3,1)  # What is this
print(zeros.shape)

# may need to change shape, said many times you do

ones = np.ones(10)  # fill with 1.0's

empty = np.empty(3)  # Creates empty array

# np.linspace(start, endpoint, numberOfElementsYouwant)  fills with numerOfelements from start to endpoint
filledWithRange = np.linspace(5,10,5)
print("filledwithRange")
for aValue in filledWithRange:
  print(aValue)

print("len of array")
createFromPythonArray = np.array([10,20])  
print(len(createFromPythonArray))
for aValue in createFromPythonArray:
  print("value of createFromPythonArray: {0}".format(aValue))

python2D = [[1,2,3,4],[9,8,7,6]]
twoDimensional = np.array(python2D)
print("Two dimensional, shape: {0}".format(np.shape(twoDimensional)))
for row in twoDimensional:
  for col in row:
    print("Col value {0}".format(col))
  print(" ")


randArray = np.random.randint(10, size=6)  # Don't think it includes the last (10) value 
print("randArray below")
print(list(randArray))

print(list(randArray[2:4])) # gives range (doesnt include top value)

print("last element")
print(randArray[-1])

aArray = np.array([1,2,3,4])
bArray = np.array([9,8,7,-1])
print(list(aArray))
print(list(bArray))
addedArray = aArray + bArray
print(list(addedArray))

multArray = aArray * bArray
print(list(multArray))

print(np.shape(multArray))
multArray.shape = (4,1)
print(np.shape(multArray))
print("original")
for aVar in multArray:
  print(aVar)
newArray = multArray.T 
print(np.shape(newArray))
print("transposed")
for bVar in newArray:
  print(bVar)

print("Minimum")
array1 = np.array([110,12,13,44,25,20])
array2 = np.array([109,11,13,43,27,21])
print(np.min(array1))
print(array2.min())  # another way to get it
print("Mins between")
print(min(np.min(array1),np.min(array2)))

# Test append
testArray = np.array([3,4,5])
print(list(testArray))



