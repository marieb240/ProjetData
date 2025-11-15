# src/utils/clean_data.py
"""Nettoie le fichier listings et extrait le csv dans data/cleaned/"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from src.utils.get_data import get_data

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/cleaned")
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_DIR / "airbnb_listings.csv"
OUTPUT_FILE = CLEAN_DIR / "airbnb_paris_clean.csv"

# colonnes que l’on garde pour histogramme + heatmap que l'on focus sur Paris
KEEP_COLS = [
    "listing_id",
    "city",
    "district",  
    "neighbourhood",
    "room_type",
    "price",
    "latitude",
    "longitude",
]

# mapping des quartiers historiques -> n° d'arrondissement
NEIGH_TO_ARR = {
    "Louvre": 1,
    "Bourse": 2,
    "Temple": 3,
    "Hotel-de-Ville": 4,
    "Pantheon": 5,
    "Luxembourg": 6,
    "Palais-Bourbon": 7,
    "Elysee": 8,
    "Opera": 9,
    "Enclos-St-Laurent": 10,  # 10e
    "Popincourt": 11,
    "Reuilly": 12,
    "Gobelins": 13,
    "Observatoire": 14,
    "Vaugirard": 15,
    "Passy": 16,
    "Batignolles-Monceau": 17,
    "Buttes-Montmartre": 18,
    "Buttes-Chaumont": 19,
    "Menilmontant": 20,
}

def _already_clean(input_file: Path, output_file: Path) -> bool:
    """Vérifie si le fichier clean est plus récent que le brut pour éviter de re-nettoyer"""
    if not output_file.exists():
        return False
    return output_file.stat().st_mtime > input_file.stat().st_mtime

def clean_airbnb_paris() -> Path:
    """Nettoie le csv brut """
    if not INPUT_FILE.exists():
        get_data()
        print(f"Récupération des données brutes → {INPUT_FILE}")
    
    # si déjà propre et à jour : on ne refait pas le travail
    if _already_clean(INPUT_FILE, OUTPUT_FILE):
        print(f"Données déjà clean → {OUTPUT_FILE}")
        return OUTPUT_FILE

    df = pd.read_csv(INPUT_FILE, encoding="latin1", low_memory=False) # latin1 pour les accents

    # garder uniquement les colonnes nécessaires
    df = df[KEEP_COLS].copy()

    # filtrer pour la ville de Paris
    df = df[df["city"].str.strip().str.lower() == "paris"]
    
    def _norm(x): return str(x).strip()

    if "district" in df.columns and "neighbourhood" in df.columns:
        mask_paris = df["city"].astype(str).str.strip().str.lower().eq("paris")
        need = mask_paris & df["district"].isna()
        if need.any():
            df.loc[need, "district"] = (
                df.loc[need, "neighbourhood"].map(lambda x: NEIGH_TO_ARR.get(_norm(x)))
            )

    # On veut écrire le district en "1er", "2e", "3e"
    if "district" in df.columns:
        def format_district(x):
            try:
                x = int(float(x))
                return f"{x}{'er' if x == 1 else 'e'}"
            except Exception:
                return None
        df["district"] = df["district"].apply(format_district)

    # convertir les colonnes numériques si nécessaire
    if not pd.api.types.is_numeric_dtype(df["price"]):
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    if not pd.api.types.is_numeric_dtype(df["latitude"]):
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    if not pd.api.types.is_numeric_dtype(df["longitude"]):
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    # supprimer lignes inexploitables ou contenant des données aberrantes
    df = df.dropna(subset=["price", "latitude", "longitude"])
    df = df[(df["price"] > 0) & (df["price"] < 10_000)]

    # exporter
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Données nettoyées → {OUTPUT_FILE}")
    return OUTPUT_FILE

def main() -> None:
    clean_airbnb_paris()

if __name__ == "__main__":
    main()
