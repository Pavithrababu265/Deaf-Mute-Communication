import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

class GestureClassifier:
    def __init__(self, model_path='models/gesture_model.p'):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def train_model(self, data_path='data/gesture_data.csv'):
        if not os.path.exists(data_path):
            print("Data file not found. Run collect_data.py first.")
            return

        df = pd.read_csv(data_path)
        if df.empty:
            print("dataset is empty")
            return

        X = df.iloc[:, 1:].values # Features
        y = df.iloc[:, 0].values  # Labels

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")

        # Save model
        if not os.path.exists('models'):
            os.makedirs('models')
            
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                # print("Model loaded successfully.")
            except Exception as e:
                print(f"Failed to load model from {self.model_path}: {e}. Discarding old model.")
                self.model = None
        else:
            # print("Model not found. Please train first.")
            pass

    def predict_gesture(self, landmarks):
        if self.model is None:
            return "No Model", 0.0
        
        try:
            if hasattr(self.model, "predict_proba"):
                probas = self.model.predict_proba([landmarks])[0]
                max_prob = np.max(probas)
                print(f"DEBUG: Best Class: {self.model.classes_[np.argmax(probas)]}, Confidence: {max_prob:.2f}")
                
                if max_prob < 0.2: 
                    return "None", max_prob
            
            prediction = self.model.predict([landmarks])
            return prediction[0], max_prob
        except Exception as e:
            print(f"Prediction Error: {e}")
            return "None", 0.0

    def predict_top_n_gestures(self, landmarks, n=5):
        if self.model is None or not hasattr(self.model, "predict_proba"):
            return []
            
        try:
            probas = self.model.predict_proba([landmarks])[0]
            # Get indices of top N probabilities
            top_indices = np.argsort(probas)[-n:][::-1]
            
            top_predictions = []
            for i in top_indices:
                prob = probas[i]
                if prob > 0.05: # Minimum threshold to even consider it as a suggestion
                    cls_name = self.model.classes_[i]
                    # Since we are removing character by character entirely, we filter out 1-letter words here
                    # If the user has 1 letter trained gestures, we'll suggest them as words. 
                    if cls_name not in ("NEXT", "SPACE"): 
                        top_predictions.append((cls_name, prob))
                        
            return top_predictions
        except Exception as e:
            print(f"Top-N Prediction Error: {e}")
            return []

if __name__ == "__main__":
    classifier = GestureClassifier()
    classifier.train_model()
