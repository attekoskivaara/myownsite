from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strava_access_token = models.CharField(max_length=255, blank=True, null=True)  # Access token
    strava_refresh_token = models.CharField(max_length=255, blank=True, null=True)  # Refresh token
    strava_token_expires_at = models.DateTimeField(blank=True, null=True)  # Token expiration time
    last_synced = models.DateTimeField(blank=True, null=True, default=None)

    def update_sync_time(self):
        self.last_synced = timezone.now()
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()