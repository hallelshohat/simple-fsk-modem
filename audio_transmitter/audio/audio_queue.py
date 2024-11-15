import sounddevice as sd
from audio_transmitter.consts import samplerate
from multiprocessing import Queue


class AudioQueue:
    def __init__(self):
        self.queue = Queue()
        self.is_muted = False

    # Callback when a new data is available from the microphone.
    def audio_callback(self, indata, frames, time, status):
        if not self.is_muted:
            audio_block = indata[:, 0]  # get the mono channel
            self.queue.put(audio_block.copy())

    def __enter__(self):
        self.stream = sd.InputStream(
            samplerate=samplerate,
            callback=self.audio_callback,
            channels=1,
            blocksize=10000,
        )
        self.stream.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.__exit__()

        if exc_type:
            print(f"An exception occurred: {exc_val}")
        return False

    def mute(self):
        self.is_muted = True
    
    def unmute(self):
        self.is_muted = False