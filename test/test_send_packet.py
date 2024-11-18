import numpy as np
from audio_transmitter.fsk.fsk_modulator import FskModulator
from audio_transmitter.receive_packet import recv_packet
from audio_transmitter.send_packet import send_packet


# with mock to modulator, assert that the modulator is called with the right bytes (length + data + checksum)
def test_send_packet(monkeypatch):
    modulate_data = []

    def mock_modualte_fsk(self, data):
        modulate_data.append(data)
        return np.array([1.0, 2.0, 3.0])

    monkeypatch.setattr(FskModulator, "modulate_fsk", mock_modualte_fsk)
    send_packet(b"\xca\xfe", play=False)

    assert modulate_data[0] == b"\x03\xca\xfe\x34"


# check if data from send_packet is parsed correctly in recv_packet
def test_send_and_recv_packet():
    data = send_packet(b"\xca\xfe", play=False)
    packet = recv_packet(np.array_split(data, 10), None, False)

    assert packet == b'\xca\xfe'
