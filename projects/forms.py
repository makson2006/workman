from .models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assignee', 'status']
