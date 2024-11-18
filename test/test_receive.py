import pytest
from receive import main


@pytest.mark.parametrize(
    "recv_packets,expected_send_packets, expceted_data",
    [
        (  # good transmit with all acks
            [b"\x00\x02", b"\x01\xca", b"\x02\xfe"],
            [b"\x00", b"\x01", b"\x02"],
            b"\xca\xfe",
        ),
        (  # packet order is not good, should drop 3 in final data
            [b"\x00\x02", b"\x03\xca", b"\x01\xca", b"\x02\xfe"],
            [b"\x00", b"\x03", b"\x01", b"\x02"],
            b"\xca\xfe",
        ),
    ],
)
def test_receive(monkeypatch, recv_packets, expected_send_packets, expceted_data):
    send_packets = []

    def mock_send_packet(packet):
        send_packets.append(packet)

    def mock_recv_packet(*args, **kwargs):
        return recv_packets.pop(0)

    monkeypatch.setattr("receive.send_packet", mock_send_packet)
    monkeypatch.setattr("receive.recv_packet", mock_recv_packet)

    data = main(sleep=False)

    assert expected_send_packets == send_packets
    assert data == expceted_data
