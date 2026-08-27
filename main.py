from etl import extraction_provinces, extraction_regions, extraction_districts, extraction_communes

def run_all():
    extraction_provinces.run_extraction()
    extraction_regions.run_extraction()
    extraction_districts.run_extraction()
    extraction_communes.run_extraction()

if __name__ == "__main__":
    run_all()
