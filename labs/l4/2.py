import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(3)

fs = 5

x = np.linspace(0, 1, 1000)
xn = np.linspace(0, 1, fs, endpoint=False) # sample

f1 = 16
f2 = 11
f3 = 6


ax[0].plot(x, np.sin(2 * np.pi * f1 * x))
ax[0].stem(xn, np.sin(2 * np.pi * f1 * xn))

ax[1].plot(x, np.sin(2 * np.pi * f2 * x))
ax[1].stem(xn, np.sin(2 * np.pi * f1 * xn))

ax[2].plot(x, np.sin(2 * np.pi * f3 * x))
ax[2].stem(xn, np.sin(2 * np.pi * f1 * xn))

ax[0].plot(x, np.sin(2 * np.pi * x))

plt.show()