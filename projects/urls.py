from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/task/<int:task_id>/change_status/', views.change_task_status,name='change_task_status'),
    path('project/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:project_id>/task/create/', views.task_create, name='task_create'),
    path('project/<int:project_id>/task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('project/<int:project_id>/task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('project/<int:project_id>/remove_user/<int:user_id>/', views.project_remove_user, name='project_remove_user'),
]
