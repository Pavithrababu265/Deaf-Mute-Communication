import cv2
import mediapipe as mp
import math
import os
import pickle
import numpy as np
from collections import deque
from statistics import mode, StatisticsError

class EmotionDetector:
    def __init__(self, mtcnn=False):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.emotion_history = deque(maxlen=8) # Stabilize over last 8 frames
        self.model = None
        self.load_model()

    def load_model(self):
        model_path = 'models/emotion_model.p'
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("[EmotionDetector] Loaded custom emotion model successfully.")
            except Exception as e:
                print(f"[EmotionDetector] Failed to load emotion model: {e}")
                self.model = None
        else:
            print("[EmotionDetector] No emotion model found. Running in Heuristic Mode.")

    def detect_emotion(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                features = []
                for lm in face_landmarks.landmark:
                    features.extend([lm.x, lm.y, lm.z])
                h, w, c = img.shape
                return self.detect_emotion_from_landmarks(features, w, h)
                
        return "Neutral", 0.0

    def detect_emotion_from_landmarks(self, features, w, h):
        emotion = "Neutral"
        score = 0.0
        
        # 1. ML Prediction (Priority if available)
        if self.model:
            try:
                emotion = self.model.predict([features])[0]
                score = 1.0 
                return emotion, score
            except Exception as e:
                print(f"[EmotionDetector] ML Error: {e}")
                pass # Fallback to heuristic
        
        # 2. Heuristics (Fallback)
        def get_pt(idx):
            base = idx * 3
            if base + 1 < len(features):
                return [features[base] * w, features[base+1] * h]
            return [0, 0]
        
        # 1. Smile Detection (Happy)
        mouth_left = get_pt(61)
        mouth_right = get_pt(291)
        mouth_top = get_pt(13)
        mouth_bottom = get_pt(14)
        
        # Eyebrows
        left_brow = get_pt(105)
        right_brow = get_pt(334)
        left_eye_top = get_pt(159)
        right_eye_top = get_pt(386)
        
        mouth_width = math.dist(mouth_left, mouth_right)
        mouth_open = math.dist(mouth_top, mouth_bottom)
        
        face_width = math.dist(get_pt(234), get_pt(454))
        if face_width == 0: face_width = 1
        
        ratio_width = mouth_width / face_width
        ratio_open = mouth_open / face_width
        
        brow_eye_dist = (math.dist(left_brow, left_eye_top) + math.dist(right_brow, right_eye_top)) / 2
        ratio_brow = brow_eye_dist / face_width
        
        mouth_center_y = (mouth_top[1] + mouth_bottom[1]) / 2
        corner_avg_y = (mouth_left[1] + mouth_right[1]) / 2
        corner_offset = corner_avg_y - mouth_center_y 
        ratio_pout = corner_offset / face_width
        
        # Heuristics Tuning
        if ratio_width > 0.45: 
            emotion = "Happy"
            score = ratio_width
        elif ratio_open > 0.15: 
            emotion = "Surprise"
            score = ratio_open
        elif ratio_brow < 0.045: 
            emotion = "Angry"
            score = 1.0 - ratio_brow
        elif ratio_pout > 0.045: 
            emotion = "Sad"
            score = ratio_pout
        else:
            emotion = "Neutral"
            score = 0.5
        
        # Add to history and smooth
        self.emotion_history.append(emotion)
        try:
            final_emotion = mode(self.emotion_history)
        except StatisticsError:
            final_emotion = self.emotion_history[-1]

        return final_emotion, score

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    ed = EmotionDetector()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        emotion, score = ed.detect_emotion(frame)
        
        cv2.putText(frame, f"{emotion}: {score:.2f}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Emotion Detection (MediaPipe)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
