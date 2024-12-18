# import json
# from pathlib import Path
# from django.core.management.base import BaseCommand
# from main.apps.location.models import Region, District  



# class Command(BaseCommand):
#     help = "Load regions and districts from JSON"

#     def handle(self, *args, **kwargs):
#         json_file_path = Path("main/apps/common/management/json/locations.json")

#         self.stdout.write(f"Looking for file at: {json_file_path}")

#         if not json_file_path.exists():
#             self.stderr.write(f"File not found: {json_file_path}")
#             return

#         with open(json_file_path, "r") as file:
#             data = json.load(file) 

#         self.stdout.write(f"Data loaded: {data}")

#         for region_data in data:
#             region_name = region_data.get("region")
#             if region_name:
#                 region, created = Region.objects.get_or_create(name=region_name)
#                 if created:
#                     self.stdout.write(f"Region created: {region_name}")
#                 else:
#                     self.stdout.write(f"Region already exists: {region_name}")

#                 for district_name in region_data.get("districts", []):
#                     if district_name:
#                         district, created = District.objects.get_or_create(
#                             name=district_name, region=region
#                         )
#                         if created:
#                             self.stdout.write(f"District created: {district_name}")
#                         else:
#                             self.stdout.write(f"District already exists: {district_name}")

#         self.stdout.write("Region and district creation process completed.")



import json
from pathlib import Path
from django.core.management.base import BaseCommand
from main.apps.location.models import Country, Region, District  

class Command(BaseCommand):
    help = 'Import countries, regions, and districts from JSON files'

    def handle(self, *args, **kwargs):
        countries_file = Path("main/apps/common/management/json/country.json")
        regions_file = Path("main/apps/common/management/json/region.json")
        districts_file = Path("main/apps/common/management/json/district.json")
       
        with open(countries_file, 'r', encoding='utf-8') as f:
            countries_data = json.load(f)

        with open(regions_file, 'r', encoding='utf-8') as f:
            regions_data = json.load(f)

        with open(districts_file, 'r', encoding='utf-8') as f:
            districts_data = json.load(f)

        for country_data in countries_data:
            country, created = Country.objects.update_or_create(
                id=country_data["id"],
                defaults={"name": country_data["name"]}
            )
            self.stdout.write(self.style.SUCCESS(f"Country '{country.name}' created/updated"))

            for region_data in regions_data:
                if region_data.get("country_id") == country_data["id"]:  
                    region, created = Region.objects.update_or_create(
                        id=region_data["id"],
                        defaults={"name": region_data["name"], "country": country}
                    )
                    self.stdout.write(self.style.SUCCESS(f"Region '{region.name}' created/updated in {country.name}"))

                    for district_data in districts_data:
                        if district_data.get("region_id") == region_data["id"]:
                            district, created = District.objects.update_or_create(
                                id=district_data["id"],
                                defaults={"name": district_data["name"], "region": region}
                            )
                            self.stdout.write(self.style.SUCCESS(f"District '{district.name}' created/updated in {region.name}"))
