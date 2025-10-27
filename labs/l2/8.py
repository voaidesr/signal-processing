import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(- np.pi /2, np.pi /2 , 2000)

sinx = np.sin(x)

fig, ax = plt.subplots(2, 2, figsize=(10, 10))

ax[0, 0].plot(x, sinx, label = '$\sin(x)$')
ax[0, 0].plot(x, x, label = '$x$')
ax[0, 0].plot(x, np.abs(sinx - x), label = '$\epsilon = |\sin(x) - x|$', color='r')
ax[0,0].legend()
ax[0, 0].set_title('$\sin(x)$ vs $x$')


ax[0, 1].plot(x, sinx, label = '$\sin(x)$')
ax[0, 1].plot(x, x, label = '$x$')
ax[0, 1].plot(x, np.abs(sinx - x), label = '$\epsilon = |\sin(x) - x|$', color='r')
ax[0, 1].legend()
ax[0, 1].set_yscale('log')
ax[0, 1].set_title('$\sin(x)$ vs $x$, logarithmic scale')

pade = (x - 7 * x ** 3 / 60) / (1 + x ** 2 / 20)
ax[1, 0].plot(x, sinx, label='$\sin(x)$')
ax[1, 0].plot(x, pade, label=r'$\frac{x - \frac{7x^3}{60}}{1 + \frac{x^2}{20}}$')
ax[1, 0].plot(x, np.abs(sinx - pade), label='error', color='r')
ax[1, 0].legend()
ax[1, 0].set_title('$\sin(x)$ vs pade')


ax[1, 1].plot(x, sinx, label='$\sin(x)$')
ax[1, 1].plot(x, pade, label=r'$\frac{x - \frac{7x^3}{60}}{1 + \frac{x^2}{20}}$')
ax[1, 1].plot(x, np.abs(sinx - pade), label='error', color='r')
ax[1, 1].set_yscale('log')
ax[1, 1].legend()
ax[1, 1].set_title('$\sin(x)$ vs pade')


ax[0, 1].grid(True)
ax[0, 0].grid(True)
ax[1, 0].grid(True)
ax[1, 1].grid(True)
plt.savefig('./imgs/8.svg')