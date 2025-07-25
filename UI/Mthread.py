from PyQt5.QtCore import QThread, pyqtSignal

class ModelLoader(QThread):
    models_loaded = pyqtSignal(object, object, object, object)  # signal to emit the loaded models

    def run(self):
        # Load models (this takes time)
        from tools.rec import AudioRecorder
        from tools.transcribe import Transcriber
        from tools.gemini import Gemini
        from tools.Speaker import TTSPlayer

        recorder = AudioRecorder()
        transcriber = Transcriber()
        gemini = Gemini()
        speaker = TTSPlayer()

        # Send them back to the main thread
        self.models_loaded.emit(recorder, transcriber, gemini, speaker)
