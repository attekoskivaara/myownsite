from django.db import models
from django.contrib.auth.models import User
from activities_app .models import Activity
from django.db.models import Sum, Avg
from datetime import timedelta


# lajit
class Sport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# välineluokat
class EquipmentType(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)  # Väline liittyy tiettyyn lajiin
    name = models.CharField(max_length=100)  # Välineen nimi, esim. juoksukenkä, jääkiekkoluistin jne.
    custom_field_structure = models.JSONField(blank=True, null=True)  # esim. [{"id": "drop", "label": "Droppi", "type": "number"}]

    def __str__(self):
        return self.name


# välineet
class Equipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sport_equipments')  # Link to the user
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True, blank=True)  # Lisää tämä rivi, jos puuttuu
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.CharField(null=True, max_length=100)
    model = models.CharField(null=True, max_length=100)
    size = models.CharField(null=True, max_length=50)
    weight = models.FloatField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_fields = models.JSONField(blank=True, null=True)
    maintenance_log = models.TextField(null=True, blank=True)
    default_uses = models.ManyToManyField(Sport, blank=True, related_name='default_use_equipments')

    STATUS_CHOICES = [
        ('unselected', 'Select status'),
        ('active', 'In active use'),
        ('secondary', 'Secondary use'),
        ('disposed', 'Disposed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unselected',
        verbose_name="Status"
    )


    def __str__(self):
        return f"{self.brand} {self.model} ({self.equipment_type.name}) {self.sport}"

    def total_distance(self):
        return Activity.objects.filter(gears=self).aggregate(Sum('distance'))['distance__sum'] or 0

    def get_total_duration(self):
        total_duration = Activity.objects.filter(gears=self).aggregate(
            total_duration=Sum('duration'))['total_duration'] or timedelta(0)

        # Tulosta diagnostiikkatietoja
        print(f"Total duration for {self}: {total_duration}")

        # Palauta tunteina (tai muuta tarvittaessa)
        return total_duration.total_seconds() / 3600


    def get_total_moving_time(self):
        total_moving_time = Activity.objects.filter(gears=self).aggregate(
            total_moving_time = Sum('moving_time'))['total_moving_time'] or timedelta(0)
        return total_moving_time.total_seconds() / 3600


    def usage_count(self):
        return Activity.objects.filter(gears=self).count()


    @property
    def average_km(self):
        activities = Activity.objects.filter(gears=self)

        total_distance = activities.aggregate(Sum('distance'))['distance__sum']
        count = activities.count()

        if not total_distance or count == 0:
            return 0  # or None, depending on your preference

        return total_distance / count

    def price_per_duration(self):
        total_duration = Activity.objects.filter(gears=self).aggregate(
        total_duration=Sum('duration'))['total_duration'] or timedelta(0)

        if total_duration.total_seconds() == 0:
            return None  # Avoid division by zero

        total_hours = total_duration.total_seconds() / 3600
        if self.purchase_price:
            return round(float(self.purchase_price) / total_hours, 2)
        return None


    def get_average_speed(self):
        average_gear_speed = Activity.objects.filter(gears=self).aggregate(
            average_gear_speed=Avg('average_speed'))
        average_speed = average_gear_speed['average_gear_speed'] or 0

        print(f"Average speed for {self}: {average_speed}")
        return average_speed

    def get_average_heartrate(self):
        average_gear_heartrate = Activity.objects.filter(gears=self).aggregate(
            average_gear_heartrate=Avg('average_heartrate')
        )
        return average_gear_heartrate

class ShoeSize(models.Model):
    us_size = models.CharField(max_length=10, null=True, blank=True)
    uk_size = models.CharField(max_length=10, null=True, blank=True)
    eu_size = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        # Näytä kokotiedot muodossa: EU 42 / UK 8 / US 9
        return f"EU {self.eu_size} / UK {self.uk_size} / US {self.us_size}"


class Gear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gears')  # related_name lisätty
    name = models.CharField(max_length=255) # nickname
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_distance = models.FloatField(default=0.0)
    total_uses = models.IntegerField(default=0)
    retailer = models.CharField(max_length=255, null=True, blank=True)
    maintenance_log = models.TextField(null=True, blank=True)
    estimated_lifespan_km = models.FloatField(null=True, blank=True)
    gear_type = models.CharField(max_length=255, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.gear_type})"