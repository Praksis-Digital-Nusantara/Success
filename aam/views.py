from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from acd.models import Proposal, Hasil, Ujian, IzinPenelitian, SuketIzinObservasi
from datetime import datetime
from django.shortcuts import get_object_or_404

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
            if user.is_superuser:
                request.session['su'] = '557799'
            else:
                request.session['su'] = '0'
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
            del request.session['su']
            logout(request)
            messages.success(request, 'Anda telah berhasil logout!')
        return redirect('login')    

    return render(request,'logout.html', context)             

# Verifikasi TTD Izin Penelitian
def ver_ttd_izp(request, id):
    data = get_object_or_404(IzinPenelitian, id=id)
    context = {
        'title' : 'Verifikasi TTD Izin Penelitian',
        'heading' : 'Verifikasi TTD Izin Penelitian',
        'data' : data,
    }
    return render(request,'verif_ttd/ver_ttd_izp.html', context) 

# Verifikasi TTD Seminar
def ver_ttd_sio(request, id):
    data = get_object_or_404(SuketIzinObservasi, id=id)
    context = {
        'title' : 'Verifikasi TTD Izin Observasi',
        'heading' : 'Verifikasi TTD Izin Observasi',
        'data' : data,
    }
    return render(request,'verif_ttd/ver_ttd_sio.html', context) 
