from transformers import pipeline
import sys

class Transcriber:
    def __init__(self, model="whisper-small"):
        self.model = model
        # load the model
        try:
            self.pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base", device=-1)
        except Exception as e:
            print("Failed to load the Whisper base model model ...")
            sys.exit(2)


    def transcribe_audio(self, audio_path):
        print("Transcribing audio...")
        result = self.pipe(audio_path)
        text = result["text"] if isinstance(result, dict) else result
        print(f"Recognized: {text}")
        return text


# try to use the class
if __name__ == "__main__":
    transcriber = Transcriber()
    text = transcriber.transcribe_audio("input.wav")
    print(text)


