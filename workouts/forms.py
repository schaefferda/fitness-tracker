from django import forms
from django.forms import inlineformset_factory
from .models import Workout, WorkoutSet

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        # We only want the user to fill out the notes.
        # Django automatically handles the 'date', and we will handle the 'user' in the view
        fields = ['notes']

# This creates a group of forms for the WorkoutSet model, tied to a specific Workout.
WorkoutSetFormSet = inlineformset_factory(
    Workout,          # Parent model
    WorkoutSet,       # Child model
    fields=('exercise', 'reps', 'weight'), # Fields for the user to fill out
    extra=3,          # Number of empty rows to show by default
    can_delete=False  # We will keep it simple for now!
)