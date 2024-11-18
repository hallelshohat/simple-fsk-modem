import numpy as np
from audio_transmitter.fsk.demodulator.preamble_finder import PreambleFinder

preamble_tones = [1300, 1700, 1300, 2100]
preamble_signal_chunks = np.array(
    [[signal] * 10 for signal in preamble_tones]
).flatten()


# test preamble_finder with 100% similarity
def test_preamble_finder():
    preamble_finder = PreambleFinder()
    (preamble_index, similarity) = preamble_finder.find_preamble(
        preamble_signal_chunks, 10
    )

    assert preamble_index == len(preamble_tones) * 10
    assert similarity == 1


# test preamble_finder with 97.5% similarity
def test_similarity_975():
    preamble_signal_chunks[-1] = 1300
    preamble_finder = PreambleFinder()
    (preamble_index, similarity) = preamble_finder.find_preamble(
        preamble_signal_chunks, 10
    )

    assert preamble_index == len(preamble_tones) * 10
    assert similarity == 0.975
