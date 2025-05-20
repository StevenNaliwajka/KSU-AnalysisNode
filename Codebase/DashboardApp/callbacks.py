from dash import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Codebase.DashboardApp.data_config import loader
from Codebase.DashboardApp.datetime_parser import parse_datetime

def register_callbacks(app, loader):
    @app.callback(
        Output('time-series', 'figure'),
        [
            Input('y1-axis', 'value'),
            Input('y2-axis', 'value'),
            Input('y3-axis', 'value'),
            Input('time-agg', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'),
            Input('soil-instance', 'value'),
            Input('tvws-instance', 'value')
        ]
    )
    def update_graph(y1_col, y2_col, y3_col, agg_str, start_date, end_date, soil_instance, tvws_instance):
        y1_col = y1_col.lower()
        y2_col = y2_col.lower()
        y3_col = y3_col.lower() if y3_col else None

        soil_key = f"SoilData_instance{soil_instance}"
        tvws_key = f"TVWSScenario_instance{tvws_instance}"

        def load_df(category_key, instance_key, parse=True):
            try:
                df = pd.concat(loader.data[category_key][instance_key]["data"]).copy()
                df.columns = df.columns.str.lower()
                if parse:
                    df["datetime"] = parse_datetime(df)
                    df = df.dropna(subset=["datetime"])
                return df
            except Exception:
                return pd.DataFrame(columns=["datetime"])

        soil_df = load_df("SoilData", soil_key)
        tvws_df = load_df("TVWSScenario", tvws_key)
        ambient_df = load_df("AmbientWeather", "AmbientWeather_instance0")

        def get_data(col):
            for df in [soil_df, tvws_df, ambient_df]:
                if col and col in df.columns:
                    return df[["datetime", col]].copy()
            return pd.DataFrame(columns=["datetime", col])

        y1_data = get_data(y1_col)
        y2_data = get_data(y2_col)
        y3_data = get_data(y3_col) if y3_col else None

        for label, df in [("y1", y1_data), ("y2", y2_data), ("y3", y3_data)]:
            if df is not None and not df.empty:
                df.set_index("datetime", inplace=True)
                df.sort_index(inplace=True)
                df = df[start_date:end_date]
                df = df.resample(agg_str).mean().dropna()
                if label == "y1":
                    y1_data = df
                elif label == "y2":
                    y2_data = df
                elif label == "y3":
                    y3_data = df

        if y1_data.empty or y2_data.empty:
            return go.Figure().add_annotation(text="No data in selected time range")

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
                marker=dict(symbol="circle-open", size=6),
                yaxis="y3"
            ))

        fig.update_layout(
            yaxis=dict(title="Y1", side="left"),
            yaxis2=dict(title="Y2", overlaying="y", side="right"),
            yaxis3=dict(
                title="Y3",
                anchor="free",
                overlaying="y",
                side="right",
                position=1.0,  # max allowed
                showgrid=False
            ),
            xaxis_title="Time",
            title=f"{y1_col} vs {y2_col}" + (f" + {y3_col}" if y3_col else "") + f" (Time Aggregated: {agg_str})",
            legend=dict(x=0.01, y=0.99),
            margin=dict(l=60, r=80, t=60, b=40),
            hovermode="x unified",
            height=600
        )

        return fig
