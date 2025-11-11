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
        df[df["price"] < 500], 
        x="price",
        nbins=60,
        title="Distribution des prix par nuit (€)",
    )
    if df is not None and "price" in df.columns
    else None
)

fig_room_type = None

if df is not None and "room_type" in df.columns:
    # value_counts donne un DF avec colonnes ['room_type', 'count'] après reset_index
    rt_counts = df["room_type"].value_counts().reset_index()
    rt_counts.columns = ["room_type", "count"]  # on force les noms, uniques et propres

    fig_room_type = px.bar(
        rt_counts,
        x="room_type",
        y="count",
        labels={"room_type": "Type de logement", "count": "Nombre d’annonces"},
        title="Répartition par type de logement",
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
