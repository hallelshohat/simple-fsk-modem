import sounddevice as sd
import soundfile as sf
import numpy as np
from audio_transmitter.fsk.demodulator.fsk_demodulator import FskDemodulator
from audio_transmitter.fsk.fsk_modulator import FskModulator
from audio_transmitter.consts import samplerate


bits = "0123456789abcdef"
modulator = FskModulator()
# data = modulator.modulate_fsk(bytes.fromhex(bits))
# sd.play(data, samplerate)
# sd.wait()
# sf.write("a.wav", data, samplerate)
demod = FskDemodulator()
[data, samplerate] = sf.read("2.wav")
splitted = np.array_split(data, 500)
for arr in splitted:
    decoded = demod.demodulate_signal(arr, samplerate)
    if decoded and len(decoded) > 0:
        print(decoded.hex())