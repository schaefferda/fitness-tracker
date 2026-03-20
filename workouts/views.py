from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout
from .forms import WorkoutForm, WorkoutSetFormSet


@login_required
def workout_list(request):
    # Fetch all workouts from the database, ordered by newest first
    workouts = Workout.objects.filter(user=request.user).order_by('-date')

    # Pass the workouts to an HTML template
    context = {'workouts': workouts}
    return render(request, 'workouts/workout_list.html', context)


@login_required
def add_workout(request):
    # Check if the user is submitting data
    if request.method == 'POST':
        # Grab the data for both the main form and the formset
        form = WorkoutForm(request.POST)
        formset = WorkoutSetFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # commit=False tells Django to prepare the save, but wait just a moment.
            # Save the parent Workout first, but don't commit to DB yet.
            workout = form.save(commit=False)
            workout.user = request.user  # Attach the currently logged-in user to this workout
            workout.save() # Now we can safely save the workout to the database

            # Attach the new workout ot the formset, then save the formset
            formset.instance = workout
            formset.save()

            # Redirect the user back to the homepage list
            return redirect('workout_list')

    else:
        # If they aren't submitting data, just show any empty form
        form = WorkoutForm()
        formset = WorkoutSetFormSet()

    # Pass both to the template
    context = {
        'form': form,
        'formset': formset
    }

    return render(request, 'workouts/add_workout.html', context)


@login_required
def edit_workout(request, pk):
    # Grab the specific workout using its Primary Key (pk),
    # and ensure it belongs to the currently logged-in user for security!
    workout = get_object_or_404(Workout, pk=pk, user=request.user)

    if request.method == 'POST':
        # Pass the existing 'instance' so Django knows we are updating, not creating new
        form = WorkoutForm(request.POST, instance=workout)
        formset = WorkoutSetFormSet(request.POST, instance=workout)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('workout_list')
    else:
        # If GET request, pre-fill the forms with the existing workout data
        form = WorkoutForm(instance=workout)
        formset = WorkoutSetFormSet(instance=workout)

    context = {
        'form': form,
        'formset': formset,
        'is_edit': True  # A little flag so our HTML knows we are editing
    }
    # We can cleverly reuse our exact same HTML template!
    return render(request, 'workouts/add_workout.html', context)


@login_required
def delete_workout(request, pk):
    # Grab the workout, ensuring it belongs to the user for security
    workout = get_object_or_404(Workout, pk=pk, user=request.user)

    if request.method == 'POST':
        # If they confirm via the POST form, delete the workout
        workout.delete()
        # The cascade rule we set in models.py means all related sets are automatically deleted too!
        return redirect('workout_list')

    # If they just navigated to the page, show them the confirmation template
    context = {'workout': workout}
    return render(request, 'workouts/confirm_delete.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            user = form.save()
            # Automatically log the user in right after they register
            login(request, user)
            return redirect('workout_list')
    else:
        # If they just visit the page, show an empty form
        form = UserCreationForm()

    return render(request, 'workouts/register.html', {'form': form})