# tasks/play_song_task.py

import time
import threading
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class PlaySongTask:
    def __init__(self, params):
        self.song_name = params.get("song_name", "")
        self.watch = params.get("watch", True)
        self.timeout = params.get("timeout", None)
        self.driver = None
        self._is_running = False
        self._is_paused = False
        self._thread = None

    def _launch_browser(self):
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")

        if self.watch:
            options.add_argument("--start-maximized")
        else:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")

        self.driver = uc.Chrome(options=options)

    def _auto_close_after_timeout(self):
        if self.timeout:
            time.sleep(self.timeout)
            if self._is_running:
                print(f"⏱️ Timeout reached ({self.timeout}s). Auto-closing...")
                self.stop()

    def _play_song(self):
        try:
            self._launch_browser()
            self.driver.get("https://www.youtube.com")
            time.sleep(2)

            search_box = self.driver.find_element(By.NAME, "search_query")
            search_box.send_keys(self.song_name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

            first_video = self.driver.find_element(By.XPATH, '//*[@id="video-title"]')
            song_title = first_video.get_attribute("title") or self.song_name
            first_video.click()
            time.sleep(5)

            if self.watch:
                ActionChains(self.driver).send_keys("f").perform()

            print(f"🎶 Now Playing: {song_title}")

            def skip_ads():
                try:
                    skip_btn = self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-modern")
                    skip_btn.click()
                    print("⏩ Ad Skipped!")
                except:
                    pass

            while self._is_running:
                if self._is_paused:
                    time.sleep(1)
                    continue
                skip_ads()
                time.sleep(1)
        except Exception as e:
            print("❌ Error:", str(e))
        finally:
            self.safe_quit()

    def run(self):
        self._is_running = True
        self._is_paused = False
        self._thread = threading.Thread(target=self._play_song)
        self._thread.start()

        if self.timeout:
            threading.Thread(target=self._auto_close_after_timeout, daemon=True).start()

    def pause(self):
        if self._is_running:
            self._is_paused = True
            print("⏸️ Song Paused")

    def resume(self):
        if self._is_running and self._is_paused:
            self._is_paused = False
            print("▶️ Song Resumed")

    def change_song(self, new_song_name):
        print(f"🔁 Changing song to: {new_song_name}")
        self.song_name = new_song_name
        self.stop()
        self.run()

    def stop(self):
        self._is_running = False
        print("🛑 Stopping song and closing browser")
        self.safe_quit()

    def safe_quit(self):
        try:
            if self.driver:
                self.driver.quit()
                print("✅ Chrome closed safely.")
        except Exception as e:
            print("⚠️ Could not close Chrome:", e)
        finally:
            self.driver = None
