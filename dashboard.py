import dash
from dash import dcc, html, Input, Output
import pandas as pd
from Codebase.DataManager.data_loader import DataLoader
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
loader = DataLoader()

# Use lowercase column names to match normalized columns
tvws_cols = {
    "date (year-mon-day)", "time (hour-min-sec)",
    "drssi", "dsnr", "urssi", "usnr"
}
soil_cols = {
    "date (year-mon-day)", "time (hour-min-sec)",
    "soil moisture value", "soil temperature (°c)", "soil moisture (%)"
}


loader.load_data("SoilData", 1, soil_cols)
loader.load_data("TVWSScenario", 1, tvws_cols)

soil_df = pd.concat(loader.data["SoilData"]["SoilData_instance1"]["data"])
tvws_df = pd.concat(loader.data["TVWSScenario"]["TVWSScenario_instance1"]["data"])

# Debug print for verification
print("[DEBUG] Loaded soil columns:", soil_df.columns.tolist())
print("[DEBUG] Loaded tvws columns:", tvws_df.columns.tolist())

# Parse time columns
def parse_datetime(df):
    # Always lower the columns list for detection
    cols = [col.strip().lower() for col in df.columns]

    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        # Map back to actual column names using index
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]

        time_str = df[time_col].astype(str).str.replace("-", ":", regex=False)
        return pd.to_datetime(df[date_col] + " " + time_str, errors="coerce")

    print("[WARNING] No recognized datetime columns found.")
    return pd.Series(pd.NaT, index=df.index)


soil_df["datetime"] = parse_datetime(soil_df)
tvws_df["datetime"] = parse_datetime(tvws_df)
print("[DEBUG] Parsed TVWS datetime sample:")
print(tvws_df["datetime"].dropna().head())


soil_df = soil_df.dropna(subset=["datetime"])
tvws_df = tvws_df.dropna(subset=["datetime"])

print("[DEBUG] Parsed datetimes:")
print("Soil data rows:", len(soil_df))
print("TVWS data rows:", len(tvws_df))


available_columns = sorted(set(soil_df.columns) | set(tvws_df.columns))

# Detect range safely
valid_soil = soil_df.dropna(subset=["datetime"])
valid_tvws = tvws_df.dropna(subset=["datetime"])

min_date = pd.Timestamp("2025-01-01")
max_date = pd.Timestamp("2025-12-31")

if not valid_soil.empty and not valid_tvws.empty:
    min_date = min(valid_soil["datetime"].min(), valid_tvws["datetime"].min())
    max_date = max(valid_soil["datetime"].max(), valid_tvws["datetime"].max())
elif not valid_soil.empty:
    min_date = valid_soil["datetime"].min()
    max_date = valid_soil["datetime"].max()
elif not valid_tvws.empty:
    min_date = valid_tvws["datetime"].min()
    max_date = valid_tvws["datetime"].max()

# Dash layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Time Series Dashboard (Dual Y-Axis)"),

    html.Div([
        html.Label("Left Y-Axis (Y1)"),
        dcc.Dropdown(
            id='y1-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value="soil moisture value"
        ),
    ], style={"width": "48%", "display": "inline-block"}),

    html.Div([
        html.Label("Right Y-Axis (Y2)"),
        dcc.Dropdown(
            id='y2-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value="drssi"
        ),
    ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%"}),

    html.Div([
        html.Label("Time Aggregation"),
        dcc.Dropdown(
            id='time-agg',
            options=[
                {"label": "1 minute", "value": "1min"},
                {"label": "5 minutes", "value": "5min"},
                {"label": "1 hour", "value": "1H"},
                {"label": "1 day", "value": "1D"},
            ],
            value="1min"
        ),
    ], style={"width": "48%", "marginTop": "20px"}),

    html.Div([
        html.Label("Select Time Range"),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=min_date.date(),
            max_date_allowed=max_date.date(),
            start_date=min_date.date(),
            end_date=max_date.date(),
            initial_visible_month=min_date.date()
        )
    ], style={"marginTop": "20px"}),

    dcc.Graph(id='time-series'),
    html.Div(id='debug-output', style={'whiteSpace': 'pre-wrap'})
])


@app.callback(
    Output('time-series', 'figure'),
    [
        Input('y1-axis', 'value'),
        Input('y2-axis', 'value'),
        Input('time-agg', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    ]
)
def update_graph(y1_col, y2_col, agg_str, start_date, end_date):
    if y1_col in soil_df.columns:
        y1_data = soil_df[["datetime", y1_col]].copy()
    elif y1_col in tvws_df.columns:
        y1_data = tvws_df[["datetime", y1_col]].copy()
    else:
        return go.Figure().add_annotation(text=f"Y1 column '{y1_col}' not found")

    if y2_col in soil_df.columns:
        y2_data = soil_df[["datetime", y2_col]].copy()
    elif y2_col in tvws_df.columns:
        y2_data = tvws_df[["datetime", y2_col]].copy()
    else:
        return go.Figure().add_annotation(text=f"Y2 column '{y2_col}' not found")

    if y1_data.empty or "datetime" not in y1_data.columns:
        return go.Figure().add_annotation(text=f"No Y1 data for '{y1_col}'")
    if y2_data.empty or "datetime" not in y2_data.columns:
        return go.Figure().add_annotation(text=f"No Y2 data for '{y2_col}'")

    y1_data = y1_data.set_index("datetime").sort_index()
    y2_data = y2_data.set_index("datetime").sort_index()

    if start_date and end_date:
        y1_data = y1_data[start_date:end_date]
        y2_data = y2_data[start_date:end_date]

    if y1_data.empty or y2_data.empty:
        return go.Figure().add_annotation(text="No data in selected time range")

    y1_resampled = y1_data.resample(agg_str).mean().dropna()
    y2_resampled = y2_data.resample(agg_str).mean().dropna()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=y1_resampled.index, y=y1_resampled[y1_col],
        name=f"{y1_col} (Y1)", mode="markers"
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=y2_resampled.index, y=y2_resampled[y2_col],
        name=f"{y2_col} (Y2)", mode="markers"
    ), secondary_y=True)

    fig.update_layout(
        title=f"{y1_col} vs {y2_col} (Time Aggregated: {agg_str})",
        xaxis_title="Time",
        yaxis_title=y1_col,
        yaxis2_title=y2_col,
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        height=600
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
