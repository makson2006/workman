from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def project_list(request):
    user = request.user
    owned_projects = Project.objects.filter(owner=user)
    participated_projects = Project.objects.filter(users=user).exclude(owner=user)
    return render(request, 'projects/project_list.html', {
        'owned_projects': owned_projects,
        'participated_projects': participated_projects
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    is_owner = project.owner == request.user
    return render(request, 'projects/project_detail.html', {'project': project, 'is_owner': is_owner})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            user_email = form.cleaned_data.get('user_email')
            if user_email:
                    user = User.objects.get(email=user_email)
                    project.users.add(user)
                    messages.success(request, f"Користувач {user_email} успішно доданий до проекту.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            user_email = form.cleaned_data.get('user_email')
            if user_email:
                try:
                    user = User.objects.get(email=user_email)
                    if user in project.users.all():
                        messages.error(request, f"Користувач з email {user_email} вже у проекті.")
                    else:
                        project.users.add(user)
                        messages.success(request, f"Користувач {user_email} успішно доданий до проекту.")
                except User.DoesNotExist:
                    messages.error(request, f"Користувач з email {user_email} не знайдений.")
            form.save()
            return redirect('project_edit', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'project': project})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project,id=project_id,owner=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request,'projects/project_confirm_delete.html',{'project':project})


@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        messages.error(request, "У вас немає доступу до цього проекту.")
        return redirect('project_list')

    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project

            if task.assignee not in project.users.all():
                form.add_error('assignee', 'Добавте користувача')
            else:
                task.save()
                messages.success(request, "Завдання успішно створено.")
                return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm(project=project)

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
    return render(request,'projects/task_confirm_delete.html',{'task':task,'project':project})


