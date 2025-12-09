import numpy as np
import scipy
import matplotlib.pyplot as plt
from matplotlib import colors

def get_time_series(N):
    t = np.arange(N)

    a, b, c = 0.0005, 0.1, 2
    trend = a * t ** 2 + b * t + c

    f1, f2 = 1/50, 1/20
    A1, A2 = 20, 10
    seasonal = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t)

    sd = 5
    noise = np.random.normal(0, sd, size=N)

    return trend + seasonal + noise, trend, seasonal

def autocorelate(time_series):
    mean = np.mean(time_series)
    var = np.var(time_series)
    t_centered = time_series - mean
    n = len(time_series)

    correlation = np.correlate(t_centered, t_centered, mode='full')
    correlation = correlation[n-1:]
    acf = correlation / (n * var)
    return acf

def fit_ar(series, p, m):
    N = len(series)

    if N <= p + m:
        raise ValueError(f"Lungimea seriei de timp = {N} <= p + m = {p + m}")

    A = []
    b = series[N-m:N]

    for i in range(N-m, N):
        prev_values = series[i-p : i][::-1]

        row = prev_values
        A.append(row)

    A = np.array(A)

    coeffs, _, _, _ = scipy.linalg.lstsq(A, b)

    fitted_values = A @ coeffs

    return np.arange(N-m, N), fitted_values

def grid_search(series):
    N = len(series)

    p_values = range(1, 100, 2)
    m_values = range(30, 400, 10)

    best_mse = float('inf')
    best_p, best_m = -1, -1

    err_map = np.full((len(p_values), len(m_values)), np.nan)

    for i, p in enumerate(p_values):
        for j, m in enumerate(m_values):

            if m < 2 * p + 5:
                continue

            errors = []
            validation_steps = 1

            start_val_idx = N - validation_steps
            if start_val_idx - m < 0:
                continue

            for t in range(start_val_idx, N):
                train_window = series[t-m : t]

                A_train = []
                b_train = train_window[p:]

                for k in range(p, len(train_window)):
                    prev = train_window[k-p : k][::-1]
                    A_train.append(prev)

                A_train = np.array(A_train)

                try:
                    coeffs, _, _, _ = scipy.linalg.lstsq(A_train, b_train)
                except:
                    errors.append(np.nan)
                    continue

                last_known_values = train_window[-p:][::-1]
                prediction = np.dot(last_known_values, coeffs)

                actual = series[t]
                errors.append((actual - prediction) ** 2)

            if len(errors) > 0:
                mse = np.nanmean(errors)
                err_map[i, j] = mse

                if mse < best_mse:
                    best_mse = mse
                    best_p = p
                    best_m = m


    fig, ax = plt.subplots(figsize=(10, 6))

    masked_map = np.ma.masked_invalid(err_map)
    finite_errs = err_map[np.isfinite(err_map)]
    if finite_errs.size == 0:
        raise RuntimeError("Grid search produced no finite errors.")
    vmin = np.percentile(finite_errs, 5)
    vmax = np.percentile(finite_errs, 95)
    if vmin <= 0:
        vmin = finite_errs[finite_errs > 0].min()

    im = ax.imshow(
        masked_map,
        origin="lower",
        aspect="auto",
        extent=[min(m_values), max(m_values), min(p_values), max(p_values)], # type: ignore
        cmap="plasma_r",
        norm=colors.LogNorm(vmin=vmin, vmax=vmax),
    )

    if best_p > 0:
        ax.scatter(best_m, best_p, color="red", marker="x", s=100, linewidth=3, label=f"Best (p={best_p}, m={best_m})")

    ax.set_xlabel("m (window length)")
    ax.set_ylabel("p (AR order)")
    ax.set_title("One-Step-Ahead Validation MSE")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Mean Squared Error")
    ax.legend()
    fig.tight_layout()
    plt.savefig('./imgs/3.svg')

def main():
    # fig, ax = plt.subplots(2, figsize=(8, 6))
    # a
    series, t, s = get_time_series(1000)
    # ax[0].plot(series, color="black", label="time series")
    # ax[0].plot(t, label="trend")

    # acf = autocorelate(series)
    # ax[1].plot(acf, label="Autocorrelation vector")
    # ax[1].grid(True)
    # ax[1].legend()


    # p = 15
    # m = 500
    # t, fitted_values  = fit_ar(series, p, m)
    # ax[0].plot(t, fitted_values, color="red", label=rf"AR predictions $p={p}, \;\; m={m}$")

    # ax[0].legend()

    # ax[1].plot(series, color="black", label="time series")
    # ax[1].plot(t, fitted_values, color="red", label=rf"AR predictions $p={p}, \;\; m={m}$")
    # ax[1].set_xlim((800, 1000))
    # ax[1].set_title("Zoom in")
    # ax[1].legend()

    # fig.tight_layout()
    # plt.savefig('./imgs/ar.svg')

    grid_search(series)

if __name__ == "__main__":
    main()
