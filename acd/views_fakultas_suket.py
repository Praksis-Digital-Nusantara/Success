from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils import timezone

from .models import NoSuratFakultas, UserMhs, UserDosen, KodeSurat, Layanan, SkripsiJudul
from .models import SuketAktifKuliah, SuketIzinObservasi, SuketRekomendasi, SuketIzinLab, SuketBerkelakuanBaik, SuketCutiAkademik, SuketBebasPustaka
from .models import SuratTugas, SuratTugas_NamaDosen, SuratTugas_NamaMhs


from .forms_fakultas import formSuketAktifKuliah, formSuketIzinObservasi, formSuketRekomendasi, formSuketIzinLab, formSuketBerkelakuanBaik, formSuketCutiAkademik, formSuketBebasPustaka
from .forms_fakultas import formSuratTugas, formSuratTugas_NamaDosen, formSuratTugas_NamaMhs

from .decorators_fakultas import check_userfakultas
from .decorators_fakultas import fakultas_required

from aam.context_processors import web_name

tgl_now = timezone.now()

import json


##########################  AKTIF KULIAH ######################################
@fakultas_required
@check_userfakultas
def suket_aktifkuliah(request):      
    userfakultas = request.userfakultas      
    data = SuketAktifKuliah.objects.all().order_by('-date_in')

    context = {
        'title': 'Suket Aktif Kuliah',
        'heading': 'Suket Aktif Kuliah',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/suket_aktifkuliah.html', context)    


@fakultas_required
@check_userfakultas
def suket_aktifkuliah_edit(request, nim):      
    userfakultas = request.userfakultas
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketAktifKuliah.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketAktifKuliah(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Suket Aktif Kuliah')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    perihal = 'Surat Aktif Kuliah ',
                    tujuan = 'Mahasiswa'  + str(mhs),
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
                suket.no_surat = nosurat 
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Keterangan Aktif Kuliah', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Keterangan Aktif Kuliah telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_aktifkuliah/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_aktifkuliah_edit', nim=nim)
    else:
        form = formSuketAktifKuliah(instance=datasuket)

    layanan = Layanan.objects.filter().order_by('-date_in').first()
    context = {
        'title': 'Suket Aktif Kuliah',
        'heading': 'Edit Suket Aktif Kuliah',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'mhs' : mhs,
        'form': form,
        'layanan': layanan,
        "layanan_isi_parsed": json.loads(layanan.layanan_isi),
    }
    return render(request, 'fakultas/suket_aktifkuliah_edit.html', context)     


@fakultas_required
@check_userfakultas
def suket_aktifkuliah_del(request, id):      
    data = get_object_or_404(SuketAktifKuliah, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:suket_aktifkuliah')     


##########################  BERKELAKUAN BAIK ######################################
@fakultas_required
@check_userfakultas
def suket_berkelakuanbaik(request):
    userfakultas = request.userfakultas
    data = SuketBerkelakuanBaik.objects.all().order_by('-date_in')

    context = {
        'title': 'Suket Berkelakuan Baik',
        'heading': 'Suket Berkelakuan Baik',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/suket_berkelakuanbaik.html', context)    


@fakultas_required
@check_userfakultas
def suket_berkelakuanbaik_edit(request, nim):      
    userfakultas = request.userfakultas
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketBerkelakuanBaik.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketBerkelakuanBaik(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Suket Berkelakuan Baik')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    tujuan = 'Mahasiswa'  + str(mhs),
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
                suket.no_surat = nosurat 
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Keterangan Berkelakuan Baik', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Keterangan Berkelakuan Baik telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_berkelakuanbaik/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_berkelakuanbaik_edit', nim=nim)
    else:
        form = formSuketBerkelakuanBaik(instance=datasuket)
    layanan = Layanan.objects.filter().order_by('-date_in').first()
    context = {
        'title': 'Surat Berkelakuan Baik',
        'heading': 'Edit Surat Berkelakuan Baik',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'mhs' : mhs,
        'form': form,
        'layanan': layanan,
        "layanan_isi_parsed": json.loads(layanan.layanan_isi),
    }
    return render(request, 'fakultas/suket_berkelakuanbaik_edit.html', context)  


@fakultas_required
@check_userfakultas
def suket_berkelakuanbaik_del(request, id):      
    data = get_object_or_404(SuketBerkelakuanBaik, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat Berkelakuan Baik')
    return redirect('acd:suket_berkelakuanbaik')  

######################### CUTI AKADEMIK ######################################
@fakultas_required
@check_userfakultas
def suket_cutiakademik(request):
    userfakultas = request.userfakultas
    data = SuketCutiAkademik.objects.all().order_by('-date_in')

    context = {
        'title': 'Suket Cuti Akademik',
        'heading': 'Suket Cuti Akademik',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/suket_cutiakademik.html', context)    



@fakultas_required
@check_userfakultas
def suket_cutiakademik_edit(request, nim):      
    userfakultas = request.userfakultas
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketCutiAkademik.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketCutiAkademik(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Suket Cuti Akademik')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    tujuan = 'Mahasiswa'  + str(mhs),
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
                suket.no_surat = nosurat 
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Keterangan Cuti Akademik', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Keterangan Cuti Akademik telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_cutiakademik/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_cutiakademik_edit', nim=nim)
    else:
        form = formSuketCutiAkademik(instance=datasuket)
    layanan = Layanan.objects.filter().order_by('-date_in').first()
    context = {
        'title': 'Surat Cuti Akademik',
        'heading': 'Edit Surat Cuti Akademik',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'mhs' : mhs,
        'form': form,
        'layanan': layanan,
        "layanan_isi_parsed": json.loads(layanan.layanan_isi),
    }
    return render(request, 'fakultas/suket_cutiakademik_edit.html', context)  



@fakultas_required
@check_userfakultas
def suket_cutiakademik_del(request, id):      
    data = get_object_or_404(SuketCutiAkademik, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat Cuti Akademik')
    return redirect('acd:suket_cutiakademik')  

##########################  IZIN OBSERVASI ######################################
@fakultas_required
@check_userfakultas
def suket_izinobservasi(request):      
    userfakultas = request.userfakultas      
    data = SuketIzinObservasi.objects.all().order_by('-date_in')

    context = {
        'title': 'Surat Izin Observasi',
        'heading': 'Surat Izin Observasi',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/suket_izinobservasi.html', context)    


@fakultas_required
@check_userfakultas
def suket_izinobservasi_edit(request, nim):      
    userfakultas = request.userfakultas
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketIzinObservasi.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketIzinObservasi(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Suket Izin Observasi')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    perihal = 'Surat Izin Observasi',
                    tujuan = 'Mahasiswa'  + str(mhs),
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
                suket.no_surat = nosurat 
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Izin Observasi', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Izin Observasi telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_izinobservasi/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_izinobservasi_edit', nim=nim)
    else:
        form = formSuketIzinObservasi(instance=datasuket)

    context = {
        'title': 'Surat Izin Observasi',
        'heading': 'Edit Surat Izin Observasi',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'mhs' : mhs,
        'form': form,
    }
    return render(request, 'fakultas/suket_izinobservasi_edit.html', context)     


@fakultas_required
@check_userfakultas
def suket_izinobservasi_del(request, id):      
    data = get_object_or_404(SuketIzinObservasi, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:suket_izinobservasi')     



##########################  IZIN LABORATORIUM ######################################
@fakultas_required
@check_userfakultas
def suket_izinlab(request):      
    userfakultas = request.userfakultas      
    data = SuketIzinLab.objects.all().order_by('-date_in')

    context = {
        'title': 'Surat Izin Laboratorium',
        'heading': 'Surat Izin Laboratorium',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/suket_izinlab.html', context)    


@fakultas_required
@check_userfakultas
def suket_izinlab_edit(request, nim):      
    userfakultas = request.userfakultas
    mhs = UserMhs.objects.filter(nim__username=nim).first()
    judul = SkripsiJudul.objects.filter(mhs=mhs).first()
    if not mhs:
        messages.error(request, 'Mahasiswa tidak ditemukan')
        return redirect('acd:suket_izinlab')
    elif not judul:
        messages.error(request, 'Mahasiswa belem memiliki judul skripsi.')
        return redirect('acd:suket_izinlab')
    else:                
        datasuket = SuketIzinLab.objects.filter(mhs=mhs).first()

        if request.method == 'POST':
            form = formSuketIzinLab(request.POST, instance=datasuket)
            if form.is_valid():
                suket = form.save(commit=False)  
                suket.adminp = request.user   
                suket.judul = judul
                suket.mhs = mhs
                if suket.no_surat is None:
                    tahun = datetime.now().year
                    nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                    if nosurat_cek:
                        nosurat_baru = nosurat_cek.nomor + 1
                    else:
                        nosurat_baru = 1  
                    kodesurat = KodeSurat.objects.get(jenis='Suket Izin Lab')

                    addnosurat = NoSuratFakultas.objects.create(
                        adminp = request.user,
                        tahun = tahun,
                        nomor = nosurat_baru, 
                        perihal = 'Surat Izin Laboratorium',
                        tujuan = 'Mahasiswa'  + str(mhs),
                        kode = kodesurat.kode
                    )
                    nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
                    suket.no_surat = nosurat 
                suket.save()
                messages.success(request, 'Berhasil Menerbitkan Surat')
                #update layanan agar status DIPROSES            
                layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Izin Pakai Lab & Pinjam Alat Lab', status__in=['Processing', 'Waiting']).first()
                if layanan:
                    context_pro = web_name(request)
                    layanan.status = 'Completed'
                    layanan.hasil_test = 'Surat Izin Pakai Lab & Pinjam Alat Lab telah terbit, download di tautan berikut:'
                    layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_izinlab/" + str(suket.id)
                    layanan.save()                  
                    messages.success(request, 'Berhasil Mengupdate Layanan')
                
            else:
                messages.error(request, 'periksa kembali isian data anda!')
            return redirect('acd:suket_izinlab_edit', nim=nim)
        else:
            form = formSuketIzinLab(instance=datasuket)

        context = {
            'title': 'Surat Izin Laboratorium',
            'heading': 'Edit Surat Izin Laboratorium',
            'userfakultas' : userfakultas,
            'photo' : userfakultas.photo,
            'mhs' : mhs,
            'judul' : judul,
            'form': form,
        }
        return render(request, 'fakultas/suket_izinlab_edit.html', context)     


@fakultas_required
@check_userfakultas
def suket_izinlab_del(request, id):      
    data = get_object_or_404(SuketIzinLab, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:suket_izinlab')     




########################## SURAT REKOMENDASI ######################################
@fakultas_required
@check_userfakultas
def suket_rekomendasi(request):      
    userfakultas = request.userfakultas      
    data = SuketRekomendasi.objects.all().order_by('-date_in')

    context = {
        'title': 'Surat Rekomendasi',
        'heading': 'Surat Rekomendasi',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/suket_rekomendasi.html', context)    


@fakultas_required
@check_userfakultas
def suket_rekomendasi_edit(request, nim):      
    userfakultas = request.userfakultas
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketRekomendasi.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketRekomendasi(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Suket Rekomendasi')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    perihal = 'Surat Rekomendasi',
                    tujuan = 'Mahasiswa'  + str(mhs),
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
                suket.no_surat = nosurat 
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Rekomendasi', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Rekomendasi telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_rekomendasi/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_rekomendasi_edit', nim=nim)
    else:
        form = formSuketRekomendasi(instance=datasuket)

    context = {
        'title': 'Surat Rekomendasi',
        'heading': 'Edit Surat Rekomendasi',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'mhs' : mhs,
        'form': form,
    }
    return render(request, 'fakultas/suket_rekomendasi_edit.html', context)     


@fakultas_required
@check_userfakultas
def suket_rekomendasi_del(request, id):      
    data = get_object_or_404(SuketRekomendasi, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:suket_rekomendasi')   




######################### SURAT TUGAS ######################################
@fakultas_required
@check_userfakultas
def surat_tugas(request):      
    userfakultas = request.userfakultas      
    data = SuratTugas.objects.all().order_by('-date_in')

    context = {
        'title': 'Surat Tugas',
        'heading': 'Surat Tugas',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/surat_tugas.html', context)    


@fakultas_required
@check_userfakultas
def surat_tugas_edit(request, id):
    userfakultas = request.userfakultas
    is_new = id == '0'
    surat = None if is_new else get_object_or_404(SuratTugas, id=id)

    if request.method == 'POST':
        if 'dosen_submitted' in request.POST:
            # Proses penyimpanan nama dosen (form tambahan)
            form_nama_dosen = formSuratTugas_NamaDosen(request.POST)
            if form_nama_dosen.is_valid():
                cekUrut = SuratTugas_NamaDosen.objects.filter(surat=surat).order_by('-urut').first()
                if cekUrut:
                    urut_baru = cekUrut.urut + 1
                else:
                    urut_baru = 1
                    
                nama_dosen = form_nama_dosen.save(commit=False)
                nama_dosen.surat = surat
                nama_dosen.urut = urut_baru
                nama_dosen.save()
                messages.success(request, 'Nama Dosen berhasil ditambahkan')
                return redirect('acd:surat_tugas_edit', id=surat.id)
            else:
                messages.error(request, 'Periksa kembali isian nama dosen!')

        if 'mhs_submitted' in request.POST:
            # Proses penyimpanan nama mhs (form tambahan)
            form_nama_mhs = formSuratTugas_NamaMhs(request.POST)
            if form_nama_mhs.is_valid():
                cekUrut = SuratTugas_NamaMhs.objects.filter(surat=surat).order_by('-urut').first()
                if cekUrut:
                    urut_baru = cekUrut.urut + 1
                else:
                    urut_baru = 1
                    
                nama_mhs = form_nama_mhs.save(commit=False)
                nama_mhs.surat = surat
                nama_mhs.urut = urut_baru
                nama_mhs.save()
                messages.success(request, 'Nama mhs berhasil ditambahkan')
                return redirect('acd:surat_tugas_edit', id=surat.id)
            else:
                messages.error(request, 'Periksa kembali isian nama Mahasiswa!')
        else:
            # Proses penyimpanan surat tugas (form utama)
            form = formSuratTugas(request.POST, instance=surat)
            if form.is_valid():
                surat = form.save(commit=False)
                surat.adminp = request.user

                if not surat.no_surat:
                    tahun = datetime.now().year
                    nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                    nosurat_baru = nosurat_cek.nomor + 1 if nosurat_cek else 1
                    kodesurat = KodeSurat.objects.get(jenis='Surat Tugas')
                    NoSuratFakultas.objects.create(
                        adminp=request.user,
                        tahun=tahun,
                        nomor=nosurat_baru,
                        perihal='Surat Tugas',
                        tujuan='Dosen',
                        kode=kodesurat.kode
                    )
                    surat.no_surat = f"{nosurat_baru}{kodesurat.kode}{tahun}"

                surat.save()
                messages.success(request, 'Surat berhasil disimpan')
                return redirect('acd:surat_tugas_edit', id=surat.id)
            else:
                messages.error(request, 'Periksa kembali isian form!')
    else:
        form = formSuratTugas(instance=surat)
        if surat:
            form_nama_dosen = formSuratTugas_NamaDosen()
            nama_dosen = SuratTugas_NamaDosen.objects.filter(surat=surat).order_by('urut')
            form_nama_mhs = formSuratTugas_NamaMhs()
            nama_mhs = SuratTugas_NamaMhs.objects.filter(surat=surat).order_by('urut')

    return render(request, 'fakultas/surat_tugas_edit.html', {
        'title': 'Surat Tugas',
        'heading': 'Edit Surat Tugas',
        'userfakultas': userfakultas,
        'photo': userfakultas.photo,
        'surat': surat,
        'form': form,
        'nama_dosen': nama_dosen if 'nama_dosen' in locals() else None,
        'form_nama_dosen': form_nama_dosen if 'form_nama_dosen' in locals() else None,
        'nama_mhs': nama_mhs if 'nama_mhs' in locals() else None,
        'form_nama_mhs': form_nama_mhs if 'form_nama_mhs' in locals() else None,

    })



@fakultas_required
@check_userfakultas
def surat_tugas_del(request, id):      
    data = get_object_or_404(SuratTugas, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:surat_tugas')  

@fakultas_required
@check_userfakultas
def surat_tugas_delnamadosen(request, id, surat):      
    data = get_object_or_404(SuratTugas_NamaDosen, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Dosen')
    return redirect('acd:surat_tugas_edit', id=surat)     

@fakultas_required
@check_userfakultas
def surat_tugas_delnamamhs(request, id, surat):      
    data = get_object_or_404(SuratTugas_NamaMhs, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Mahasiswa')
    return redirect('acd:surat_tugas_edit', id=surat)     



#################### BEBAS PUSTAKA FAKULTAS ####################
@fakultas_required
@check_userfakultas
def suket_bebaspustaka(request):
    userfakultas = request.userfakultas
    data = SuketBebasPustaka.objects.all().order_by('-date_in')

    context = {
        'title': 'Suket Bebas Pustaka',
        'heading': 'Suket Bebas Pustaka',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/suket_bebaspustaka.html', context)    


@fakultas_required
@check_userfakultas
def suket_bebaspustaka_edit(request, nim):      
    userfakultas = request.userfakultas
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketBebasPustaka.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketBebasPustaka(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Suket Bebas Pustaka')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    tujuan = 'Mahasiswa'  + str(mhs),
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
                suket.no_surat = nosurat 
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Keterangan Bebas Pustaka', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Keterangan Bebas Pustaka telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_bebaspustaka/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_bebaspustaka_edit', nim=nim)
    else:
        form = formSuketBebasPustaka(instance=datasuket)
    layanan = Layanan.objects.filter().order_by('-date_in').first()
    context = {
        'title': 'Surat Bebas Pustaka',
        'heading': 'Edit Surat Bebas Pustaka',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'mhs' : mhs,
        'form': form,
        'layanan': layanan,
        "layanan_isi_parsed": json.loads(layanan.layanan_isi),
    }
    return render(request, 'fakultas/suket_bebaspustaka_edit.html', context)  


@fakultas_required
@check_userfakultas
def suket_bebaspustaka_del(request, id):      
    data = get_object_or_404(SuketBebasPustaka, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat Bebas Pustaka')
    return redirect('acd:suket_bebaspustaka')  

