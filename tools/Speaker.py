import asyncio
import edge_tts
import pygame
from time import sleep
import os 


class TTSPlayer:
    def __init__(self, voice="en-US-JennyNeural"):
        self.voice = voice
        pygame.mixer.init()

    async def synthesize(self, text, filename="output.mp3"):
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(filename)

    def play(self, filename="output.mp3"):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)  # Wait for 10ms to check if playback is still busy

    def stop(self, filename="output.mp3"):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()  # Ensure the file is not locked
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"✅ {filename} deleted successfully.")
            except PermissionError:
                print(f"❌ File in use. Cannot delete {filename}.")

    def speak(self, text):
        self.stop() 
        asyncio.run(self.synthesize(text))
        self.play()


# ========================================
# 🌍 Microsoft Edge TTS Voices (edge-tts)
# ========================================

# 🔸 English (US)
# - en-US-JennyNeural         # Female, Natural American
# - en-US-GuyNeural           # Male, Natural American
# - en-US-AriaNeural          # Female, slightly younger tone
# - en-US-DavisNeural         # Male
# - en-US-AmberNeural         # Female

# 🔸 English (UK)
# - en-GB-RyanNeural          # Male, British accent
# - en-GB-SoniaNeural         # Female, British accent
# - en-GB-LibbyNeural         # Female, soft tone
# - en-GB-ThomasNeural        # Male

# 🔸 English (India)
# - en-IN-NeerjaNeural        # Female, Indian accent
# - en-IN-PrabhatNeural       # Male, Indian accent

# 🔸 Hindi (India)
# - hi-IN-MadhurNeural        # Male
# - hi-IN-SwaraNeural         # Female

# 🔸 Japanese
# - ja-JP-NanamiNeural        # Female
# - ja-JP-KeitaNeural         # Male

# 🔸 Chinese (Mandarin)
# - zh-CN-XiaoxiaoNeural      # Female, Mandarin (Simplified)
# - zh-CN-YunxiNeural         # Male
# - zh-CN-XiaochenNeural      # Female, calm tone

# 🔸 French (France)
# - fr-FR-DeniseNeural        # Female
# - fr-FR-HenriNeural         # Male

# 🔸 Spanish (Spain)
# - es-ES-ElviraNeural        # Female
# - es-ES-AlvaroNeural        # Male

# 🔸 Spanish (Mexico)
# - es-MX-DaliaNeural         # Female
# - es-MX-JorgeNeural         # Male

# 🔸 German
# - de-DE-KatjaNeural         # Female
# - de-DE-ConradNeural        # Male

# 🔸 Italian
# - it-IT-ElsaNeural          # Female
# - it-IT-DiegoNeural         # Male

# 🔸 Arabic (Egypt)
# - ar-EG-SalmaNeural         # Female
# - ar-EG-ShakirNeural        # Male

# 🔸 Portuguese (Brazil)
# - pt-BR-FranciscaNeural     # Female
# - pt-BR-AntonioNeural       # Male

# 🔸 Russian
# - ru-RU-DariyaNeural        # Female
# - ru-RU-DmitryNeural        # Male

# 🔸 Korean
# - ko-KR-SoonBokNeural       # Female
# - ko-KR-InJoonNeural        # Male

# 🔸 Turkish
# - tr-TR-EmelNeural          # Female
# - tr-TR-AhmetNeural         # Male

# 🔸 Bengali (India)
# - bn-IN-TanishaaNeural      # Female
# - bn-IN-BashkarNeural       # Male

# 🔸 Tamil (India)
# - ta-IN-PallaviNeural       # Female
# - ta-IN-ValluvarNeural      # Male

# 🔸 Telugu (India)
# - te-IN-ShrutiNeural        # Female
# - te-IN-MohanNeural         # Male

# 🔸 Malayalam (India)
# - ml-IN-SobhanaNeural       # Female
# - ml-IN-MidhunNeural        # Male

# ✅ Tip:
# To use a voice, pass its `ShortName` in `edge_tts.Communicate(voice="...")`
# Example:
# communicate = edge_tts.Communicate(text="Hello!", voice="en-GB-SoniaNeural")


# Usage:
if __name__ == "__main__":
    tts_player = TTSPlayer()
    tts_player.speak("You do not need to call stop for normal playback to finish.")
    # To stop playback:
    tts_player.stop()