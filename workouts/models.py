"""
This module defines the data models for the workout tracking application.

Classes:
    Profile: Stores additional user information like age, gender, and physical metrics.
    Exercise: Defines specific physical activities, which can be global or user-specific.
    WorkoutSession: Groups a collection of exercise sets performed by a user on a specific date.
    WorkoutSet: Records the specific performance metrics for an exercise within a workout session.
"""

__author__ = ['Daniel Schaeffer']
__version__ = '0.1.0'
__py_version__ = '3.12'
__creation_date__ = '2026-03-18'

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    """
    Stores additional user information like age, gender, and physical metrics.
    Linked to a specific Django User via a OneToOneField.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Height in inches (in)")
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Weight in pounds (lbs)")

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Exercise(models.Model):
    """
    Defines specific physical activities, which can be global (user=None)
    or user-specific (Custom exercises).
    """

    EXERCISE_TYPES = [
        ('Resistance', 'Resistance'),
        ('Cardio', 'Cardio'),
        ('Flexibility', 'Flexibility'),
        ('Balance', 'Balance'),
        ('Sport-specific', 'Sport-specific'),
        ('Other', 'Other')
    ]

    MUSCLE_GROUPS = [
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Shoulders', 'Shoulders'),
        ('Legs', 'Legs'),
        ('Arms', 'Arms'),
        ('Core', 'Core'),
    ]

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES, default='Resistance')
    major_muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUPS, default='Core')
    secondary_muscles = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        if self.user:
            return f"{self.name} ({self.user.username})"
        return f"{self.name} (Global)"

class WorkoutSession(models.Model):
    """
    Represents a single workout session for a specific user.
    Tracks the date of the workout and includes optional notes.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    session_duration = models.DurationField(null=True, blank=True, help_text="Duration of the workout session")
    notes = models.TextField(blank=True, help_text="How did you feel during this workout?")

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d')}"

    @property
    def total_volume(self):
        # Calculate the total weight lifted in this specific workout
        return sum(ws.reps * ws.weight for ws in self.sets.all() if ws.reps and ws.weight)

    @property
    def total_exercises(self):
        # Counts how many unique exercises were performed
        return self.sets.values('exercise').distinct().count()


class WorkoutSet(models.Model):
    """
    Records the specific performance metrics for an exercise within a workout session,
    including both target and actual values for reps, weight, duration, and distance.
    """
    
    session = models.ForeignKey(WorkoutSession, related_name='sets', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    # Core Metrics (Actual vs Target)
    reps = models.PositiveIntegerField(null=True, blank=True)
    reps_target = models.PositiveIntegerField(null=True, blank=True)

    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    weight_target = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    duration = models.DurationField(null=True, blank=True)
    duration_target = models.DurationField(null=True, blank=True)

    distance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    distance_target = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Details (Merged from WorkoutSetDetails)
    positioning = models.CharField(max_length=50, blank=True)
    equipment = models.CharField(max_length=50, blank=True)
    modification = models.CharField(max_length=50, blank=True)

    # OLD STRING REPRESENTATION. CAN BE RESTORED IF NEEDED/WANTED
    # def __str__(self):
    #     return f"{self.exercise.name}:  {self.reps} reps @ {self.weight} lbs"

    def __str__(self):
        return f"{self.exercise.name} Set in Session {self.session.id}"