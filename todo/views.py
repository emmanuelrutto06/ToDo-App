from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Task

def home(request):
    tasks = Task.objects.filter(is_completed=False).order_by('-updated_at')
    completed_tasks = Task.objects.filter(is_completed=True)
    incompleted_tasks = Task.objects.filter(is_completed=False)
    context = {
        'tasks':tasks,
        'completed_tasks':completed_tasks,
        'incompleted_tasks':incompleted_tasks,
    }
    return render(request, 'home.html', context) 

def add_task(request):
    task = request.POST['task']
    Task.objects.create(task=task)
    return redirect('home')

def mark_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed=True
    task.save()
    return redirect('home')

def mark_as_undone(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed=False
    task.save()
    return redirect('home')

def edit_task(request, pk):
    edittask = get_object_or_404(Task, pk=pk)
    if request.method=='POST':
        new_task = request.POST['task']
        edittask.task = new_task
        edittask.save()
        return redirect('home')
    else:
        context={
            'edittask':edittask
        }
        return render(request, 'edit_task.html', context)

def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('home')