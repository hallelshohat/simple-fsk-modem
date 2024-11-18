import numpy as np
from audio_transmitter.audio.audio_generator import AudioGenerator
from audio_transmitter.fsk.fsk_modulator import FskModulator


# test that the modulator is translating the symbols correctly and generates the right tones.
def test_fsk_modulator(monkeypatch):
    expected_tones = [
        1300,
        1300,
        1300,
        1300,
        1700,
        1300,
        2100,
        2500,
        1300,
        2100,
        2100,
        2500,
        2500,
        2500,
        2100,
        2100,
        2100,
        2100,
    ]
    tones = []

    def mock_generate_tone(self, freq, *args, **kwargs):
        tones.append(freq)
        return np.array([])

    monkeypatch.setattr(AudioGenerator, "generate_tone", mock_generate_tone)
    modulator = FskModulator()
    modulator.modulate_fsk(b"\xca\xfe")
    assert tones == expected_tones
