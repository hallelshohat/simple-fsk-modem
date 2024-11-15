import sounddevice as sd
from multiprocessing import Process, Queue
from audio_transmitter.checksum import calculate_checksum
from audio_transmitter.fsk.demodulator.fsk_demodulator import FskDemodulator
from audio_transmitter.consts import samplerate


# main function for audio processing. runs in a different subprocess
def process_audio(audio_queue: Queue, response_queue: Queue):
    demod = FskDemodulator()
    packet_data = b''
    packet_length = 0

    print("Start listening to packet")
    while True:
        audio_block = audio_queue.get()
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
                    response_queue.put(packet_data[:-1])
                else:
                    print("Got a packet with bad checksum, skipping.")
                break

def recv_packet(audio_queue: Queue, timeout=None):
    response_queue = Queue()

    demod_subprocess = Process(target=process_audio, args=(audio_queue, response_queue))
    demod_subprocess.start()
    demod_subprocess.join(timeout=timeout)
    demod_subprocess.kill()

    if not response_queue.empty():
        return response_queue.get()
