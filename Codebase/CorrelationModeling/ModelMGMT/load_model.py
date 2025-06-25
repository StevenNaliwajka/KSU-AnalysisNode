import joblib

def load_model(path: str):
    model = joblib.load(path)
    print(f"[INFO] Model loaded from {path}")
    return model
