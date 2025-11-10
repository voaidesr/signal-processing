import numpy as np
import matplotlib.pyplot as plt
import time as tm

def signal(x, *freq):
    s = np.zeros(len(x))
    for f in freq:
        s += np.sin(2 * np.pi * f * x)
    return s

def dft_mult(sig):
    N = len(sig)
    X = np.zeros(N)

    for m in range(N):
        s = 0.0 + 0.0j
        for n in range(N):
            s += sig[n] * np.exp(-2j * np.pi * m * n /N)
        X[m] = np.hypot(np.real(s), np.imag(s))

    k = N//2 + 1
    f = np.arange(k)
    mag = np.abs(X[:k]) / N

    return mag, f

def dft_matrix(sig):
    N = len(sig)

    n = np.arange(N)
    F = np.exp(-2j * np.pi * np.outer(n, n) / N)

    X = np.abs(F @ sig)


    k = N//2 + 1
    f = np.arange(k)
    mag = np.abs(X[:k]) / N

    return mag, f

def fft(sig):
    N = len(sig)

    if N == 1:
        return sig

    sig_even = fft(sig[::2])
    sig_odd  = fft(sig[1::2])

    k = np.arange(N//2)
    factor = np.exp(-2j * np.pi * k / N)

    sig = np.concatenate([sig_even + factor * sig_odd, sig_even -  factor * sig_odd])

    return sig


ks = np.arange(7, 14)
dim = [(signal(np.linspace(0, 1, 2 ** k), 19, 23, 43), np.linspace(0, 1, 2 ** k)) for k in ks]
sample_sizes = 2 ** ks

t1 = []

for i in range(len(dim)):
    t0 = tm.perf_counter()
    s, _ = dim[i]
    fft(s)
    t1.append(tm.perf_counter() - t0)

t2 = []
for i in range(len(dim)):
    t0 = tm.perf_counter()
    s, _ = dim[i]
    np.fft.fft(s)
    t2.append(tm.perf_counter() - t0)

t3 = []
for i in range(len(dim)):
    t0 = tm.perf_counter()
    s, _ = dim[i]
    dft_matrix(s)
    t3.append(tm.perf_counter() - t0)

t4 = []
for i in range(len(dim)):
    t0 = tm.perf_counter()
    s, _ = dim[i]
    dft_mult(s)
    t4.append(tm.perf_counter() - t0)

plt.plot(sample_sizes, np.log(t1), 'r', label='Recursive FFT')
plt.plot(sample_sizes, np.log(t2), 'k', label='NumPy FFT')
plt.plot(sample_sizes, np.log(t3), 'b', label='Matrix DFT')
plt.plot(sample_sizes, np.log(t4), 'g', label='Nested-loop DFT')
plt.xlabel('Signal length (samples)')
plt.ylabel('log runtime (s)')
plt.title('Runtime comparison for Fourier implementations')
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
plt.tight_layout()
plt.savefig('./imgs/1.svg')
