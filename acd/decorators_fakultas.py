from django.shortcuts import redirect
from django.contrib import messages
from .models import UserFakultas 
from functools import wraps

def check_userfakultas(function):
    def wrapper(request, *args, **kwargs):   
        userfakultas = UserFakultas.objects.get(username=request.user)
        request.userfakultas = userfakultas
        if userfakultas.photo == None :
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_fakultas')               
        return function(request, *args, **kwargs)
    return wrapper

def fakultas_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.last_name != "Admin Fakultas":
            return redirect('/acd/dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view