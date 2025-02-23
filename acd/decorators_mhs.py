from django.shortcuts import redirect
from django.contrib import messages
from .models import UserMhs 
from functools import wraps

def check_usermhs(function):
    def wrapper(request, *args, **kwargs):
        try:
            # Ambil data UserMhs terkait user
            usermhs = UserMhs.objects.get(nim=request.user)
            # Tambahkan data UserMhs ke request
            request.usermhs = usermhs
        except UserMhs.DoesNotExist:
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