import soundfile as sf

from audio_transmitter.send_packet import send_packet

data = send_packet(b'\x0f')
sf.write('./test/files/packet_without_preamble.wav', data, 44100)