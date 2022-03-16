from multiprocessing import context
from re import search
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from todo.models import Todo
from todo.forms import TodoForm

# Create your views here.
@login_required
def homePage(request):
    

    pk = request.user.id
    user = User.objects.get(id=pk)
    task = Todo.objects.filter(user = user)
    context = {
        
        'tasks':task,
    }
    return render(request, 'todo/homePage.html', context)

@login_required
def detailTask(request, pk):
    task = Todo.objects.get(id= pk)
    context = {
        'task':task
    }
    return render(request, 'todo/detailTask.html', context)

@login_required
def deleteTask(request,pk):
    task = Todo.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('todo-home')

    context = {
        'task':task
    }
    return render(request, 'todo/deleteTask.html', context)

@login_required
def addTask(request):
    form = TodoForm(request.POST)
    if request.method == 'POST':
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('todo-home')
    context = {
        'form':form,
    }
    return render(request, 'todo/addTask.html', context)

@login_required
def updateTask(request, pk):
    task = Todo.objects.get(id=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo-home')
    else:
        form = TodoForm(instance=task)
    context = {
        'form':form,
    }
    return render(request, 'todo/updateTask.html',context)

def search(request):
    user = request.user
    if request.method == 'GET':
        searched = request.GET.get('search-todo')
        if searched:
            task = Todo.objects.filter(title__icontains = searched)
        else:
            task = Todo.objects.filter(user=user)
        context = {
            'search':searched,
            'tasks':task,
        }
    return render(request, 'todo/searchPage.html', context)