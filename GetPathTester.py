import matplotlib.pyplot as plt
import math

import SparkiPath
show_animation = True

def main():
    print(__file__ + " start!!")

    # start and goal position
    sx = -5.0  # [m]
    sy = -5.0  # [m]
    gx = 50.0  # [m]
    gy = 50.0  # [m]
    grid_size = 2.0  # [m]
    robot_radius = 5.0  # [m]

    # set obstacle positions
    ox, oy = [], []
    for i in range(-10, 60):
        ox.append(i)
        oy.append(-10.0)
    for i in range(-10, 60):
        ox.append(60.0)
        oy.append(i)
    for i in range(-10, 61):
        ox.append(i)
        oy.append(60.0)
    for i in range(-10, 61):
        ox.append(-10.0)
        oy.append(i)
    for i in range(-10, 40):
        ox.append(20.0)
        oy.append(i)

    for i in range(0, 40):
        ox.append(40.0)
        oy.append(60.0 - i)

    for i in range(4,10):
        ox.append(i)
        oy.append(15.0)
    for i in range(4, 10):
        ox.append(i)
        oy.append(20.0)

    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    dijkstra = SparkiPath.DijkstraPathPlanning(ox, oy, grid_size, robot_radius)
    rx, ry = dijkstra.getPath(sx, sy, gx, gy)
    print("Path len: {0}".format(len(ry)))
    print("rx is: ")
    print(list(rx))
    print("ry is: ")
    print(list(ry))
    if show_animation:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.show()


if __name__ == '__main__':
    main()
