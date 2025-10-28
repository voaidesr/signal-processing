import numpy as np
import matplotlib.pyplot as plt
from helpers import colored_line_between_pts

fs = 1000
t = np.arange(0, 1, 1/fs)

fig, ax = plt.subplots(2, figsize=(6,8))
for a in fig.get_axes():
    a.set_aspect('equal')
    a.set_xlabel('Real')
    a.set_ylabel('Imaginar')
    a.axhline(0, color='k', linewidth=1)
    a.axvline(0, color='k', linewidth=1)
    a.set_xlim(-1, 1)
    a.set_ylim(-1, 1)

xn = np.sin(2 * np.pi * 6 * t)
yn = xn * np.exp(-2j * np.pi * t)
d1 = np.hypot(np.real(yn), np.imag(yn))
line1 = colored_line_between_pts(np.real(yn), np.imag(yn), d1, ax[0], linewidth=1)
fig.colorbar(line1, ax=ax[0])
fig.colorbar(line1, ax=ax[1])

# ax[0].plot(np.real(yn), np.imag(yn))

for o in [2, 4, 6, 8]:
    zn = xn * np.exp(-2j * np.pi * o * t)
    d = np.hypot(np.real(zn), np.imag(zn))
    colored_line_between_pts(np.real(zn), np.imag(zn), d, ax[1])

plt.savefig('./imgs/2.svg')