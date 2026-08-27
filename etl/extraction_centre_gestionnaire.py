from pathlib import Path
import re
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

def parse_wereda(file_path):
    wereda = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((\d+),\d+,'((?:''|[^'])*)'", line)
            if match:
                wereda_no, commune = match.groups()
                wereda[int(wereda_no)] = commune.replace("''", "'").strip()
    return wereda

def parse_centre(file_path):
    centres = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\((.*?)\)", line)
            if match:
                # Découper tous les champs par virgule
                fields = [f.strip().strip("'") for f in match.group(1).split(",")]

                # Sécuriser la longueur
                if len(fields) >= 13:
                    centres.append({
                        "designation": fields[1] if fields[1] != "NULL" else "",
                        "lieu": fields[2] if fields[2] != "NULL" else "",
                        "mail": fields[4] if fields[4] != "NULL" else "",
                        "tel": fields[5] if fields[5] != "NULL" else "",
                        "tel2": fields[6] if fields[6] != "NULL" else "",
                        "adresse": fields[7] if fields[7] != "NULL" else "",
                        "code_postal": fields[8] if fields[8] != "NULL" else "",
                        "code_bureau": fields[9] if fields[9] != "NULL" else "",
                        "rib": fields[10] if fields[10] != "NULL" else "",
                        "abbrev": fields[11] if fields[11] != "NULL" else "",
                        "wereda_no": int(fields[12]) if fields[12].isdigit() else None
                    })
    return centres

def run_extraction():
    wereda = parse_wereda(DATA_DIR / "communes_districts.sql")
    centres = parse_centre(DATA_DIR / "centre_gestionnaire.sql")

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_DIR / "coordonnees.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Commune", "Email", "Telephone", "TelephoneSecondaire",
            "SiteWeb", "Adresse", "CodePostal", "Latitude", "Longitude", "TypeAdresse", "Etat"
        ])
        for c in centres:
            commune = wereda.get(c["wereda_no"], "UNKNOWN")

            # Conditions : si champ vide ou NULL → valeur par défaut
            email = c["mail"] if c["mail"] else "Non disponible"
            tel = c["tel"] if c["tel"] else "Non disponible"
            tel2 = c["tel2"] if c["tel2"] else "Non disponible"
            adresse = c["adresse"] if c["adresse"] else "Non disponible"
            code_postal = c["code_postal"] if c["code_postal"] else "Non disponible"

            site_web = "N/A"
            latitude = "N/A"
            longitude = "N/A"

            type_adresse = c["adresse"] if c["adresse"] else "Inconnu"

            writer.writerow([
                commune, email, tel, tel2,
                site_web, adresse, code_postal,
                latitude, longitude, type_adresse, "Validé"
            ])

    with open(OUTPUT_DIR / "centre_gestionnaire.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Email", "CodeBureau", "Abreviation", "Designation", "CompteBancaire", "Commune", "Etat"
        ])
        for c in centres:
            commune = wereda.get(c["wereda_no"], "UNKNOWN")
            writer.writerow([
                c["mail"], c["code_bureau"], c["abbrev"],
                c["designation"], c["rib"], commune, "Validé"
            ])

    print("Fichiers coordonnees.csv et centre_gestionnaire.csv générés avec succès.")

if __name__ == "__main__":
    run_extraction()
