from .models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        models = Project
        fields = ['name','description']

class TaskForm(forms.ModelForm):
    class Mets:
        models = Task
        fields = ['project', 'title', 'description', 'assignee', 'status']
