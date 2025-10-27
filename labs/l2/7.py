import matplotlib.pyplot as plt
import numpy as np

fs = 1000
x = np.linspace(0, 10, fs)
sinx = np.sin(4 *x)

x1 = x[::4]
sinx1 = np.sin(4 * x1)

x2 = x[1::4]
sinx2 = np.sin(4 *x2)

plt.plot(x1, sinx1)
plt.plot(x2, sinx2)
plt.plot(x, sinx)
plt.savefig('./imgs/7.svg')