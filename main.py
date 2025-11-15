from dash import Dash, html
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
        # Sidebar (logo + menu)
        html.Aside(
            [
                html.Div(
                    [
                        html.Div("Airbnb Paris", className="sidebar-logo-main"),
                        html.Div("Data Dashboard", className="sidebar-logo-sub"),
                    ],
                    className="sidebar-logo-block",
                ),
                navbar,
                html.Div(
                    [
                        html.P("Projet Data · ESIEE 2025", className="sidebar-meta"),
                        html.P("Ghita Bensaleh et Marie Bouëtel", className="sidebar-meta-secondary"),
                    ],
                    className="sidebar-footer-block",
                ),
            ],
            className="app-sidebar",
        ),

        # Zone principale (header + contenu des pages + footer)
        html.Div(
            [
                header,
                html.Main(
                    dash.page_container,
                    className="main-content",
                ),
                footer,
            ],
            className="app-main",
        ),
    ],
    className="page-container",
)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
