import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

fs = 1000
t = np.arange(0, 1, 1/fs)

xn = np.sin(2 * np.pi * 6 * t)
yn = xn * np.exp(-2j * np.pi * t)
x1 = np.real(yn)
y1 = np.imag(yn)
d1 = np.hypot(np.real(yn), np.imag(yn))

zn1 = xn * np.exp(-2j * np.pi * 2 * t)
x2 = np.real(zn1)
y2 = np.imag(zn1)

zn2 = xn * np.exp(-2j * np.pi * 4 * t)
x3 = np.real(zn2)
y3 = np.imag(zn2)

zn3 = xn * np.exp(-2j * np.pi * 6 * t)
x4 = np.real(zn3)
y4 = np.imag(zn3)

zn4 = xn * np.exp(-2j * np.pi * 8 * t)
x5 = np.real(zn4)
y5 = np.imag(zn4)

fig, ax = plt.subplots(2, figsize=(9, 16))

for a in fig.get_axes():
    a.set_aspect('equal')
    a.set_xlim(-1, 1)
    a.set_ylim(-1, 1)
    a.axhline(0, color='k', linewidth=1)
    a.axvline(0, color='k', linewidth=1)

(line1, ) = ax[0].plot([], [])
(dot1,)  = ax[0].plot([], [], 'o', ms=6)
(line2, ) = ax[1].plot([], [])
(line3, ) = ax[1].plot([], [])
(line4, ) = ax[1].plot([], [])
(line5, ) = ax[1].plot([], [])

def update(i):
    line1.set_data(x1[:i], y1[:i])
    dot1.set_data([x1[i-1]], [y1[i-1]])
    line2.set_data(x2[:i], y2[:i])
    line3.set_data(x3[:i], y3[:i])
    line4.set_data(x4[:i], y4[:i])
    line5.set_data(x5[:i], y5[:i])
    return line1, dot1, line2, line3, line4, line5

ani = FuncAnimation(fig, update, frames=len(t), interval=5, blit=True)
ani.save('./imgs/2.gif', writer='ffmpeg', fps=30)
