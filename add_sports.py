import os
import django

# Aseta Django-projektin asetukset
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from gear_app.models import Sport

# Lista lajeista, jotka haluat lisätä
sports = [
    'Run',
    'Trail Run',
    'Ride',
    'Swim',
    'Hike',
    'Walk',
    'Yoga',
    'Weight Training',
    'Crossfit',
    'Soccer',
    'Basketball',
    'Tennis',
    'Golf',
    'Cycling',
    'Rowing',
    'Skiing',
    'Snowboarding',
    'Skating',
    'Climbing',
    'Dancing'
    # Lisää kaikki lajit tähän
]

# Lisää lajit tietokantaan
for sport_name in sports:
    sport, created = Sport.objects.get_or_create(name=sport_name)
    if created:
        print(f'Lisätty uusi laji: {sport_name}')
    else:
        print(f'Laji {sport_name} on jo olemassa')

print('Kaikki lajit lisätty.')
