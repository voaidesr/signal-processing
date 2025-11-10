import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def spectrogram_by_spec(task_wav_path):
    sr, x = wavfile.read(task_wav_path)
    if x.ndim == 2:
        x = x.mean(axis=1)

    N = len(x)
    L = max(2, int(0.01 * N)) # len of frames
    if L % 2 == 1:
        L += 1
    hop = L // 2
    n_frames = 1 + int(np.ceil((N - L) / hop)) if N > L else 1

    win = np.hanning(L) # hanning window
    n_bins = L // 2 + 1
    S = np.empty((n_bins, n_frames))

    for i in range(n_frames):
        start = i * hop
        seg = x[start:start + L]
        if len(seg) < L:
            seg = np.pad(seg, (0, L - len(seg)))
        X = np.fft.rfft(seg * win, n=L)
        S[:, i] = np.abs(X)

    t_max = (n_frames - 1) * hop / sr
    f_max = sr / 2
    plt.figure(figsize=(9, 4))
    plt.imshow(
        20 * np.log10(S + 1e-12),
        origin='lower', aspect='auto',
        extent=(0.0, float(t_max), 0.0, float(f_max)),
        cmap='plasma'
    )
    plt.xlabel('timp [s]')
    plt.ylabel('frecventa [Hz]')
    plt.title('Spectograma')
    plt.colorbar(label='amplitudine [dB]')
    plt.tight_layout()
    plt.savefig('./imgs/5.svg')

if __name__ == "__main__":
    spectrogram_by_spec("1.wav")