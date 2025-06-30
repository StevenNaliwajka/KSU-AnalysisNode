from dash import html, dcc

def build_date_range_picker():
    return html.Div([
        html.Label("Select Date Range:"),
        dcc.DatePickerRange(
            id="date-range-picker",
            display_format="YYYY-MM-DD",
            start_date_placeholder_text="Start Date",
            end_date_placeholder_text="End Date",
            clearable=True
        )
    ])
