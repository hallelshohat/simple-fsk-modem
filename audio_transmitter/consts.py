import numpy as np

samplerate = 44100
sym_rate = 4
sym_duration = 1 / sym_rate

fsk_tones = [1300, 1700, 2100, 2500]

symbols_per_byte = int(8 / np.log2(len(fsk_tones)))

preamble = b"\x12"

max_packet_length = 10