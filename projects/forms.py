from .models import *
from django import forms

class ProjectForm(forms.ModelForm):
    user_email = forms.EmailField(required=False, help_text="Введіть електронну адресу користувача для додавання до проекту")

    class Meta:
        model = Project
        fields = ['name', 'description']

    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        if email:
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError("Користувача з такою електронною адресою не існує.")
        return email

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assignee']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['assignee'].queryset = project.users.all()