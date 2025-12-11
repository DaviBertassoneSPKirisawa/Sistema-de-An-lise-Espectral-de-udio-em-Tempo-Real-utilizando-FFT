import queue
import sys
import numpy as np
import sounddevice as sd
from scipy.signal import windows
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# utilitário: próxima potência de 2 >= n
def next_pow2(n: int) -> int:
    if n <= 1:
        return 1
    return 1 << ((n - 1).bit_length())

# ---------- Configurações (altere aqui se precisar) ----------
SR = 48000              # taxa de amostragem desejada (Hz)
BLOCK_DURATION = 0.05   # duração de cada bloco em segundos (latência)
CHANNELS = 1            # mono
DEVICE = 12             # id do dispositivo (ou None)
WINDOW = 'hann'         # janela: 'hann' ou 'hamming' etc.
SMOOTHING = 0.6         # suavização temporal (0..0.99)
DEFAULT_FFT = 4096      # FFT padrão sugerida (pode ajustar)
# -------------------------------------------------------------

# Derived (sempre calcular AFTER definir SR e BLOCK_DURATION)
BLOCKSIZE = int(SR * BLOCK_DURATION)

# Garantir FFT_SIZE como potência de 2 >= BLOCKSIZE (e >= DEFAULT_FFT)
FFT_SIZE = max(DEFAULT_FFT, next_pow2(BLOCKSIZE))

# HOP_SIZE com overlap de 50% (melhora suavidade visual)
HOP_SIZE = BLOCKSIZE // 2

# fila limitada para robustez
q = queue.Queue(maxsize=20)
stream = None


def audio_callback(indata, frames, time_info, status):
    """Callback chamado pelo sounddevice para cada bloco de áudio."""
    if status:
        # status pode reportar under/overflows; só logamos
        print(f"Status: {status}", file=sys.stderr)
    # indata shape: (frames, channels)
    if CHANNELS == 1:
        data = indata[:, 0].copy()
    else:
        data = np.mean(indata, axis=1)  # mixdown estéreo para mono
    # push para fila não bloquear callback
    try:
        q.put_nowait(data)
    except queue.Full:
        pass

def get_window(winname, N):
    if winname == 'hann':
        return windows.hann(N, sym=False)
    elif winname == 'hamming':
        return windows.hamming(N, sym=False)
    else:
        return np.ones(N)

# estado para suavização
prev_mag = None

def process_block(accum):
    """Recebe blocos acumulados e calcula FFT (retorna magnitudes e freq axis)."""
    global prev_mag
    # aplicamos janela e zero-pad para FFT_SIZE se necessário
    win = get_window(WINDOW, len(accum))
    x = accum * win
    # zero-pad ou trunc
    if len(x) < FFT_SIZE:
        x = np.concatenate((x, np.zeros(FFT_SIZE - len(x))))
    else:
        x = x[:FFT_SIZE]
    # FFT
    X = np.fft.rfft(x)
    mag = np.abs(X)
    # converte para dB opcionalmente: mag_db = 20*np.log10(mag+1e-10)
    # suavização exponencial
    if prev_mag is None:
        smoothed = mag
    else:
        smoothed = SMOOTHING * prev_mag + (1 - SMOOTHING) * mag
    prev_mag = smoothed
    # freq axis
    freqs = np.fft.rfftfreq(FFT_SIZE, d=1.0/SR)
    return freqs, smoothed

def main():
    global stream
    print("Iniciando captura. Pressione Ctrl+C para sair.")
    print(f"Config: SR={SR}, block={BLOCK_DURATION}s ({BLOCKSIZE} samples), FFT_SIZE={FFT_SIZE}")
    # Configura figura matplotlib
    plt.style.use('classic')
    fig, ax = plt.subplots(figsize=(10,4))
    line, = ax.plot([], [], lw=1)
    ax.set_xlim(0, SR/2)
    ax.set_xlabel('Frequência (Hz)')
    ax.set_ylabel('Magnitude')
    ax.set_title('Espectro em tempo real')
    text_peak = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    # inicia stream
    try:
        stream = sd.InputStream(samplerate=SR, blocksize=BLOCKSIZE, device=DEVICE,
                                channels=CHANNELS, callback=audio_callback)
        stream.start()
    except Exception as e:
        print("Erro ao abrir stream de áudio:", e)
        return

    # buffer circular para acumular até FFT_SIZE
    buffer = np.zeros(0, dtype='float32')

    def update(frame):
        nonlocal buffer
        # consome tudo da fila
        got_any = False
        while not q.empty():
            data = q.get_nowait()
            buffer = np.concatenate((buffer, data))
            got_any = True
        if len(buffer) >= BLOCKSIZE:
            # processamos em blocos de HOP_SIZE (aqui HOP_SIZE=BLOCKSIZE)
            # mas para freq melhor podemos processar FFT_SIZE com overlap; mantemos simples
            # pegamos os últimos FFT_SIZE samples (se disponíveis) para calcular a FFT
            if len(buffer) >= FFT_SIZE:
                window_data = buffer[-FFT_SIZE:]
            else:
                # se não temos FFT_SIZE ainda, zero-pad
                window_data = np.concatenate((np.zeros(FFT_SIZE - len(buffer)), buffer))
            freqs, mag = process_block(window_data)
            line.set_data(freqs, mag)
            ax.set_ylim(0, np.max(mag)*1.05 + 1e-6)
            # frequência dominante:
            peak_idx = np.argmax(mag)
            peak_freq = freqs[peak_idx]
            text_peak.set_text(f'Freq. dominante: {peak_freq:.1f} Hz')
            # para controle de consumo do buffer (manter tamanho razoável)
            # removemos os samples já muito antigos (mantemos últimos FFT_SIZE)
            if len(buffer) > FFT_SIZE * 4:
                buffer = buffer[-FFT_SIZE*4:]
        return line, text_peak

    ani = animation.FuncAnimation(fig, update, interval=int(BLOCK_DURATION*1000), blit=False)
    try:
        plt.show()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
    finally:
        print("Parando stream...")
        if stream:
            stream.stop()
            stream.close()

if __name__ == "__main__":
    main()
