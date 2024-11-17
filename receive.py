from audio_transmitter.audio.audio_queue import AudioQueue
from audio_transmitter.receive_packet import recv_packet
from audio_transmitter.send_packet import send_packet
import time

# main program for receiver
if __name__ == "__main__":
    with AudioQueue() as audio_queue:
        print("Real-time audio stream started. Press Ctrl+C to stop.")
        data = b""
        total_length = -1 # total packets. the first packet includes this value.
        last_ack = -1 # last packet_id received, should be incremental

        while total_length > 0 or total_length == -1:
            packet = recv_packet(audio_queue.queue)
            if packet:
                print(f"Got packet {packet[0]} successfully")
                time.sleep(0.5)  # let the transmitting time to clean buffer
                send_packet(packet[0].to_bytes()) # ack with packet_id

                if last_ack + 1 == packet[0]:
                    last_ack += 1
                    if total_length == -1:  # first packet indicates number of packets
                        total_length = packet[1]
                        print(f"Total number of packets is {total_length}")
                    else:
                        data += packet[1:]  # without length field
                        total_length -= 1

        with open("output.bin", "wb") as f:
            f.write(data)

        print("Output is saved in output.bin!")
        time.sleep(5)
