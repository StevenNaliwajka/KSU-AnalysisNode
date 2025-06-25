# Codebase/Dashboard/callbacks/plot_callbacks.py

from dash import Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Codebase.Dashboard.DashboardApp.datetime_parser import parse_datetime

def _register_plot_callbacks(app, loader):
    @app.callback(
        Output('time-series', 'figure'),
        [
            Input('y1-axis', 'value'),
            Input('y2-axis', 'value'),
            Input('y3-axis', 'value'),
            Input('time-agg', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'),
        ]
    )
    def update_graph(y1_col, y2_col, y3_col, agg_str, start_date, end_date):
        if y1_col == "__none__": y1_col = None
        if y2_col == "__none__": y2_col = None
        if y3_col == "__none__": y3_col = None

        if y1_col is None and y2_col is None and (y3_col is None or y3_col == ""):
            return go.Figure().add_annotation(
                text="Please select at least one Y-axis column.",
                xref="paper", yref="paper", showarrow=False, font=dict(size=16)
            )

        def get_data(col):
            if col is None:
                return pd.DataFrame(columns=["datetime", col])
            col = col.lower()
            for cat in loader.data:
                for subkey in loader.data[cat]:
                    try:
                        data_obj = loader.data[cat][subkey]["data"]
                        df = pd.concat(data_obj).copy() if isinstance(data_obj, list) else data_obj.copy()
                        df.columns = df.columns.str.lower()
                        if col in df.columns:
                            df["datetime"] = parse_datetime(df)
                            df = df.dropna(subset=["datetime"])
                            return df[["datetime", col]]
                    except Exception as e:
                        print(f"[ERROR] Processing {cat} - {subkey}: {e}")
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
                if label == "y1": y1_data = df
                elif label == "y2": y2_data = df
                elif label == "y3": y3_data = df

        if (y1_col and y1_data.empty) and (y2_col and y2_data.empty) and (y3_col and (y3_data is None or y3_data.empty)):
            return go.Figure().add_annotation(text="No data in selected time range")

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        if y1_col and not y1_data.empty:
            fig.add_trace(go.Scatter(x=y1_data.index, y=y1_data[y1_col.lower()],
                                     name=f"{y1_col} (Y1)", mode="markers"),
                          secondary_y=False)

        if y2_col and not y2_data.empty:
            fig.add_trace(go.Scatter(x=y2_data.index, y=y2_data[y2_col.lower()],
                                     name=f"{y2_col} (Y2)", mode="markers"),
                          secondary_y=True)

        if y3_col and y3_data is not None and not y3_data.empty:
            fig.add_trace(go.Scatter(x=y3_data.index, y=y3_data[y3_col.lower()],
                                     name=f"{y3_col} (Y3)", mode="markers",
                                     marker=dict(symbol="circle-open", size=6),
                                     yaxis="y3"))

        fig.update_layout(
            yaxis=dict(title="Y1", side="left"),
            yaxis2=dict(title="Y2", overlaying="y", side="right"),
            yaxis3=dict(title="Y3", anchor="free", overlaying="y", side="right",
                        position=1.0, showgrid=False),
            xaxis_title="Time",
            title=" | ".join(filter(None, [y1_col, y2_col, y3_col])) + f" (Aggregated: {agg_str})",
            legend=dict(x=0.01, y=0.99),
            margin=dict(l=60, r=80, t=60, b=40),
            hovermode="x unified",
            height=600
        )

        return fig
