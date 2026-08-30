from pathlib import Path
import re
import csv

BASE_DIR = Path(__file__).resolve().parent.parent 
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Parser PARISH (provinces)
def parse_parish(file_path):
    parish = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((\d+),\d+,'((?:''|[^'])*)'", line)
            if match:
                parish_no, parish_name = match.groups()
                parish[int(parish_no)] = parish_name.replace("''", "'").strip()
    return parish

# Parser CITY (régions)
def parse_city(file_path):
    city = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\(\d+,\s*(\d+),'((?:''|[^'])*)'", line)
            if match:
                parish_no, city_name = match.groups()
                city.append({
                    "parish_no": int(parish_no),
                    "region": city_name.replace("''", "'").strip()
                })
    return city

def run_extraction():
    parish = parse_parish(DATA_DIR/"provinces.sql")
    city = parse_city(DATA_DIR/"regions.sql")

    rows = []
    for c in city:
        province = parish.get(c["parish_no"], "UNKNOWN")
        rows.append([province, c["region"], "Validé"])

    rows = sorted(set(tuple(r) for r in rows))

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "regions.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Province", "Region", "Etat"])
        writer.writerows(rows)
    
    print("Fichier regions.csv généré avec succès.")
