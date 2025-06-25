import joblib

def save_model(model, path: str):
    joblib.dump(model, path)
    print(f"[INFO] Model saved to {path}")