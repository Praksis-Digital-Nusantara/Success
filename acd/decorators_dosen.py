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
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.last_name != "Dosen":
            return redirect('/acd/dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view