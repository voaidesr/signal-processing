import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fft_plot(sig, fs):
    N = len(sig)
    fq = np.fft.fft(sig)
    fq = abs(fq / N)
    fq = fq[:N//2]
    f = fs * np.linspace(0, N/2, N//2)/N
    plt.plot(f, (fq))
    plt.savefig('./imgs/d.svg')

def eliminate_dc(sig, fs):
    N = len(sig)
    sig = sig - np.mean(sig)
    fq = np.fft.fft(sig)
    f = np.fft.fftfreq(N, 1/fs)
    fq = abs(fq/N)

    fq = fq[:N//2]
    f = f[:N//2]
    return fq, f

def get_freq(sig, fs):
    N = len(sig)
    sig = sig - np.mean(sig)

    fq = np.fft.fft(sig)
    f = np.fft.fftfreq(N, 1/fs)
    f = f[:N//2]

    fq_mag = np.abs(fq / N)
    fq_mag = fq_mag[:N//2]

    sorted_ind = np.argsort(fq_mag)
    top4 = sorted_ind[-4:]

    ts = np.sort((f[top4]))
    print("Main frequencies:")
    for i  in range(len(ts)):
        print(f"\t- f{i+1} = {ts[i]} Hz, T = {1/(ts[i] * 3600)} h")

    return

def show_month(sig, fs, contents, path='./imgs/f.svg'):
    start_idx = None
    month_h = 30 * 24

    temp = contents.reset_index()

    for i in range(1000, len(temp)):
        if temp.loc[i, "Datetime"].dayofweek == 0:
            start_idx = i
            break

    if start_idx is None:
        raise ValueError("Couldn't find a Monday after the first 1000 samples.")

    end_idx = start_idx + month_h
    subset = temp.iloc[start_idx:end_idx]
    sig_subset = subset["Count"].to_numpy()
    dates = subset["Datetime"]
    plt.figure(figsize=(10, 6))
    plt.plot(dates, sig_subset)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    plt.xticks(rotation=45)
    plt.title(f"Trafic pe o lună (Start: {subset.iloc[0]['Datetime']})")
    plt.xlabel("Data calendaristică")
    plt.ylabel("Nr Mașini")
    plt.grid(True)
    plt.savefig(path)

def low_pass_filter(sig, fs):
    N = len(sig)
    X = np.fft.fft(sig)
    freqs = np.fft.fftfreq(N, 1/fs)

    cutoff_freq = 1 / (12 * 3600)

    mask = np.abs(freqs) < cutoff_freq
    X_filtered = X * mask / N

    sig_filtered = np.fft.ifft(X_filtered)

    return np.real(sig_filtered)

if __name__ == "__main__":
    fs = 1 / 3600
    contents = pd.read_csv("Train.csv", parse_dates=["Datetime"], index_col=["ID"])
    sig = contents["Count"].to_numpy().astype(np.float64)

    # ---- d
    # fft_plot(sig, fs)

    # ---- e

    # s, x = eliminate_dc(sig, fs)
    # print(s[0])
    # plt.plot(x, s)
    # plt.savefig('./imgs/e.svg')

    # ---- f
    # get_freq(sig, fs)

    # ---- g
    # show_month(sig, fs, contents)

    # ---- i
    sig = sig[:1001]
    filter = low_pass_filter(sig, fs)
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    axes[0].plot(sig, label="Semnal original")
    axes[0].set_ylabel("Număr mașini")
    axes[0].set_title("Semnal inițial")
    axes[0].legend()

    axes[1].plot(filter, label="Semnal filtrat")
    axes[1].set_xlabel("Eșantion")
    axes[1].set_ylabel("Număr mașini")
    axes[1].set_title("Semnal după filtrare")
    axes[1].legend()

    for axis in axes:
        axis.set_xlim(0, 1000)

    fig.tight_layout()
    plt.savefig('./imgs/i.svg')
