from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import LayananJenis
from .models import Layanan
from .models import SkripsiJudul

from .forms_mhs import formAddLayanan
from .forms_mhs import formProfile
from .forms_mhs import formSkripsiJudul

from .decorators_mhs import check_usermhs
from .decorators_mhs import mahasiswa_required



@mahasiswa_required
@check_usermhs
def profile_mhs(request):
    usermhs = request.usermhs    
    if request.method == 'POST':
        form = formProfile(request.POST, request.FILES, instance=usermhs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_mhs')
    else:
        form = formProfile(instance=usermhs)

    context = {
        'title' : 'Edit Profile',
        'heading' : 'Edit Profile',
        'usermhs' : usermhs,
        'photo' : usermhs.photo,
        'form': form,
    }
    return render(request, 'mhs/set/profile.html', context)




#################### LAYANAN MAHASISWA

@mahasiswa_required
@check_usermhs
def layananMe(request):
    usermhs = request.usermhs 
    context = {
        'title': 'Layanan',
        'heading': 'List Layanan',
    }
    layanan_data = Layanan.objects.filter(mhs=request.user)
    context = {
        'title' : 'Layanan Akademik',
        'heading' : 'Layanan Akademik',
        'usermhs' : usermhs,
        'photo' : usermhs.photo,
        'layanan_data': layanan_data,
    }
    return render(request, 'mhs/layanan_me.html', context)


def get_prasyarat_layanan(request): #untuk json respon jenis layanan
    layanan_id = request.GET.get('layanan_id')
    try:
        layanan = LayananJenis.objects.get(id=layanan_id)
        return JsonResponse({'prasyarat_layanan': layanan.prasyarat_layanan}, status=200)
    except LayananJenis.DoesNotExist:
        return JsonResponse({'error': 'Jenis layanan tidak ditemukan'}, status=404)


@mahasiswa_required
@check_usermhs
def layananAdd(request):
    usermhs = request.usermhs 
    if request.method == 'POST':
        form = formAddLayanan(request.POST, request.FILES)
        if form.is_valid():
            layanan = form.save(commit=False)  
            layanan.mhs = request.user 
            layanan.prodi = usermhs.prodi   
            layanan.save()  
            messages.success(request, 'Layanan berhasil ditambahkan!')
            return redirect('/acd/layanan_me') 
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan periksa input Anda.')
    else:
        form = formAddLayanan()

    context = {
        'title' : 'Layanan Baru',
        'heading' : 'Layanan Baru',
        'usermhs' : usermhs,
        'photo' : usermhs.photo,
        'form': form,
    }
    return render(request, 'mhs/layanan_add.html', context)




#################### SKRIPSI

@mahasiswa_required
@check_usermhs
def skripsi(request):
    usermhs = request.usermhs    
    context = {
        'title' : 'Skripsi',
        'heading' : 'Skripsi',
        'usermhs' : usermhs,
        'photo' : usermhs.photo,
    }
    return render(request, 'mhs/skripsi.html', context)


@mahasiswa_required
@check_usermhs
def skripsi_pjudul(request):
    usermhs = request.usermhs
    try:
        skripsi_judul = SkripsiJudul.objects.get(user=request.user)
    except ObjectDoesNotExist:
        skripsi_judul = None

    if request.method == 'POST':
        form = formSkripsiJudul(request.POST, instance=skripsi_judul)
        if form.is_valid():
            # Menambahkan user yang sedang login jika menambah data baru
            skripsi_judul = form.save(commit=False)
            skripsi_judul.status = 'Waiting'
            skripsi_judul.prodi = usermhs.prodi
            skripsi_judul.user = request.user
            skripsi_judul.save()
            messages.success(request, 'Judul berhasil disimpan.')
            return redirect('/acd/skripsi_pjudul')
        else:
            messages.error(request, 'Periksa kembali isian form.') 
    else:
        form = formSkripsiJudul(instance=skripsi_judul)
     
    context = {
        'title' : 'Pengajuan Judul',
        'heading' : 'Pengajuan Judul',
        'usermhs' : usermhs,
        'photo' : usermhs.photo,
        'form': form,
    }
    return render(request, 'mhs/skripsi_pjudul.html', context)