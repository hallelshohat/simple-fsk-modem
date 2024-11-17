import sounddevice as sd
from audio_transmitter.consts import samplerate

# Class for handling audio input, and appending it into a queue
class AudioQueue:
    def __init__(self):
        self.queue = []

    # Callback when a new data is available from the microphone.
    def audio_callback(self, indata, frames, time, status):
        audio_block = indata[:, 0]  # get the mono channel
        self.queue.append(audio_block.copy())

    # use context manager to close the stream when done
    def __enter__(self):
        self.stream = sd.InputStream(
            samplerate=samplerate,
            callback=self.audio_callback,
            channels=1, # mono
            blocksize=10000,
        )
        self.stream.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.__exit__()

        if exc_type:
            print(f"An exception occurred: {exc_val}")
        return False