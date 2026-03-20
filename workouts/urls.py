from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # The empty string '' means this is the default page for this app
    path('', views.workout_list, name='workout_list'),
    path('add/', views.add_workout, name='add_workout'),
    path('edit/<int:pk>/', views.edit_workout, name='edit_workout'),
    path('delete/<int:pk>/', views.delete_workout, name='delete_workout'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='workouts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]