from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import LayananJenis
from .models import Layanan
from .models import SkripsiJudul

from .forms_dosen import formProfile

from .decorators_dosen import check_userdosen
from .decorators_dosen import dosen_required



@dosen_required
@check_userdosen
def profile_dosen(request):
    userdosen = request.userdosen    
    if request.method == 'POST':
        form = formProfile(request.POST, request.FILES, instance=userdosen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_dosen')
    else:
        form = formProfile(instance=userdosen)

    context = {
        'title' : 'Edit Profile',
        'heading' : 'Edit Profile',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'form': form,
    }
    return render(request, 'dosen/set/profile.html', context)



