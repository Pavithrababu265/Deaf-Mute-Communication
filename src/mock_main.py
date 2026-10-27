import tkinter as tk
from tkinter import ttk
import threading
import time
import random

# Mock Classes to replace heavy dependencies
class MockHandDetector:
    def findHands(self, img):
        return img
    def findPosition(self, img, draw=True):
        # Simulate moving hands
        t = time.time()
        x = int(160 + 50 * math.sin(t))
        y = int(120 + 50 * math.cos(t))
        # Return generic list of landmarks
        return [[i, x + i, y + i, 0] for i in range(21)]
    def findWorldPosition(self, handNo=0):
        return [[random.random(), random.random(), 0] for _ in range(21)]

class MockGestureClassifier:
    def predict_gesture(self, landmarks):
        gestures = ["Hello", "Thanks", "Yes", "No", "Nice"]
        return random.choice(gestures) if random.random() > 0.9 else "None"

class MockEmotionDetector:
    def detect_emotion(self, img):
        emotions = ["Happy", "Sad", "Neutral", "Surprise"]
        return random.choice(emotions), random.random()

class MockAvatarController:
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height
    def update(self, lms, emotion):
        # Return a blank colored image based on emotion
        # Since we can't use numpy, we use PIL or just bytes? 
        # Actually `tkinter` canvas expects an image object.
        # In main_gui we used numpy+opencv to make the image, then PIL.
        # If user has no numpy, we can't use the original main_gui easily without edits.
        # So we have to write a fully mock main_gui or just assume PIL is there.
        # PIL usually installs fine.
        pass

# We will implement a FULL standalone mock main that doesn't import the other files
# to guarantee it runs on 3.14 (assuming PIL/Pillow installs, which it usually does, or `tkinter` native).

import math

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class MockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Avatar System (MOCK MODE)")
        self.root.geometry("800x600")
        
        # UI
        self.label = tk.Label(root, text="MOCK MODE - No Camera/AI", font=("Arial", 20))
        self.label.pack(pady=20)
        
        self.canvas = tk.Canvas(root, width=320, height=240, bg="black")
        self.canvas.pack()
        
        self.info_label = tk.Label(root, text="Simulating...", font=("Arial", 16))
        self.info_label.pack(pady=20)
        
        self.running = True
        self.update_loop()
        
    def update_loop(self):
        if not self.running:
            return
            
        gestures = ["Hello", "Thanks", "Yes", "No", "Please"]
        emotions = ["Happy", "Sad", "Neutral", "Angry"]
        
        g = random.choice(gestures) if random.random() > 0.95 else "..."
        e = random.choice(emotions) if random.random() > 0.95 else "Neutral"
        
        self.info_label.config(text=f"Gesture: {g} | Emotion: {e}")
        
        # Draw simulated "Face"
        self.canvas.delete("all")
        color = "green" if e == "Happy" else "blue" if e == "Sad" else "white"
        self.canvas.create_oval(110, 70, 210, 170, fill=color)
        self.canvas.create_text(160, 200, text=e, fill="white")
        
        self.root.after(100, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = MockApp(root)
    root.mainloop()
