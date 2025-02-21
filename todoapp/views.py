from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, TaskForm

from django.contrib.auth import login,logout
from .models import Task

@login_required
def hello(request):
    return HttpResponse("Hello, World!")

@login_required
def hello_protected(request):
    user = request.user
    return render(request, "todoapp/protected.html", {"user": user})
def index(request):
    return HttpResponse("Welcome to the todoapp index")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # automatically redirect to login page
            return redirect('task_list') #  redirect to login page
    else:
        form = UserRegistrationForm()
    return render(request, 'todoapp/register.html',{'form':form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user = request.user).order_by('-created_at')
    return render(request, 'todoapp/task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)  
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')  
    else:
        form = TaskForm()
    return render(request, 'todoapp/create_task.html', {"form": form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todoapp/create_task.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('task_list')
    