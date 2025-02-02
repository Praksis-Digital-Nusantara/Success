from  django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    context = {
        'title' : 'Home',
        'heading' : 'Home Web Akademik' 
    }
    return render(request,'index.html', context) 

def about(request):
    context = {
        'title' : 'About',
        'heading' : 'TENTANG APLIKASI' 
    }
    return render(request,'about.html', context) 

def loginView(request):
    context = {
        'title': 'Login',
        'heading': 'Login',
    }
    if request.method == "POST":
        print (request.POST)
        username_in = request.POST['username']
        password_in = request.POST['password']
        # username_in = 'risal' 
        # password_in = '@ahmad123'

        user = authenticate(request, username=username_in, password=password_in)        

        if user is not None:
            login(request, user)
            print(user)
            return redirect('/acd')
        else:
            return redirect('login')
    
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request,'login.html', context) 


@login_required
def LogoutView(request):
    context = {
        'title': 'Login',
        'heading': 'Login Gaes',
    }
    if request.method == "POST":
        if request.POST['logout']=='ya':
            logout(request)
        return redirect('login')    

    return render(request,'logout.html', context)             
