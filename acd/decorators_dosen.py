from django.shortcuts import redirect
from django.contrib import messages
from .models import UserDosen, Pejabat
from functools import wraps
from django.utils import timezone

now = timezone.now()

def check_userdosen(function):
    def wrapper(request, *args, **kwargs): 
        userdosen = UserDosen.objects.get(nip=request.user)
        request.userdosen = userdosen
        if userdosen.photo == None :
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_dsn')     
        return function(request, *args, **kwargs)
    return wrapper

def dosen_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        userdosen = UserDosen.objects.get(nip=request.user)
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.last_name != "Dosen":
            return redirect('/acd/dashboard')
        is_pejabat_aktif = Pejabat.objects.filter(
            pejabat=userdosen,
            tgl_mulai__lte=now,
            tgl_selesai__gte=now
        ).exists()
        request.is_pejabat_aktif = is_pejabat_aktif  # bisa dipakai di view & template
        return view_func(request, *args, **kwargs)
    return _wrapped_view