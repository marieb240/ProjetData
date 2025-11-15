from dash import html

header = html.Header(
    [
        html.Div(
            [
                html.H1("Dashboard", className="app-title"),
                html.P(
                    "Analyse des annonces Airbnb à Paris",
                    className="app-subtitle",
                ),
            ],
            className="app-title-block",
        ),
    ],
    className="app-header",
)
