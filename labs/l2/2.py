import numpy as np
import matplotlib.pyplot as plt
import scipy

fig, ax = plt.subplots(2)

x = np.linspace(0, 1, 4000)

s0 = 2*np.sin(2 * np.pi * 3 * x)
s1 = 2*np.sin(2 * np.pi * 3 * x + np.pi/5)
s2 = 2*np.sin(2 * np.pi * 3 * x + 2*np.pi/5)

ax[0].plot(x, s0)
ax[0].plot(x, s1)
ax[0].plot(x, s2)

# zgomot
samples = 500
z = np.random.normal(0, 1, samples)
x2 = np.linspace(0, 1, samples)
s00 = 2*np.sin(2 * np.pi * 3 * x2)
SRN = 1

gamma = np.sqrt(np.linalg.norm(x2) ** 2 / (SRN * np.linalg.norm(z) ** 2))

noise = s00 + gamma * z

ax[1].plot(x2, noise, 'r')
ax[1].plot(x, s0, "black", alpha=0.7)

# plt.savefig('./imgs/2.svg')h
plt.show()

