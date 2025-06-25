import plotly.graph_objs as go

def format_timeseries_figure(
    df,
    y1_col=None,
    y2_col=None,
    y3_col=None,
    x_col="datetime",
    plot_title="Time Series Data",
    y1_label="Y1 Axis",
    y2_label="Y2 Axis"
):
    fig = go.Figure()

    if y1_col and y1_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y1_col],
            name=f"{y1_label}",
            yaxis="y1", mode="markers"
        ))

    if y2_col and y2_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y2_col],
            name=f"{y2_label}",
            yaxis="y2", mode="markers"
        ))

    if y3_col and y3_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y3_col],
            name=f"{y3_col}",  # uses original column name for Y3
            yaxis="y1", mode="markers", line=dict(dash="dot")
        ))

    layout = dict(
        title={"text": plot_title, "x": 0.5, "xanchor": "center"},
        xaxis=dict(title="Time"),
        yaxis=dict(
            title=y1_label,
            side="left"
        ),
        legend=dict(x=0, y=1.1, orientation="h"),
        margin=dict(t=40, b=40, l=40, r=40),
        height=600,
    )

    if y2_col and y2_col in df.columns:
        layout["yaxis2"] = dict(
            title=y2_label,
            side="right",
            overlaying="y"
        )

    fig.update_layout(**layout)
    return fig
