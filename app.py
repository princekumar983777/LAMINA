import os
import sys
import time
import json
import asyncio

from google import genai
from google.genai import types
import edge_tts as tts
import numpy as np
from PyQt5.QtWidgets import QApplication


from UI.doddle import Robo

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Robo()
    pet.show()
    sys.exit(app.exec_())