import soundfile as sf
import pytest
from audio_transmitter.audio.signal_processing import find_tone
from audio_transmitter.consts import fsk_tones


# validate goertzel algorithm with several tone files.
@pytest.mark.parametrize("tone", fsk_tones)
def test_find_tone(tone: int):
    (signal_data, samplerate) = sf.read(f"./test/files/{tone}.wav")
    signal_tone = find_tone(signal_data, fsk_tones, samplerate)

    assert tone == signal_tone
