# src/utils/get_data.py
"""Télécharge le zip Airbnb et extrait le fichier listings dans data/raw/"""

from __future__ import annotations
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

# Configuration des chemins
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)  # crée data/raw si besoin

ZIP_URL = "https://maven-datasets.s3.amazonaws.com/Airbnb/Airbnb+Data.zip"
ZIP_NAME = "airbnb_data.zip"

# Nom du fichier à extraire avec le mot clef
TARGET_MATCH = "listings"  
OUT_CSV = "airbnb_listings.csv"

def _download_bytes(url: str) -> bytes:
    """Télécharge une ressource et renvoie son contenu brut """
    with urlopen(url) as r:
        return r.read()

def _save(path: Path, data: bytes) -> None:
    """Sauvegarde des données binaires dans un fichier"""
    path.write_bytes(data)

def _extract_one(zip_bytes: bytes, match_substr: str, out_path: Path) -> None:
    """
    Ouvre le zip  et extrait le fichier dont le nom contient le mot clef "match_substr"
    """
    with ZipFile(BytesIO(zip_bytes)) as zf:
        names = zf.namelist()
        # on cherche le fichier correspondant au mot clef 
        candidates = [n for n in names if match_substr.casefold() in n.casefold()]
        if not candidates:
            raise RuntimeError(f"Aucun fichier ne contient '{match_substr}' dans le ZIP: {names}")

        # on préfère un .csv si plusieurs fichiers matchent
        csv_candidates = [n for n in candidates if n.lower().endswith(".csv")]
        chosen = csv_candidates[0] if csv_candidates else candidates[0]

        _save(out_path, zf.read(chosen))

def main() -> None:
    """Télécharge et extrait le fichier listings du zip Airbnb """
    zip_path = RAW_DIR / ZIP_NAME
    csv_path = RAW_DIR / OUT_CSV

    # cas 1 si le CSV est déjà présent : on ne refait rien
    if csv_path.exists():
        print(f" csv déjà présent → {csv_path}")
        return

    # cas 2 si le zip existe déjà : on extrait juste
    if zip_path.exists():
        print(f"zip déjà présent, on extrait → {csv_path}")
        _extract_one(zip_path.read_bytes(), TARGET_MATCH, csv_path)
        print(f" zip extrait → {csv_path}")
        return

    # cas 3 on télécharge le zip, on le stocke et on l'extrait
    print("téléchargement du zip")
    zip_bytes = _download_bytes(ZIP_URL)
    _save(zip_path, zip_bytes)  # on conserve le ZIP brut
    print(f"zip save → {zip_path}")

    print(f"extraction du fichier '{TARGET_MATCH}' → {csv_path}")
    _extract_one(zip_bytes, TARGET_MATCH, csv_path)
    print(f"fichier extrait → {csv_path}")

if __name__ == "__main__":
    main()
