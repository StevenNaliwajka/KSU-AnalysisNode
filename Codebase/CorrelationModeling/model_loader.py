# model_loader.py

import joblib

def save_model(model, path: str):
    joblib.dump(model, path)
    print(f"[INFO] Model saved to {path}")

def load_model(path: str):
    model = joblib.load(path)
    print(f"[INFO] Model loaded from {path}")
    return model
