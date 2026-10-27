import pandas as pd
import numpy as np
import random

class GesturePlayer:
    def __init__(self, data_path='data/gesture_data.csv'):
        self.data_path = data_path
        self.data_by_label = {}
        self.load_data()

    def load_data(self):
        try:
            df = pd.read_csv(self.data_path)
            # Assuming Column 0 is Label, Columns 1..126 are features
            # Group by label for quick access
            grouped = df.groupby(df.columns[0])
            for name, group in grouped:
                self.data_by_label[name] = group.iloc[:, 1:].values
            print(f"GesturePlayer loaded gestures: {list(self.data_by_label.keys())}")
        except Exception as e:
            print(f"Error loading gesture data: {e}")

    def get_gesture_landmarks(self, gesture_name):
        """
        Returns a formatted list of landmarks for the avatar to display.
        Returns None if gesture not found.
        """
        # Case insensitive match
        found_key = None
        for key in self.data_by_label.keys():
            if key.lower() == gesture_name.lower():
                found_key = key
                break
        
        if not found_key:
            return None

        # Pick a random sample from the recorded data for variety
        samples = self.data_by_label[found_key]
        if len(samples) == 0:
            return None
        
        raw_row = samples[random.randint(0, len(samples) - 1)]
        
        # Convert raw flat world coordinates to formatted screen coordinates for Avatar
        return self._format_for_avatar(raw_row)

    def _format_for_avatar(self, flat_data):
        """
        Converts 126-float array (Normalized Coords 0-1) into 
        Avatar-friendly [[id, x, y, z], ...] list (Screen Coords).
        Auto-centers and scales the hand to fit the 400x400 canvas.
        """
        # 1. Parse all points first to find bounds
        hands_points = []
        
        # Helper to parse chunk
        def parse_chunk(chunk, hand_offset):
            points = []
            non_zero_count = 0
            for i in range(21):
                idx = i * 3
                wx = chunk[idx]
                wy = chunk[idx+1]
                wz = chunk[idx+2]
                
                if wx == 0 and wy == 0 and wz == 0:
                    continue
                
                non_zero_count += 1
                points.append({'id': i, 'x': wx, 'y': wy, 'z': wz})
            
            if non_zero_count > 5:
                return points
            return []

        h1_pts = parse_chunk(flat_data[0:63], 0)
        h2_pts = parse_chunk(flat_data[63:126], 21)
        
        all_pts = h1_pts + h2_pts
        
        if not all_pts:
            return []
            
        # 2. Find Bounds
        min_x = min(p['x'] for p in all_pts)
        max_x = max(p['x'] for p in all_pts)
        min_y = min(p['y'] for p in all_pts)
        max_y = max(p['y'] for p in all_pts)
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        width = max_x - min_x
        height = max_y - min_y
        
        # Avoid division by zero
        if width == 0: width = 0.1
        if height == 0: height = 0.1
        
        # 3. Determine Scale
        # We want the larger dimension to fill about 250 pixels of the 400x400 canvas
        target_size = 250.0
        scale = target_size / max(width, height)
        
        # Cap scale to avoid exploding tiny noise (though unlikely with valid hand data)
        scale = min(scale, 1000) 
        
        # 4. Transform Points
        formatted_lms = []
        canvas_center = 200 # 400/2
        
        # Process Hand 1
        for p in h1_pts:
            # Center at (0,0) then scale, then move to canvas center
            sx = int((p['x'] - center_x) * scale + canvas_center)
            sy = int((p['y'] - center_y) * scale + canvas_center)
            formatted_lms.append([p['id'], sx, sy, p['z']]) # ID 0-20
            
        # Process Hand 2
        # For AvatarController, we might need distinct IDs if it draws separate lines?
        # AvatarController.connections uses 0-20. 
        # If we send two hands, we usually just send a flat list [[id, x,y,z], ...]
        # The current AvatarController draws lines for any points present in the dict if ID matches 0-20.
        # It will draw overlapping lines if we have duplicate IDs (0-20 for both hands).
        # This is actually fine for visual "ghosting" overlap, 
        # BUT ideally we should handle L/R hands. 
        # However, `AvatarController` logic is simple: 
        # `points = {lm[0]: (lm[1], lm[2]) ...}` 
        # This Dictionary comprehension will OVERWRITE the first hand with the second if IDs match!
        # WARNING: We can only draw ONE hand properly with current AvatarController if IDs clash.
        # OR we need to verify if AvatarController supports multiple hands.
        # It creates a dict `points`. So it only supports one set of 0-20 IDs.
        
        # FIX: For now, if we have two hands, we might lose one visuals. 
        # But `gesture_player` usually plays back single hand gestures mostly? 
        # Or we can just return the dominant hand (more points).
        # Let's check which hand has points.
        
        # If both hands exist, AvatarController needs update to handle 21-41 IDs or separate lists.
        # For this turn, I will just append them. If one overwrites, at least one shows.
        # If I want both, I'd need to modify AvatarController.
        # Given the task scope, let's just get *something* visible first.
        
        for p in h2_pts:
             sx = int((p['x'] - center_x) * scale + canvas_center)
             sy = int((p['y'] - center_y) * scale + canvas_center)
             formatted_lms.append([p['id'] + 21, sx, sy, p['z']])

        return formatted_lms
