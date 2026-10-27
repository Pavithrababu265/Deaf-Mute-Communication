import sys
sys.path.append('src')
from gesture_player import GesturePlayer

print("Loading GesturePlayer...")
player = GesturePlayer()

print("\nTesting 'Hello' gesture...")
landmarks = player.get_gesture_landmarks("Hello")

if landmarks:
    print(f"\nSuccess! Got {len(landmarks)} landmarks.")
    print("First 5 landmarks:")
    for lm in landmarks[:5]:
        print(u"  ID: {}, X: {}, Y: {}, Z: {}".format(lm[0], lm[1], lm[2], lm[3]))
else:
    print("\nFailure! No landmarks found for 'Hello'.")
