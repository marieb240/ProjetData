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


# 1) Histogramme des prix (< 500 € pour lisibilité)
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
# 2) Répartition par type de logement

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
# 3) Heatmap de densité géographique
fig_heatmap = None

if (
    df is not None
    and "latitude" in df.columns
    and "longitude" in df.columns
):
    # points propres + prix raisonnables
    df_geo = df[
        (df["price"] < 500)
        & df["latitude"].notna()
        & df["longitude"].notna()
    ]

     # échantillonnage pour éviter une tache uniforme
    if len(df_geo) > 3000:
        df_geo = df_geo.sample(3000, random_state=42)

    if not df_geo.empty:
        fig_heatmap = px.density_mapbox(
            df_geo,
            lat="latitude",
            lon="longitude",
            radius=2.5,  # taille des "taches" de densité
            center={"lat": 48.8566, "lon": 2.3522},  # centre sur Paris
            zoom=10.25,
            mapbox_style="open-street-map",
            title="Densité des annonces Airbnb à Paris",
        )



layout = html.Div(
    [ # Titre principal
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
    "Les annonces au-delà de 500 € correspondent à des biens de luxe situés dans les quartiers les plus prisés."
    "",
            className="section-text",
        ),
        
 # 2)Types de logements
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
             "Le marché parisien est dominé par les logements entiers, " \
             "tandis que les chambres privées occupent une part secondaire. "
            "Les offres de chambres partagées ou d’hôtel restent minoritaires, " \
            "illustrant une préférence marquée des hôtes et des voyageurs pour des hébergements indépendants.",
        ),

        # 3) Répartition géographique (heatmap)
        html.H4("Répartition géographique", className="section-subtitle"),
        html.Div(
            [
              dcc.Graph(figure=fig_heatmap),
                html.P(
                    "Plus la couleur est claire, plus la densité d'annonces Airbnb est élevée.",
                    className="section-text",                    
                    style={
                        "fontStyle": "italic",
                        "textAlign": "center",
                        "marginTop": "10px",
                        "color": "#555",
                    },
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
            "Les logements entiers dominent largement l’offre, confirmant une utilisation d’Airbnb orientée vers la location touristique complète. Les prix se situent majoritairement entre 80 € et 200 € par nuit, "
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
