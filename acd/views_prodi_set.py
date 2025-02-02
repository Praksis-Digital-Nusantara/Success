from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib import messages

from .models import Layanan, UserMhs, UserProdi, UserDosen, SkripsiJudul
from django.contrib.auth.models import User

from .forms_prodi import formLayananEdit, formProfile, formUserEdit
from .decorators_prodi import admin_prodi_required, check_userprodi

########### SET PROFILE #####################################################

@check_userprodi
@admin_prodi_required
def profile_prodi(request):
    userprodi = request.userprodi    
    if request.method == 'POST':
        form = formProfile(request.POST,  request.FILES, instance=userprodi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_prodi')
    else:
        form = formProfile(instance=userprodi)

    context = {
        'title' : 'Edit Profile',
        'heading' : 'Edit Profile',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'form': form,
    }
    return render(request, 'prodi/set/profile.html', context)



########### SETTING USER LAIN #####################################################

@check_userprodi
@admin_prodi_required
def user_list(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Password tidak cocok.")
        else:
            user = get_object_or_404(User, id=user_id)
            user.set_password(new_password)
            user.save()
            messages.success(request, f"Password untuk {user.username} berhasil diganti.")
            
    userprodi = request.userprodi
    role = request.GET.get('role', 'Mahasiswa')    
    user_data = User.objects.filter(last_name = role)
    context = {
        'title': 'User List',
        'heading': role,
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'user_data': user_data,
    }
    return render(request, 'prodi/set/user_list.html', context)



@check_userprodi
@admin_prodi_required
def user_edit(request, id, role):
    userprodi = request.userprodi  
    userMaster = get_object_or_404(User, id=id)
    if role == 'Mahasiswa':
        userSelect = get_object_or_404(UserMhs, user_id=id)
    if role == 'Dosen':
        userSelect = get_object_or_404(UserDosen, user_id=id)
    if request.method == 'POST':
        form = formUserEdit(request.POST, request.FILES, instance=userSelect)
        if form.is_valid():
            userSelect.save()  
            messages.success(request, 'Berhasil')
            return redirect('acd:user_edit', userSelect.user_id, role)
        else:
            messages.error(request, 'periksa kembali isian data anda!')
            return redirect('acd:user_edit', userSelect.user_id, role)
    else:
        form = formUserEdit(instance=userSelect)

    context = {
        'title' : 'Edit User',
        'heading' : 'Edit User',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'userselect' : userSelect,
        'usermaster' : userMaster,
        'form': form,
    }
    return render(request, 'prodi/set/user_edit.html', context)





