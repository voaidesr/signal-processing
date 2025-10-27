import matplotlib.pyplot as plt
import numpy as np

fs = 50
x = np.linspace(0,0.05, fs)

s0 = np.sin(2 * np.pi * fs/2 * x)
s1 = np.sin(2 * np.pi * fs/4 * x)
s2 = np.sin(2 * np.pi * 0 * x)

plt.plot(x, s0, 'r')
plt.plot(x, s1)
plt.plot(x, s2)

# plt.show()
plt.savefig('./imgs/6.svg')