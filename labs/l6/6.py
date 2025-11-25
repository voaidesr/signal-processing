import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy


def plot_a_b():
    contents = pd.read_csv("Train.csv", parse_dates=["Datetime"], index_col="ID")
    sig = contents["Count"].to_numpy().astype(float)
    start = 5500
    three_days = 24 * 3
    sig = sig[start : start + three_days]
    t = np.arange(len(sig))

    plt.figure(figsize=(10, 8))
    plt.plot(t, sig, color="gray", alpha=0.7, ls="dashed", label="Semnalul original")

    w_list = [5, 9, 13, 17]
    for w in w_list:
        filtered = np.convolve(sig, np.ones(w), "valid") / w
        plt.plot(t[w - 1 :], filtered, label=f"w = {w}")
    plt.legend()
    plt.savefig("./imgs/6a.svg")
    plt.close()


def plot_c():
    contents = pd.read_csv("Train.csv", parse_dates=["Datetime"], index_col="ID")
    sig = contents["Count"].to_numpy().astype(float)
    start = 5500
    three_days = 24 * 3
    sig = sig[start : start + three_days]
    t = np.arange(len(sig))

    plt.figure(figsize=(10, 8))
    plt.plot(t, sig, label="Original")

    N = 5  # order
    Wn = 2 / 5  # chosen frequency fs = 1/5
    b, a = scipy.signal.butter(N, Wn, btype="low")
    sig_butter = scipy.signal.filtfilt(b, a, sig)
    plt.plot(t, sig_butter, label="Butterworth filtered")

    rp = 5
    b, a = scipy.signal.cheby1(N, rp, Wn, btype="low")
    sig_cheby = scipy.signal.filtfilt(b, a, sig)
    plt.plot(t, sig_cheby, label="Chebyshev filtered")

    plt.legend()
    plt.savefig("./imgs/6c.svg")
    plt.close()


def plot_f():
    contents = pd.read_csv("Train.csv", parse_dates=["Datetime"], index_col="ID")
    sig = contents["Count"].to_numpy().astype(float)
    start = 5500
    three_days = 24 * 3
    sig = sig[start : start + three_days]
    t = np.arange(len(sig))

    fig, ax = plt.subplots(3, figsize=(12, 9))

    for a in fig.get_axes():
        a.plot(t, sig, color="gray", ls="dashed", alpha=0.8, label="Original signal")

    ax[0].set_title("Butterworth")
    ax[1].set_title("Chebyshev with different orders")
    ax[2].set_title("Chebyshev with different ripple values")

    orders = [5, 13, 21]

    W = 2 / 5

    for o in orders:
        b_butt, a_butt = scipy.signal.butter(o, W, btype="low")
        y_butt = scipy.signal.filtfilt(b_butt, a_butt, sig)

        b_cheb, a_cheb = scipy.signal.cheby1(o, 5, W, btype="low")
        y_cheb = scipy.signal.filtfilt(b_cheb, a_cheb, sig)

        ax[0].plot(t, y_butt, label=f"Order = {o}")
        ax[1].plot(t, y_cheb, label=f"Order = {o}")

    ripples = [2, 5, 8, 11]
    for rp in ripples:
        b_cheb, a_cheb = scipy.signal.cheby1(1, rp, W, btype="low")
        y_cheb = scipy.signal.filtfilt(b_cheb, a_cheb, sig)
        ax[2].plot(t, y_cheb, label=f"rp = {rp}")

    for a in fig.get_axes():
        a.legend()

    fig.tight_layout()
    plt.savefig("./imgs/6f.svg")
    plt.close()


def main():
    plot_a_b()
    plot_c()
    plot_f()


if __name__ == "__main__":
    main()
