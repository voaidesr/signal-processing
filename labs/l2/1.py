import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2)

x = np.linspace(0, 1, 4000)
sin_x = 2*np.sin(2 * np.pi * 3 * x + np.pi/8)
cos_x = 2*np.cos(2 * np.pi * 3 * x + np.pi/8 - np.pi/2)

ax[0].plot(x, sin_x)
ax[1].plot(x, cos_x)

plt.savefig('./imgs/1.svg')
# plt.show()