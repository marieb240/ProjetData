# src/utils/build_db.py
"""Construire la base SQLite à partir du csv nettoyé """

from __future__ import annotations
from pathlib import Path
import sqlite3
import pandas as pd

from src.utils.clean_data import clean_airbnb_paris  # on réutilise le csv nettoyé

CLEAN_FILE = Path("data/cleaned/airbnb_paris_clean.csv")
DB_PATH = Path("data/airbnb.db")
TABLE_NAME = "listings_paris"

def build_db() -> Path:
    """
    Créer (ou recréer) une base SQLite à partir du csv clean
    On s'assure que le csv nettoyé existe (clean_airbnb_paris),
    on supprime l'ancienne base si elle existe,
    et on importe le csv dans une table listings_paris
    """
    # vérifie que le fichier clean est présent et à jour
    clean_airbnb_paris()

    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"Fichier csv clean introuvable : {CLEAN_FILE}")

    # on repart d'une base propre à chaque build
    if DB_PATH.exists():
        DB_PATH.unlink()

    df = pd.read_csv(CLEAN_FILE)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql(TABLE_NAME, conn, index=False)
    conn.close()

    print(f"Base SQLite créée → {DB_PATH} (table: {TABLE_NAME})")
    return DB_PATH

def main() -> None:
    build_db()

if __name__ == "__main__":
    main()
