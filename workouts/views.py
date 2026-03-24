import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import WorkoutSession, Exercise
from .forms import ExerciseForm, ProfileForm, UserForm, WorkoutForm, WorkoutSetFormSet




class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'workouts/dashboard.html'

    def get_context_data(self, **kwargs):
        # Override this method to pass our Chart.js data to the template
        context = super().get_context_data(**kwargs)
        workouts = WorkoutSession.objects.filter(user=self.request.user).order_by('date')[:10]

        dates = [w.date.strftime('%b %d') for w in workouts]
        volumes = [float(w.total_volume) for w in workouts]

        context['dates'] = json.dumps(dates)
        context['volumes'] = json.dumps(volumes)
        return context


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'workouts/add_exercise.html'
    success_url = reverse_lazy('add_workout')

    def form_valid(self, form):
        # Attach the logged-in user before saving, making it a "Custom" exercise
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserSettingsView(LoginRequiredMixin, View):
    template_name = 'workouts/settings.html'

    def get(self, request):
        # Load both forms, pre-filled with the logged-in user's current data
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        # Catch the submitted data for both forms
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        # If both are valid, save them both to the database
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Send a success flash message to the user
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('settings')  # Reload the page

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    form_class = WorkoutForm
    template_name = 'workouts/add_workout.html'
    success_url = reverse_lazy('workout_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = WorkoutSetFormSet(self.request.POST, form_kwargs={'user': self.request.user})
        else:
            context['formset'] = WorkoutSetFormSet(form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            form.instance.user = self.request.user
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutSession
    template_name = 'workouts/confirm_delete.html'
    success_url = reverse_lazy('workout_list')

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutSession
    template_name = 'workouts/workout_detail.html'
    context_object_name = 'workout'

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)


class WorkoutListView(LoginRequiredMixin, ListView):
    model = WorkoutSession
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'
    paginate_by = 5  # CBVs handle pagination automatically!

    def get_queryset(self):
        # Security check: you can only view details of your own workouts
        return WorkoutSession.objects.filter(user=self.request.user).order_by('-date')


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutSession
    form_class = WorkoutForm
    template_name = 'workouts/add_workout.html'
    success_url = reverse_lazy('workout_list')

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        if self.request.POST:
            context['formset'] = WorkoutSetFormSet(self.request.POST, instance=self.object, form_kwargs={'user': self.request.user})
        else:
            context['formset'] = WorkoutSetFormSet(instance=self.object, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


# Keep your registration view exactly the same!
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('workout_list')
    else:
        form = UserCreationForm()
    return render(request, 'workouts/register.html', {'form': form})