from dash import Dash, html, dcc
import dash

from src.components.header import header
from src.components.navbar import navbar
from src.components.footer import footer
from src.utils.data_access import ensure_data_ready

# ensure that data is ready before starting the app
ensure_data_ready()

app = Dash(__name__, use_pages=True, pages_folder="src/pages")
server = app.server  # utile si déploiement

app.layout = html.Div(
    [
        # Mini-sidebar à gauche
        html.Div(
            [
                dcc.Link("Données ", href="/", className="side-link"),
                dcc.Link("Carte des Airbnbs", href="/more", className="side-link"),
            ],
            className="side-navbar",
        ),

        # Zone principale
        html.Div(
            [
                header,
                html.Main(dash.page_container, className="main-content"),
                footer,
            ],
            className="content-wrapper",
        )
    ],
    className="page-layout",
)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
