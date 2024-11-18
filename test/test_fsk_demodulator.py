import numpy as np
import pytest
import soundfile as sf

from audio_transmitter.fsk.demodulator.fsk_demodulator import FskDemodulator


# With several files, expect the demodulator to find preamble, and demodulate bytes after that
@pytest.mark.parametrize(
    "filename,expected_bytes",
    [("good_packet.wav", b"\x02\x0f\x0f"), ("packet_without_preamble.wav", b"")],
)
def test_fsk_demodulator(filename: str, expected_bytes: bytes):
    (data, samplerate) = sf.read(f"./test/files/{filename}")
    chunks = np.array_split(data, 10)
    demod = FskDemodulator()
    data = b""

    for chunk in chunks:
        decoded = demod.demodulate_signal(chunk, samplerate)
        if decoded:
            data += decoded

    assert data.startswith(expected_bytes)
