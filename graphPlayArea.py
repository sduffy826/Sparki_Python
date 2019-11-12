
import math
import numpy as np
import matplotlib.pyplot as plt

oy = np.array([1,2,3,4])
ox = np.array([8,7,6,5])


plt.figure(1, figsize=(10,4))
plt.subplot(121)
plt.xlabel('x-label')
plt.ylabel('y-label')
plt.title('foo oo coo')
plt.plot([ox, np.zeros(np.size(oy))], [oy, np.zeros(np.size(oy))], color="green", linestyle="dashed", linewidth=2, marker="o", markersize=7)
#plt.plot(ox, oy, "ro-")
plt.axis("equal")
plt.plot(0.0, 0.0, "ob")
plt.gca().set_aspect("equal", "box")
bottom, top = plt.ylim()  # return the current ylim
plt.ylim((top, bottom)) # rescale y axis, to match the grid orientation
plt.grid(True)
plt.gca().invert_yaxis()
plt.show()
