import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

def train_emotion_model():
    data_path = 'data/emotion_data.csv'
    model_path = 'models/emotion_model.p'
    
    if not os.path.exists(data_path):
        print("Data file not found. Run collect_emotion_data.py first.")
        return

    print("Loading dataset...")
    df = pd.read_csv(data_path)
    if df.empty:
        print("Dataset is empty.")
        return

    print(f"Training on {len(df)} samples...")
    X = df.iloc[:, 1:].values
    y = df.iloc[:, 0].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    if not os.path.exists('models'):
        os.makedirs('models')
        
    with open(model_path, 'wb') as f:
        pickle.dump(clf, f)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_emotion_model()
