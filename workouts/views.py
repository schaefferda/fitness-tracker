import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout
from .forms import ExerciseForm, WorkoutForm, WorkoutSetFormSet


@login_required
def workout_list(request):
    # Fetch all workouts from the database, ordered by newest first
    all_workouts = Workout.objects.filter(user=request.user).order_by('-date')

    # Tell Paginator to split up workouts, showing 5 per page
    paginator = Paginator(all_workouts, 10)

    # Look at URL to see what page number a user clicked (e.g., ?page=2)
    # If there is no page number in the URL it defaults to None
    page_number = request.GET.get('page')

    # Get the specific page of workouts
    # If page_number is None, get_page automatically returns page 1
    page_obj = paginator.get_page(page_number)

    # Pass the specific page object to the HTML template instead of all_workouts
    context = {'workouts': page_obj}
    return render(request, 'workouts/workout_list.html', context)


@login_required
def add_workout(request):
    # Check if the user is submitting data
    if request.method == 'POST':
        # Grab the data for both the main form and the formset
        form = WorkoutForm(request.POST)
        formset = WorkoutSetFormSet(request.POST, form_kwargs={'user': request.user})

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
        formset = WorkoutSetFormSet(form_kwargs={'user': request.user})

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
        formset = WorkoutSetFormSet(request.POST, instance=workout, form_kwargs={'user': request.user})

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('workout_list')
    else:
        # If GET request, pre-fill the forms with the existing workout data
        form = WorkoutForm(instance=workout)
        formset = WorkoutSetFormSet(instance=workout, form_kwargs={'user': request.user})

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


@login_required
def dashboard(request):
    # Grab the user's workouts, ordered by oldest to newest so the chart flows left to right.
    # We will slice [:10] to only get the last 10 workouts to keep the chart clean.
    workouts = Workout.objects.filter(user=request.user).order_by('date')[:10]

    dates = []
    volumes = []

    for workout in workouts:
        # Format the date nicely (e.g., 'Oct 15')
        dates.append(workout.date.strftime('%b %d'))

        # Calculate the total volume for this specific workout
        total_volume = sum(set.reps * set.weight for set in workout.sets.all())
        # We convert it to a float because sometimes Decimal fields confuse JavaScript
        volumes.append(float(total_volume))

    # We must use json.dumps() so the Python lists are safely converted into
    # a format that JavaScript can easily read in our HTML template.
    context = {
        'dates': json.dumps(dates),
        'volumes': json.dumps(volumes),
    }

    return render(request, 'workouts/dashboard.html', context)


@login_required
def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            # Pause the save
            exercise = form.save(commit=False)

            # Attach the user! Because we do this, it becomes a "Custom" exercise.
            exercise.user = request.user

            # Save it to the database
            exercise.save()

            # Send them right back to the workout logging page
            return redirect('add_workout')
    else:
        form = ExerciseForm()

    return render(request, 'workouts/add_exercise.html', {'form': form})


@login_required
def workout_detail(request, pk):
    # Grab the specific workout, ensuring it belongs to the logged-in user
    workout = get_object_or_404(Workout, pk=pk, user=request.user)

    return render(request, 'workouts/workout_detail.html', {'workout': workout})