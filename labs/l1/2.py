import matplotlib.pyplot as plt
import numpy as np


fig, ax = plt.subplots(4, 2, width_ratios=[1, 2])

# (a)

x1 = np.linspace(0, 0.01, 1600)
sin_x = np.sin(800 * np.pi * x1)

ax[0,0].plot(x1, sin_x, 'black')
ax[0, 0].set_xlim(0, 0.01)

# (b)

x2 = np.linspace(0, 3, 100000)
sin_x2 = np.sin(1600 * np.pi * x2)
ax[1, 0].set_xlim(0, 0.01)
ax[1, 0].plot(x2, sin_x2, 'black')

# (c)

sawtooth = (240 * x2 - np.floor(240 * x2))
ax[2, 0].plot(x2, sawtooth, 'black')
ax[2, 0].set_xlim(0, 0.1)

# (d)

ax[3, 0].plot(x2, np.floor(np.sin(300 * np.pi * x2)), 'black')
ax[3, 0].set_xlim(0, 0.01)

# (e)

rdm_sig = np.random.rand(128, 128)

ax[0, 1].imshow(rdm_sig, cmap='grey', interpolation='none')

# (f)

def f(i, j):
    return np.sin(i * j) - i + j

proc_sig = np.fromfunction(f, (128, 128), dtype=int)
ax[1, 1].imshow(proc_sig, cmap='grey', interpolation=None)

ax[2, 1].axis('off')
ax[3, 1].axis('off')

fig.tight_layout()

plt.show()