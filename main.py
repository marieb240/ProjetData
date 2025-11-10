from dash import Dash, html
import dash

from src.components.header import header
from src.components.navbar import navbar
from src.components.footer import footer

app = Dash(__name__, use_pages=True, pages_folder="src/pages")
server = app.server  # utile si déploiement

app.layout = html.Div(
    [
        header,
        navbar,
        dash.page_container,  # ici Dash affichera le contenu des pages
        footer,
    ],
    className="page-container",
)

if __name__ == "__main__":
    app.run(debug=True)

