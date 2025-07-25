import sounddevice as sd
from scipy.io.wavfile import write
from time import sleep
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

class AudioRecorder:
    def __init__(self, fs=16000):
        self.fs = fs
        self.recording = []
        self.stream = None

    def start_recording(self):
        import os

# BEFORE recording starts
        if os.path.exists("output.mp3"):
            try:
                os.remove("output.mp3")
                print("✅ Old output.mp3 removed before recording.")
            except PermissionError:
                print("❌ File in use. Cannot delete output.mp3.")
        self.recording = []
        self.stream = sd.InputStream(samplerate=self.fs, channels=1, dtype='int16', callback=self.callback)
        self.stream.start()

    def callback(self, indata, frames, time, status):
        self.recording.append(indata.copy())

    def stop_recording(self, filename="input.wav"):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        audio = np.concatenate(self.recording, axis=0)
        # file_loc = "./files/audio/"
        write(filename, self.fs, audio)
        return filename


# def record_audio(filename="input.wav", fs=16000, seconds=10):
#     print(f"Recording for up to {seconds} seconds. Speak now...")
#     recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
#     sd.wait()
#     write(filename, fs, recording)
#     print(f"Recording saved as {filename}")
#     return filename

# try to use the class
if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.start_recording()
    sleep(5)
    recorder.stop_recording()