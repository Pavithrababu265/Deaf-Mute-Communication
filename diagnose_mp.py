import sys
import mediapipe
import os

print(f"Python executing this script: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"MediaPipe File: {mediapipe.__file__}")
print(f"Current Working Directory: {os.getcwd()}")
print(f"Directory Contents: {os.listdir('.')}")

try:
    print(f"MediaPipe Solutions available: {dir(mediapipe.solutions)}")
except AttributeError as e:
    print(f"Error accessing solutions: {e}")
    print(f"Dir(mediapipe): {dir(mediapipe)}")
