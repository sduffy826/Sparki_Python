import time

startTime = time.time()
while True:
  theString = input("enter some text to send (quit) to quit: ")
  if theString == "quit":
    print("\nbye\n")
    break

  elapsed = time.time() - startTime
  print(theString + " time: {0:.2f}".format(elapsed))