from django import forms
from django.db.models import Q
from django.forms import inlineformset_factory
from .models import Exercise, Workout, WorkoutSet

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


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

class WorkoutSetForm(forms.ModelForm):
    class Meta:
        model = WorkoutSet
        fields = ['exercise', 'reps', 'weight']

    def __init__(self, *args, **kwargs):
        # Pop the user out of the dictionary before passing it to the standard Django form
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If a user was passed in, filter the dropdown menu!
        if user:
            self.fields['exercise'].queryset = Exercise.objects.filter(
                # Q objects allow the use of the pipe '|' as an OR operator
                Q(user__isnull=True) | Q(user=user)
            ).order_by('name')


# This creates a group of forms for the WorkoutSet model, tied to a specific Workout.
# UPDATE: Tell the factory to use our new WorkoutSetForm
WorkoutSetFormSet = inlineformset_factory(
    Workout,          # Parent model
    WorkoutSet,       # Child model
    form=WorkoutSetForm,
    # fields=('exercise', 'reps', 'weight'), # Fields for the user to fill out
    extra=3,          # Number of empty rows to show by default
    can_delete=False  # We will keep it simple for now!
)