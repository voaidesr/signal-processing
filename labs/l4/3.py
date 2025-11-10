import numpy as np
import matplotlib.pyplot as plt

# Semnale
f1, f2, f3 = 16, 11, 6
A = 1.0
phi = 0.0

x = np.linspace(0, 1, 2000, endpoint=False)

fs_alias = 5
xn_alias = np.linspace(0, 1, fs_alias, endpoint=False)

fig2, ax2 = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
ax2[0].plot(x, A*np.sin(2*np.pi*f1*x + phi))
ax2[0].stem(xn_alias, A*np.sin(2*np.pi*f1*xn_alias + phi))
ax2[0].set_title(f"f1={f1} Hz, fs={fs_alias} Hz (aliere)")

ax2[1].plot(x, A*np.sin(2*np.pi*f2*x + phi))
ax2[1].stem(xn_alias, A*np.sin(2*np.pi*f2*xn_alias + phi))
ax2[1].set_title(f"f2={f2} Hz, fs={fs_alias} Hz")

ax2[2].plot(x, A*np.sin(2*np.pi*f3*x + phi))
ax2[2].stem(xn_alias, A*np.sin(2*np.pi*f3*xn_alias + phi))
ax2[2].set_title(f"f3={f3} Hz, fs={fs_alias} Hz")
ax2[2].set_xlabel("t [s]")

fig2.tight_layout()
fig2.savefig("./imgs/2_fixed.svg")

# 3
fs_good = 40  # > 2 * f1
xn_good = np.linspace(0, 1, fs_good, endpoint=False)

fig3, ax3 = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
ax3[0].plot(x, A*np.sin(2*np.pi*f1*x + phi))
ax3[0].stem(xn_good, A*np.sin(2*np.pi*f1*xn_good + phi))
ax3[0].set_title(f"f1={f1} Hz, fs={fs_good} Hz (> 2*f1, fara aliere)")

ax3[1].plot(x, A*np.sin(2*np.pi*f2*x + phi))
ax3[1].stem(xn_good, A*np.sin(2*np.pi*f2*xn_good + phi))
ax3[1].set_title(f"f2={f2} Hz, fs={fs_good} Hz")

ax3[2].plot(x, A*np.sin(2*np.pi*f3*x + phi))
ax3[2].stem(xn_good, A*np.sin(2*np.pi*f3*xn_good + phi))
ax3[2].set_title(f"f3={f3} Hz, fs={fs_good} Hz")
ax3[2].set_xlabel("t [s]")

fig3.tight_layout()
fig3.savefig("./imgs/3.svg")
