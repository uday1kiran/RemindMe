from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login
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

def currentreminders(request):
    return render(request,'reminder/currentreminders.html')