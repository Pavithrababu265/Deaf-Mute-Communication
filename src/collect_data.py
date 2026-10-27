import cv2
import numpy as np
import os
import csv
from hand_detection import HandDetector

def collect_data():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=2)
    
    # Setup data storage
    if not os.path.exists('data'):
        os.makedirs('data')
    
    file_path = 'data/gesture_data.csv'
    
    # Initialize CSV if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            # Header: label, then 21*3 (x,y,z) for hand 1, then maybe hand 2...
            # For simplicity, let's assume we train on single hand or primary hand for now, 
            # or flatten both. Let's support up to 2 hands (42 landmarks * 3 coords = 126 features)
            header = ['label']
            for i in range(42):
                header.extend([f'x{i}', f'y{i}', f'z{i}'])
            writer.writerow(header)

    print("Controls:")
    print("Press 's' to start/stop recording gesture")
    print("Press 'q' to quit")
    
    recording = False
    current_label = ""
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = detector.findHands(img)
        
        # We need a way to ensure consistent input size. 
        # Strategy: Always serialize 2 hands. If 1 hand only, pad with zeros.
        
        # Get world positions (normalized)
        lmList1 = detector.findWorldPosition(0)
        lmList2 = detector.findWorldPosition(1)
        
        features = []
        if lmList1:
            # Flatten list
            flat_lm1 = [coord for lm in lmList1 for coord in lm]
            features.extend(flat_lm1)
        else:
            features.extend([0.0] * 63) # 21 * 3
            
        if lmList2:
            flat_lm2 = [coord for lm in lmList2 for coord in lm]
            features.extend(flat_lm2)
        else:
            features.extend([0.0] * 63)
            
        cv2.putText(img, f"Recording: {recording}", (10, 40), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0) if recording else (0, 0, 255), 2)
        
        if recording and (lmList1 or lmList2):
            cv2.putText(img, f"Label: {current_label}", (10, 70),
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
            # Save to CSV
            with open(file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                row = [current_label] + features
                writer.writerow(row)
        
        cv2.imshow("Data Collection", img)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key & 0xFF == ord('s'):
            if not recording:
                # Ask for label in console
                # Note: Input in console might be blocking if not handled carefully, 
                # but for a simple script this is fine or we can use input() before loop
                # Better: Toggle recording state, if turning ON, ask label via input()
                # Use cv2.waitKey to detect 's', then break out to console?
                # Let's try non-blocking approach: user sets label before running or we input in console now
                # Since we are in an agent environment, we can't easily type into the console while the loop runs 
                # unless we stop the loop.
                # Modified approach: Press keys '0'-'9' to verify specific classes, or just hardcode for now?
                # Real approach: use 'input' before entering loop, or stop CV window to get input.
                
                # For this script, let's assume valid labels are passed via command line or we just pause to ask.
                cv2.destroyWindow("Data Collection")
                current_label = input("Enter gesture label: ")
                recording = True
                # Re-create window
            else:
                recording = False
                print("Stopped recording.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    collect_data()
