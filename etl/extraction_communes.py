from pathlib import Path
import re
import csv

BASE_DIR = Path(__file__).resolve().parent.parent 
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

def parse_fokontany(file_path):
    fokontany = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((\d+),(\d+),'((?:''|[^'])*)'\)", line)
            if match:
                fkt_no, wereda_no, fkt_desc = match.groups()
                fokontany.append({
                    "wereda_no": int(wereda_no),
                    "commune": fkt_desc.replace("''", "'").strip()
                })
    return fokontany

# Fonction pour parser wereda.sql
def parse_wereda(file_path):
    wereda = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((\d+),(\d+),'((?:''|[^'])*)'", line)
            if match:
                wereda_no, locality_no, wereda_desc = match.groups()
                wereda[int(wereda_no)] = int(locality_no)
    return wereda

# Fonction pour parser locality.sql
def parse_locality(file_path):
    locality = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((\d+),\d+,'((?:''|[^'])*)'", line)
            if match:
                locality_no, locality_desc = match.groups()
                locality[int(locality_no)] = locality_desc.replace("''", "'").strip()
    return locality

def run_extraction():
    fokontany = parse_fokontany(DATA_DIR/"communes.sql")
    wereda = parse_wereda(DATA_DIR/"communes_districts.sql")
    locality = parse_locality(DATA_DIR/"districts.sql")


    # Construire la correspondance District - Commune sans doublons
    rows_set = set()
    for fkt in fokontany:
        locality_no = wereda.get(fkt["wereda_no"])
        district = locality.get(locality_no, "UNKNOWN")
        # Ajouter dans un set pour éviter les doublons
        rows_set.add((district, fkt["commune"], "Validé"))

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR /"communes.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["District", "Commune","Etat"])
        writer.writerows(sorted(rows_set))  # tri pour lisibilité

    print("Fichier communes.csv généré avec succès.")