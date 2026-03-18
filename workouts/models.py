__author__ = ['Daniel Schaeffer']
__version__ = '0.1.0'
__py_version__ = '3.12'
__creation_date__ = '2026-03-18'

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exercise(models.Model):

    MAJOR_MUSCLE_GROUPS = [
        (0, 'Chest'),
        (1, 'Back'),
        (2, 'Shoulders'),
        (3, 'Legs'),
        (4, 'Arms'),
        (5, 'Core'),
    ]

    name = models.CharField(max_length=100)
    major_muscle_group = models.PositiveSmallIntegerField(choices=MAJOR_MUSCLE_GROUPS, default=5)
    secondary_muscles = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    # Links this workout to a built-in Django User.
    # CASCADE means if te user is deleted, their workouts are deleted, too.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="How did you feel during this workout?")

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d')}"

class WorkoutSet(models.Model):
    # Links this set to a specific workout and exercise
    workout = models.ForeignKey(Workout, related_name='sets', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    # The actual data for the set
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in lbs")

    def __str__(self):
        return f"{self.exercise.name}:  {self.reps} reps @ {self.weight} lbs"