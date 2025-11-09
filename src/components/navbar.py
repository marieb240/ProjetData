from dash import html, dcc


# Style commun pour les liens de navigation
_LINK_STYLE = {
    "padding": "10px 14px",
    "borderRadius": "10px",
    "textDecoration": "none",
    "fontWeight": 600,
    "color": "white",
}


def render_navbar() -> html.Nav:
    """
    Render the top navigation bar of the dashboard.

    Returns:
        A Dash HTML Nav component containing navigation links.
    """
    return html.Nav(
        children=[
            dcc.Link("Accueil", href="/", style=_LINK_STYLE),
            dcc.Link("Page simple", href="/simple", style=_LINK_STYLE),
            dcc.Link("À propos", href="/about", style=_LINK_STYLE),
        ],
        style={
            "backgroundColor": "#34495e",
            "padding": "10px 16px",
            "display": "flex",
            "justifyContent": "center",
            "gap": "12px",
            "position": "sticky",
            "top": "60px",  # juste sous ton header
            "zIndex": 9,
        },
    )
