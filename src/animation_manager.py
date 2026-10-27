import json
import os
import numpy as np

class AnimationManager:
    def __init__(self, data_dir='data/animations'):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save_animation(self, name, frames, duration=2.0):
        """
        Saves animation data to JSON.
        frames: list of lists (landmarks flattened or structured)
        """
        file_path = os.path.join(self.data_dir, f"{name}.json")
        data = {
            "name": name,
            "duration": duration,
            "frame_count": len(frames),
            "frames": frames
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print(f"Animation '{name}' saved to {file_path}")

    def load_animation(self, name):
        file_path = os.path.join(self.data_dir, f"{name}.json")
        if not os.path.exists(file_path):
            print(f"Animation '{name}' not found.")
            return None
            
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
