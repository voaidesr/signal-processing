import numpy as np
import matplotlib.pyplot as plt

def rect(size: int):
    return np.ones(size)

def hanning(size: int):
    x = np.arange(size)
    return 0.5 * (1 - np.cos(2 * np.pi * x / size))

def main():
    N = 200
    fs = 2000
    x = np.arange(N) / fs
    f = 100
    sig = np.sin(2 * np.pi * f * x)

    plt.figure(figsize=(10, 10))
    plt.plot(x, sig, label="pure")
    plt.plot(x, sig * rect(N), label="rectangular")
    plt.plot(x, sig * hanning(N), label="hanning")
    plt.legend()
    plt.savefig('./imgs/5.svg')

if __name__ == "__main__":
    main()