import numpy as np
import matplotlib.pyplot as plt

N = 64

n = np.arange(N)
F = np.exp(-2j * np.pi * np.outer(n, n) / N)

fig, ax = plt.subplots(6, 2, figsize=(6, 12), constrained_layout=True)
for m in range(3):
    ax[m, 0].stem(np.real(F[m]))
    ax[m, 1].stem(np.imag(F[m]))
    ax[5 - m, 0].stem(np.real(F[N - 1 - m]))
    ax[5 - m, 1].stem(np.real(F[N - 1 - m]))
    ax[m, 0].grid(True)
    ax[m, 1].grid(True)
    ax[m, 0].set_ylim(-1.2, 1.2)
    ax[m, 1].set_ylim(-1.2, 1.2)
    if m < N - 1:
        ax[m, 0].tick_params(labelbottom=False)
        ax[m, 1].tick_params(labelbottom=False)

plt.savefig('./imgs/1modif.svg')

FH = F.conj().T

R = FH @ F
R = R / N # scale each by 1/sqrt(N) --> in the end scale by 1/N

# check unit condition
if np.allclose(np.eye(N), R):
    print("true")
else:
    print("false")