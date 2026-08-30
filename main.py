from etl import extraction_provinces, extraction_regions, extraction_districts, extraction_communes, extraction_centre_gestionnaire

def run_all():
    extraction_provinces.run_extraction()
    extraction_regions.run_extraction()
    extraction_districts.run_extraction()
    extraction_communes.run_extraction()
    extraction_centre_gestionnaire.run_extraction()

if __name__ == "__main__":
    run_all()
