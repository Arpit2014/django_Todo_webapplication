from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Task
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login')
def index(request):
    log_user = request.user
    tasks = Task.objects.filter(user=log_user)

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        data = request.POST['title']
        new = Task(title=data, user=request.user)
        new.save()
        if form.is_valid():
            form.save()
        # return redirect("tasks")

    context = {'tasks': tasks,  'form': form}
    # new = Task(title=tasks, user=request.user)
    # new.save()
    return render(request, 'tasks/list.html', context)


def updateTask(request, pk):
    # log_user = request.user
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/tasks/')

    context = {'form': form}

    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):
    # log_user = request.user
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/tasks/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)
