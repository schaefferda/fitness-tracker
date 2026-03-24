from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import inlineformset_factory
from .models import Exercise, Profile, WorkoutSession, WorkoutSet

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['date', 'session_duration', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'session_duration': forms.TextInput(attrs={'placeholder': 'e.g., 01:15:00 for 1h 15m'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'How did the session go?'}),
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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'height', 'weight']


class WorkoutSetForm(forms.ModelForm):
    class Meta:
        model = WorkoutSet
        fields = ['exercise', 'reps', 'reps_target', 'weight', 'weight_target',
                  'distance', 'distance_target', 'duration', 'duration_target',
                  'equipment', 'positioning', 'modification']

        widgets = {
            'reps': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'reps_target': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'weight_target': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'distance': forms.NumberInput(attrs={'placeholder': '(in miles)', 'class': 'form-control-sm'}),
            'distance_target': forms.NumberInput(attrs={'placeholder': '(in miles)', 'class': 'form-control-sm'}),
            'duration': forms.TextInput(attrs={'placeholder': '(mm:ss)', 'class': 'form-control-sm'}),
            'duration_target': forms.TextInput(attrs={'placeholder': '(mm:ss)', 'class': 'form-control-sm'}),
            'equipment': forms.TextInput(attrs={'placeholder': 'e.g., Barbell, dumbbell, cable, banded, etc.', 'class': 'form-control-sm'}),
            'positioning': forms.TextInput(attrs={'placeholder': 'e.g., Standing, seated, upside-down, etc.', 'class': 'form-control-sm'}),
            'modification': forms.TextInput(attrs={'placeholder': 'e.g., Wide grip, narrow grip, drop set, etc.', 'class': 'form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
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
    WorkoutSession,     # Parent model
    WorkoutSet,         # Child model
    form=WorkoutSetForm,
    # fields=('exercise', 'reps', 'weight'), # Fields for the user to fill out
    extra=1,            # Number of empty rows to show by default
    can_delete=False
)