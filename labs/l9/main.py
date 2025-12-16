import sys
import os
import numpy as np
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from l8 import ar

def exponential_average(time_series: np.ndarray, alpha: float) -> np.ndarray:
    ema = np.zeros(len(time_series))
    ema[0] = time_series[0]

    for t in range(1, len(time_series)):
        ema[t] = alpha * time_series[t] + (1 - alpha) * ema[t-1]

    return ema

def mse(original: np.ndarray, approximated: np.ndarray) -> float:
    return np.mean((original - approximated) ** 2).astype(float)

def find_optimal_alpha(time_series: np.ndarray, reference: np.ndarray, depth: int = 1) -> tuple[float, float, np.ndarray]:
    best_alpha = 0
    best_mse = float('inf')
    best_approx = None

    alphas = np.linspace(0.01, 0.99, 100)
    for alpha in alphas:
        s1 = exponential_average(time_series, alpha)
        approx = s1
        if depth >= 2:
            s2 = exponential_average(s1, alpha)
            approx = 2 * s1 - s2

        if depth >= 3:
            s3 = exponential_average(s2, alpha)
            approx = 3 * s1 - 3 * s2 + s3

        valid_ref = reference[20:]
        valid_approx = approx[20:]

        err = mse(valid_ref, valid_approx)

        if err < best_mse:
            best_mse = err
            best_approx = approx
            best_alpha = alpha

    return best_alpha, best_mse, best_approx # type: ignore

def ma(data: np.ndarray, p: int, theta: float) -> np.ndarray:
    n = len(data)

    rolling_mean = np.zeros(n)

    for t in range(p, n):
        rolling_mean[t] = np.mean(data[t-p:t])

    errs = np.zeros(n)
    predictions = np.zeros(n)

    for t in range(p, n):
        correction = theta * errs[t-1] # take the error from one step before

        predictions[t] = rolling_mean[t] + correction

        errs[t] = data[t] - predictions[t]

    return predictions


def find_optimal_ma_params(series: np.ndarray) -> tuple[int, float, float]:
    best_p = 0
    best_theta = 0
    best_mse = float('inf')

    p_values = range(1, 31)
    theta_values = np.linspace(0, 1, 20)

    for p in p_values:
        for theta in theta_values:
            pred = ma(series, p, theta)

            valid_pred = pred[p:]
            valid_actual = series[p:]

            error = mse(valid_actual, valid_pred)

            if error < best_mse:
                best_mse = error
                best_p = p
                best_theta = theta

    return best_p, best_theta, best_mse

## solutions
def pt_b():
    plt.figure(figsize=(10,6))
    N = 200
    series, trend, seasonal = ar.get_time_series(N)
    reference = trend + seasonal

    alpha1, mse1, approx1 = find_optimal_alpha(series, reference, depth=1)
    alpha2, mse2, approx2 = find_optimal_alpha(series, reference, depth=2)
    alpha3, mse3, approx3 = find_optimal_alpha(series, reference, depth=3)
    ema = exponential_average(series, alpha=0.6)
    plt.plot(np.arange(N), reference, label="time series with no noise")
    plt.plot(np.arange(N), approx1, label=rf"ema, $\alpha = {alpha1}, mse = {mse1}$")
    plt.plot(np.arange(N), approx2, label=rf"double ema, $\alpha = {alpha2}, mse = {mse2} $")
    plt.plot(np.arange(N), approx3, label=rf"triple ema, $\alpha = {alpha3}$, mse = {mse3}")
    plt.legend()
    plt.savefig('./imgs/b.svg')
    plt.show()
    plt.close()


def pt_c():
    plt.figure(figsize=(10,6))
    N = 200
    series, trend, seasonal = ar.get_time_series(N)

    best_p, best_theta, best_err = find_optimal_ma_params(series)
    print(f"Best Found: p={best_p}, theta={best_theta:.2f} (MSE: {best_err:.2f})")

    prediction = ma(series, p=best_p, theta=best_theta)

    plt.plot(series, label="Noisy Time Series", alpha=0.6)

    plt.plot(range(best_p, N), prediction[best_p:],
             label=f"MA Model (p={best_p}, $\\theta$={best_theta:.2f})",
             color='red', linewidth=2)

    plt.title("Optimized Moving Average Model")
    plt.legend()
    # plt.show()
    plt.savefig('./imgs/3.svg')

if __name__ == "__main__":
    # pt_b()
    pt_c()