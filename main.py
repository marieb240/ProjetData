# main.py

"""
Point d'entrée du dashboard Projet Data (Airbnb / Open Data).

- Lance l'application Dash
- Gère la navigation entre les pages :
    /        -> page d'accueil (home)
    /simple  -> page simple
    /about   -> page "À propos"
"""

from dash import Dash, html, dcc, Input, Output

from src.components.header import render_header
from src.components.navbar import render_navbar
from src.components.footer import render_footer

# ⚠ Ces imports supposent que tu as :
# src/pages/home.py   avec une variable `layout`
# src/pages/simple.py avec une variable `layout`
# src/pages/about.py  avec une variable `layout`
from src.pages.home import layout as home_layout
from src.pages.simple import layout as simple_layout
from src.pages.about import layout as about_layout


def create_app() -> Dash:
    """
    Create and configure the Dash application.

    Returns:
        Configured Dash app instance.
    """
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,  # autorise les layouts multipages
    )
    app.title = "Dashboard Open Data"

    # Layout global : header + navbar + zone de contenu + footer
    app.layout = html.Div(
        id="app-root",
        style={
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "backgroundColor": "#f9fafb",
            "fontFamily": "system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
        },
        children=[
            dcc.Location(id="url"),  # lit l'URL courante
            render_header("Dashboard Open Data"),
            render_navbar(),
            html.Div(
                id="page-content",
                style={
                    "flex": "1",
                    "padding": "18px 24px",
                    "maxWidth": "1400px",
                    "margin": "0 auto",
                },
            ),
            render_footer(),
        ],
    )

    # Routing : choisi quel layout afficher selon le pathname
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def display_page(pathname: str):
        """
        Route the user to the correct page based on URL.
        """
        if pathname in ("/", "/home", None):
            return home_layout
        if pathname == "/simple":
            return simple_layout
        if pathname == "/about":
            return about_layout

        # Page 404 simple
        return html.Div(
            style={
                "padding": "40px 0",
                "textAlign": "center",
            },
            children=[
                html.H2("404 - Page introuvable"),
                html.P("La page demandée n'existe pas sur ce dashboard."),
                dcc.Link("⬅ Retour à l'accueil", href="/"),
            ],
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)
