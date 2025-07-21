# import_data.py

from gear_app.models import Gear
import csv

with open('activities_app_activity.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Gear.objects.create(**row)
