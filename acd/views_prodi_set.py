from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib import messages

from .models import Layanan, UserMhs, UserProdi, UserDosen, SkripsiJudul
from django.contrib.auth.models import User

from .forms_prodi import formLayananEdit, formProfile, formUserEdit
from .decorators_prodi import admin_prodi_required, check_userprodi

########### SET PROFILE #####################################################

@admin_prodi_required
def profile_prodi(request):
    userprodi = UserProdi.objects.get(username=request.user)      
    if request.method == 'POST':
        form = formProfile(request.POST,  request.FILES, instance=userprodi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_prodi')
    else:
        form = formProfile(instance=userprodi)

    context = {
        'title' : 'Profile',
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
    if role == 'Mahasiswa':
        user_data = UserMhs.objects.filter(prodi=userprodi.prodi)
    elif role == 'Dosen':
        user_data = UserDosen.objects.filter(prodi=userprodi.prodi)
    
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
    userMaster = get_object_or_404(User, username=id)
    if role == 'Mahasiswa':
        userSelect = get_object_or_404(UserMhs, nim=id)
    if role == 'Dosen':
        userSelect = get_object_or_404(UserDosen, nip=id)
    if request.method == 'POST':
        form = formUserEdit(request.POST, request.FILES, instance=userSelect)
        if form.is_valid():
            userSelect.save()  
            messages.success(request, 'Update User Berhasil')
            if role == 'Mahasiswa':
                return redirect('acd:user_edit', userSelect.nim_id, role)
            else:
                return redirect('acd:user_edit', userSelect.nip_id, role)
        else:
            messages.error(request, 'periksa kembali isian data anda!')
            if role == 'Mahasiswa':
                return redirect('acd:user_edit', userSelect.nim_id, role)
            else:
                return redirect('acd:user_edit', userSelect.nip_id, role)

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





