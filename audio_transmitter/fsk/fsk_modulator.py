import numpy as np
from audio_transmitter.audio.audio_generator import AudioGenerator
from audio_transmitter.audio.signal_processing import to_symbols
from audio_transmitter.consts import fsk_tones, sym_duration, samplerate, preamble


class FskModulator:
    def modulate_fsk(self, bits: bytes):
        data = np.array([])
        audio_generator = AudioGenerator()
        symbols = to_symbols(preamble + bits)
        for symbol in symbols:
            carrier = fsk_tones[symbol]
            data = np.concatenate(
                (data, audio_generator.generate_tone(carrier, sym_duration, samplerate))
            )

        return data
