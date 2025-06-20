# poly_predict.py

import pandas as pd
from Codebase.CorrelationModeling.metrics import compute_metrics

def predict_and_evaluate(model, df: pd.DataFrame, input_cols: list, output_col: str = None):
    X = df[input_cols]
    y_pred = model.predict(X)

    if output_col and output_col in df.columns:
        y_true = df[output_col]
        metrics = compute_metrics(y_true, y_pred)
        return {"y_true": y_true, "y_pred": y_pred, "metrics": metrics}
    else:
        return {"y_pred": y_pred}
