import numpy as np
from audio_transmitter.audio.signal_processing import to_symbols
from audio_transmitter.consts import fsk_tones, preamble


class PreambleFinder:
    def find_preamble(self, signal_buffer, chunks_per_bit):
        preamble_tones = np.array(
            [[fsk_tones[c]] * chunks_per_bit for c in to_symbols(preamble)]
        ).flatten()
        index = 0
        preamble_index = -1
        max_similarity = 0
        while index + len(preamble_tones) < len(signal_buffer):
            arr = signal_buffer[index : index + len(preamble_tones)]
            similarity = self.calculate_similarity(arr, preamble_tones)
            if similarity > max_similarity:
                max_similarity = similarity
                if similarity >= 0.95:
                    preamble_index = index
            index += 1

        return (
            preamble_index + len(preamble_tones) if preamble_index != -1 else -1,
            max_similarity,
        )

    def calculate_similarity(self, arr1, arr2):
        similar = 0
        for num1, num2 in zip(arr1, arr2):
            if num1 == num2:
                similar += 1

        return similar / len(arr1)
