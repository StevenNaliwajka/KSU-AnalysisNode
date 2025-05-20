import dash
from dash import dcc, html, Input, Output
import pandas as pd
from Codebase.DataManager.old_data_loader import DataLoader
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------
# Extract metadata
# -------------------------

def extract_all_soil_depths(csv_paths):
    depths = set()
    for path in csv_paths:
        try:
            df = pd.read_csv(path, nrows=2, header=None)
            if df.shape[1] >= 2:
                depths.add(str(df.iloc[1, 1]))
        except Exception:
            continue
    return sorted(depths)

def extract_all_tvws_specials(csv_paths):
    specials = set()
    for path in csv_paths:
        try:
            df = pd.read_csv(path, nrows=2, header=None)
            if df.shape[1] >= 9:
                specials.add(str(df.iloc[1, 8]))
        except Exception:
            continue
    return sorted(specials)

data_dir = Path(__file__).resolve().parent / "Data"
soil_depths = {}
tvws_specials = {}

for instance in [1, 2]:
    soil_files = list(data_dir.glob(f"**/SoilData_instance{instance}_*.csv"))
    tvws_files = list(data_dir.glob(f"**/TVWSScenario_instance{instance}_*.csv"))

    depths = extract_all_soil_depths(soil_files)
    specials = extract_all_tvws_specials(tvws_files)

    soil_depths[instance] = ', '.join(f'{d}"' for d in depths) if depths else "?"
    tvws_specials[instance] = ', '.join(f'{v}"' for v in specials) if specials else "?"

# -------------------------
# Load Data
# -------------------------

loader = DataLoader()

tvws_cols = {
    "date (year-mon-day)", "time (hour-min-sec)",
    "drssi", "dsnr", "urssi", "usnr"
}
soil_cols = {
    "date (year-mon-day)", "time (hour-min-sec)",
    "soil moisture value", "soil temperature (°c)", "soil moisture (%)"
}

for i in [1, 2]:
    loader.load_data("SoilData", i, soil_cols)
    loader.load_data("TVWSScenario", i, tvws_cols)

def parse_datetime(df):
    cols = [col.strip().lower() for col in df.columns]
    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]
        time_str = df[time_col].astype(str).str.replace("-", ":", regex=False)
        return pd.to_datetime(df[date_col] + " " + time_str, errors="coerce")
    return pd.Series(pd.NaT, index=df.index)

available_columns = sorted(set(soil_cols | tvws_cols))

# -------------------------
# Dash Layout
# -------------------------

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Time Series Dashboard (Dual Y-Axis)"),

    html.Div([
        html.Label("SoilData Instance"),
        dcc.Dropdown(
            id='soil-instance',
            options=[
                {"label": f"Soil ({soil_depths.get(i, '?')})", "value": i}
                for i in [1, 2]
            ],
            value=1
        ),
    ], style={"width": "48%", "display": "inline-block"}),

    html.Div([
        html.Label("TVWS Instance"),
        dcc.Dropdown(
            id='tvws-instance',
            options=[
                {
                    'label': f"TVWS ({tvws_specials.get(i, '?').replace('\"', '\'')})",
                    'value': i
                }
                for i in [1, 2]
            ],
            value=1
        ),
    ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%"}),

    html.Div([
        html.Label("Left Y-Axis (Y1)"),
        dcc.Dropdown(
            id='y1-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value="soil moisture value"
        ),
    ], style={"width": "48%", "display": "inline-block", "marginTop": "20px"}),

    html.Div([
        html.Label("Right Y-Axis (Y2)"),
        dcc.Dropdown(
            id='y2-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value="drssi"
        ),
    ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%", "marginTop": "20px"}),

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
            start_date="2025-01-01",
            end_date="2025-12-31",
            initial_visible_month="2025-01-01"
        )
    ], style={"marginTop": "20px"}),

    dcc.Graph(id='time-series'),
    html.Div(id='debug-output', style={'whiteSpace': 'pre-wrap'})
])


# -------------------------
# Graph Callback
# -------------------------

@app.callback(
    Output('time-series', 'figure'),
    [
        Input('y1-axis', 'value'),
        Input('y2-axis', 'value'),
        Input('time-agg', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
        Input('soil-instance', 'value'),
        Input('tvws-instance', 'value')
    ]
)
def update_graph(y1_col, y2_col, agg_str, start_date, end_date, soil_instance, tvws_instance):
    soil_key = f"SoilData_instance{soil_instance}"
    tvws_key = f"TVWSScenario_instance{tvws_instance}"

    try:
        soil_df = pd.concat(loader.data["SoilData"][soil_key]["data"]).copy()
        soil_df["datetime"] = parse_datetime(soil_df)
        soil_df = soil_df.dropna(subset=["datetime"])
    except Exception:
        soil_df = pd.DataFrame(columns=["datetime"])

    try:
        tvws_df = pd.concat(loader.data["TVWSScenario"][tvws_key]["data"]).copy()
        tvws_df["datetime"] = parse_datetime(tvws_df)
        tvws_df = tvws_df.dropna(subset=["datetime"])
    except Exception:
        tvws_df = pd.DataFrame(columns=["datetime"])

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
