import pytest
from audio_transmitter.fsk.demodulator.fsk_demodulator import FskDemodulator
from audio_transmitter.receive_packet import recv_packet


# validate recv_packet with demodulate signal, expect length and checksum to be calculated correctly
@pytest.mark.parametrize(
    "packet_data,expected_bytes",
    [(b"\x03\x05\xff\xfa", b"\x05\xff"), (b"\x03\x05\xff\x22", None)],
)
def test_recv_packet(monkeypatch, packet_data: bytes, expected_bytes: bytes):
    def mock_demodulate(*args, **kwargs):
        return packet_data

    monkeypatch.setattr(FskDemodulator, "demodulate_signal", mock_demodulate)
    packet = recv_packet([b"\x00"], None, False)

    assert packet == expected_bytes
