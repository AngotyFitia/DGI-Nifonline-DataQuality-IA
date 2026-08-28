from pathlib import Path
import re
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

def parse_fokontany(file_path):
    communes = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # FKT_NO, WEREDA_NO, FKT_DESC
            match = re.search(r"\(\d+,\s*(\d+),'((?:''|[^'])*)'\)", line)
            if match:
                wereda_no, commune = match.groups()
                communes[int(wereda_no)] = commune.replace("''", "'").strip()
    return communes

def parse_wereda(file_path):
    wereda = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # WEREDA_NO, LOCALITY_NO, WEREDA_DESC
            match = re.search(r"\((\d+),(\d+),'((?:''|[^'])*)'", line)
            if match:
                wereda_no, locality_no, wereda_desc = match.groups()
                wereda[int(wereda_no)] = {
                    "locality_no": int(locality_no),
                    "wereda_desc": wereda_desc.replace("''", "'").strip()
                }
    return wereda

def parse_locality(file_path):
    locality = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # LOCALITY_NO, CITY_NO, LOCALITY_DESC
            match = re.search(r"\((\d+),\d+,'((?:''|[^'])*)'", line)
            if match:
                locality_no, locality_desc = match.groups()
                locality[int(locality_no)] = locality_desc.replace("''", "'").strip()
    return locality

def parse_centre(file_path):
    centres = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((.*?)\)", line)
            if match:
                fields = [f.strip().strip("'") for f in match.group(1).split(",")]
                if len(fields) >= 13:
                    centres.append({
                        "designation": fields[1] if fields[1] != "NULL" else "Non disponible",
                        "lieu": fields[2] if fields[2] != "NULL" else "Non disponible",
                        "mail": fields[4] if fields[4] != "NULL" else "Non disponible"+ fields[9],
                        "tel": fields[5] if fields[5] != "NULL" else 000000000,
                        "tel2": fields[6] if fields[6] != "NULL" else 0000000000,
                        "adresse": fields[7] if fields[7] != "NULL" else "Non disponible",
                        "code_postal": fields[8] if fields[8] != "NULL" else 000,
                        "code_bureau": fields[9] if fields[9] != "NULL" else 0000,
                        "rib": fields[10] if fields[10] != "NULL" else "Non disponible",
                        "abbrev": fields[11] if fields[11] != "NULL" else "Non disponible",
                        "wereda_no": int(fields[12]) if fields[12].isdigit() else None
                    })
    return centres

def run_extraction():
    communes = parse_fokontany(DATA_DIR / "communes.sql")
    wereda = parse_wereda(DATA_DIR / "communes_districts.sql")
    locality = parse_locality(DATA_DIR / "districts.sql")
    centres = parse_centre(DATA_DIR / "centre_gestionnaire.sql")

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "coordonnees.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "District", "Commune", "Email", "Telephone", "TelephoneSecondaire",
            "SiteWeb", "Adresse", "CodePostal", "Latitude", "Longitude", "Etat"
        ])
        for c in centres:
            w = wereda.get(c["wereda_no"])
            if w:
                district = locality.get(w["locality_no"], "UNKNOWN")
                commune = communes.get(c["wereda_no"], w["wereda_desc"])
            else:
                district = "Non disponible"
                commune = "Non disponible"

            writer.writerow([district, commune, 
                             c["mail"], c["tel"], c["tel2"],
                             "Non disponible", c["adresse"], c["code_postal"],
                             0.0, 0.0, "Validé"])

    with open(OUTPUT_DIR / "centre_gestionnaire.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Email", "CodeBureau", "Abreviation", "NomCentre", "CompteBancaire", "Etat"
        ])
        for c in centres:
            writer.writerow([
                c["mail"], c["code_bureau"], c["abbrev"],
                c["designation"], c["rib"], "Validé"
            ])
    print("Fichiers coordonnees.csv et centre_gestionnaire.csv générés avec succès.")

if __name__ == "__main__":
    run_extraction()
