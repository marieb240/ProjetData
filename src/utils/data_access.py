# src/utils/data_access.py
from __future__ import annotations
from pathlib import Path
import pandas as pd
import sqlite3

# on importe TES fonctions existantes, sans les modifier
from src.utils.get_data import get_data
from src.utils.clean_data import clean_airbnb_paris  # ou le nom exact de ta fonction clean
from src.utils.build_db import build_db

DB_PATH    = Path("data/airbnb.db")
CSV_CLEAN  = Path("data/cleaned/airbnb_paris_clean.csv")
TABLE_NAME = "listings_paris"  # adapte si ta table s'appelle autrement

def ensure_data_ready() -> None:
    """
    Déclenche ton pipeline si besoin, dans l'ordre :
    get_data() -> clean_airbnb_paris() -> build_db()
    """
    try:
        # ces appels ne refont rien si tes fonctions gèrent déjà le 'si présent, ne refais pas'
        build_db()
    except Exception as e:
        print(f"[data_access] Pipeline a rencontré un problème: {e!r}")

def load_dataframe() -> pd.DataFrame:
    """
    Charge les données pour le dashboard. Priorité DB (si présente),
    sinon CSV nettoyé, sinon on (ré)lance ensure_data_ready() et on retente.
    """
    if DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)

    if CSV_CLEAN.exists():
        return pd.read_csv(CSV_CLEAN)

    ensure_data_ready()

    if DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            print("Données chargées depuis la base de données après pipeline.")
            return pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)

    if CSV_CLEAN.exists():
        return pd.read_csv(CSV_CLEAN)

    raise FileNotFoundError(
        "Impossible de charger les données (ni DB ni CSV nettoyé). "
        "Vérifie le nom de la table et les chemins."
    )
