from pathlib import Path
import re
import csv

BASE_DIR = Path(__file__).resolve().parent.parent 
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Fonction pour parser city.sql (les régions)
def parse_city(file_path):
    city = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Regex qui capture tout jusqu'au prochain ')'
            match = re.search(r"\((\d+),\d+,'((?:''|[^'])*)'", line)
            if match:
                city_no, city_name = match.groups()
                # Corriger les doubles apostrophes
                city[int(city_no)] = city_name.replace("''", "'").strip()
    return city

# Fonction pour parser locality.sql (les districts)
def parse_locality(file_path):
    locality = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((\d+),(\d+),'((?:''|[^'])*)'", line)
            if match:
                locality_no, city_no, locality_desc = match.groups()
                locality.append({
                    "city_no": int(city_no),
                    "district": locality_desc.replace("''", "'").strip()
                })
    return locality

def run_extraction():
    city = parse_city(DATA_DIR/ "regions.sql")
    locality = parse_locality(DATA_DIR/"districts.sql")

    rows = []
    for loc in locality:
        region = city.get(loc["city_no"], "UNKNOWN")
        rows.append([region, loc["district"], "Validé"])

    OUTPUT_DIR.mkdir(exist_ok=True) 
    with open(OUTPUT_DIR / "districts.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Region", "District", "Etat"])
        writer.writerows(rows)

    print("Fichier districts.csv généré avec succès.")

