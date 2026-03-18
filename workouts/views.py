from django.shortcuts import render
from .models import Workout


def workout_list(request):
    # Fetch all workouts from the database, ordered by newest first
    workouts = Workout.objects.all().order_by('-date')

    # Pass the workouts to an HTML template
    context = {'workouts': workouts}
    return render(request, 'workouts/workout_list.html', context)