
import numpy as np
import matplotlib.pyplot as plt

def signal(x, *freq):
    s = np.zeros(len(x))
    for f in freq:
        s += np.sin(2 * np.pi * f * x)
    return s

fig, ax = plt.subplots(1, 2, figsize=(16, 9))

fs = 200
x = np.arange(0, 1, 1/fs)

sig = signal(x, 10, 30, 40, 50, 60, 65, 90)

N = len(sig)

n = np.arange(N)
F = np.exp(-2j * np.pi * np.outer(n, n) / N)

X = np.abs(F @ sig)


k = N//2 + 1
f = np.arange(k) * fs / N
mag = np.abs(X[:k]) / N

ax[0].plot(x, sig)
ax[1].stem(f, mag)
plt.savefig('./imgs/3matrix.svg')