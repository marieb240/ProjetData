import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

# 🔌 pipeline (DB ou CSV clean)
from src.utils.data_access import load_dataframe

dash.register_page(
    __name__,
    path="/more",
    name="Analyse détaillée",
)

# ---------- Chargement des données ----------
try:
    df = load_dataframe()
except Exception:
    # DataFrame vide avec les colonnes nécessaires, pour éviter les crashs
    df = pd.DataFrame(columns=["price", "room_type", "latitude", "longitude", "district"])

# ---------- Graphique 1 : Histogramme des prix (<500€ pour lisibilité) ----------
fig_price_dist = (
    px.histogram(
        df[df["price"] < 500],
        x="price",
        nbins=60,
        title="Distribution des prix par nuit (€)",
    )
    if not df.empty and "price" in df.columns
    else None
)

# ---------- Graphique 2 : Répartition par type de logement ----------
fig_room_type = None
if not df.empty and "room_type" in df.columns:
    rt_counts = df["room_type"].value_counts().reset_index()
    rt_counts.columns = ["room_type", "count"]
    fig_room_type = px.bar(
        rt_counts,
        x="room_type",
        y="count",
        labels={"room_type": "Type de logement", "count": "Nombre d’annonces"},
        title="Répartition par type de logement",
    )

# ---------- Helpers / options d’arrondissement ----------
def _district_key(v: str) -> int:
    # "1er" -> 1, "14e" -> 14 (tri 1→20)
    try:
        return int("".join(ch for ch in str(v) if ch.isdigit()))
    except Exception:
        return 999

def arrondissement_label(v: str | None) -> str:
    if not v or v == "__ALL__":
        return "Paris (tous arrondissements)"
    return f"{v} arrondissement"

arr_options = [{"label": "Tous Paris", "value": "__ALL__"}]
if "district" in df.columns:
    uniq = (
        df["district"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    uniq = sorted(uniq, key=_district_key)
    arr_options += [{"label": lab, "value": lab} for lab in uniq]

# -- bornes propres pour le filtre de prix (5e-95e percentiles)
if not df.empty and "price" in df.columns:
    p05 = float(df["price"].quantile(0.05))
    p95 = float(df["price"].quantile(0.95))
    PRICE_MIN, PRICE_MAX = int(p05), int(p95)
else:
    PRICE_MIN, PRICE_MAX = 20, 500  # fallback

# ---------- Layout ----------
layout = html.Div(
    [
        # Titre principal
        html.H2("Analyse détaillée", className="section-title"),
        html.P(
            "Visualisation des distributions de prix, des types de logements et de la répartition géographique des annonces Airbnb à Paris.",
            className="section-subtitle",
        ),

        # 1) Distribution des prix
        html.H3("Distribution des prix", className="section-subtitle"),
        html.Div(
            [
                dcc.Graph(figure=fig_price_dist)
                if fig_price_dist
                else html.P(
                    "Données indisponibles pour la distribution des prix.",
                    className="section-text",
                ),
            ],
            className="chart-block",
        ),
        html.P(
            "La majorité des logements se situent entre 80 € et 200 € par nuit, "
            "traduisant une offre de milieu de gamme destinée à une clientèle touristique. "
            "Les annonces au-delà de 500 € correspondent à des biens de luxe situés dans les quartiers les plus prisés de Paris.",
            className="section-text",
        ),

        # 2) Types de logements
        html.H3("Types de logements", className="section-subtitle"),
        html.Div(
            [
                dcc.Graph(figure=fig_room_type)
                if fig_room_type
                else html.P(
                    "Données indisponibles pour les types de logements.",
                    className="section-text",
                ),
            ],
            className="chart-block",
        ),
        html.P(
            "Le marché parisien est dominé par les logements entiers, tandis que les chambres privées occupent une part secondaire. "
            "Les offres de chambres partagées ou d’hôtel restent minoritaires, illustrant une préférence marquée des hôtes et des voyageurs pour des hébergements indépendants.",
            className="section-text",
        ),

        # 3) Répartition géographique (carte dynamique)
        html.H4("Répartition géographique", className="section-subtitle"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Vue"),
                        dcc.RadioItems(
                            id="view-scope",
                            options=[
                                {"label": "Paris (tous arrondissements)", "value": "PARIS"},
                                {"label": "Par arrondissement", "value": "ARR"},
                            ],
                            value="PARIS",
                            inline=True,
                        ),
                        html.Div(
                            [
                                html.Label("Arrondissement"),
                                dcc.Dropdown(
                                    id="arr-select",
                                    options=arr_options,  # type: ignore[arg-type]  (Pylance)
                                    value="__ALL__",
                                    clearable=False,
                                    placeholder="Choisir un arrondissement",
                                ),
                            ],
                            id="arr-select-wrapper",
                            style={"display": "none"},  # masqué par défaut (vue PARIS)
                        ),
                    ],
                    className="controls",
                    style={"marginBottom": "12px"},
                ),

                # Toggle points individuels
                dcc.Checklist(
                    id="show-points",
                    options=[{"label": "Afficher les points individuels", "value": "POINTS"}],
                    value=[],  # vide = heatmap par défaut
                    inline=True,
                    style={"marginBottom": "6px"},
                ),

                # Filtre de prix (tranche)
                dcc.RangeSlider(
                    id="price-range",
                    min=PRICE_MIN,
                    max=PRICE_MAX,
                    step=5,
                    value=[PRICE_MIN, PRICE_MAX],
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={
                        PRICE_MIN: f"{PRICE_MIN}€",
                        (PRICE_MIN + PRICE_MAX)//2: f"{(PRICE_MIN + PRICE_MAX)//2}€",
                        PRICE_MAX: f"{PRICE_MAX}€",
                    },
                    allowCross=False,
                    pushable=10,
                ),

                dcc.Graph(id="map-graph", figure={}),
                html.P(
                    "Plus la couleur est claire, plus la densité d'annonces Airbnb est élevée.",
                    className="section-text",
                    style={"fontStyle": "italic", "textAlign": "center", "marginTop": "10px", "color": "#555"},
                ),
                html.P(
                    id="price-help",
                    className="section-text",
                    style={"fontStyle": "italic", "textAlign": "left", "marginTop": "6px", "color": "#555"},
                ),
            ],
            className="chart-block",
        ),

        # Analyse de la répartition géographique
        html.Div(
            [
                html.H4("Analyse de la répartition géographique", className="section-subtitle"),
                html.P(
                    "La concentration des annonces Airbnb est nettement plus forte dans les arrondissements centraux "
                    "de Paris, notamment autour du Marais, du Quartier Latin et de Montmartre. "
                    "Ces zones, très touristiques, attirent une forte demande en hébergement de courte durée. "
                    "À l’inverse, les arrondissements périphériques présentent une densité beaucoup plus faible, "
                    "ce qui reflète leur caractère davantage résidentiel.",
                    className="section-text",
                ),
            ],
            className="analysis-block",
        ),

        # 4) Analyse globale
        html.Div(
            [
                html.H3("Analyse globale des visualisations", className="section-subtitle"),
                html.P(
                    "L’ensemble des visualisations met en lumière un marché Airbnb fortement concentré dans le centre de Paris. "
                    "Les logements entiers dominent largement l’offre, confirmant une utilisation d’Airbnb orientée vers la location touristique complète. "
                    "Les prix se situent majoritairement entre 80 € et 200 € par nuit, "
                    "ce qui traduit une offre de milieu de gamme accessible à une clientèle internationale. "
                    "La carte de densité illustre cette pression locative accrue dans les arrondissements centraux, "
                    "alors que la périphérie conserve un profil plus résidentiel et moins tourné vers la location de courte durée. "
                    "Ces observations soulignent la forte attractivité économique et touristique du cœur de la capitale.",
                    className="section-text",
                ),
            ],
            className="analysis-block",
        ),
    ],
    className="page-content",
)

# ---------- Callback : mise à jour de la carte ----------
@callback(
    Output("map-graph", "figure"),
    Output("arr-select-wrapper", "style"),
    Output("price-help", "children"),
    Input("view-scope", "value"),
    Input("arr-select", "value"),
    Input("price-range", "value"),
    Input("show-points", "value"),
)
def update_map(scope, selected_arr, price_range, show_points_values):
    data = df.copy()

    # bornes prix sélectionnées
    if price_range and len(price_range) == 2:
        pmin, pmax = price_range
    else:
        pmin, pmax = PRICE_MIN, PRICE_MAX

    # Filtres de base
    if not data.empty:
        for c in ("latitude", "longitude"):
            if c in data.columns:
                data = data[data[c].notna()]
        if "price" in data.columns:
            data = data[(data["price"] >= pmin) & (data["price"] <= pmax)]

    # Montrer/masquer le dropdown
    show_arr = {"display": "none"} if scope == "PARIS" else {"marginTop": "8px"}

    # Filtrage par arrondissement
    if scope == "ARR" and selected_arr and selected_arr != "__ALL__" and "district" in data.columns:
        data = data[data["district"].astype(str) == str(selected_arr)]

    # Échantillonnage léger pour lisibilité
    if len(data) > 5000:
        data = data.sample(5000, random_state=42)

    # Texte d’aide dynamique (prix + nb points)
    help_text = f"Tranche de prix : {int(pmin)}–{int(pmax)} € · Annonces affichées : {len(data)}."

    # Pas de données → figure vide
    if data.empty or "latitude" not in data.columns or "longitude" not in data.columns:
        fig = px.scatter_mapbox(lat=[], lon=[])
        fig.update_layout(
            mapbox_style="open-street-map",
            margin=dict(l=0, r=0, t=0, b=0),
            annotations=[dict(text="Aucune annonce dans cette tranche de prix.", showarrow=False)]
        )
        return fig, show_arr, help_text

    # Titre dynamique
    title_base = (
        "Annonces Airbnb à Paris"
        if scope == "PARIS" or selected_arr in (None, "__ALL__")
        else f"Annonces — {arrondissement_label(selected_arr)}"
    )
    title = f"{title_base} · {int(pmin)}–{int(pmax)} €"

    # Points ou heatmap ?
    show_points = "POINTS" in (show_points_values or [])

    if show_points:
        # Points plus fins et transparents
        fig = px.scatter_mapbox(
            data_frame=data,
            lat="latitude",
            lon="longitude",
            hover_name="district" if "district" in data.columns else None,
            center={"lat": 48.8566, "lon": 2.3522},
            zoom=10,
            opacity=0.80,
            title=title,
        )
        # taille des points ↓
        fig.update_traces(marker={"size": 4})
        fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=40, b=0))
        return fig, show_arr, help_text

    # Heatmap (densité moins épaisse)
    fig = px.density_mapbox(
        data_frame=data,
        lat="latitude",
        lon="longitude",
        radius=8,  # rayon plus fin qu'avant (8 recommandé)
        center={"lat": 48.8566, "lon": 2.3522},
        zoom=10,
        mapbox_style="open-street-map",
        title=f"Densité — {title}",
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig, show_arr, help_text
