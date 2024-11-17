import numpy as np
from audio_transmitter.audio.audio_generator import AudioGenerator
from audio_transmitter.audio.signal_processing import to_symbols
from audio_transmitter.consts import (
    fsk_tones,
    sym_duration,
    samplerate,
    preamble,
    sym_rate,
)


# Class for FSK modulation, takes data, wraps it with preamble and returns modulated audio.
class FskModulator:
    def modulate_fsk(self, bits: bytes):
        data = np.array([])
        audio_generator = AudioGenerator()

        # transform bytes into symbols
        symbols = to_symbols(preamble + bits)
        
        # the first last symbol is repeated 0.25s for better reception
        symbols = (
            [symbols[0]] * int(sym_rate / 4)
            + symbols
            + [symbols[-1]] * int(sym_rate / 4)
        )
        for symbol in symbols:
            carrier = fsk_tones[symbol]
            # create frequency audio for each symbol and concat it together.
            data = np.concatenate(
                (data, audio_generator.generate_tone(carrier, sym_duration, samplerate))
            )

        return data
