
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import taskform
from .models import task

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
       if request.method == 'GET':
              return render(request, 'signup.html', {
              'form': UserCreationForm
       })
              
       else:
              if request.POST['password1'] == request.POST['password1']:
                 try:
                     user = User.objects.create_user(
                         username=request.POST['username'],password=request.POST
                         ['password1'])
                     user.save()
                     login(request,user)
                     return redirect('tasks') 
                 except IntegrityError:
                           return  render(request, 'signup.html', {
                         'form': UserCreationForm,
                         "error": 'user already exists'
                      })
                  
                   
def tasks(request):
    tasks = task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {
          'form': taskform
      })
    else:
        try:
            form = taskform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except: ValueError
        return render(request, 'create_task.html',  {
                'form': taskform,
                'error': 'please provide valida date'
            }) 
     
def task_detail(request, task_id):
 if request.method == 'GET':
        Task = get_object_or_404(task, pk=task_id)
        form = taskform(instance=task)
        return render(request, 'task_detail.html', {'Task': Task, 'form': form})
 else:
    try:
         Task = get_object_or_404(task, pk=task_id)
         form = taskform(request.POST, instance=Task)
         form.save()
         return redirect('tasks')
    except ValueError:
         return render(request, 'task_detail.html', {'Task': Task, 'form': form,
             'error': "Error updating task" })
          

       
     
  

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
          'form': AuthenticationForm
    })    
    else:
     User=authenticate(
            request, username=request.POST['username'],password=request.POST
            ['password'])
     if User is None:
         return render(request, 'signin.html', {
             'form': AuthenticationForm,
             'error': 'Username or password is incorrect'              
         })
     else:
         login(request, User)
         return redirect('tasks')        
         
      #buena loca vea bien las cosas jajjajaja 

       
   
   

