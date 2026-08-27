from pathlib import Path
import re
import csv

BASE_DIR = Path(__file__).resolve().parent.parent 
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

def parse_parish(file_path):
    provinces = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Regex qui capture le PARISH_NAME (en tenant compte des apostrophes doublées)
            match = re.search(r"\(\d+,\d+,'((?:''|[^'])*)'", line)
            if match:
                parish_name = match.group(1).replace("''", "'").strip()
                provinces.append([parish_name, "Validé"])
    return provinces

def run_extraction():
    provinces = parse_parish(DATA_DIR/"provinces.sql")

    # Supprimer les doublons en convertissant chaque ligne en tuple
    provinces = sorted(set(tuple(p) for p in provinces))
    
    OUTPUT_DIR.mkdir(exist_ok=True) 
    with open(OUTPUT_DIR / "provinces.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Province", "Etat"])
        for p in provinces:
            writer.writerow(p)
            
    print("Fichier provinces.csv généré avec succès.")

if __name__ == "__main__":
    run_extraction()
