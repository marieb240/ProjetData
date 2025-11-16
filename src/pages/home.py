import dash
import numpy as np
from dash import html, dcc
import plotly.express as px
import pandas as pd

from src.utils.data_access import load_dataframe

dash.register_page(
    __name__,
    path="/",
    name="Accueil",
)

# -------- Chargement des données --------
try:
    # plus tard, si on veut gèrer plusieurs villes :
    # df = load_dataframe(city="paris")
    df = load_dataframe()
except Exception:
    df = pd.DataFrame()

if df is None:
    df = pd.DataFrame()

df = df.copy()

# Nettoyage basique des prix pour des graphes lisibles
if "price" in df.columns and not df.empty:
    df = df[df["price"] > 0]
    q01 = df["price"].quantile(0.01)
    q99 = df["price"].quantile(0.99)
    df = df[df["price"].between(q01, q99)]

# -------- KPIs --------
def _safe_int(x: float | int | None) -> str:
    try:
        return f"{x:,}".replace(",", " ")
    except Exception:
        return "–"

if not df.empty:
    n_listings = _safe_int(len(df))
    price_mean = f"{df['price'].mean():.0f} €"
    n_districts = _safe_int(df["district"].nunique()) if "district" in df.columns else "–"
else:
    n_listings = price_mean = n_hosts = n_districts = "–"

# -------- Figures statiques --------
# Histogramme des prix par tranches
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

df["price_range"] = pd.cut(
    df["price"],
    bins=price_bins,
    labels=price_labels,
    include_lowest=True,
    right=False,
)

price_counts = (
    df["price_range"]
    .value_counts()
    .reindex(price_labels, fill_value=0)   
    .rename("count")                       
    .reset_index()                         
    .rename(columns={"index": "price_range"})
)


fig_price_hist = px.bar(
    price_counts,
    x="price_range",
    y="count",
    title="Distribution des prix par nuit ",
    labels={
        "price_range": "Prix par nuit (€)",
        "count": "Nombre d'annonces",
    },
)
fig_price_hist.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
)


# Répartition des types de logements
if "room_type" in df.columns and not df.empty:
    fig_room_type = px.pie(
        df,
        names="room_type",
        title="Répartition des types de logements (en %)",
        hole=0.45,
    )
    fig_room_type.update_traces(textposition="inside", textinfo="percent+label")
    fig_room_type.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=380)
else:
    fig_room_type = px.pie(
        title="Répartition des types de logements (données manquantes)"
    )

# Top 5 arrondissements par prix moyen
if "district" in df.columns and not df.empty:
    district_stats = (
        df.groupby("district")["price"]
        .mean()
        .reset_index()
        .rename(columns={"price": "price_mean"})
    )
    district_stats = district_stats.sort_values("price_mean", ascending=False).head(5)
    fig_top_districts = px.bar(
        district_stats,
        x="price_mean",
        y="district",
        orientation="h",
        title="Top 5 arrondissements par prix moyen",
        labels={"price_mean": "Prix moyen (€)", "district": "Arrondissement"},
    )
    fig_top_districts.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        yaxis={"categoryorder": "total ascending"},
    )
else:
    fig_top_districts = px.bar(title="Top arrondissements (données manquantes)")

# Boxplot des prix par arrondissement (top 10 en nombre d'annonces)
if "district" in df.columns and not df.empty:
    counts = df["district"].value_counts()
    top_districts_for_box = counts.head(10).index.tolist()
    df_box = df[df["district"].isin(top_districts_for_box)]

    fig_price_box = px.box(
        df_box,
        x="district",
        y="price",
        title="Distribution des prix par arrondissement (top 10)",
        labels={"district": "Arrondissement", "price": "Prix par nuit (€)"},
    )
    fig_price_box.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis={"categoryorder": "array", "categoryarray": top_districts_for_box},
    )
else:
    fig_price_box = px.box(title="Prix par arrondissement (données manquantes)")

# -------- Composant KPI --------
def kpi_block(label: str, value: str) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="kpi-label"),
            html.Div(value, className="kpi-value"),
        ],
        className="kpi-card",
    )

# -------- Layout de la page --------
layout = html.Div(
    [
        html.H2("Vue d'ensemble", className="section-title"),
        html.P(
            "Synthèse des annonces Airbnb de Paris : volume, niveaux de prix et répartition des logements.",
            className="section-subtitle",
        ),
        html.P(
            "Le jeu de données utilisé correspond aux annonces Airbnb actives à Paris. "
            "Chaque ligne du fichier airbnb_listings.csv représente une annonce, avec des informations sur "
            "le prix par nuit, le type de logement (logement entier, chambre privée, etc.), l’arrondissement, "
            "le nombre de chambre et la note moyenne laissée par les voyageurs. "
            "Après un nettoyage des données et la suppression des valeurs extrêmes, "
            "plus de 60 000 annonces sont conservées pour construire les graphiques ci-dessous.",
            className="section-text",
        ),

        # KPIs principaux
        html.Div(
            [
                kpi_block("Nombre d’annonces", n_listings),
                kpi_block("Prix moyen par nuit", price_mean),
                kpi_block("Arrondissements couverts", n_districts),
            ],
            className="kpi-container",
        ),

        # Ligne 1 : histogramme + donut
                # Ligne 1 : histogramme + donut
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            figure=fig_price_hist,
                            config={"displayModeBar": False},
                        ),
                    ],
                    className="chart-block",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=fig_room_type,
                            config={"displayModeBar": False, "responsive": False},
                            style={"height": "380px"},
                        ),
                    ],
                    className="chart-block",
                ),
            ],
            className="grid-2",
        ),

        # Texte explication des graphes du bas
        html.Div(
            [
                dcc.Markdown(
                    """Les deux graphiques suivants approfondissent la *dimension géographique* des prix Airbnb à Paris.  
                        À gauche, le **classement des arrondissements les plus chers** met immédiatement en évidence les zones premium de la capitale, où la demande touristique et la proximité des monuments emblématiques tirent les prix vers le haut.  
                        À droite, le **boxplot** permet d’observer la structure complète des prix dans les arrondissements les plus représentés :  
                            - la **médiane**, qui reflète le prix typique,  
                            - la **dispersion**, indicatrice de l’hétérogénéité du marché,  
                            - et les **valeurs atypiques**, correspondant aux annonces très haut de gamme.
                        Ces deux visualisations offrent ainsi une lecture plus fine des dynamiques locales, en montrant que l’attractivité d’un quartier influence fortement la diversité et le niveau des prix pratiqués.
                    """,
                    className="section-text",
                ),
            ],
            className="analysis-block",
        ),

        # Ligne 2 : top arrondissements + boxplot
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            figure=fig_top_districts,
                            config={"displayModeBar": False},
                        ),
                    ],
                    className="chart-block",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=fig_price_box,
                            config={"displayModeBar": False},
                        ),
                    ],
                    className="chart-block",
                ),
            ],
            className="grid-2",
        ),

        # Bloc d'analyse textuelle global
        html.Div(
            [
                dcc.Markdown(
                    """ Globalement, ces analyses soulignent un marché Airbnb parisien **dense, contrasté et fortement structuré par la géographie**.  
                        La majorité des annonces se concentre dans une fourchette de prix relativement accessible, mais certains arrondissements affichent des niveaux nettement plus élevés, reflet de **leur notoriété touristique** et de **leur attractivité**.  
                        Les variations de prix suivent donc principalement **une logique géographique** : on retrouve au centre des prix moyens plus élevés alors que la périphérie se distinguent avec des prix plus bas.
                        Ces résultats permettent d’obtenir une vision claire et synthétique du marché en montrant comment **la localisation**, **la demande touristique** et **la diversité des logements** influencent les prix à travers la capitale.""",
                    className="section-text",
                ),
            ],
            className="analysis-block",
        ),
    ],
    className="page-content",
)