from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    type = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strava_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=100, null=True, blank=True)
    distance = models.FloatField()  # Matka kilometreinä
    duration = models.DurationField()  # Suorituksen kesto
    start_date = models.DateTimeField()
    elevation_gain = models.FloatField(max_length=255)
    gears = models.ManyToManyField("gear_app.Equipment", related_name="activities", blank=True)
    average_speed = models.FloatField(null=True, blank=True)
    average_heartrate = models.FloatField(null=True, blank=True)
    moving_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.sport_type})'