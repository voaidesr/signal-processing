import matplotlib.pyplot as plt
import numpy as np
import sounddevice

x1 = np.linspace(0, 10, 44100 * 10)
sin_x = np.sin(100 * np.pi * x1)


# (b)

sin_x2 = np.sin(1200 * np.pi * x1)

# (c)

sawtooth = (240 * x1 - np.floor(240 * x1))

# (d)
box = np.floor(np.sin(300 * np.pi * x1))

c = np.sin(4 * 261.63 * np.pi * x1)
e = np.sin(4 * 329.63 * np.pi * x1)
g = np.sin(4 * 392.0 * np.pi * x1)

chord = c + e + g
chord /= np.max(np.abs(chord))

fs = 44100

sounddevice.play(chord, fs)

sounddevice.wait()