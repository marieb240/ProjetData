from dash import html

header = html.Header(
    [
        html.H1("Airbnb Paris Dashboard", className="app-title"),
        html.P("Analyse des annonces Airbnb à Paris", className="app-subtitle"),
    ],
    className="app-header",
)
