from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .models import (Layanan, 
                     SkripsiJudul, 
                     NoSurat, 
                     ProdiPejabat, 
                     TTDProdi)

from .forms_prodi import (formLayananEdit, 
                          formNosuratAdd, 
                          formTTD
                          )
from .decorators_prodi import admin_prodi_required, check_userprodi


########### NOMOR SURAT #####################################################

@check_userprodi
@admin_prodi_required
def nosurat(request):           
    userprodi = request.userprodi
    tahun = datetime.now().year
    nosurat_cek = NoSurat.objects.filter(tahun=tahun, jurusan=userprodi.prodi.jurusan).order_by('-nomor').first()
    if nosurat_cek:
        nosurat_baru = nosurat_cek.nomor + 1
    else:
        nosurat_baru = 1  

    if request.method == 'POST':
        form = formNosuratAdd(request.POST)
        if form.is_valid():
            nosurat = form.save(commit=False)  
            nosurat.adminp = request.user   
            nosurat.jurusan = userprodi.prodi.jurusan   
            nosurat.tahun = tahun
            nosurat.nomor = nosurat_baru 
            nosurat.save()  
            messages.success(request, 'Berhasil')
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:nosurat')
    else:
        form = formNosuratAdd(request.POST)

    data = NoSurat.objects.filter(jurusan=userprodi.prodi.jurusan )
    context = {
        'title': 'Nomor Surat',
        'heading': 'Nomor Surat',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data' : data,
        'form' : form
    }
    return render(request, 'prodi/nosurat.html', context)


###################### TTD QRCODE ########################
@check_userprodi
@admin_prodi_required
def ttd(request):           
    userprodi = request.userprodi  
    data = TTDProdi.objects.filter(prodi=userprodi.prodi)
    context = {
        'title': 'TTD Qrcode',
        'heading': 'TTD Qrcode',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/ttd.html', context)

@check_userprodi
@admin_prodi_required
def ttd_edit(request, id=0):
    userprodi = request.userprodi
    try:
        data = TTDProdi.objects.get(id=id)
    except ObjectDoesNotExist:
        data = None
    if request.method == 'POST':
        form = formTTD(request.POST, instance=data)
        if form.is_valid():
            data = form.save(commit=False)  
            data.adminp = request.user   
            data.prodi = userprodi.prodi
            data.save()  
            messages.success(request, 'Berhasil')
            return redirect('acd:ttd')
        else:
            messages.error(request, 'periksa kembali isian data anda!')
    else:
        form = formTTD(instance=data)

    context = {
        'title' : 'Kelolah TTD',
        'heading' : 'Kelolah TTD',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'form': form,
    }
    return render(request, 'prodi/ttd_edit.html', context)



###################### LAYANAN ########################

@check_userprodi
@admin_prodi_required
def layanan(request):
    userprodi = request.userprodi  
    layanan_data = Layanan.objects.all()
    # data = User.objects.filter(last_name='Mahasiswa').select_related('usermhs').prefetch_related('skripsi_judul')
    context = {
        'title': 'Layanan',
        'heading': 'List Layanan',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'layanan_data': layanan_data,
    }
    return render(request, 'prodi/layanan.html', context)


@check_userprodi
@admin_prodi_required
def layanan_edit(request, id):
    userprodi = request.userprodi  
    layanan = get_object_or_404(Layanan, id=id)
    if request.method == 'POST':
        form = formLayananEdit(request.POST, request.FILES, instance=layanan)
        if form.is_valid():
            layanan = form.save(commit=False)  
            layanan.adminp = request.user   
            layanan.save()  
            messages.success(request, 'Berhasil')
            return redirect('acd:layanan_edit', id=layanan.id)
        else:
            messages.error(request, 'periksa kembali isian data anda!')
            return redirect('acd:layanan_edit', id=layanan.id)
    else:
        form = formLayananEdit(instance=layanan)

    context = {
        'title' : 'Kelolah Layanan',
        'heading' : 'Kelolah Layanan',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'form': form,
    }
    return render(request, 'prodi/layanan_edit.html', context)


###################### PENGAJUAN JUDUL ########################

@check_userprodi
@admin_prodi_required
def skripsi_sjudul(request):
    if request.method == "POST":
        skripsi_id = request.POST.get("skripsi_id")
        status_ket = request.POST.get("status_ket")
        status = request.POST.get("status")

        skripsi = get_object_or_404(SkripsiJudul, id=skripsi_id)
        skripsi.status = status
        skripsi.status_ket = status_ket
        skripsi.save()       
        messages.success(request, f"Status Skripsi {skripsi_id} = {status}")

    userprodi = request.userprodi  
    data = SkripsiJudul.objects.all()
    context = {
        'title': 'Seleksi Judul',
        'heading': 'Seleksi Judul',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/skripsi_sjudul.html', context)