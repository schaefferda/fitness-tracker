__author__ = ['Daniel Schaeffer']
__version__ = '0.1.0'
__py_version__ = '3.12'
__creation_date__ = '2026-03-18'

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Exercise(models.Model):

    MAJOR_MUSCLE_GROUPS = [
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Shoulders', 'Shoulders'),
        ('Legs', 'Legs'),
        ('Arms', 'Arms'),
        ('Core', 'Core'),
    ]

    name = models.CharField(max_length=100)
    major_muscle_group = models.CharField(max_length=20, choices=MAJOR_MUSCLE_GROUPS, default='Core')
    secondary_muscles = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        if self.user:
            return f"{self.name} ({self.user.username})"
        return f"{self.name} (Global)"

class Workout(models.Model):
    """
    Represents a single workout session for a specific user.
    Tracks the date of the workout and includes optional notes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, help_text="How did you feel during this workout?")

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d')}"

    @property
    def total_volume(self):
        # Calculate the total weight lifted in this specific workout
        return sum(set.reps * set.weight for set in self.sets.all())

    @property
    def total_exercises(self):
        # Counts how many unique exercises were performed
        return self.sets.values('exercise').distinct().count()

class WorkoutSet(models.Model):
    # Links this set to a specific workout and exercise
    workout = models.ForeignKey(Workout, related_name='sets', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    # The actual data for the set
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=4, decimal_places=1, help_text="Weight in lbs")

    def __str__(self):
        return f"{self.exercise.name}:  {self.reps} reps @ {self.weight} lbs"