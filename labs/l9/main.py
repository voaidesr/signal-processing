import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def get_time_series(N):
    t = np.arange(N)

    a, b, c = 0.005, 0.1, 2
    trend = a * t**2 + b * t + c

    f1, f2 = 1 / 5, 1 / 3
    A1, A2 = 5, 3
    seasonal = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t)

    sd = 5
    noise = np.random.normal(0, sd, size=N)

    return trend + seasonal + noise, trend, seasonal


def mse(original: np.ndarray, approximated: np.ndarray) -> float:
    return np.mean((original - approximated) ** 2).astype(float)


def exponential_average(time_series: np.ndarray, alpha: float) -> np.ndarray:
    ema = np.zeros(len(time_series) - 1)
    ema[0] = time_series[0]

    for t in range(1, len(time_series) - 1):
        ema[t] = alpha * time_series[t] + (1 - alpha) * ema[t - 1]

    return ema


def optimal_alpha(original: np.ndarray) -> tuple[float, float, np.ndarray]:
    best_alpha = 0
    best_mse = float("inf")
    best_approx = np.ndarray([])

    alphas = np.linspace(0.01, 0.99, 100).astype(float)

    for alpha in alphas:
        approx = exponential_average(original, alpha)
        err = mse(original[1:], approx)

        if err < best_mse:
            best_mse = err
            best_approx = approx
            best_alpha = alpha

    return best_alpha, best_mse, best_approx

def double_ema(original: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    n = len(original)

    s = np.zeros(n)
    b = np.zeros(n)

    s[0] = original[0]
    b[0] = original[1] - original[0]
    predictions = np.zeros(n)

    predictions[0] = s[0]
    predictions[1] = s[0] + b[0]

    for t in range(1, n-1):
        s[t] = alpha * original[t] + (1 - alpha) * (s[t - 1] + b[t - 1])
        b[t] = beta * (s[t] - s[t - 1]) + (1 - beta) * b[t - 1]

        predictions[t + 1] = s[t] + b[t]

    return predictions[2:]

def optimal_alpha_beta(original: np.ndarray) -> tuple[float, float, float, np.ndarray]:
    best_alpha = 0
    best_beta = 0
    best_mse = float('inf')
    best_prediction = np.ndarray([])

    steps = np.linspace(0.01, 0.99, 40)

    for alpha in steps:
        for beta in steps:
            pred = double_ema(original, alpha, beta)

            err = mse(original[2:], pred)

            if err < best_mse:
                best_alpha = alpha
                best_beta = beta
                best_mse = err
                best_prediction = pred

    return best_alpha, best_beta, best_mse, best_prediction

def triple_ema(data: np.ndarray, alpha: float, beta: float, gamma: float, L: int) -> np.ndarray:
    n = len(data)

    s = np.zeros(n)
    b = np.zeros(n)
    c = np.zeros(n)
    predictions = np.zeros(n)

    s[L - 1] = np.mean(data[:L])
    b[L - 1] = (data[L] - data[0]) / L

    for t in range(L):
        c[t] = data[t] - s[L - 1] # deviation from the mean

    for t in range(L, n):
        predictions[t] = s[t-1] + b[t-1] + c[t-L] # c[t - 1 - L + 1 + 0 mod L]

        s[t] = alpha * (data[t] - c[t-L]) + (1 - alpha) * (s[t-1] + b[t-1])
        b[t] = beta * (s[t] - s[t-1]) + (1 - beta) * b[t-1]
        c[t] = gamma * (data[t] - s[t] - b[t-1]) + (1 - gamma) * c[t-L]

    return predictions

def optimal_al_be_ga(original: np.ndarray, L: int) -> tuple[float, float, float, np.ndarray]:

    def triple_ema_objective(params, series, L):
        alpha, beta, gamma = params

        if not (0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1):
            return float('inf')

        try:
            predictions = triple_ema(series, alpha, beta, gamma, L)
            err = np.mean((series[L:] - predictions[L:])**2)
            return err
        except Exception:
            return float('inf')

    initial_guess = [0.1, 0.1, 0.1]
    bounds = [(0, 1), (0, 1), (0, 1)]

    result = minimize(
        triple_ema_objective,
        initial_guess,
        args=(original, L),
        method='L-BFGS-B',
        bounds=bounds
    )

    al, be, ga = result.x

    predicted = triple_ema(original, al, be, ga, L)

    return al, be, ga, predicted


def ma(data: np.ndarray, p: int, theta: float) -> np.ndarray:
    n = len(data)

    rolling_mean = np.zeros(n)

    for t in range(p, n):
        rolling_mean[t] = np.mean(data[t - p : t])

    errs = np.zeros(n)
    predictions = np.zeros(n)

    for t in range(p, n):
        correction = theta * errs[t - 1]  # take the error from one step before

        predictions[t] = rolling_mean[t] + correction

        errs[t] = data[t] - predictions[t]

    return predictions


def find_optimal_ma_params(series: np.ndarray) -> tuple[int, float, float]:
    best_p = 0
    best_theta = 0
    best_mse = float("inf")

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
    N = 100
    series, trend, seasonal = get_time_series(N)
    reference = trend + seasonal

    fig, ax = plt.subplots(3, 2, figsize=(15, 8))

    alpha, err, predict = optimal_alpha(series)

    ax[0][0].plot(
        np.arange(0, N), series, label=f"Noisy series\n$\\alpha = {alpha:.2f}$"
    )
    ax[0][0].plot(np.arange(1, N), predict, label="Predicted with Exponential MA")
    ax[0][0].legend(fontsize='small')

    ax[0][1].plot(series[1:] - predict, label="Error")
    ax[0][1].legend(fontsize="small")

    alpha, beta, err, predict = optimal_alpha_beta(series)

    ax[1][0].plot(
        np.arange(0, N), series, label=f"Noisy series\n$\\alpha = {alpha:.2f}$\n$\\beta={beta:.2f}$"
    )
    ax[1][0].plot(np.arange(2, N), predict, label="Double Exponential MA")
    ax[1][0].legend(fontsize='small')

    ax[1][1].plot(series[2:] - predict, label="Error")
    ax[1][1].legend(fontsize='small')

    L = 15
    al, be, ga, predict = optimal_al_be_ga(series, L)
    ax[2][0].plot(
        np.arange(L, N), series[L:], label=f"Noisy series\n$\\alpha={alpha:.2f}$\n$\\beta={be:.2f}$\n$\\gamma={ga:.2f}$"
    )
    ax[2][0].plot(
        np.arange(L, N), predict[L:], label="Triple Exponential MA"
    )
    ax[2][0].legend(fontsize=6)
    ax[2][1].plot(
        np.arange(L, N), series[L:] - predict[L:], label="Error"
    )
    ax[2][1].legend(fontsize='small')

    plt.savefig('./imgs/2.svg')


def pt_c():
    plt.figure(figsize=(10, 6))
    N = 200
    series, trend, seasonal = get_time_series(N)

    best_p, best_theta, best_err = find_optimal_ma_params(series)
    print(f"Best Found: p={best_p}, theta={best_theta:.2f} (MSE: {best_err:.2f})")

    prediction = ma(series, p=best_p, theta=best_theta)

    plt.plot(series, label="Noisy Time Series", alpha=0.6)

    plt.plot(
        range(best_p, N),
        prediction[best_p:],
        label=f"MA Model (p={best_p}, $\\theta$={best_theta:.2f})",
        color="red",
        linewidth=2,
    )

    plt.title("Optimized Moving Average Model")
    plt.legend()
    # plt.show()
    plt.savefig("./imgs/3.svg")


if __name__ == "__main__":
    pt_b()
    # pt_c()
