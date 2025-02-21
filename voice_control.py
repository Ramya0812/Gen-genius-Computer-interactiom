import speech_recognition as sr
import pyautogui
import pyttsx3
import keyboard
import time
import sys
import sounddevice as sd
import numpy as np
import wavio

class VoiceController:
    def __init__(self):
        """Initialize text-to-speech and speech recognition"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.recognizer = sr.Recognizer()
        self.is_listening = True

        # Command Mappings
        self.commands = {
            "zoom in": self.zoom_in,
            "zoom out": self.zoom_out,
            "screenshot": self.take_screenshot,
            "scroll up": self.scroll_up,
            "scroll down": self.scroll_down,
            "scroll left": self.scroll_left,
            "scroll right": self.scroll_right,
            "volume up": self.volume_up,
            "volume down": self.volume_down,
            "mute": self.toggle_mute,
            "brightness up": self.brightness_up,
            "brightness down": self.brightness_down,
            "next window": self.next_window,
            "previous window": self.previous_window,
            "minimize": self.minimize_window,
            "maximize": self.maximize_window,
            "close window": self.close_window,
            "stop listening": self.stop_listening
        }

    def speak(self, text):
        """Convert text to speech"""
        print(f"Bot: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def record_audio(self, filename="temp.wav", duration=3, fs=44100):
        """Record audio"""
        print("🎤 Recording...")
        try:
            audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
            sd.wait()
            wavio.write(filename, audio_data, fs, sampwidth=2)
            print("✅ Recording complete.")
            return filename
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            return None

    def recognize_audio(self, filename="temp.wav"):
        """Recognize speech from the recorded audio file"""
        try:
            with sr.AudioFile(filename) as source:
                audio = self.recognizer.record(source)
            command = self.recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")
            return command
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error in recognition: {e}")
            return None

    # System Control Functions
    def zoom_in(self):
        keyboard.press_and_release('ctrl++')
        return "Zooming in"

    def zoom_out(self):
        keyboard.press_and_release('ctrl+-')
        return "Zooming out"

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshot_{int(time.time())}.png")
        return "Screenshot taken"

    def scroll_up(self):
        pyautogui.scroll(10)
        return "Scrolling up"

    def scroll_down(self):
        pyautogui.scroll(-10)
        return "Scrolling down"

    def scroll_left(self):
        pyautogui.hscroll(-10)
        return "Scrolling left"

    def scroll_right(self):
        pyautogui.hscroll(10)
        return "Scrolling right"

    def volume_up(self):
        pyautogui.press('volumeup')
        return "Volume increased"

    def volume_down(self):
        pyautogui.press('volumedown')
        return "Volume decreased"

    def toggle_mute(self):
        pyautogui.press('volumemute')
        return "Volume muted/unmuted"

    def brightness_up(self):
        keyboard.press_and_release('fn+f12')
        return "Increasing brightness"

    def brightness_down(self):
        keyboard.press_and_release('fn+f11')
        return "Decreasing brightness"

    def next_window(self):
        keyboard.press_and_release('alt+tab')
        return "Switching to next window"

    def previous_window(self):
        keyboard.press_and_release('alt+shift+tab')
        return "Switching to previous window"

    def minimize_window(self):
        keyboard.press_and_release('windows+down')
        return "Window minimized"

    def maximize_window(self):
        keyboard.press_and_release('windows+up')
        return "Window maximized"

    def close_window(self):
        keyboard.press_and_release('alt+f4')
        return "Closing window"

    def stop_listening(self):
        self.is_listening = False
        return "Stopping voice control"

    def listen(self):
        """Main loop to listen for voice commands"""
        self.speak("Voice control activated. Listening for commands.")

        while self.is_listening:
            audio_file = self.record_audio()
            if audio_file:
                command = self.recognize_audio(audio_file)

                if command:
                    action = self.commands.get(command, None)
                    if action:
                        response = action()
                        self.speak(response)
                    else:
                        self.speak("Command not recognized. Please try again.")
            time.sleep(1)

def main():
    print("🚀 Starting voice controller...")
    controller = VoiceController()
    try:
        controller.listen()
    except KeyboardInterrupt:
        print("\n👋 Exiting voice control system...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
