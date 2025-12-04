from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear/', views.create_task, name='create_task'),
    path('toggle/<int:task_id>/', views.toggle_task_complete, name='toggle_task'),
    path('perfil/', views.edit_profile, name='edit_profile'),
    path('calendario/', views.calendar_view, name='calendar_view'),
    path('recordatorios/', views.reminders, name='reminders'),
    path('api/check-due-tasks/', views.check_due_tasks, name='check_due_tasks'),




]
