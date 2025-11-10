from dash import html, dcc

navbar = html.Nav(
    [
        dcc.Link("Accueil", href="/", className="nav-link"),
        dcc.Link(" Analyse détaillée", href="/more", className="nav-link"),
    ],
    className="app-navbar",
)
