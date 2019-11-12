import matplotlib.pyplot as plt
import math

import GetPathClass

show_animation = True

def main():
  print(__file__ + " start!!")

  # start and goal position
  startX = -5.0  # [m]
  startY = -5.0  # [m]
  goalX = 50.0  # [m]
  goalY = 50.0  # [m]
  grid_size = 2.0  # [m]
  robot_radius = 5.0  # [m]

  # set obstacle positions
  obstacleX, obstacleY = [], []
  for i in range(-10, 60):
    obstacleX.append(i)
    obstacleY.append(-10.0)
  for i in range(-10, 60):
    obstacleX.append(60.0)
    obstacleY.append(i)
  for i in range(-10, 61):
    obstacleX.append(i)
    obstacleY.append(60.0)
  for i in range(-10, 61):
    obstacleX.append(-10.0)
    obstacleY.append(i)
  for i in range(-10, 40):
    obstacleX.append(20.0)
    obstacleY.append(i)

  for i in range(0, 40):
    obstacleX.append(40.0)
    obstacleY.append(60.0 - i)

  for i in range(4,10):
    obstacleX.append(i)
    obstacleY.append(15.0)
  for i in range(4, 10):
    obstacleX.append(i)
    obstacleY.append(20.0)

  if show_animation:  # pragma: no cover
    plt.plot(obstacleX, obstacleY, ".k")
    plt.plot(startX, startY, "og")
    plt.plot(goalX, goalY, "xb")
    plt.grid(True)
    plt.axis("equal")

  dijkstra = GetPathClass.DijkstraPathPlanning(obstacleX, obstacleY, grid_size, robot_radius, show_animation)
  pathReturnedX, pathReturnedY = dijkstra.getPath(startX, startY, goalX, goalY)
  print("Path len: {0}".format(len(pathReturnedY)))
  print("pathReturnedX is: ")
  print(list(pathReturnedX))
  print("pathReturnedY is: ")
  print(list(pathReturnedY))

  shortenedXPath, shortenedYPath = dijkstra.mergePointsWithSameSlope(pathReturnedX, pathReturnedY)
  print("pathXCondensed:")
  print(list(shortenedXPath))
  print("pathYCondensed:")
  print(list(shortenedYPath))
  if show_animation:  # pragma: no cover
    plt.plot(pathReturnedX, pathReturnedY, "-r")
    plt.show()


if __name__ == '__main__':
    main()
