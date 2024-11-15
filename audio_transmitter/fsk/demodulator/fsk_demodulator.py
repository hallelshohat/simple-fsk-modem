import numpy as np
from audio_transmitter.audio.signal_processing import find_tone, symbols_to_byte
from audio_transmitter.consts import sym_duration, fsk_tones, symbols_per_byte
from audio_transmitter.fsk.demodulator.preamble_finder import PreambleFinder


class FskDemodulator:
    signal_buffer = []
    data_buffer = np.array([])
    symbols_buffer = []
    chunks_per_symbol = 5
    preamble_found = False

    def __init__(self):
        self.preamble_finder = PreambleFinder()

    def demodulate_signal(self, data: np.ndarray, samplerate: int):
        chunks = self.get_voice_chunks(data, samplerate)

        for chunk in chunks:
            self.signal_buffer.append(find_tone(chunk, fsk_tones, samplerate))
        
        if not self.preamble_found:
            (preamble_index, similarity) = self.preamble_finder.find_preamble(
                self.signal_buffer, self.chunks_per_symbol
            )
            if preamble_index != -1:
                print(f"Found preamble. similarity={similarity}")
                self.preamble_found = True
                self.signal_buffer = self.signal_buffer[preamble_index:]
        else:
            decoded_bytes = b""
            symbols = self.decide_symbol()
            self.symbols_buffer += symbols
            while len(self.symbols_buffer) >= symbols_per_byte:
                decoded_bytes += symbols_to_byte(
                    self.symbols_buffer[:symbols_per_byte]
                ).to_bytes(1)
                self.symbols_buffer = self.symbols_buffer[symbols_per_byte:]
            return decoded_bytes

    def get_voice_chunks(self, data: np.ndarray, samplerate: int):
        chunk_size = int(sym_duration * samplerate * (1 / self.chunks_per_symbol))
        self.data_buffer = np.concat((self.data_buffer, data))
        if len(self.data_buffer) < chunk_size:
            return []

        chunks = []
        while len(self.data_buffer) >= chunk_size:
            chunks.append(self.data_buffer[:chunk_size])
            self.data_buffer = self.data_buffer[chunk_size:]

        return chunks

    def decide_symbol(self):
        symbols = []
        while len(self.signal_buffer) >= self.chunks_per_symbol:
            signals = np.array(self.signal_buffer[: self.chunks_per_symbol])

            count_arr = np.zeros(len(fsk_tones))
            for index, freq in enumerate(fsk_tones):
                count_arr[index] = np.count_nonzero(signals == freq)

            max_index = np.argmax(count_arr)
            symbols.append(int(max_index))
            self.signal_buffer = self.signal_buffer[self.chunks_per_symbol :]
        return symbols
