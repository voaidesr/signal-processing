import numpy as np

def main():

    N_TESTS = 10000

    # metoda 1
    for _ in range(N_TESTS):
        x = np.random.rand(20)
        d = np.random.randint(0, 20)
        y = np.roll(x, d)

        X = np.fft.fft(x)
        Y = np.fft.fft(y)
        X = np.conj(X)

        new_d = np.argmax(np.abs(np.fft.ifft(X * Y)))

        assert d == new_d, f"Fail Method 1: found d = {new_d}, real d = {d}"

    print("All tests pass for method 1.")

    # metoda 2
    for _ in range(N_TESTS):
        x = np.random.rand(20)
        d = np.random.randint(0, 20)
        y = np.roll(x, d)

        X = np.fft.fft(x)
        Y = np.fft.fft(y)


        new_d = np.argmax(np.real(np.fft.ifft(Y / (X + 1e-10))))

        assert d == new_d, f"Fail Method 2: found d = {new_d}, real d = {d}"

    print("All tests pass for method 2.")


if __name__ == "__main__":
    main()