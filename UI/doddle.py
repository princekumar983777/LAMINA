import sys
import random
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu, QAction
from PyQt5.QtGui import QPixmap
from chibi.map import chibi_map, chibi_map_list

from UI.Mthread import ModelLoader
import json
import time 





# def rec_to_gen(file_path):
#     user_input = transcriber.transcribe_audio(file_path)
#     response = Gemini.query_gemini(user_input)
#     data = json.loads(response)
#     """{
#         'reply': "I'm playing the song Sahiba on YouTube for you.",
#         'task': 'play_song',
#         'param': {
#                     'song_name': 'Sahiba',
#                     'platform': 'YouTube'
#                 }
#         }
#     """
#     reply = data("reply")
#     task = data("tsak")
#     """
#         code for doing the task
#         add to task bar
#     """
#     return reply

class Robo(QWidget):
    def __init__(self):
        super().__init__()

        # Load screen size
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.screen_width = size.width()
        self.screen_height = size.height()

        # Window transparency and no frame
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)


        self.is_recording = False 


        # Set label for holding image
        self.label = QLabel(self)
        self.label.setScaledContents(True)

        # List of images to toggle on click
        
        self.current_feeling = "happy"
        self.set_image(chibi_map(self.current_feeling))

        # Start Position - bottom-right corner
        self.x_pos = self.screen_width - self.width() 
        self.y_pos = self.screen_height - self.height() 
        self.move(self.x_pos, self.y_pos)

        # Drag and fixed state
        self.is_movable = False
        self.old_pos = None

        self.set_image(chibi_map("sleep"))  # bot looks sleepy while loading

        # Set placeholders for now
        self.recorder = None
        self.transcriber = None
        self.gemini = None
        self.speaker = None

        # Start background model loading
        self.model_loader = ModelLoader()
        self.model_loader.models_loaded.connect(self.models_ready)  # what to do after loading
        self.model_loader.start()

    def models_ready(self, recorder, transcriber, gemini, speaker):
        # Save models to use later
        self.recorder = recorder
        self.transcriber = transcriber
        self.gemini = gemini
        self.speaker = speaker

        print("✅ Models loaded successfully!")
        self.set_image(chibi_map("happy"))  # bot is now happy and ready



    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.size())

    def start_recording(self):
        self.is_recording = True
        print("🎙️ Recording started...")
        self.speaker.stop()
        self.recorder.start_recording()
        self.set_image(chibi_map("listen"))

    def stop_recording(self):
        if not self.recorder or not self.transcriber or not self.gemini or not self.speaker:
            print("⏳ Models not loaded yet.")
            return
        self.is_recording = False
        print("🛑 Recording stopped.")
        filename = self.recorder.stop_recording()

        self.start_thinking() # change the image to thinking 
        start = time.time()             #time start
        user_input = self.transcriber.transcribe_audio(filename)
        print("Time Taken in Transcription ", time.time() - start)      #time
        start = time.time()
        response = self.gemini.query_gemini(user_input)
        reply_text = response.get("reply", "")
        task = response.get("task", None)
        print("Time Taken for generating responses ", time.time() - start)      #time
        params = response.get("param", {})
        self.stop_thinking()

        start = time.time()
        self.start_talking()
        self.speaker.speak(reply_text)
        self.stop_talking()
        print("Time Taken for speech genearting ", time.time() - start) 

    def start_talking(self):
        self.is_talking = True
        QApplication.processEvents() 
        print("💬 Talking started...")
        self.set_image(chibi_map("talk"))

    def stop_talking(self):
        self.is_talking = False
        print("🛑 Talking stopped.")
        self.set_image(chibi_map("happy"))

    def start_thinking(self):
        self.is_thinking = True
        print("🤔 Thinking started...")
        self.set_image(chibi_map("think"))
        QApplication.processEvents() 

    def stop_thinking(self):
        self.is_thinking = False
        print("🛑 Thinking stopped.")
        self.set_image(chibi_map("happy"))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_movable:
                self.old_pos = event.globalPos()
                # if moving 
                self.set_image(chibi_map("confused"))
            else:
                # Toggle recording mode
                self.is_recording = not self.is_recording
                if self.is_recording:
                    self.start_recording()
                else:
                    self.stop_recording()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())

    def mouseMoveEvent(self, event):
        if self.is_movable and self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        if self.is_movable:
            # Restore normal image
            self.set_image(chibi_map("happy"))

    def show_context_menu(self, pos):
        menu = QMenu()

        toggle_action = QAction("Make Movable" if not self.is_movable else "Fix Position", self)
        toggle_action.triggered.connect(self.toggle_movable)
        menu.addAction(toggle_action)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        menu.exec_(pos)

    def toggle_movable(self):
        self.is_movable = not self.is_movable


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     pet = Robo()
#     pet.show()
#     sys.exit(app.exec_())
