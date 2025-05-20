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
    "soil moisture value", "soil temperature (\u00b0c)", "soil moisture (%)"
}
ambient_cols = {
    "date", "simple date", "outdoor temperature (\u00b0f)", "feels like (\u00b0f)", "dew point (\u00b0f)",
    "wind speed (mph)", "wind gust (mph)", "max daily gust (mph)", "wind direction (\u00b0)",
    "rain rate (in/hr)", "daily rain (in)", "weekly rain (in)", "monthly rain (in)",
    "yearly rain (in)", "relative pressure (inhg)", "humidity (%)", "ultra-violet radiation index",
    "solar radiation (w/m^2)", "indoor temperature (\u00b0f)", "indoor humidity (%)",
    "avg wind direction (10 mins) (\u00b0)", "outdoor battery", "absolute pressure (inhg)",
    "indoor battery", "co2 battery", "indoor feels like (\u00b0f)", "indoor dew point (\u00b0f)"
}

for i in [1, 2]:
    loader.load_data("SoilData", i, soil_cols)
    loader.load_data("TVWSScenario", i, tvws_cols)

loader.load_data("AmbientWeather", 0, ambient_cols)

def parse_datetime(df):
    cols = [col.strip().lower() for col in df.columns]
    if "date (year-mon-day)" in cols and "time (hour-min-sec)" in cols:
        date_col = df.columns[cols.index("date (year-mon-day)")]
        time_col = df.columns[cols.index("time (hour-min-sec)")]
        time_str = df[time_col].astype(str).str.replace("-", ":", regex=False)
        return pd.to_datetime(df[date_col] + " " + time_str, errors="coerce")
    elif "simple date" in cols:
        simple_col = df.columns[cols.index("simple date")]
        return pd.to_datetime(df[simple_col], errors="coerce")
    return pd.Series(pd.NaT, index=df.index)

available_columns = sorted(set(soil_cols | tvws_cols | ambient_cols))

# -------------------------
# Dash Layout
# -------------------------

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("\ud83d\udcca Time Series Dashboard (Dual Y-Axis)"),

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
        html.Label("Third Metric (Y3, plotted on Y1 axis)"),
        dcc.Dropdown(
            id='y3-axis',
            options=[{"label": col, "value": col} for col in available_columns],
            value=None
        ),
    ], style={"width": "48%", "marginTop": "20px"}),

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
        Input('y3-axis', 'value'),  # NEW
        Input('time-agg', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
        Input('soil-instance', 'value'),
        Input('tvws-instance', 'value')
    ]
)
def update_graph(y1_col, y2_col, y3_col, agg_str, start_date, end_date, soil_instance, tvws_instance):
    # Normalize selected column names
    y1_col = y1_col.lower()
    y2_col = y2_col.lower()
    y3_col = y3_col.lower() if y3_col else None

    soil_key = f"SoilData_instance{soil_instance}"
    tvws_key = f"TVWSScenario_instance{tvws_instance}"

    try:
        soil_df = pd.concat(loader.data["SoilData"][soil_key]["data"]).copy()
        soil_df.columns = soil_df.columns.str.lower()
        soil_df["datetime"] = parse_datetime(soil_df)
        soil_df = soil_df.dropna(subset=["datetime"])
    except Exception:
        soil_df = pd.DataFrame(columns=["datetime"])

    try:
        tvws_df = pd.concat(loader.data["TVWSScenario"][tvws_key]["data"]).copy()
        tvws_df.columns = tvws_df.columns.str.lower()
        tvws_df["datetime"] = parse_datetime(tvws_df)
        tvws_df = tvws_df.dropna(subset=["datetime"])
    except Exception:
        tvws_df = pd.DataFrame(columns=["datetime"])

    try:
        ambient_df = pd.concat(loader.data["AmbientWeather"]["AmbientWeather_instance0"]["data"]).copy()
        ambient_df.columns = ambient_df.columns.str.lower()
        ambient_df["datetime"] = parse_datetime(ambient_df)
        ambient_df = ambient_df.dropna(subset=["datetime"])
    except Exception:
        ambient_df = pd.DataFrame(columns=["datetime"])

    # Y1
    if y1_col in soil_df.columns:
        y1_data = soil_df[["datetime", y1_col]].copy()
    elif y1_col in tvws_df.columns:
        y1_data = tvws_df[["datetime", y1_col]].copy()
    elif y1_col in ambient_df.columns:
        y1_data = ambient_df[["datetime", y1_col]].copy()
    else:
        return go.Figure().add_annotation(text=f"Y1 column '{y1_col}' not found")

    # Y2
    if y2_col in soil_df.columns:
        y2_data = soil_df[["datetime", y2_col]].copy()
    elif y2_col in tvws_df.columns:
        y2_data = tvws_df[["datetime", y2_col]].copy()
    elif y2_col in ambient_df.columns:
        y2_data = ambient_df[["datetime", y2_col]].copy()
    else:
        return go.Figure().add_annotation(text=f"Y2 column '{y2_col}' not found")

    # Y3 (optional)
    y3_data = None
    if y3_col:
        if y3_col in soil_df.columns:
            y3_data = soil_df[["datetime", y3_col]].copy()
        elif y3_col in tvws_df.columns:
            y3_data = tvws_df[["datetime", y3_col]].copy()
        elif y3_col in ambient_df.columns:
            y3_data = ambient_df[["datetime", y3_col]].copy()

    # Convert to datetime index and filter by range
    for data in [("y1", y1_data), ("y2", y2_data), ("y3", y3_data)]:
        name, df = data
        if df is not None:
            df.set_index("datetime", inplace=True)
            df.sort_index(inplace=True)
            df = df[start_date:end_date]
            df = df.resample(agg_str).mean().dropna()
            if name == "y1":
                y1_data = df
            elif name == "y2":
                y2_data = df
            elif name == "y3":
                y3_data = df

    # Handle empty data
    if y1_data.empty or y2_data.empty:
        return go.Figure().add_annotation(text="No data in selected time range")

    # Create plot
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=y1_data.index, y=y1_data[y1_col],
        name=f"{y1_col} (Y1)", mode="markers"
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=y2_data.index, y=y2_data[y2_col],
        name=f"{y2_col} (Y2)", mode="markers"
    ), secondary_y=True)

    if y3_col and y3_data is not None and not y3_data.empty:
        fig.add_trace(go.Scatter(
            x=y3_data.index, y=y3_data[y3_col],
            name=f"{y3_col} (Y3)", mode="markers",
            marker=dict(symbol="circle-open", size=6)
        ), secondary_y=False)

    fig.update_layout(
        title=f"{y1_col} vs {y2_col}" + (f" + {y3_col}" if y3_col else "") + f" (Time Aggregated: {agg_str})",
        xaxis_title="Time",
        yaxis_title="Y1 / Y3",
        yaxis2_title="Y2",
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        height=600
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)