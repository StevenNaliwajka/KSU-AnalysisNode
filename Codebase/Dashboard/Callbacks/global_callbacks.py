from dash import Input, Output, ctx

def register_callbacks(app):
    @app.callback(
        Output("url", "pathname"),
        Input("function-selector", "value"),
        prevent_initial_call=True
    )
    def route_to_page(path):
        current = ctx.triggered_id
        if not path:
            return dash.no_update
        return path
