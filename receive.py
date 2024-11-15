import multiprocessing
from audio_transmitter.audio.audio_queue import AudioQueue
from audio_transmitter.receive_packet import recv_packet
from audio_transmitter.send_packet import send_packet
import time

if __name__ == "__main__":
    multiprocessing.freeze_support()

    with AudioQueue() as audio_queue:
        print("Real-time audio stream started. Press Ctrl+C to stop.")
        data = b""
        total_length = -1
        last_ack = -1

        while total_length > 0 or total_length == -1:
            packet = recv_packet(audio_queue.queue)
            if packet:
                print(f"Got packet {packet[0]} successfully")
                time.sleep(1)
                send_packet(packet[0].to_bytes(), audio_queue)
                
                if last_ack + 1 == packet[0]:
                    last_ack += 1
                    if total_length == -1:  # first packet indicates number of packets
                        total_length = packet[1]
                        print(f"Total number of packets is {total_length}")
                    else:
                        data += packet[1:]  # without length field
                        total_length -= 1

        print(data)
