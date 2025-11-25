import numpy as np
import matplotlib.pyplot as plt

def main():
    fig, ax = plt.subplots(4, 2, figsize=(10,8))
    N = 200
    x = np.random.random(N)
    block = np.arange(N)
    block = (block >= 75) & (block <= 125)
    block = block.astype(float)

    for i in range(4):
        ax[i, 0].plot(x)
        ax[i, 1].plot(block)
        ax[i, 0].set_title(f"Convolution {i}")
        ax[i, 1].set_title(f"Convolution {i}")
        x = np.convolve(x, x)
        block = np.convolve(block, block)

    fig.tight_layout()
    plt.savefig('./imgs/2.svg')

if __name__ == "__main__":
    main()