import soundfile as sf
import sounddevice as sd
from audio_transmitter.audio.audio_queue import AudioQueue
from audio_transmitter.checksum import calculate_checksum
from audio_transmitter.consts import samplerate
from audio_transmitter.fsk.fsk_modulator import FskModulator

# Packet structure is Length (1 Byte) + Data + Checksum (1 byte)
def send_packet(data: bytes, audio_queue: AudioQueue):
    audio_queue.mute()
    modulator = FskModulator()
    length_field = (len(data) + 1).to_bytes() # 1 is for checksum
    checksum_field = calculate_checksum(data).to_bytes()
    packet = length_field + data + checksum_field
    data = modulator.modulate_fsk(packet)
    sd.play(data, samplerate, blocking=True)
    audio_queue.unmute()