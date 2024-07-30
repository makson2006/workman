from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request,'projects/project_list.html',{'projects': projects})


@login_required
def project_detail(request,project_id):
    project = get_object_or_404(Project,id=project_id,owner=request.user)
    tasks = project.tasks.all()
    return render(request,'projects/project_detail',{'project':project,'tasks':tasks})

    # ПІДКЛЮЧИТИ МАЙСКЛ АБО ПОСТГРЕ