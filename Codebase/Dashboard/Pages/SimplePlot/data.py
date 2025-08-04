import dash
from dash import html, dcc

from Codebase.Dashboard.Pages.SimplePlot.Formating.get_plot_controls_with_grouping import \
    get_plot_controls_with_grouping
from Codebase.Dashboard.Pages.SimplePlot.Formating.row_layout import row_layout

# Register the page in the multi-page Dash app
dash.register_page(__name__, path="/data", name="Plot Value")

layout = html.Div([
    dcc.Interval(id="page-init-trigger", interval=300, n_intervals=0, max_intervals=1),
    dcc.Store(id="loader-store"),

    html.Div([
        # Row 1: Y1
        row_layout(
            row_id="y1-row",
            dropdown_id="dropdown-1",
            special_id="dropdown-special-1",
            conditional_id="conditional-1",
            placeholder="Select Data Source",
            time_grouping_id="time-grouping-y1",
            outlier_filter_id="outlier-filter-y1",
            extra_transform_id="extra-transform-y1"
        ),
        # Row 2: Y2
        row_layout(
            row_id="y2-row",
            dropdown_id="dropdown-2",
            special_id="dropdown-special-2",
            conditional_id="conditional-2",
            placeholder="Select Data Source",
            time_grouping_id="time-grouping-y2",
            outlier_filter_id="outlier-filter-y2",
            extra_transform_id="extra-transform-y2"
        ),
        # Row 3: Y3
        row_layout(
            row_id="y3-row",
            dropdown_id="dropdown-3",
            special_id="dropdown-special-3",
            conditional_id="conditional-3",
            placeholder="Select Data Source",
            time_grouping_id="time-grouping-y3",
            outlier_filter_id="outlier-filter-y3",
            extra_transform_id="extra-transform-y3"
        ),

        # ✅ LCD Sync Button
        html.Div([
            html.Button(
                "Auto-Sync Time Grouping to LCD",
                id="lcd-sync-button",
                n_clicks=0,
                style={
                    "marginTop": "15px",
                    "backgroundColor": "#007bff",
                    "color": "white",
                    "border": "none",
                    "padding": "10px 20px",
                    "borderRadius": "6px",
                    "cursor": "pointer",
                    "fontWeight": "bold"
                }
            )
        ], style={"textAlign": "center"})
    ]),

    get_plot_controls_with_grouping(),

    html.Div(id="plot-container"),
])
