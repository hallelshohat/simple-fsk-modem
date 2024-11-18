import sounddevice as sd
from audio_transmitter.checksum import calculate_checksum
from audio_transmitter.consts import samplerate
from audio_transmitter.fsk.fsk_modulator import FskModulator


# Packet structure is Length (1 Byte) + Data + Checksum (1 byte)
def send_packet(data: bytes, play=True):
    modulator = FskModulator()
    length_field = (len(data) + 1).to_bytes()  # 1 is for checksum
    checksum_field = calculate_checksum(data).to_bytes()
    packet = length_field + data + checksum_field
    modulated = modulator.modulate_fsk(packet)
    if play:
        sd.play(modulated, samplerate, blocking=True)
    return modulated
