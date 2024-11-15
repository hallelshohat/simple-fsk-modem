import numpy as np
from scipy.signal import butter, lfilter

# Generate bandpass filter for noise reduction
def bandpass_filter(signal, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)

# Goertzel Algorithm to detect frequency power
def goertzel(samples, target_freq, sample_rate):
    N = len(samples)
    k = int(0.5 + (N * target_freq) / sample_rate)
    omega = (2.0 * np.pi * k) / N
    cosine = np.cos(omega)
    coeff = 2.0 * cosine
    q0, q1, q2 = 0.0, 0.0, 0.0
    for sample in samples:
        q0 = coeff * q1 - q2 + sample
        q2 = q1
        q1 = q0
    power = q1 * q1 + q2 * q2 - q1 * q2 * coeff
    return power

# finds the tone with the maximum power from a tone list, using goertzel algorithm
def find_tone(samples, tone_list, samplerate):
    tones_power = [goertzel(samples, tone, samplerate) for tone in tone_list]
    max_index = np.argmax(tones_power)
    return tone_list[max_index]


def to_symbols(arr: bytes):
    symbols = []
    for byte in arr:
        section_1 = (byte >> 6) & 0b11
        section_2 = (byte >> 4) & 0b11
        section_3 = (byte >> 2) & 0b11
        section_4 = byte & 0b11
        symbols += [section_1, section_2, section_3, section_4]

    return symbols

def symbols_to_byte(sections: list):
    byte = (sections[0] << 6) | (sections[1] << 4) | (sections[2] << 2) | sections[3]
    return byte