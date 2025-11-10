import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from pathlib import Path

dash.register_page(
    __name__,
    path="/more",
    name="Analyse détaillée",
)

DATA_PATH = Path("data/cleaned/airbnb_paris_clean.csv")

if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
else:
    df = None

fig_price_dist = (
    px.histogram(
        df,
        x="price",
        nbins=50,
        title="Distribution des prix par nuit (€)",
    )
    if df is not None and "price" in df.columns
    else None
)

fig_room_type = (
    px.bar(
        df["room_type"].value_counts().reset_index(),
        x="index",
        y="room_type",
        labels={"index": "Type de logement", "room_type": "Nombre d’annonces"},
        title="Répartition par type de logement",
    )
    if df is not None and "room_type" in df.columns
    else None
)

layout = html.Div(
    [
        html.H2("Analyse détaillée", className="section-title"),
        html.P(
            "Visualisation des distributions de prix et des types de logements Airbnb à Paris.",
            className="section-subtitle",
        ),

        html.Div(
            [
                dcc.Graph(figure=fig_price_dist) if fig_price_dist else html.P(
                    "Données indisponibles pour la distribution des prix."
                ),
            ],
            className="chart-block",
        ),

        html.Div(
            [
                dcc.Graph(figure=fig_room_type) if fig_room_type else html.P(
                    "Données indisponibles pour les types de logements."
                ),
            ],
            className="chart-block",
        ),
    ],
    className="page-content",
)
