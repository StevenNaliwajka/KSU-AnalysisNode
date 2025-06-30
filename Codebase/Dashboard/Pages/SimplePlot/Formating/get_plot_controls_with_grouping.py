from dash import html, dcc
from Codebase.Dashboard.Pages.UniversalFormating.build_date_range_picker import build_date_range_picker
from Codebase.Dashboard.Pages.UniversalFormating.get_plot_label_inputs import get_plot_label_inputs
from Codebase.Dashboard.Pages.UniversalFormating.get_filter_and_extra_dropdowns import get_filter_and_extra_dropdowns


def get_plot_controls_with_grouping():
    return html.Div([
        # ✅ Store for sync data range logic
        dcc.Store(id="plot-data-store"),

        html.Div([
            html.H4("Plot Controls", style={"marginBottom": "20px"}),

            html.Div([
                # Left side — plot title and Y axis labels
                html.Div(
                    get_plot_label_inputs(),
                    style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}
                ),

                # Right side — grouped box for calendar, sync button, and link range
                html.Div([
                    build_date_range_picker(),

                    html.Button(
                        "Auto-Sync to Plot Overlap",
                        id="auto-sync-date-range-button",
                        n_clicks=0,
                        style={
                            "marginTop": "10px",
                            "width": "100%",
                            "backgroundColor": "#007bff",
                            "color": "white",
                            "border": "none",
                            "padding": "8px",
                            "borderRadius": "5px",
                            "cursor": "pointer"
                        }
                    ),

                    html.Label("Link Axis Ranges (sync scales)", style={"marginTop": "15px", "fontWeight": "bold"}),

                    dcc.Dropdown(
                        id="link-axes-dropdown",
                        options=[
                            {"label": "Y1 & Y2", "value": "y1-y2"},
                            {"label": "Y1 & Y3", "value": "y1-y3"},
                            {"label": "Y2 & Y3", "value": "y2-y3"},
                        ],
                        multi=True,
                        placeholder="Select axes to link"
                    )
                ], style={
                    "width": "48%",
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "marginLeft": "4%"
                }),
            ]),

        ], style={
            "border": "1px solid #ccc",
            "borderRadius": "10px",
            "padding": "20px",
            "margin": "10px 0",
            "backgroundColor": "#f9f9f9"
        })
    ])
