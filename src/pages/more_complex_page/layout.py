import dash
import numpy as np
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from typing import Any


from src.utils.data_access import load_dataframe

dash.register_page(
    __name__,
    path="/more",
    name="Analyse détaillée",
)

# ---------- Chargement des données ----------
try:
    df_base = load_dataframe()
except Exception:
    df_base = pd.DataFrame()

if df_base is None:
    df_base = pd.DataFrame()

# On garde uniquement les colonnes utiles si elles existent
expected_cols = [
    "price",
    "room_type",
    "latitude",
    "longitude",
    "district",
    "review_scores_rating",
]
for col in expected_cols:
    if col not in df_base.columns:
        df_base[col] = pd.NA

df_base = df_base.copy()
df_base = df_base.dropna(subset=["latitude", "longitude"])

# Nettoyage léger des prix pour les graphes
if not df_base.empty:
    df_base = df_base[df_base["price"] > 0]
    q01 = df_base["price"].quantile(0.01)
    q99 = df_base["price"].quantile(0.99)
    df_base = df_base[df_base["price"].between(q01, q99)]

# ---------- Options des filtres ----------

# Arrondissements
def _district_sort_key(x: str) -> tuple[int, str]:
    """
    Clé de tri pour les arrondissements :
    - d'abord ceux qui sont numériques (01, 02, ..., 20)
    - ensuite les autres valeurs éventuelles, triées alpha.
    """
    x_str = str(x)
    try:
        # on met les arrondissements numériques en premier, formatés sur 2 chiffres
        return (0, f"{int(x_str):02d}")
    except Exception:
        # tout le reste passe après, trié alphabétiquement
        return (1, x_str)

# Liste des arrondissements
arr_options: list[dict[str, Any]] = [
    {"label": "Tous les arrondissements", "value": "__ALL__"},
]

if "district" in df_base.columns:
    uniq = (
        df_base["district"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    uniq = sorted(uniq, key=_district_sort_key)
    arr_options.extend(
        {"label": v, "value": v} for v in uniq
    )

# Types de logements
room_type_options: list[dict[str, Any]]
if "room_type" in df_base.columns:
    uniq_rt = (
        df_base["room_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    room_type_options = [{"label": rt, "value": rt} for rt in sorted(uniq_rt)]
else:
    room_type_options = []

# Plage de prix
if not df_base.empty:
    price_min = int(df_base["price"].quantile(0.05))
    price_max = int(df_base["price"].quantile(0.95))
else:
    price_min, price_max = 0, 500

# ---------- Aides pour graphes vides ----------


def _empty_map_figure() -> go.Figure:
    fig = px.scatter_mapbox(
        lat=[],
        lon=[],
        zoom=10,
        center={"lat": 48.8566, "lon": 2.3522},
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=40, b=0),
        title="Carte des annonces (aucune donnée à afficher)",
    )
    return fig


def _empty_hist_figure() -> go.Figure:
    fig = px.histogram(x=[])
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis_title="Prix par nuit (€)",
        yaxis_title="Nombre d'annonces",
        title="Distribution des prix (aucune donnée à afficher)",
    )
    return fig



# ---------- Layout de la page ----------

layout = html.Div(
    [
        html.H2("Analyse détaillée des annonces", className="section-title"),
        html.P(
            "Explorez les annonces Airbnb à Paris par arrondissement, niveau de prix et type de logement.",
            className="section-subtitle",
        ),

        # Filtres
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Arrondissement"),
                        dcc.Dropdown(
                            id="more-arrondissement",
                            options=arr_options, #type: ignore
                            value="__ALL__",
                            clearable=False,
                        ),
                    ],
                    className="control-item",
                ),
                html.Div(
                    [
                        html.Label("Types de logements"),
                        dcc.Checklist(
                            id="more-room-type",
                            options=room_type_options, #type: ignore
                            value=[opt["value"] for opt in room_type_options],
                            inline=True,
                        ),
                    ],
                    className="control-item",
                ),
                html.Div(
                    [
                        html.Label("Prix maximum par nuit"),
                        dcc.Slider(
                            id="more-price-max",
                            min=price_min,
                            max=price_max,
                            step=5,
                            value=price_max,
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                        html.Div(
                            id="more-price-max-label",
                            className="slider-value-label",
                        ),
                    ],
                    className="control-item control-item-wide",
                ),
            ],
            className="controls",
        ),

        # Deux colonnes : gauche = cartes, droite = résumé
        html.Div(
            [
                # Colonne gauche : carte + histogramme
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="more-map",
                                    figure=_empty_map_figure(),
                                    config={"displayModeBar": False},
                                ),
                            ],
                            className="chart-block",
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="more-hist",
                                    figure=_empty_hist_figure(),
                                    config={"displayModeBar": False},
                                ),
                            ],
                            className="chart-block",
                        ),
                    ],
                    className="left-panel",
                ),

                # Colonne droite : résumé et détails
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Résumé de la sélection",
                                    className="section-subtitle",
                                ),
                                html.Div(
                                    id="more-summary",
                                    className="section-text",
                                ),
                            ],
                            className="analysis-block details-panel",
                        ),
                    ],
                    className="right-panel",
                ),
            ],
            className="main-two-cols",
        ),
    ],
    className="page-content",
)


# ---------- Callback d'actualisation ----------


@callback(
    Output("more-map", "figure"),
    Output("more-hist", "figure"),
    Output("more-summary", "children"),
    Output("more-price-max-label", "children"),
    Input("more-arrondissement", "value"),
    Input("more-room-type", "value"),
    Input("more-price-max", "value"),
)
def update_detailed_view(arr_value, room_types, price_max_value):
    # Sécurité si pas de données
    if df_base.empty:
        return (
            _empty_map_figure(),
            _empty_hist_figure(),
            "Aucune donnée disponible.",
            "",
        )

    data = df_base.copy()

    # Filtre arrondissement
    if arr_value and arr_value != "__ALL__":
        data = data[data["district"].astype(str) == str(arr_value)]

    # Filtre types de logements
    if room_types:
        data = data[data["room_type"].isin(room_types)]

    # Filtre prix max
    if price_max_value is not None:
        data = data[data["price"] <= price_max_value]

    # Texte sous le slider
    slider_label = f"Prix maximum sélectionné : {int(price_max_value)} €" if price_max_value else ""

    if data.empty:
        summary_children = (
            "Aucune annonce ne correspond à cette sélection de filtres. "
            "Essayez d'élargir la plage de prix ou d'inclure plus de types de logements."
        )
        return _empty_map_figure(), _empty_hist_figure(), summary_children, slider_label

    # -------- Carte --------
    fig_map = px.scatter_mapbox(
        data_frame=data,
        lat="latitude",
        lon="longitude",
        color="price",
        hover_name="district",
        hover_data={"price": True, "room_type": True},
        zoom=10,
        center={"lat": 48.8566, "lon": 2.3522},
        mapbox_style="open-street-map",
        title="Localisation des annonces filtrées",
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    # -------- Histogramme  --------
    price_bins = [0, 50, 100, 150, 200, 300, 500, np.inf]
    price_labels = [
        "≤ 50 €",
        "50–100 €",
        "100–150 €",
        "150–200 €",
        "200–300 €",
        "300–500 €",
        "> 500 €",
    ]

    data["price_range"] = pd.cut(
        data["price"],
        bins=price_bins,
        labels=price_labels,
        include_lowest=True,
        right=False,
    )

    price_counts = (
    data["price_range"]
    .value_counts()
    .reindex(price_labels, fill_value=0)
    .rename("count")
    .reset_index()
    .rename(columns={"index": "price_range"})
    )

    fig_hist = px.bar(
        price_counts,
        x="price_range",
        y="count",
        title="Distribution des prix pour la sélection (par tranches)",
        labels={
            "price_range": "Tranche de prix",
            "count": "Nombre d'annonces",
        },
    )
    fig_hist.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
    )

    # -------- Résumé textuel --------
    n_listings = len(data)
    price_mean = data["price"].mean()
    price_median = data["price"].median()
    rating_mean = (
        data["review_scores_rating"].mean() if "review_scores_rating" in data.columns else None
    )

    parts = [
        html.P(
            f"La sélection actuelle contient {n_listings} annonces Airbnb.",
            className="summary-line",
        ),
        html.Ul(
            [
                html.Li(f"Prix moyen : {price_mean:.0f} € par nuit"),
                html.Li(f"Prix médian : {price_median:.0f} € par nuit"),
            ]
            + (
                [html.Li(f"Note moyenne des voyageurs : {rating_mean:.1f}/100")]
                if rating_mean is not None and not pd.isna(rating_mean)
                else []
            ),
            className="summary-list",
        ),
    ]

    if arr_value and arr_value != "__ALL__":
        parts.append(
            html.P(
                f"Ces chiffres concernent uniquement l’arrondissement {arr_value}.",
                className="summary-line",
            )
        )
    else:
        parts.append(
            html.P(
                "Ces chiffres prennent en compte l’ensemble des arrondissements de Paris.",
                className="summary-line",
            )
        )

    return fig_map, fig_hist, parts, slider_label
