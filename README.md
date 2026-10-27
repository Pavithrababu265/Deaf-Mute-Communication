🤟 Deaf-Mute Communication - AI Sign Language Translator

> Empowering communication through AI - Translating Sign Language to Speech in Real-Time

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-orange)](https://google.github.io/mediapipe/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 🌟 Overview
This is an AI-powered system that translates **Sign Language gestures into Speech & Text** in real-time. It helps bridge the communication gap for deaf and mute individuals using Computer Vision and Machine Learning.

Built with **Python, OpenCV, and MediaPipe Hands**.

### ✨ Features
- 👋 Real-time Hand Gesture Recognition
- 🗣️ Sign to Speech Conversion
- 📝 Sign to Text Display
- 📷 Works with normal Webcam (No extra hardware)
- ⚡ Fast & Lightweight - Runs on laptop itself
- 🎯 Supports common signs like Help, Thank You, etc.

### 🛠️ Tech Stack
- **Python 3.11**
- **OpenCV** - For camera and image processing
- **MediaPipe** - For hand tracking (21 landmarks)
- **pyttsx3 / gTTS** - For Text-to-Speech

### 📁 Project StructureDeaf-Mute-Communication/
├── assets/signs/   # Sign images dataset
├── models/         # Trained models
├── src/            # Main source code
├── QUICKSTART.md   # Quick start guide
└── debug_*.py      # Debug scriptsjavascript
### 🚀 How to Run

1. Clone the repo
```bash
git clone https://github.com/Pavithrababu265/Deaf-Mute-Communication.git
cd Deaf-Mute-CommunicationInstall dependenciesbashpip install opencv-python mediapipe pyttsx3Run the appbashpython src/main.py
# or
python debug_playback.py🎥 How it Works
Camera captures hand gestureMediaPipe detects 21 hand landmarksModel classifies the signText is displayed + Speech is generated🔮 Future Improvements
Add more Indian Sign Language (ISL) signsBuild Mobile AppAdd Sentence FormationAdd Tamil Sign Language supportmarkdown### 👩‍💻👨‍💻 Authors
**Team:** Pavithra Babu & Vishal S
- Pavithra Babu - [@Pavithrababu265](https://github.com/Pavithrababu265)
- Vishal S - [@vishalsk2564](https://github.com/vishalsk2564)

> Built together to make communication accessible for all ❤️ to make communication accessible for all.📄 License
This project is open source and available under the MIT License.
