# src/components/footer.py

from dash import html


def render_footer() -> html.Footer:
    """
    Render the footer displayed at the bottom of the dashboard.

    Returns:
        A Dash HTML Footer component.
    """
    return html.Footer(
        children=[
            html.P(
                "Projet Data ESIEE 2025 — Réalisé par Marie et [Ton prénom ici]",
                style={
                    "margin": "0",
                    "fontSize": "14px",
                    "color": "#555",
                },
            ),
            html.P(
                "Données issues de l'Open Data | Dashboard réalisé avec Python, Dash & Plotly",
                style={
                    "margin": "2px 0 0 0",
                    "fontSize": "12px",
                    "color": "#7a7a7a",
                },
            ),
        ],
        style={
            "textAlign": "center",
            "padding": "16px 0",
            "borderTop": "1px solid #e5e7eb",
            "backgroundColor": "#f9fafb",
            "marginTop": "auto",  # colle le footer en bas même si peu de contenu
        },
    )
from dash import html

footer = html.Footer(
    [
        html.P("Projet Data - Airbnb Paris • ESIEE", className="footer-text"),
    ],
    className="app-footer",
)
