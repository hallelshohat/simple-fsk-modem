import multiprocessing
from audio_transmitter.audio.audio_queue import AudioQueue
from audio_transmitter.packet_split import split_data
from audio_transmitter.receive_packet import recv_packet
from audio_transmitter.send_packet import send_packet

if __name__ == '__main__':
    multiprocessing.freeze_support()

    with AudioQueue() as audio_queue:
        bits = b"Hi how are you? I'm fine thanks."
        packets = split_data(bits)
        
        total_packets_message = b'\x00' + len(packets).to_bytes()
        packets.insert(0, total_packets_message)

        print(f'sending total {len(packets)} packets')
        while len(packets) > 0:
            packet = packets[0]
            print(f'Sending packet {packet[0]}')
            send_packet(packet, audio_queue)
            ack = recv_packet(audio_queue.queue, timeout=10)
            if ack and ack[0] == packet[0]:
                print(f"Received ack for packet {ack[0]}")
                packets.pop(0)
            else:
                print(f"Resending packet {packet[0]}")
        
        print("Sent all packets successfully!")