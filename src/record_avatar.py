import cv2
import time
from hand_detection import HandDetector
from animation_manager import AnimationManager

def record_gesture():
    # Setup
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=2)
    manager = AnimationManager()
    
    recording = False
    start_time = 0
    frames = []
    gesture_name = input("Enter the name of the gesture to record (e.g. Hello): ")
    duration = 2.5 # Record for 2.5 seconds
    
    print(f"Get ready to record '{gesture_name}'...")
    print("Press SPACE to start recording.")
    print("Press Q to quit.")
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = detector.findHands(img)
        # We need landmarks. For Avatar, we want consistently 2 hands.
        # findPosition returns screen coords? No, lets use findWorldPosition for 3D if possible?
        # AvatarEngine expects flattened list of 42 points (21*2).
        # We need to standardize: Hand 0 is First detected, Hand 1 is Second.
        # Ideally capture World Coordinates for better 3D.
        
        # Detector returns:
        # findPosition -> list of [id, x, y, z(pixel depth)]
        # findWorldPosition -> list of [x, y, z] (normalized 0-1 or centered)
        
        # Taking World Position is better for 3D avatar re-projection
        lm_world_1 = detector.findWorldPosition(0)
        lm_world_2 = detector.findWorldPosition(1)
        
        current_frame_data = []
        
        # Helper to flatten
        def flatten(lms):
            if not lms: 
                return [0.0] * 63 # 21 * 3
            return [c for p in lms for c in p]
            
        current_frame_data.extend(flatten(lm_world_1))
        current_frame_data.extend(flatten(lm_world_2))
        
        # Drawing status
        if recording:
            elapsed = time.time() - start_time
            cv2.putText(img, f"REC {elapsed:.2f}s", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            frames.append(current_frame_data)
            
            if elapsed >= duration:
                recording = False
                print(f"Recording finished. captured {len(frames)} frames.")
                # Save
                manager.save_animation(gesture_name, frames, duration)
                print("Saved. Press SPACE to record again or Q to quit.")
                frames = [] # Reset
        else:
            cv2.putText(img, f"Press SPACE to Record '{gesture_name}'", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Avatar Recorder", img)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord(' '):
            if not recording:
                recording = True
                start_time = time.time()
                frames = []
                print("Recording started...")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_gesture()
