import numpy as np
import sounddevice as sd

def note(freq):
    global quarter
    return np.sin(2 * np.pi * freq * quarter)

fs = 44100
quarter = np.linspace(0, 0.3, int(np.round(fs * 0.3)))

e = note(329.63)
f = note(349.23)
g = note(392.00)
d = note(293.66)
c = note(261.63)

meledy = [e, f, g, g, f, e, d]

arr = e

for n in meledy:
    arr = np.concatenate((arr, n))

sd.play(arr, fs)
sd.wait()