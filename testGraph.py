import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

x = [1, 2, 3, 4, 5, 6]
y = [1.2, 1.2, 2.1, 2.1, -4.1, -4.1]

plt.plot(x, y, 'm--')

pair_x_array = np.reshape(x, (-1, 2))
print(list(pair_x_array))
pair_y_array = np.reshape(y, (-1, 2))
print(list(pair_y_array))
print("Entering loop")
for i, pair_x in enumerate(pair_x_array):
    pair_y = pair_y_array[i]
    print(list(pair_x))
    print(list(pair_y))
    plt.plot(pair_x, pair_y, 'm', linewidth=3)

plt.show()