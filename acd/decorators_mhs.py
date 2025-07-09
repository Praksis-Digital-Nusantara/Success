from django.shortcuts import redirect
from django.contrib import messages
from .models import UserMhs, User 
from functools import wraps

def check_usermhs(function):
    def wrapper(request, *args, **kwargs):
        usermhs = UserMhs.objects.get(nim=request.user) 
        request.usermhs = usermhs
        if usermhs.photo == None or usermhs.tempat_lahir == None or usermhs.tgl_lahir == None or usermhs.gender == None or usermhs.penasehat_akademik == None:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_mhs')               
        return function(request, *args, **kwargs)
    return wrapper


def mahasiswa_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.last_name != "Mahasiswa":
            return redirect('/acd/dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view