import numpy as np

samplerate = 44100  # microphone input sample rate
sym_rate = 15  # symbol rate (symbols / sec)
sym_duration = 1 / sym_rate  # Symbol duration (in seconds)

fsk_tones = [1300, 1700, 2100, 2500]  # frequencies for fsk, array index is the symbol

symbols_per_byte = int(8 / np.log2(len(fsk_tones)))  # how many symbols are in one byte

preamble = b"\x12"  # preamble - used at the beginning of every packet

max_packet_length = 25  # maximum data packet length

min_preamble_similarity = 0.95  # Minimum similarity for preamble to consider valid.
