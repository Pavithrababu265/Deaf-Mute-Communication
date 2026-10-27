import cv2
import numpy as np
import socket
import json

class AvatarController:
    def __init__(self, width=640, height=480, stream_ip='127.0.0.1', stream_port=5005):
        self.width = width
        self.height = height
        # UDP socket for potentially streaming to Unity/Blender
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverAddressPort = (stream_ip, stream_port)
        
        # Connections for hand skeleton (MediaPipe standard)
        self.connections = [
            (0,1), (1,2), (2,3), (3,4),         # Thumb
            (0,5), (5,6), (6,7), (7,8),         # Index
            (0,9), (9,10), (10,11), (11,12),    # Middle
            (0,13), (13,14), (14,15), (15,16),  # Ring
            (0,17), (17,18), (18,19), (19,20),  # Pinky
            # Second Hand (Offset by 21)
            (21,22), (22,23), (23,24), (24,25),
            (21,26), (26,27), (27,28), (28,29),
            (21,30), (30,31), (31,32), (32,33),
            (21,34), (34,35), (35,36), (36,37),
            (21,38), (38,39), (39,40), (40,41)
        ]

    def update(self, hand_landmarks, emotion):
        """
        hand_landmarks: list of dicts or objects with x, y, z. 
                        For this simple visualizer, we expect a flat list or list of [id, x, y] lists.
                        Actually, let's expect the format from HandDetector.findPosition which is [[id, x, y, z], ...]
        emotion: str describing the emotion
        """
        # Create a blank black canvas for the avatar
        avatar_img = np.zeros((self.height, self.width, 3), np.uint8)
        
        # 1. Visualize Hands (The Avatar's "Hands")
        if hand_landmarks:
            # We assume hand_landmarks is a list of points [[id, x, y, z], ...]
            # or a list of such lists if multiple hands.
            # Let's handle a single flattened list of points or list of lists.
            # Adaptation: accepted format is list of (id, x, y, z) tuples/lists
            
            # Draw points
            for lm in hand_landmarks:
                if len(lm) >= 3:
                    x, y = int(lm[1]), int(lm[2])
                    cv2.circle(avatar_img, (x, y), 5, (0, 255, 255), cv2.FILLED) # Yellow joints
            
            # Draw connections
            # We need to access points by ID.
            points = {lm[0]: (lm[1], lm[2]) for lm in hand_landmarks if len(lm) >= 3}
            
            for p1_id, p2_id in self.connections:
                if p1_id in points and p2_id in points:
                    pt1 = (int(points[p1_id][0]), int(points[p1_id][1]))
                    pt2 = (int(points[p2_id][0]), int(points[p2_id][1]))
                    cv2.line(avatar_img, pt1, pt2, (0, 255, 0), 2) # Green bones

        # 2. Visualize Emotion (The Avatar's "Face")
        # User requested to remove the "emoji" face.
        # We will strictly keep the hands and maybe the text.
        
        # Define colors for text
        color_map = {
            'happy': (0, 255, 0),    # Green
            'sad': (255, 0, 0),      # Blue
            'angry': (0, 0, 255),    # Red
            'neutral': (255, 255, 255), # White
            'surprise': (0, 255, 255), # Yellow
            'fear': (128, 0, 128)      # Purple
        }
        face_color = color_map.get(emotion.lower(), (255, 255, 255))
        
        # (Face drawing removed)
        
        # Draw mouth (simple line or curve based on emotion can be added)
        # Just text for now
        # Just text for now - REMOVED to avoid double drawing in main_gui
        # cv2.putText(avatar_img, f"Emotion: {emotion}", (10, self.height - 20),
        #             cv2.FONT_HERSHEY_PLAIN, 2, face_color, 2)

        # 3. Stream Data (Simulating external 3D engine support)
        # We can enable this if we have a listener.
        # data = {'emotion': emotion, 'landmarks': hand_landmarks}
        # self.sock.sendto(json.dumps(data).encode(), self.serverAddressPort)
        
        return avatar_img

if __name__ == "__main__":
    ac = AvatarController()
    # Dummy data
    dummy_lms = [[i, 100 + i*10, 100 + i*5, 0] for i in range(21)]
    img = ac.update(dummy_lms, "happy")
    cv2.imshow("Avatar", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
