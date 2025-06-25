# poly_train.py

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import pandas as pd

def poly_train(df: pd.DataFrame, input_cols: list, output_col: str, degree: int = 2):
    X = df[input_cols]
    y = df[output_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = Pipeline([
        ('poly', PolynomialFeatures(degree=degree)),
        ('regressor', LinearRegression())
    ])

    model.fit(X_train, y_train)
    r2_score = model.score(X_test, y_test)

    return model, r2_score
