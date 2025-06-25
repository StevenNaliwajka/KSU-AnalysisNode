import plotly.graph_objs as go

def format_timeseries_figure(df, y1_col=None, y2_col=None, y3_col=None, x_col="datetime"):
    fig = go.Figure()

    if y1_col:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y1_col], name=f"Y1: {y1_col.title()}",
            yaxis="y1", mode="markers"
        ))

    if y2_col:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y2_col], name=f"Y2: {y2_col.title()}",
            yaxis="y2", mode="markers"
        ))

    if y3_col:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y3_col], name=f"Y3: {y3_col.title()} (Y1 Axis)",
            yaxis="y1", mode="markers", line=dict(dash="dot")
        ))

    layout = dict(
        title="Time Series Data",
        xaxis=dict(title="Time"),
        yaxis=dict(
            title=y1_col.title() if y1_col else "Y1",
            side="left"
        ),
        legend=dict(x=0, y=1.1, orientation="h"),
        margin=dict(t=40, b=40, l=40, r=40),
        height=600,
    )

    if y2_col:
        layout["yaxis2"] = dict(
            title=y2_col.title(),
            side="right",
            overlaying="y"
        )

    fig.update_layout(**layout)
    return fig
