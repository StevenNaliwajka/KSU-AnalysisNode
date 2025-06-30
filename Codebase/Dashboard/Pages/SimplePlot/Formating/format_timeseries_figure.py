import plotly.graph_objs as go

def format_timeseries_figure(
    df,
    y1_col=None,
    y2_col=None,
    y3_col=None,
    x_col="datetime",
    plot_title="Time Series Data",
    y1_label="Y1 Axis",
    y2_label="Y2 Axis",
    y3_label="Y3 Axis",
    grouping_info=None,
    shared_ranges=None
):
    fig = go.Figure()

    def build_legend_label(label, role):
        if grouping_info and role in grouping_info:
            base = grouping_info[role].get("base", "—")
            blocked = grouping_info[role].get("blocked", "—")
            return f"{label} (Collected every {base}, Averaged to {blocked})"
        return label

    if y1_col and y1_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y1_col],
            name=build_legend_label(y1_label, "y1"),
            yaxis="y1", mode="markers"
        ))

    if y2_col and y2_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y2_col],
            name=build_legend_label(y2_label, "y2"),
            yaxis="y2", mode="markers"
        ))

    if y3_col and y3_col in df.columns:
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[y3_col],
            name=build_legend_label(y3_label, "y3"),
            yaxis="y3", mode="markers"
        ))

    def get_range_for_axis(role):
        if shared_ranges and role in shared_ranges:
            ymin, ymax = shared_ranges[role]
            return [ymin, ymax]
        return None

    layout = dict(
        title=dict(
            text=plot_title,
            x=0.5,
            xanchor="center",
            font=dict(size=32)
        ),
        xaxis=dict(
            title=dict(text="Time", font=dict(size=24)),
            tickfont=dict(size=24)
        ),
        yaxis=dict(
            title=dict(text=y1_label, font=dict(size=24)),
            tickfont=dict(size=24),
            side="left",
            range=get_range_for_axis("y1")
        ),
        legend=dict(
            x=0,
            y=1.1,
            orientation="h",
            font=dict(size=20)
        ),
        font=dict(size=24),
        margin=dict(t=100, b=80, l=80, r=140),
        height=600,
    )

    if y2_col and y2_col in df.columns:
        layout["yaxis2"] = dict(
            title=dict(text=y2_label, font=dict(size=24)),
            tickfont=dict(size=24),
            side="right",
            overlaying="y",
            anchor="x",
            range=get_range_for_axis("y2")
        )

    if y3_col and y3_col in df.columns:
        layout["yaxis3"] = dict(
            title=dict(text=y3_label, font=dict(size=24)),
            tickfont=dict(size=24),
            side="right",
            overlaying="y",
            anchor="free",
            position=.96,  # ⬅️ Move it slightly to the right of y2
            range=get_range_for_axis("y3")
        )

    fig.update_layout(**layout)
    return fig
