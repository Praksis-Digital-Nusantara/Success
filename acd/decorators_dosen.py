from django.shortcuts import redirect
from django.contrib import messages
from .models import UserDosen 
from functools import wraps

def check_userdosen(function):
    def wrapper(request, *args, **kwargs):
        try:
            # Ambil data Userdosen terkait user
            userdosen = UserDosen.objects.get(user=request.user)
            # Tambahkan data Userdosen ke request
            request.userdosen = userdosen
        except UserDosen.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_dosen')
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