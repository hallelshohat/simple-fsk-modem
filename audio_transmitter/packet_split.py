from audio_transmitter.consts import max_packet_length


def split_data(data: bytes):
    packets = []
    packet_id = 1
    while len(data) > 0:
        packets.append(packet_id.to_bytes() + data[:max_packet_length])
        data = data[max_packet_length:]
        packet_id += 1
        
    return packets