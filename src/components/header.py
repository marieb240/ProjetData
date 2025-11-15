from dash import html

header = html.Header(
    [
        html.Div(
            [
                html.H1("Airbnb Paris Dashboard", className="app-title"),
                html.P(
                    "Analyse des annonces Airbnb à Paris",
                    className="app-subtitle",
                ),
            ],
            className="app-title-block",
        ),
        html.Div(
            [
                html.Div("Airbnb · Open Data", className="tag-pill"),
                html.Div("2025", className="tag-pill tag-soft"),
            ],
            className="header-right",
        ),
    ],
    className="app-header",
)
