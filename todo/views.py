from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login ,logout,authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import TodoModel
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request) : 
    return render(request,'todo/home.html')

def signupview(request) : 
    if request.method == 'GET' :

        return render(request,'todo/signup_user.html' ,{'form':UserCreationForm()})
    else : 
        if request.POST['password1'] == request.POST['password2'] : 
            try : 
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('current')
            except IntegrityError : 
                return render(request,'todo/signup_user.html' ,{'form':UserCreationForm(),'error':'Username already taken pick a new username'})


        else : 
            return render(request,'todo/signup_user.html' ,{'form':UserCreationForm(),'error':'passwords are not match!'})

def loginview(request) : 
    if request.method == 'GET' :
        return render(request,'todo/login_user.html' ,{'form':AuthenticationForm()})
    else : 
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        login(request,user)
        return redirect('welcome')
@login_required
def todo(request) : 
    if request.method == 'GET' :
        return render(request,'todo/todo.html' ,{'form':TodoForm()})
    else : 
        form = TodoForm(request.POST)
        newtodo=form.save(commit=False)
        newtodo.user=request.user
        newtodo.save()
        return redirect('home')


@login_required
def logoutview(request):
    logout(request) 
    return redirect('home')
@login_required
def current(request) : 
    todos = TodoModel.objects.filter(user=request.user,finished_on__isnull=True)
    return render(request,'todo/current.html',{'todos':todos})
@login_required
def completed(request) : 
    todos = TodoModel.objects.filter(user=request.user,finished_on__isnull=False).order_by('-finished_on')
    return render(request,'todo/completed.html',{'todos':todos})
@login_required
def viewtodo(request , todo_pk) :
    todo = get_object_or_404(TodoModel,pk=todo_pk,user=request.user)
    if request.method == 'GET' : 

        form = TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,})
    else : 
        try : 
            form = TodoForm(request.POST,instance=todo) 
            form.save()
        except ValueError : 
            return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,'error':'bad data'})
        return redirect('current')
@login_required
def completetodo(request,todo_pk) : 
    todo = get_object_or_404(TodoModel,pk=todo_pk,user=request.user)
    if request.method == 'POST' :
        todo.finished_on = timezone.now()
        todo.save()
        return redirect('current')

@login_required
def deletetodo(request,todo_pk) : 
    todo = get_object_or_404(TodoModel,pk=todo_pk,user=request.user)
    if request.method == 'POST' :
        todo.delete()
        return redirect('current')
