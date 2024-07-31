from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request,'projects/project_list.html',{'projects': projects})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm
    return render(request,'projects/project_form.html',{'form':form})

@login_required
def project_edit(request,project_id):
    project = get_object_or_404(Project, id=project_id,owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=Project)
    return render(request,'projects/project_form.html',{'form':form})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project,id=project_id,owner=request.user)
    if request.method == 'POST':
        project.detelete()
        return redirect('project_list')
    return render(request,'projects/project_confirm_delete.html',{'project':project})

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'projects/task_form.html', {'form': form, 'project': project})


@login_required
def task_edit(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # Передача екземпляра моделі
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm(instance=task)  # Передача екземпляра моделі

    return render(request, 'projects/task_form.html', {'form': form, 'project': project})

@login_required
def task_delete(request,project_id,task_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=project.id)
    return render(request,'projects/task_confirm_delete',{'task':task,'project':project})


