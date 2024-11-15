import numpy as np


class AudioGenerator:
    current_phase = 0

    def generate_tone(self, frequency: int, duration: int, samplerate: int):
        start_t = np.arcsin(self.current_phase) / (2 * np.pi * frequency)
        t = np.linspace(
            start_t, start_t + duration, int(samplerate * duration), endpoint=False
        )
        self.current_phase = np.sin(2 * np.pi * frequency * (start_t + duration))
        tone = np.sin(2 * np.pi * frequency * t)
        return self.apply_fade(tone)

    def apply_fade(self, tone, fade_percentage=0.1):
        fade_length = int(len(tone) * fade_percentage)
        fade_in = np.linspace(0, 1, fade_length)
        fade_out = np.linspace(1, 0, fade_length)
        tone[:fade_length] *= fade_in
        tone[-fade_length:] *= fade_out
        return tone
