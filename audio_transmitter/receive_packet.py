from audio_transmitter.checksum import calculate_checksum
from audio_transmitter.fsk.demodulator.fsk_demodulator import FskDemodulator
from audio_transmitter.consts import samplerate
from time import time

def recv_packet(audio_queue: list, timeout=None):
    demod = FskDemodulator()
    audio_queue.clear()
    packet_data = b''
    packet_length = 0
    start_time = time()

    print("Start listening to packet")
    while timeout == None or time() - start_time < timeout:
        if len(audio_queue) == 0:
            continue
        
        audio_block = audio_queue.pop(0)
        decoded = demod.demodulate_signal(audio_block, samplerate)
        if decoded and len(decoded) > 0:
            if len(packet_data) == 0 and packet_length == 0:
                packet_length = decoded[0]
                print(f'packet length is {packet_length}')
                decoded = decoded[1:]

            while len(decoded) > 0 and packet_length > 0:
                packet_data += decoded[0].to_bytes()
                packet_length -= 1
                decoded = decoded[1:]

            if packet_length == 0:
                checksum = calculate_checksum(packet_data[:-1]) # without checksum field
                if checksum == packet_data[-1]:
                    return packet_data[:-1]
                else:
                    print("Got a packet with bad checksum, skipping.")
                break
