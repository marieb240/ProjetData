# src/utils/get_data.py
from pathlib import Path
import requests

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def download_static(url: str, out_name: str) -> Path:
    """Télécharge un fichier (CSV/JSON/…) et le stocke en brut dans data/raw/."""
    dest = RAW_DIR / out_name
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return dest

if __name__ == "__main__":
    # Exemple : remplacer par l’URL de ton dataset
    download_static("https://exemple.org/mon_fichier.csv", "interventions2023.csv")
