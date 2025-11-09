# src/pages/home.py

"""
Page d'accueil du dashboard.

Contient :
- une présentation rapide
- des filtres (type de logement, prix)
- un histogramme des prix
- une carte géolocalisée des annonces
"""

from dash import html, dcc, Input, Output, Dash
import plotly.express as px
import pandas as pd


# === Configuration des données ===
# ⚠️ Adapte le chemin et les noms de colonnes aux sorties de votre clean_data.py
CLEANED_PATH = "data/cleaned/airbnb_listings_clean.csv"

PRICE_COL = "price"
ROOM_TYPE_COL = "room_type"
NEIGHBOURHOOD_COL = "neighbourhood"
LAT_COL = "latitude"
LON_COL = "longitude"

# Chargement des données (au lancement de l'app)
df = pd.read_csv(CLEANED_PATH)

# Valeurs par défaut pour les filtres
min_price = int(df[PRICE_COL].min())
max_price = int(df[PRICE_COL].max())

room_type_options = [
    {"label": rt, "value": rt}
    for rt in sorted(df[ROOM_TYPE_COL].dropna().unique())
]


# === Layout de la page d'accueil ===
layout = html.Div(
    children=[
        html.Div(
            style={
                "marginBottom": "18px",
            },
            children=[
                html.H2(
                    "Vue d'ensemble des annonces Airbnb",
                    style={
                        "margin": "0 0 6px 0",
                        "fontSize": "24px",
                        "color": "#111827",
                    },
                ),
                html.P(
                    "Explore les prix, types de logements et leur répartition géographique à partir du jeu de données nettoyé.",
                    style={
                        "margin": "0",
                        "fontSize": "14px",
                        "color": "#6b7280",
                    },
                ),
            ],
        ),
        # Filtres
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "18px",
                "marginBottom": "22px",
            },
            children=[
                html.Div(
                    style={
                        "minWidth": "220px",
                        "flex": "1",
                    },
                    children=[
                        html.Label(
                            "Type de logement",
                            style={
                                "fontWeight": 600,
                                "fontSize": "13px",
                                "color": "#374151",
                            },
                        ),
                        dcc.Dropdown(
                            id="room-type-filter",
                            options=room_type_options,
                            value=[opt["value"] for opt in room_type_options],
                            multi=True,
                            placeholder="Sélectionne un ou plusieurs types",
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "minWidth": "260px",
                        "flex": "1",
                    },
                    children=[
                        html.Label(
                            "Plage de prix (par nuit)",
                            style={
                                "fontWeight": 600,
                                "fontSize": "13px",
                                "color": "#374151",
                            },
                        ),
                        dcc.RangeSlider(
                            id="price-range-filter",
                            min=min_price,
                            max=max_price,
                            value=[min_price, max_price],
                            step=5,
                            tooltip={"placement": "bottom", "always_visible": False},
                            marks={
                                min_price: str(min_price),
                                max_price: str(max_price),
                            },
                        ),
                    ],
                ),
            ],
        ),
        # Graphiques
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1.4fr 1.6fr",
                "gridGap": "20px",
            },
            children=[
                html.Div(
                    children=[
                        html.H3(
                            "Distribution des prix",
                            style={
                                "fontSize": "18px",
                                "marginBottom": "8px",
                                "color": "#111827",
                            },
                        ),
                        dcc.Graph(
                            id="price-histogram",
                            config={"displayModeBar": False},
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.H3(
                            "Localisation des annonces",
                            style={
                                "fontSize": "18px",
                                "marginBottom": "8px",
                                "color": "#111827",
                            },
                        ),
                        dcc.Graph(
                            id="map-scatter",
                            config={"displayModeBar": False},
                        ),
                    ]
                ),
            ],
        ),
    ]
)


# === Callbacks liés à cette page ===
def register_callbacks(app: Dash) -> None:
    """
    Enregistre les callbacks nécessaires à la page d'accueil.

    Args:
        app: instance Dash principale.
    """

    @app.callback(
        Output("price-histogram", "figure"),
        Output("map-scatter", "figure"),
        Input("room-type-filter", "value"),
        Input("price-range-filter", "value"),
    )
    def update_charts(selected_room_types, selected_price_range):
        # Sécurité si aucun type sélectionné
        if not selected_room_types:
            filtered = df.copy()
        else:
            filtered = df[df[ROOM_TYPE_COL].isin(selected_room_types)]

        min_p, max_p = selected_price_range
        filtered = filtered[
            (filtered[PRICE_COL] >= min_p) & (filtered[PRICE_COL] <= max_p)
        ]

        # Histogramme des prix
        hist_fig = px.histogram(
            filtered,
            x=PRICE_COL,
            nbins=40,
        )
        hist_fig.update_layout(
            title="Distribution des prix (après filtres)",
            xaxis_title="Prix par nuit",
            yaxis_title="Nombre d'annonces",
            bargap=0.05,
            margin=dict(l=10, r=10, t=40, b=40),
            template="plotly_white",
        )

        # Carte des annonces
        map_fig = px.scatter_mapbox(
            filtered,
            lat=LAT_COL,
            lon=LON_COL,
            color=ROOM_TYPE_COL,
            hover_name=NEIGHBOURHOOD_COL,
            hover_data={PRICE_COL: True},
            zoom=10,
            height=480,
        )
        map_fig.update_layout(
            mapbox_style="open-street-map",
            margin=dict(l=0, r=0, t=0, b=0),
            legend_title_text="Type de logement",
        )

        return hist_fig, map_fig
