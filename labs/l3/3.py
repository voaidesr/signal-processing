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
X = np.zeros(N)

for m in range(N):
    s = 0.0 + 0.0j
    for n in range(N):
        s += sig[n] * np.exp(-2j * np.pi * m * n /N)
    X[m] = np.hypot(np.real(s), np.imag(s))

k = N//2 + 1
f = np.arange(k) * fs / N
mag = np.abs(X[:k]) / N

ax[0].plot(x, sig)
ax[1].stem(f, mag)
plt.savefig('./imgs/3.svg')