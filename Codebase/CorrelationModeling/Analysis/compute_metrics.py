# metrics.py

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def compute_metrics(y_true, y_pred):
    return {
        "MSE": mean_squared_error(y_true, y_pred),
        "MAE": mean_absolute_error(y_true, y_pred),
        "R²": r2_score(y_true, y_pred)
    }
