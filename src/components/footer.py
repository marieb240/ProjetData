from dash import html

footer = html.Footer(
    [
        html.P(
            """Projet Data - ESIEE 2025 · Ghita BENSALEH & Marie BOUËTEL""" ,
            className="footer-text-main",
        ),
        html.P(
            "Données : Airbnb Listings ",
            className="footer-text-sub",
        ),
    ],
    className="app-footer",
)
