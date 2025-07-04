from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.


def all_event(request):
    return render(request,'index.html',{'task': Task})

def login_page(request):
    return render(request,'login.html')


def task_list(request):
    tasks = Task.objects.all()    # Retrieve all tasks

    if request.method == 'POST':    # Handle form submissions
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to avoid duplicate submissions
    else:
        form = TaskForm()

    # Pass tasks and the form to the template
    return render(request, 'task_list.html', {'tasks': tasks, 'form': form})

def mark_task_done(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = True
        task.save()
        messages.success(request, f'Task "{task.title}" marked as done!')
    return redirect('task_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.save()
        messages.success(request, f'Task updated successfully!')
    
    return redirect('task_list')

def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted!')
    return redirect('task_list')