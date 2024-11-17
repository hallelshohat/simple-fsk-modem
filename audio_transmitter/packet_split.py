from audio_transmitter.consts import max_packet_length

# data should be splitted to packets to ensure reliabilty.
# each packet is wrapped with packet_id, and returns a list of all the packets.
def split_data(data: bytes):
    packets = []
    packet_id = 1
    while len(data) > 0:
        packets.append(packet_id.to_bytes() + data[:max_packet_length])
        data = data[max_packet_length:]
        packet_id += 1

    return packets