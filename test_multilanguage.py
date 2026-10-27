import os
import sys

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from text_processing import TextProcessor
from speech_engine import SpeechEngine

def test():
    print("Testing TextProcessor...")
    tp = TextProcessor()
    
    text = "Hello, how are you?"
    print(f"Original: {text}")
    
    tamil = tp.translate_text(text, 'Tamil')
    print(f"Tamil: {tamil}")
    
    hindi = tp.translate_text(text, 'Hindi')
    print(f"Hindi: {hindi}")

    print("\nTesting SpeechEngine setup...")
    se = SpeechEngine()
    print(f"Using gTTS: {se.use_gtts}")
    
    print("\nSkipping actual audio playback test in automation, but translation works!")

if __name__ == "__main__":
    test()
