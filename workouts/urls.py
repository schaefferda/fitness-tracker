from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # The empty string '' means this is the default page for this app
    path('', views.WorkoutListView.as_view(), name='workout_list'),
    path('workout/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('add/', views.WorkoutCreateView.as_view(), name='add_workout'),
    path('edit/<int:pk>/', views.WorkoutUpdateView.as_view(), name='edit_workout'),
    path('delete/<int:pk>/', views.WorkoutDeleteView.as_view(), name='delete_workout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('exercise/add/', views.ExerciseCreateView.as_view(), name='add_exercise'),

    # Auth views remain the same
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='workouts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]