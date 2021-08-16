import numpy as np
import matplotlib.pyplot as plt

cost_array = np.loadtxt('cost_array.csv', dtype=int, delimiter=',')
collision_array = np.loadtxt('collision_array.csv', dtype=int, delimiter=',')

plt.matshow(cost_array.transpose())
plt.show()