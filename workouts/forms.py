from django import forms
from django.forms import inlineformset_factory
from .models import Exercise, Workout, WorkoutSet

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


# This creates a group of forms for the WorkoutSet model, tied to a specific Workout.
WorkoutSetFormSet = inlineformset_factory(
    Workout,          # Parent model
    WorkoutSet,       # Child model
    fields=('exercise', 'reps', 'weight'), # Fields for the user to fill out
    extra=3,          # Number of empty rows to show by default
    can_delete=False  # We will keep it simple for now!
)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        # We deliberately DO NOT include the 'user' field here.
        # We want to set that automatically in the background for security!
        fields = ['name', 'description']

        # Make the description box a little smaller so it looks nicer
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }