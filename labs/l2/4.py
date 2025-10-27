import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 10000)

sinx = 0.5 * np.sin(2 * np.pi * 48 * x)
sawtooth = 2*(16 * x - np.floor(16 * x)) - 1

fig, ax = plt.subplots(2)

ax[0].plot(x, sinx, 'black')
ax[0].plot(x, sawtooth, 'r')

ax[1].plot(x, sinx + sawtooth)

plt.savefig('./imgs/4.svg')