import numpy as np


# Goertzel Algorithm to detect frequency power within a sample
def goertzel(samples, target_freq, sample_rate):
    N = len(samples)
    k = int(0.5 + (N * target_freq) / sample_rate)
    omega = (2.0 * np.pi * k) / N
    cosine = np.cos(omega)
    coeff = 2.0 * cosine
    q0, q1, q2 = 0.0, 0.0, 0.0  # induction initials
    for sample in samples:
        q0 = coeff * q1 - q2 + sample  # induction step
        q2 = q1
        q1 = q0
    power = q1 * q1 + q2 * q2 - q1 * q2 * coeff
    return power


# finds the tone with the maximum power from a tone list, using goertzel algorithm
def find_tone(samples, tone_list, samplerate):
    tones_power = [goertzel(samples, tone, samplerate) for tone in tone_list]
    max_index = np.argmax(tones_power)
    return tone_list[max_index]


# Generates a list of symbols, from a bytes object, for each byte, split it to 4 symbols.
def to_symbols(arr: bytes):
    symbols = []
    for byte in arr:
        section_1 = (byte >> 6) & 0b11
        section_2 = (byte >> 4) & 0b11
        section_3 = (byte >> 2) & 0b11
        section_4 = byte & 0b11
        symbols += [section_1, section_2, section_3, section_4]

    return symbols


# Generate a byte from a list of 4 symbols.
def symbols_to_byte(sections: list):
    byte = (sections[0] << 6) | (sections[1] << 4) | (sections[2] << 2) | sections[3]
    return byte
