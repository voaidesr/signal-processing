import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

def main():
    fig, ax = plt.subplots(2, 2, figsize=(10, 5))
    B = 1

    x = np.linspace(-3, 3, 3000)
    sinc = np.sinc(B * x) ** 2

    xn1 = np.arange(-3, 3, 1/1)
    xn2 = np.arange(-3, 3, 1/1.5)
    xn3 = np.arange(-3, 3, 1/2)
    xn4 = np.arange(-3, 3, 1/4)

    samples = [xn1, xn2, xn3, xn4]
    samples[1] += 0.33
    sample_t = [1, 1.5, 2, 4]

    axes = fig.get_axes()
    for i, ax in enumerate(axes):
        ax.plot(x, sinc, label="Continuu")
        ax.stem(samples[i], np.sinc(samples[i] * B) ** 2, linefmt='orange', markerfmt='o', label="Eșantioane")

        xn = samples[i]
        ts = 1 / sample_t[i]

        sinc_mat = np.sinc((x[:, np.newaxis] - xn[np.newaxis, :]) / ts)
        reconstrc = np.dot(sinc_mat, np.sinc(xn * B) ** 2)
        ax.plot(x, reconstrc, 'g--', label="Reconstruit")
        ax.set_title(f"T_s = {ts:.2f}")
        ax.set_xlabel("t")
        ax.set_ylabel("Amplitude")
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend()

    fig.suptitle("Reconstrucția sinc^2 pentru diferite perioade de eșantionare")
    fig.tight_layout()
    plt.savefig('./imgs/1.svg')

if __name__ == "__main__":
    main()
