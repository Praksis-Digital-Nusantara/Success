from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from acd.models import Proposal, Hasil, Ujian
from datetime import datetime

tanggal_now = datetime.now().date()

def custom_404(request, exception):
    return render(request, "404.html", status=404)

def index(request):
    proposal = Proposal.objects.filter(seminar_tgl=tanggal_now).order_by('-date_in')
    hasil = Hasil.objects.filter(seminar_tgl=tanggal_now).order_by('-date_in')
    ujian = Ujian.objects.filter(ujian_tgl=tanggal_now).order_by('-date_in')
    context = {
        'title' : 'Home',
        'heading' : 'Home Web Akademik',
        'proposal' : proposal,
        'hasil' : hasil,
        'ujian' : ujian,
    }
    return render(request,'index.html', context) 




def about(request):
    context = {
        'title' : 'About',
        'heading' : 'TENTANG APLIKASI' 
    }
    return render(request,'about.html', context) 

def verTTD(request):
    context = {
        'title' : 'Verifikasi TTD',
        'heading' : 'Verifikasi TTD',
    }
    return render(request,'ver_ttd.html', context) 

def loginView(request):
    context = {
        'title': 'Login',
        'heading': 'Login',
    }
    if request.method == "POST":
        print (request.POST)
        username_in = request.POST['username']
        password_in = request.POST['password']
        user = authenticate(request, username=username_in, password=password_in)        
        if user is not None:
            login(request, user)
            print(user)
            messages.success(request, 'Selamat Datang!')
            return redirect('/acd/')
        else:
            messages.warning(request, 'Periksa Kembali Username dan Password Anda!')
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
