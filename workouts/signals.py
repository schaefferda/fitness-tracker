from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# 1. Listen for the User being saved. If it's a brand new user (created=True), make a Profile.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# 2. If an existing User is saved, just save the Profile alongside it to keep them in sync.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()