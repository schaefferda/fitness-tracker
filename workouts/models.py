from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=100)
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