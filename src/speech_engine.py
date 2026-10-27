import pyttsx3
import speech_recognition as sr
import threading

class SpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.recognizer = sr.Recognizer()
        
        # Initialize pygame mixer for gTTS audio playback
        self.use_gtts = False
        try:
            import pygame
            pygame.mixer.init()
            self.use_gtts = True
        except ImportError:
            print("pygame not found. Falling back to pyttsx3 for TTS.")

    def speak(self, text, language_code='en-IN'):
        if not text or len(text.strip()) == 0:
            return
            
        try:
            thread = threading.Thread(target=self._speak_thread, args=(text, language_code))
            thread.start()
        except Exception as e:
            print(f"Threading Error: {e}")

    def _speak_thread(self, text, language_code):
        try:
            # Simple heuristic: if english, pyttsx3 is often faster and fine.
            # But the user might want Indian accents for English too via gTTS. Let's use gTTS for everything if available.
            if self.use_gtts and language_code != 'en-US': 
                from gtts import gTTS
                import pygame
                import os
                import tempfile
                
                # gTTS language code is usually the first part of locale (e.g. 'hi' from 'hi-IN')
                gtts_lang = language_code.split('-')[0] if '-' in language_code else language_code
                
                tts = gTTS(text=text, lang=gtts_lang)
                
                # Create a temp file
                fd, temp_path = tempfile.mkstemp(suffix=".mp3")
                os.close(fd)
                
                tts.save(temp_path)
                
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                    
                # Unload and remove
                pygame.mixer.music.unload()
                try:
                    os.remove(temp_path)
                except:
                    pass
            else:
                # Fallback to pyttsx3
                local_engine = pyttsx3.init()
                local_engine.say(text)
                local_engine.runAndWait()
                
        except Exception as e:
            print(f"TTS Error ({language_code}): {e}")
            # Ultimate fallback to pyttsx3 if gTTS fails (e.g. network issue)
            try:
                local_engine = pyttsx3.init()
                local_engine.say(text)
                local_engine.runAndWait()
            except:
                pass

    def listen(self, language_code='en-IN'):
        try:
            with sr.Microphone() as source:
                print(f"Listening... (Language: {language_code})")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    try:
                        text = self.recognizer.recognize_google(audio, language=language_code)
                        print(f"Recognized: {text}")
                        return text
                    except sr.UnknownValueError:
                        return ""
                    except sr.RequestError as e:
                        print(f"Network Error: {e}")
                        return ""
                except sr.WaitTimeoutError:
                    return ""
        except Exception as e:
            print(f"Microphone/System Error: {e}")
            return ""

if __name__ == "__main__":
    se = SpeechEngine()
    se.speak("Hello, this is a test.")
    print("Listening test... say something.")
    print(se.listen())
