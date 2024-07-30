from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:project_id>/task/create/', views.task_create, name='task_create'),
    path('project/<int:project_id>/task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('project/<int:project_id>/task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
]
