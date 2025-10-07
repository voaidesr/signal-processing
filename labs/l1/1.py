import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 0.03, int(np.floor(0.03/0.0005)))

cos_x = np.cos(520 * np.pi * x + np.pi / 3)
cos_y = np.cos(280 * np.pi * x - np.pi/3)
cos_z = np.cos(120 * np.pi * x + np.pi /3)

fig, ax = plt.subplots(3)
ax[0].plot(x, cos_x, 'b')
ax[1].plot(x, cos_y, 'b')
ax[2].plot(x, cos_z, 'b')

# sampling
freq = 200
xn = np.arange(0, 0.03, 1 / freq)


cos_xn = np.cos(520 * np.pi * xn + np.pi / 3)
cos_yn = np.cos(280 * np.pi * xn - np.pi/3)
cos_zn = np.cos(120 * np.pi * xn + np.pi /3)

ax[0].stem(xn, cos_xn, 'r')
ax[1].stem(xn, cos_yn, 'r')
ax[2].stem(xn, cos_zn, 'r')

plt.show()