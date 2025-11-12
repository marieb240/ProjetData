import dash
from dash import html
import pandas as pd
from pathlib import Path

from src.utils.data_access import load_dataframe

dash.register_page(
    __name__,
    path="/",
    name="Accueil",
)

try:
    df = load_dataframe()
    n_listings = len(df)
    price_mean = int(df["price"].mean()) if "price" in df.columns else None
    n_hosts = df["host_id"].nunique() if "host_id" in df.columns else None
    
except Exception:
    df = None
    n_listings = price_mean = n_hosts = None

def kpi_block(label, value, suffix=""):
    return html.Div(
        [
            html.Div(label, className="kpi-label"),
            html.Div(
                "-" if value is None else f"{value}{suffix}",
                className="kpi-value",
            ),
        ],
        className="kpi-card",
    )

layout = html.Div(
    [
        html.H2("Accueil", className="section-title"),
        html.P(
            "Vue d’ensemble des annonces Airbnb à Paris à partir des données ouvertes.",
            className="section-subtitle",
        ),

        html.Div(
            [
                kpi_block("Nombre d’annonces", n_listings),
                kpi_block("Prix moyen par nuit (€)", price_mean),
                kpi_block("Nombre d’hôtes uniques", n_hosts),
            ],
            className="kpi-container",
        ),

        html.P(
            "Utilisez la navigation pour explorer plus en détail la répartition géographique, les prix et les caractéristiques des logements.",
            className="section-text",
        ),
    ],
    className="page-content",
)
