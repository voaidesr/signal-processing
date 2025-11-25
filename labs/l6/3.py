from contextlib import contextmanager
import numpy as np
import matplotlib.pyplot as plt
import time

@contextmanager
def timer(message: str):
    start = time.perf_counter()

    yield

    passed = time.perf_counter() - start
    print(f"For {message}, {passed * 1000} ms have passed.")

def multiply_naive(p, q):
    length = len(p) + len(q) - 1
    result = [0] * length

    for i, valp in enumerate(p):
        for j, valq in enumerate(q):
            result[i + j] += valp * valq

    return result

def mult_conv(p, q):
    return np.convolve(p, q)

def multiply_opt(p, q):
    target_len = len(p) + len(q) - 1
    length = 2 ** np.ceil(np.log2(target_len)).astype(int)
    p_padded = np.pad(p, (0, length - len(p)))
    q_padded = np.pad(q, (0, length - len(q)))

    Y = np.fft.fft(p_padded) * np.fft.fft(q_padded)

    results_coef = np.round(np.real(np.fft.ifft(Y))).astype(int)

    return results_coef[:target_len].tolist()

def plot_times():
    min_coef = -100
    max_coef = 100

    naive_time = []
    fft_time = []
    conv_time = []

    for N in range(500, 10000, 50):
        a = np.random.randint(low=min_coef, high=max_coef, size=N)
        b = np.random.randint(low=min_coef, high=max_coef, size=N)

        # start = time.perf_counter()
        # res1 = multiply_naive(a, b)
        # time_passed = time.perf_counter() - start
        # naive_time.append(time_passed)

        start = time.perf_counter()
        res2 = multiply_opt(a, b)
        time_passed = time.perf_counter() - start
        fft_time.append(time_passed)

        start = time.perf_counter()
        res3 = mult_conv(a, b)
        time_passed = time.perf_counter() - start
        conv_time.append(time_passed)

        # assert res1 == res2, f"Failed on N = {N}, coefficients are not equal"
        assert res2 == res3.tolist(), f"Failed: multiplication with convolution doesn't work on N = {N}"

    x = np.arange(500, 10000, 50)
    # plt.plot((naive_time))
    plt.plot(x, fft_time, label="fft")
    plt.plot(x, conv_time, label="convolution")
    plt.legend()
    plt.savefig('./imgs/3.svg')


def main():
    N = 500

    min_coef = -100
    max_coef = 100

    a = np.random.randint(low=min_coef, high=max_coef, size=N)
    b = np.random.randint(low=min_coef, high=max_coef, size=N)

    with timer("Normal multiplication"):
        res1 = multiply_naive(a, b)

    with timer("Multiplication with fft"):
        res2 = multiply_opt(a, b)

    assert res1 == res2, "Failed: different results"

    plot_times()

if __name__ == "__main__":
    main()

