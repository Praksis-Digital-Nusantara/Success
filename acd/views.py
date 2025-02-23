from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import UserMhs, UserProdi, UserFakultas, UserDosen



@login_required
def index(request):

    userC = None # izin menambahkan userC = None
    if request.user.last_name == 'Mahasiswa':
        try:
            userC = UserMhs.objects.get(nim=request.user)
            request.usermhs = userC
        except UserMhs.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_mhs')
    elif request.user.last_name == 'Dosen':  
        try:
            userC = UserDosen.objects.get(nip=request.user)
            request.usermhs = userC
        except UserDosen.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_dosen')
    elif request.user.last_name == 'Admin Prodi':  
        try:
            userC = UserProdi.objects.get(user=request.user)
            request.usermhs = userC
        except UserProdi.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_prodi')
    elif request.user.last_name == 'Admin Fakultas':  
        try:
            userC = UserFakultas.objects.get(user=request.user)
            request.usermhs = userC
        except UserFakultas.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_fakultas')  
        
    context = {
        'title' : 'Dashboard',
        'heading' : 'Home Web Akademik',
        'photo' : userC.photo if userC else None, # izin menambahkan # if userC else None,
    }
    if request.user.last_name == "Admin Prodi":
        return render(request,'prodi/index.html', context)
    elif request.user.last_name == "Admin Fakultas":
        return render(request,'fakultas/index.html', context)
    elif request.user.last_name == "Mahasiswa":
        return render(request,'mhs/index.html', context)
    elif request.user.last_name == "Dosen":
        return render(request,'dosen/index.html', context)
    else:
        # return render(request,'mhs/index.html', context)
        return HttpResponse("Hello, world!")

 
@login_required
def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update session auth hash untuk mencegah logout setelah ganti password
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Anda berhasil diubah!')
            return redirect('/acd/changepass')
        else:
            messages.error(request, 'Harap periksa kembali isian formulir.')
    else:
        form = PasswordChangeForm(user=request.user)

    if request.user.last_name == 'Mahasiswa':
        try:
            userC= UserMhs.objects.get(user=request.user)
            request.userC = userC
        except UserMhs.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_mhs')
    elif request.user.last_name == 'Dosen':
        try:
            userC= UserDosen.objects.get(user=request.user)
            request.userC = userC
        except UserDosen.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_dosen')
    elif request.user.last_name == 'Admin Prodi':
        try:
            userC= UserProdi.objects.get(user=request.user)
            request.userC = userC
        except UserProdi.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_prodi')
    elif request.user.last_name == 'Admin Fakultas':
        try:
            userC= UserFakultas.objects.get(user=request.user)
            request.userC = userC
        except UserFakultas.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_fakultas')


    context = {
        'title' : 'Change Password',
        'heading' : 'Change Password',
        'photo' : userC.photo,
        'form': form,
    }
    return render(request, 'changepass.html', context)

