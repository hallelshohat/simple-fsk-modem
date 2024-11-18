import pytest
from transmit import main

file = bytes([1, 2, 3, 4] * 10)


@pytest.mark.parametrize(
    "recv_packets,expected_send_packets",
    [
        (  # good transmit with all acks
            [b"\x00", b"\x01", b"\x02"],
            [b"\x00\x02", b"\x01" + file[:25], b"\x02" + file[25:]],
        ),
        (  # retransmit on packet 1
            [b"\x00", None, b"\x01", b"\x02"],
            [
                b"\x00\x02",
                b"\x01" + file[:25],
                b"\x01" + file[:25],
                b"\x02" + file[25:],
            ],
        ),
    ],
)
def test_transmit(monkeypatch, recv_packets, expected_send_packets):
    send_packets = []

    def mock_send_packet(packet):
        send_packets.append(packet)

    def mock_recv_packet(*args, **kwargs):
        return recv_packets.pop(0)

    monkeypatch.setattr("transmit.send_packet", mock_send_packet)
    monkeypatch.setattr("transmit.recv_packet", mock_recv_packet)

    main(file)

    assert expected_send_packets == send_packets
