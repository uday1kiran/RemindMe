from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ReminderForm
from .models import Reminder

# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request,'reminder/signupuser.html',{'form':UserCreationForm()})
    else:
        #fields copied from browser inspect
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentreminders')
            except IntegrityError:
                return render(request,'reminder/signupuser.html',{'form':UserCreationForm(),'error':'User already exists,please use a different name'})

        else:
            return render(request, 'reminder/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'reminder/loginuser.html', {'form': AuthenticationForm()})
    else:
        authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'reminder/loginuser.html', {'form': AuthenticationForm(),'error':'Username and password  did not match'})
        else:
            login(request,user)
            return redirect('currentreminders')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request,'reminder/home.html')

def currentreminders(request):
    #reminders = Reminder.objects.all()
    reminders = Reminder.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'reminder/currentreminders.html',{'reminders':reminders})

def createreminder(request):
    if request.method == 'GET':
        return render(request, 'reminder/createreminder.html',{'form':ReminderForm()})
    else:
        try:
            form = ReminderForm(request.POST)
            newreminder = form.save(commit=False)
            newreminder.user = request.user
            newreminder.save()
            return redirect('currentreminders')
        except ValueError:
            return render(request, 'reminder/createreminder.html', {'form': ReminderForm(),'error':'bad data passed in. Try again.'})