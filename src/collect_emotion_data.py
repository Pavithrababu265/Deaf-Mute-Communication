import cv2
import mediapipe as mp
import numpy as np
import os
import csv

def collect_face_data():
    cap = cv2.VideoCapture(0)
    
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # Setup data storage
    if not os.path.exists('data'):
        os.makedirs('data')
    
    file_path = 'data/emotion_data.csv'
    
    # Initialize CSV if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            # Header: label, then 478 landmarks (468 + iris) * 3 coords
            header = ['label']
            for i in range(478): 
                header.extend([f'x{i}', f'y{i}', f'z{i}'])
            writer.writerow(header)

    print("Controls:")
    print("Type the emotion label when prompted.")
    print("Press 's' to start/stop recording.")
    print("Press 'q' to quit.")
    
    recording = False
    current_label = ""
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(img_rgb)
        
        cv2.putText(img, f"Recording: {recording}", (10, 40), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0) if recording else (0, 0, 255), 2)
        
        if recording:
            cv2.putText(img, f"Label: {current_label}", (10, 70),
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw mesh (lightly)
                mp.solutions.drawing_utils.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
                
                if recording:
                    # Save data
                    features = []
                    for lm in face_landmarks.landmark:
                        features.extend([lm.x, lm.y, lm.z])
                    
                    with open(file_path, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([current_label] + features)

        cv2.imshow("Emotion Data Collection", img)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'):
            if not recording:
                cv2.destroyWindow("Emotion Data Collection")
                current_label = input("Enter Emotion Label (e.g., Happy, Sad, Angry): ")
                recording = True
            else:
                recording = False
                print("Stopped recording.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    collect_face_data()
