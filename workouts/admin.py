from django.contrib import admin
from .models import Exercise, Profile, WorkoutSession, WorkoutSet

# Register your models here.
admin.site.register(Exercise)
admin.site.register(Profile)
admin.site.register(WorkoutSession)
admin.site.register(WorkoutSet)