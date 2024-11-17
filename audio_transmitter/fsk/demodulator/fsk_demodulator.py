import numpy as np
from audio_transmitter.audio.signal_processing import find_tone, symbols_to_byte
from audio_transmitter.consts import sym_duration, fsk_tones, symbols_per_byte
from audio_transmitter.fsk.demodulator.preamble_finder import PreambleFinder


# Class for demodulating FSK, preamble finding and symbols decision.
class FskDemodulator:
    def __init__(self):
        self.preamble_finder = PreambleFinder()
        self.signal_buffer = []  # Buffer for signals found, using georzel
        self.audio_buffer = np.array(
            []
        )  # Buffer for audio data, before applying georzel
        self.symbols_buffer = []  # Buffer for symbols decoded
        self.chunks_per_symbol = 5  # Sample the signals in this rate * sym duration
        self.preamble_found = (
            False  # preamble should be found once, at the beginning of the packet
        )

    # Get a signal from the microphone, and return decoded bytes if found
    def demodulate_signal(self, data: np.ndarray, samplerate: int):
        # get chunks in signal sample duration
        chunks = self.get_voice_chunks(data, samplerate)

        for chunk in chunks:
            # apply georzel to find the maximum tone of each chunk
            self.signal_buffer.append(find_tone(chunk, fsk_tones, samplerate))

        if not self.preamble_found:
            # Try to find preamble, if not found, returns -1
            (preamble_index, similarity) = self.preamble_finder.find_preamble(
                self.signal_buffer, self.chunks_per_symbol
            )
            if preamble_index != -1:
                print(f"Found preamble. similarity={similarity}")
                self.preamble_found = True
                # chop the preamble from the signal buffer
                self.signal_buffer = self.signal_buffer[preamble_index:]
        else:
            decoded_bytes = b""
            # decide symbols from the buffer of signals
            symbols = self.decide_symbol()
            self.symbols_buffer += symbols
            while len(self.symbols_buffer) >= symbols_per_byte:
                # decode byte in chunks of symbols
                decoded_bytes += symbols_to_byte(
                    self.symbols_buffer[:symbols_per_byte]
                ).to_bytes()
                self.symbols_buffer = self.symbols_buffer[symbols_per_byte:]
            return decoded_bytes

    # the voice should be cut into chunks of selected sample size.
    # this function concats the audio and split it into chunks if available.
    def get_voice_chunks(self, data: np.ndarray, samplerate: int):
        chunk_size = int(sym_duration * samplerate * (1 / self.chunks_per_symbol))
        self.audio_buffer = np.concat((self.audio_buffer, data))
        if len(self.audio_buffer) < chunk_size:
            return []

        chunks = []
        while len(self.audio_buffer) >= chunk_size:
            chunks.append(self.audio_buffer[:chunk_size])
            self.audio_buffer = self.audio_buffer[chunk_size:]

        return chunks

    # after syncing on preamble, the signals should determine the symbols.
    # this function picks the symbol by the most occuring frequency in this range.
    def decide_symbol(self):
        symbols = []
        while len(self.signal_buffer) >= self.chunks_per_symbol:
            signals = np.array(self.signal_buffer[: self.chunks_per_symbol])

            # count for each tone it's occurencecs in the signals arr.
            count_arr = np.zeros(len(fsk_tones))
            for index, freq in enumerate(fsk_tones):
                count_arr[index] = np.count_nonzero(signals == freq)

            max_index = np.argmax(count_arr)
            symbols.append(int(max_index))
            self.signal_buffer = self.signal_buffer[self.chunks_per_symbol :]
        return symbols
