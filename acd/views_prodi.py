from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import JsonResponse

from aam.context_processors import web_name

from uuid import UUID

from .models import (UserMhs, Layanan,
                     SkripsiJudul, 
                     NoSurat, 
                     Hasil,
                     Ujian,
                     Proposal, 
                     skUjian,
                     skPembimbing, 
                     TTDProdi,
                     NoSuratFakultas,
                     KodeSurat,
                     SuketBebasKuliah,
                     SuketBebasPlagiasi,
                     IzinPenelitian,
                     SuketUsulanUjianSkripsi,
                     SuketBerkelakuanBaik,
                     SuketBebasPustaka,
                     )


from .forms_prodi import (formLayananEdit, 
                          formNosuratAdd, 
                          formTTD,
                          formSkripsiJudulEdit,
                          formProposal,
                          formHasil,
                          formUjian,
                          formSuketBebasKuliah,
                          formSuketBebasPlagiasi,
                          formSuketUsulanUjianSkripsi,
                          )

from .decorators_prodi import admin_prodi_required, check_userprodi

import json

########### NOMOR SURAT #####################################################


@check_userprodi
@admin_prodi_required
def notif_prodi(request):
    userprodi = request.userprodi
    layanan_waiting = Layanan.objects.filter(mhs__prodi=userprodi.prodi, status='Waiting').count() or 0,
    layanan = Layanan.objects.filter(mhs__prodi=userprodi.prodi, status='Waiting').order_by('-date_in')[:3]  # Ambil 10 notifikasi terbaru
    data = [
        {
            'mhs': str(l.mhs),
            'jenis_layanan': l.layanan_jenis.nama_layanan,
            'date_in': l.date_in,
            'avatar': str(l.mhs.photo)
        }
        for l in layanan
    ]
    return JsonResponse({'count': layanan_waiting, 'data': data})


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

    data = NoSurat.objects.filter(jurusan=userprodi.prodi.jurusan).order_by('-nomor')
    context = {
        'title': 'Nomor Surat',
        'heading': 'Nomor Surat',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data' : data,
        'form' : form
    }
    return render(request, 'prodi/nosurat.html', context)

@check_userprodi
@admin_prodi_required
def nosurat_del(request):
    userprodi = request.userprodi
    data = NoSurat.objects.filter(jurusan=userprodi.prodi.jurusan).order_by('-date_in').first()
    data.delete()
    messages.success(request, 'Berhasil Mebatalkan Nomor Surat Terakhir')
    return redirect('acd:nosurat')



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

    if id == '0' :
        data = None
    else :
        data = TTDProdi.objects.get(id=id)
        

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
        'title' : 'TTD Qrcode',
        'heading' : 'Kelolah TTD',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'form': form,
    }
    return render(request, 'prodi/ttd_edit.html', context)

@check_userprodi
@admin_prodi_required
def ttd_del(request, id):
    data = get_object_or_404(TTDProdi, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Data')
    return redirect('acd:ttd')



###################### LAYANAN ########################

@check_userprodi
@admin_prodi_required
def layanan(request, filter):
    userprodi = request.userprodi  
    if filter == 'All':
        layanan_data = Layanan.objects.filter(mhs__prodi=userprodi.prodi).order_by('-date_in')
    elif filter == 'Waiting':
        layanan_data = Layanan.objects.filter(mhs__prodi=userprodi.prodi, status='Waiting').order_by('-date_in')
    elif filter == 'Processing':
        layanan_data = Layanan.objects.filter(mhs__prodi=userprodi.prodi, status='Processing').order_by('-date_in')
    elif filter == 'Completed':
        layanan_data = Layanan.objects.filter(mhs__prodi=userprodi.prodi, status='Completed').order_by('-date_in')
    elif filter == 'Rejected':
        layanan_data = Layanan.objects.filter(mhs__prodi=userprodi.prodi, status='Rejected').order_by('-date_in')
    # data = User.objects.filter(last_name='Mahasiswa').select_related('usermhs').prefetch_related('skripsi_judul')
    context = {
        'title': 'Layanan',
        'heading': 'List Layanan',
        'userprodi' : userprodi,
        'filter' : filter,
        'photo' : userprodi.photo,
        'layanan_data': layanan_data,
    }
    return render(request, 'prodi/layanan.html', context)


@check_userprodi
@admin_prodi_required
def layanan_edit(request, id, filter):
    userprodi = request.userprodi  
    layanan = get_object_or_404(Layanan, id=id)
    if request.method == 'POST':
        form = formLayananEdit(request.POST, request.FILES, instance=layanan)
        if form.is_valid():
            layanan = form.save(commit=False)  
            layanan.adminp = request.user   
            layanan.save()  
            messages.success(request, 'Berhasil')
            return redirect('acd:layanan_edit', id=layanan.id, filter=filter)
        else:
            messages.error(request, 'periksa kembali isian data anda!')
            return redirect('acd:layanan_edit', id=layanan.id, filter=filter)
    else:
        form = formLayananEdit(instance=layanan)

    context = {
        'title' : 'Kelolah Layanan',
        'heading' : 'Kelolah Layanan',
        'userprodi' : userprodi,
        'filter' : filter,
        'photo' : userprodi.photo,
        'form': form,
    }
    return render(request, 'prodi/layanan_edit.html', context)


###################### PENGAJUAN JUDUL ########################

@check_userprodi
@admin_prodi_required
def skripsi_sjudul(request):
    userprodi = request.userprodi  

    if request.method == "POST":
        skripsi_id = request.POST.get("skripsi_id")
        status_ket = request.POST.get("status_ket")
        status = request.POST.get("status")

        skripsi = get_object_or_404(SkripsiJudul, id=skripsi_id)
        skripsi.status = status
        skripsi.status_ket = status_ket
        skripsi.save()       
        messages.success(request, f"Status Skripsi {skripsi_id} = {status}")
    
    data = SkripsiJudul.objects.filter(status__in=['Waiting', 'Revision', 'Approved'], prodi=userprodi.prodi)

    context = {
        'title': 'Seleksi Judul',
        'heading': 'Seleksi Judul',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/skripsi_sjudul.html', context)



@check_userprodi
@admin_prodi_required
def skripsi_djudul(request):
    if request.method == "POST":
        skripsi_id = request.POST.get("skripsi_id")
        skripsi = get_object_or_404(SkripsiJudul, id=skripsi_id)
        
        # Cek apakah pbb1 dan pbb2 kosong
        # if not skripsi.pembimbing1 or not skripsi.pembimbing2 or skripsi.pembimbing2_persetujuan in['Waiting', 'Rejected']:
        if not skripsi.pembimbing1 or not skripsi.pembimbing2 or skripsi.kajur_persetujuan in['Waiting', 'Rejected']:
            messages.error(request, "Pengajuan SK gagal! Pembimbing 1, 2 Belum Diisi / Persetujuan Kaprodi & Kajur belum diberikan")
        else:
            skripsi.status_sk = "Pengajuan"
            skripsi.save()
            #update layanan agar status DIPROSES      
            try:    
                layanan = Layanan.objects.get(
                        layanan_jenis__nama_layanan='Penerbitan SK Pembimbing',
                        status__in=['Waiting', 'Processing'],
                        mhs=skripsi.mhs
                    )
                layanan.status = 'Processing'
                layanan.hasil_test = 'telah diajukan oleh prodi, menunggu bagian fakultas menerbitkan SK'
                layanan.save() 
                messages.success(request, f"Layana Mahasiswa berhasil diperbaharui")
            except Layanan.DoesNotExist:
                # Tidak ada data layanan, program tetap jalan
                messages.info(request, "Tidak ada layanan yang perlu diperbarui")

            messages.success(request, f"Pengajuan SK {skripsi.mhs} berhasil diajukan")
    userprodi = request.userprodi  
    data = SkripsiJudul.objects.filter(prodi=userprodi.prodi).order_by('-date_in')       
    context = {
        'title': 'Daftar Judul',
        'heading': 'Daftar Judul',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/skripsi_djudul.html', context)


@check_userprodi
@admin_prodi_required
def skripsi_ejudul(request, nim):
    userprodi = request.userprodi  
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    judul, create = SkripsiJudul.objects.get_or_create(
        mhs__nim__username=nim,
        defaults={
            'mhs': mhs,
            'prodi': mhs.prodi,
            'status': 'Added',
        }
    )

    if judul.pembimbing2:
        pbb2_lama = judul.pembimbing2.nip.username
    else:
        pbb2_lama = None

    if request.method == 'POST':
        form = formSkripsiJudulEdit(request.POST, instance=judul)
        if form.is_valid():
            judulform = form.save(commit=False)
            pbb2_baru = request.POST.get('pembimbing2')
            
            print(pbb2_baru, pbb2_lama)
            if pbb2_baru != pbb2_lama:
                judulform.pembimbing2_persetujuan = 'Waiting' 
                judulform.kajur_persetujuan = 'Waiting'
                judulform.kaprodi_persetujuan = 'Waiting'
                messages.info(request, 'Menunggu persetujuan dari pembimbing 2, kaprodi dan kajur') 
            judulform.save()  
            messages.success(request, 'Berhasil Mengupdate Judul Skripsi')
            return redirect('acd:skripsi_ejudul', nim=nim)
    else:
        form = formSkripsiJudulEdit(instance=judul)

    context = {
        'title' : 'Edit Judul Skripsi',
        'heading' : 'Edit Judul Skripsi',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'form': form,
        'judul': judul,
    }
    return render(request, 'prodi/skripsi_ejudul.html', context)


###################### PROPOSAL ########################

@check_userprodi
@admin_prodi_required
def proposal(request):
    userprodi = request.userprodi      
    data = Proposal.objects.filter(mhs_judul__prodi=userprodi.prodi, seminar_tgl__isnull=False).order_by('-date_in')

    context = {
        'title': 'Proposal',
        'heading': 'Proposal Penelitian',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/proposal.html', context)

@check_userprodi
@admin_prodi_required
def proposal_del(request, id):
    data = get_object_or_404(Proposal, id=id)
    if data:
        data.no_surat = None
        data.seminar_tgl = None
        data.seminar_jam = None
        data.seminar_tempat = None
        data.penguji1 = None
        data.penguji2 = None
        data.ttd_status = None
        data.ttd = None
        data.save()
        messages.success(request, "Undangan Berhasil Dihapus")
        return redirect('acd:proposal')
    else:
        messages.error(request, "Undangan Tidak Ditemukan")
        return redirect('acd:proposal')



@check_userprodi
@admin_prodi_required
def proposal_edit(request, nim):
    userprodi = request.userprodi  
    judul = get_object_or_404(SkripsiJudul, mhs__nim__username = nim)
    proposal, create = Proposal.objects.get_or_create(
        mhs_judul__mhs__nim__username=nim,
        defaults={
            'mhs_judul': judul,
            'pembimbing1': judul.pembimbing1,
            'pembimbing2': judul.pembimbing2,
            'adminp': userprodi,
        }
    )

    if request.method == 'POST':
        form = formProposal(request.POST, instance=proposal)
        if form.is_valid():
            tosave = form.save(commit=False)
            tosave.adminp = userprodi
            tosave.mhs_judul = judul
            tosave.pembimbing1 = judul.pembimbing1
            tosave.pembimbing2 = judul.pembimbing2
            if tosave.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Undangan Seminar Proposal')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    perihal = 'Undangan Seminar Proposal ' + str(judul.mhs),
                    tujuan = 'Dosen Pembimbing dan Penguji',
                    kode = kodesurat.kode
                )
                tosave.no_surat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun)               
            tosave.save()

            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=judul.mhs, layanan_jenis__nama_layanan='Undangan Seminar Proposal', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Undangan Telah Diterbitkan, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_undangan/Proposal/" + str(tosave.id)
                layanan.save()

            messages.success(request, "Undangan Berhasil Diproses")
            return redirect('acd:proposal_edit', nim=nim)
    else:
        form = formProposal(instance=proposal)  
    
    skpbb = skPembimbing.objects.filter(mhs=judul.mhs).order_by('-date_in')
    context = {
        'title': 'Proposal',
        'heading': 'Set Undangan Proposal',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'judul': judul,
        'proposal': proposal,
        'form': form,
        'skpbb': skpbb,
    }
    return render(request, 'prodi/proposal_edit.html', context)


@check_userprodi
@admin_prodi_required
def proposal_nilai(request, id):
    userprodi = request.userprodi  
    data = get_object_or_404(Proposal, id=id)
    context = {
        'title': 'Proposal',
        'heading': 'Nilai Proposal',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/proposal_nilai.html', context)





######################### HASIL ########################
@check_userprodi
@admin_prodi_required
def hasil(request):
    userprodi = request.userprodi      
    data = Hasil.objects.filter(mhs_judul__prodi=userprodi.prodi, seminar_tgl__isnull=False).order_by('-date_in')

    context = {
        'title': 'Hasil',
        'heading': 'Hasil Penelitian',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/hasil.html', context)


@check_userprodi
@admin_prodi_required
def hasil_edit(request, nim):
    userprodi = request.userprodi  
    judul = get_object_or_404(SkripsiJudul, mhs__nim__username = nim)
    hasil, create = Hasil.objects.get_or_create(
        mhs_judul__mhs__nim__username=nim,
        defaults={
            'mhs_judul': judul,
            'pembimbing1': judul.pembimbing1,
            'pembimbing2': judul.pembimbing2,
            'adminp': userprodi,
        }
    )

    if request.method == 'POST':
        form = formHasil(request.POST, instance=hasil)
        if form.is_valid():
            tosave = form.save(commit=False)
            tosave.adminp = userprodi
            tosave.mhs_judul = judul
            tosave.prodi = judul.prodi
            tosave.pembimbing1 = judul.pembimbing1
            tosave.pembimbing2 = judul.pembimbing2
            if tosave.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Undangan Seminar Hasil')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    perihal = 'Undangan Seminar Hasil ' + str(judul.mhs),
                    tujuan = 'Dosen Pembimbing dan Penguji',
                    kode = kodesurat.kode
                )
                tosave.no_surat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun)               
            tosave.save()

            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=judul.mhs, layanan_jenis__nama_layanan='Undangan Seminar Hasil', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Undangan Telah Diterbitkan, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_undangan/Hasil/" + str(tosave.id)
                layanan.save()

            messages.success(request, "Undangan Berhasil Diproses")
            return redirect('acd:hasil_edit', nim=nim)
    else:
        form = formHasil(instance=hasil)  
    skpbb = skPembimbing.objects.filter(mhs=judul.mhs).order_by('-date_in')
    izinpenelitian = IzinPenelitian.objects.filter(mhs_judul=judul).order_by('-date_in')

    context = {
        'title': 'Hasil',
        'heading': 'Set Undangan Hasil',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'judul': judul,
        'proposal': Proposal.objects.get(mhs_judul__mhs=judul.mhs),
        'hasil': hasil,
        'form': form,
        'skpbb': skpbb,
        'izinpenelitian': izinpenelitian,
    }
    return render(request, 'prodi/hasil_edit.html', context)


@check_userprodi
@admin_prodi_required
def hasil_nilai(request, id):
    userprodi = request.userprodi  
    data = get_object_or_404(Hasil, id=id)
    context = {
        'title': 'Hasil',
        'heading': 'Nilai Hasil',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/hasil_nilai.html', context)



######################### USULAN UJIAN ########################
@check_userprodi
@admin_prodi_required
def usulan_ujian_edit(request, nim):
    userprodi = request.userprodi  
    judul = get_object_or_404(SkripsiJudul, mhs__nim__username = nim)
    ujian, create = Ujian.objects.get_or_create(
        mhs_judul__mhs__nim__username=nim,
        defaults={
            'mhs_judul': judul,
            'pembimbing1': judul.pembimbing1,
            'pembimbing2': judul.pembimbing2,
        }
    )

    if request.method == 'POST':
        form = formUjian(request.POST, instance=ujian)
        if form.is_valid():
            tosave = form.save(commit=False)
            tosave.mhs_judul = judul
            tosave.pembimbing1 = judul.pembimbing1
            tosave.pembimbing2 = judul.pembimbing2    
            tosave.status_ujian = "Usulan"
            tosave.save()

            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=judul.mhs, layanan_jenis__nama_layanan='Usulan Ujian Tutup', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Processing'
                layanan.hasil_test = 'Usulan Ujian Telah Disetujui Prodi, menunggu bagian fakultas menerbitkan Ketua, Wakil Ketua'
                layanan.save()

            messages.success(request, "Usulan Berhasil Diproses")
    else:
        form = formUjian(instance=ujian)  

    context = {
        'title': 'Ujian',
        'heading': 'Set Lembar Persetujuan Waktu',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'judul': judul,
        'ujian': ujian,
        'bebaskuliah': SuketBebasKuliah.objects.filter(mhs=judul.mhs).first(),
        'bebasplagiasi': SuketBebasPlagiasi.objects.filter(mhs=judul.mhs).first(),
        'skpbb': skPembimbing.objects.filter(mhs=judul.mhs).order_by('-date_in').first(),
        'berkelakuanbaik': SuketBerkelakuanBaik.objects.filter(mhs=judul.mhs).first(),
        'bebaspustaka': SuketBebasPustaka.objects.filter(mhs=judul.mhs).first(),
        'proposal': Proposal.objects.get(mhs_judul__mhs=judul.mhs),
        'hasil': Hasil.objects.get(mhs_judul__mhs=judul.mhs),
        'form': form,
    }
    return render(request, 'prodi/usulan_ujian_edit.html', context)

######################### UJIAN ########################
@check_userprodi
@admin_prodi_required
def ujian(request, filter):           
    userprodi = request.userprodi    
    if filter == 'usulan':
        title = 'Ujian Tutup - Usulan'
        data = Ujian.objects.filter(mhs_judul__prodi=userprodi.prodi, status_ujian='-', no_surat__isnull=True, ujian_tgl__isnull=False).order_by('-date_in')
    elif filter == 'pengajuan':
        title = 'Ujian Tutup - Pengajuan'
        data = Ujian.objects.filter(mhs_judul__prodi=userprodi.prodi, ujian_tgl__isnull=False, no_surat__isnull=True, status_ujian='Pengajuan').order_by('-date_in')
    elif filter == 'terbit':
        title = 'Ujian Tutup - Terbit'
        data = Ujian.objects.filter(mhs_judul__prodi=userprodi.prodi, ujian_tgl__isnull=False, no_surat__isnull=False).order_by('-date_in')
    else:
        title = 'Ujian Tutup'
        data = Ujian.objects.all().order_by('-date_in')

    
    context = {
        'title': title,
        'heading': title,
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data' : data,
    }
    return render(request, 'prodi/ujian.html', context)

@check_userprodi
@admin_prodi_required
def ujian_edit(request, nim):
    userprodi = request.userprodi  
    judul = get_object_or_404(SkripsiJudul, mhs__nim__username = nim)
    ujian, create = Ujian.objects.get_or_create(
        mhs_judul__mhs__nim__username=nim,
        defaults={
            'mhs_judul': judul,
            'pembimbing1': judul.pembimbing1,
            'pembimbing2': judul.pembimbing2,
        }
    )

    if request.method == 'POST':
        form = formUjian(request.POST, instance=ujian)
        if form.is_valid():
            tosave = form.save(commit=False)
            tosave.mhs_judul = judul
            tosave.pembimbing1 = judul.pembimbing1
            tosave.pembimbing2 = judul.pembimbing2   
            tosave.status_ujian = "Pengajuan"          
            tosave.save()

            #update layanan agar status DIPROSES    
                    
            skujian, created = skUjian.objects.get_or_create(
                ujian=ujian,
                defaults={
                    'ujian': ujian
                }
            )

            layanan = Layanan.objects.filter(mhs=judul.mhs, layanan_jenis__nama_layanan='Undangan Ujian Tutup', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Processing'
                layanan.hasil_test = 'Berkas Telah Disetujui Prodi, menunggu bagian fakultas menerbitkan undangan dan SK Ujian'
                layanan.save()

            messages.success(request, "Undangan dan SK Ujian Segera Diproses")
    else:
        form = formUjian(instance=ujian)  

    context = {
        'title': 'Ujian',
        'heading': 'Set Undangan Ujian',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'judul': judul,
        'ujian': ujian,
        'bebaskuliah': SuketBebasKuliah.objects.filter(mhs=judul.mhs).first(),
        'bebasplagiasi': SuketBebasPlagiasi.objects.filter(mhs=judul.mhs).first(),
        'usulanujian': SuketUsulanUjianSkripsi.objects.filter(mhs_judul__mhs=judul.mhs).first(),
        'skpbb': skPembimbing.objects.filter(mhs=judul.mhs).order_by('-date_in').first(),
        'berkelakuanbaik': SuketBerkelakuanBaik.objects.filter(mhs=judul.mhs).first(),
        'bebaspustaka': SuketBebasPustaka.objects.filter(mhs=judul.mhs).first(),
        'proposal': Proposal.objects.get(mhs_judul__mhs=judul.mhs),
        'hasil': Hasil.objects.get(mhs_judul__mhs=judul.mhs),
        'form': form,
    }
    return render(request, 'prodi/ujian_edit.html', context)


@check_userprodi
@admin_prodi_required
def ujian_nilai(request, id):
    userprodi = request.userprodi  
    data = get_object_or_404(Ujian, id=id)
    context = {
        'title': 'Ujian',
        'heading': 'Nilai Ujian',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/ujian_nilai.html', context)



######################### BEBAS BEBAN KULIAH ########################
@check_userprodi
@admin_prodi_required
def suket_bebaskuliah(request):
    userprodi = request.userprodi      
    data = SuketBebasKuliah.objects.filter(mhs__prodi=userprodi.prodi).order_by('-date_in')

    context = {
        'title': 'Suket Bebas Kuliah',
        'heading': 'Suket Bebas Beban Kuliah',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/suket_bebaskuliah.html', context)


@check_userprodi
@admin_prodi_required
def suket_bebaskuliah_edit(request, nim):
    userprodi = request.userprodi
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketBebasKuliah.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketBebasKuliah(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.jurusan = userprodi.prodi.jurusan   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSurat.objects.filter(jurusan=userprodi.prodi.jurusan,tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                addnosurat = NoSurat.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru,
                    jurusan  = userprodi.prodi.jurusan,
                    perihal = 'Suket Bebas Beban Kuliah',
                    tujuan = str(mhs),
                )
                suket.no_surat =  str(nosurat_baru) + str(userprodi.prodi.jurusan.kode_surat) + str(tahun)
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Suket Bebas Beban Kuliah', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Keterangan Bebas Beban Kuliah, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_bebaskuliah/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_bebaskuliah_edit', nim=nim)
    else:
        form = formSuketBebasKuliah(instance=datasuket)

    context = {
        'title': 'Suket Bebas Kuliah',
        'heading': 'Edit Suket Bebas Kuliah',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'mhs' : mhs,
        'form': form,
    }
    return render(request, 'prodi/suket_bebaskuliah_edit.html', context)


@check_userprodi
@admin_prodi_required
def suket_bebaskuliah_del(request, id):
    data = get_object_or_404(SuketBebasKuliah, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:suket_bebaskuliah')



######################### BEBAS PALGIASI ########################
@check_userprodi
@admin_prodi_required
def suket_bebasplagiasi(request):
    userprodi = request.userprodi      
    data = SuketBebasPlagiasi.objects.filter(mhs__prodi=userprodi.prodi).order_by('-date_in')

    context = {
        'title': 'Suket Bebas Plagiasi',
        'heading': 'Surat Keterangan Bebas Plagiasi',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/suket_bebasplagiasi.html', context)


@check_userprodi
@admin_prodi_required
def suket_bebasplagiasi_edit(request, nim):
    userprodi = request.userprodi
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketBebasPlagiasi.objects.filter(mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketBebasPlagiasi(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.jurusan = userprodi.prodi.jurusan   
            suket.mhs = mhs
            if suket.no_surat is None:
                tahun = datetime.now().year
                nosurat_cek = NoSurat.objects.filter(jurusan=userprodi.prodi.jurusan,tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  

                addnosurat = NoSurat.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru,
                    jurusan  = userprodi.prodi.jurusan,
                    perihal = 'Suket Bebas Plagiasi',
                    tujuan = str(mhs),
                )
                suket.no_surat =  str(nosurat_baru) + str(userprodi.prodi.jurusan.kode_surat) + str(tahun)
            suket.save()
            messages.success(request, 'Berhasil Menerbitkan Surat')
            #update layanan agar status DIPROSES            
            layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Keterangan Bebas Plagiasi', status__in=['Processing', 'Waiting']).first()
            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Keterangan Plagiasi telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_bebasplagiasi/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:suket_bebasplagiasi_edit', nim=nim)
    else:
        form = formSuketBebasPlagiasi(instance=datasuket)
    
    layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Surat Keterangan Bebas Plagiasi') .order_by('-date_in').first()
    context = {
        'title': 'Suket Bebas Plagiasi',
        'heading': 'Edit Surat Keterangan Bebas Plagiasi',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'mhs' : mhs,
        'form': form,
        "layanan_isi_parsed": json.loads(layanan.layanan_isi) if layanan else {},
    }
    return render(request, 'prodi/suket_bebasplagiasi_edit.html', context)


@check_userprodi
@admin_prodi_required
def suket_bebasplagiasi_del(request, id):
    data = get_object_or_404(SuketBebasPlagiasi, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:suket_bebasplagiasi')


################ USULAN UJIAN SKRIPSI ########################
@check_userprodi
@admin_prodi_required
def usulanujianskripsi(request):
    userprodi = request.userprodi      
    data = SuketUsulanUjianSkripsi.objects.filter(mhs_judul__prodi=userprodi.prodi).order_by('-date_in')
    context = {
        'title': 'Suket Usulan Ujian Skripsi',
        'heading': 'Surat Usulan Ujian Skripsi',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'data': data,
    }
    return render(request, 'prodi/suket_usulanujianskripsi.html', context)



@check_userprodi
@admin_prodi_required
def usulanujianskripsi_edit(request, nim):
    userprodi = request.userprodi
    mhs = get_object_or_404(UserMhs, nim__username = nim)
    datasuket = SuketUsulanUjianSkripsi.objects.filter(mhs_judul__mhs=mhs).first()

    if request.method == 'POST':
        form = formSuketUsulanUjianSkripsi(request.POST, instance=datasuket)
        if form.is_valid():
            suket = form.save(commit=False)  
            suket.adminp = request.user   
            suket.jurusan = userprodi.prodi.jurusan   
            skripsi_judul = SkripsiJudul.objects.filter(mhs=mhs).first()
            if skripsi_judul:
                suket.mhs_judul = skripsi_judul
                tahun = datetime.now().year
                nosurat_baru = None  
                if suket.no_surat is None:
                    nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                    if nosurat_cek:
                        nosurat_baru = nosurat_cek.nomor + 1
                    else:
                        nosurat_baru = 1  
                
                kodesurat = KodeSurat.objects.get(jenis='Suket Usulan Ujian Skripsi')
                if suket.no_surat is None:
                    addnosurat = NoSuratFakultas.objects.create(
                        adminp = request.user,
                        tahun = tahun,
                        nomor = nosurat_baru, 
                        perihal = 'Suket Usulan Ujian Skripsi',
                        tujuan = str(skripsi_judul.mhs.nim.username) + ' - ' + str(skripsi_judul.mhs.nim.first_name) + ' - Program Studi ' + str(skripsi_judul.prodi.nama_prodi),
                        kode = kodesurat.kode
                    )
                    suket.no_surat = str(nosurat_baru) + str(kodesurat.kode) + str(tahun)
                    
            suket.save()

            messages.success(request, 'Berhasil Menerbitkan Surat')

            layanan = Layanan.objects.filter(
                mhs=mhs,
                layanan_jenis__nama_layanan='Suket Usulan Ujian Skripsi',
                status__in=['Processing', 'Waiting']
            ).first()

            if layanan:
                context_pro = web_name(request)
                layanan.status = 'Completed'
                layanan.hasil_test = 'Surat Usulan Ujian Skripsi telah terbit, download di tautan berikut:'
                layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_suket_usulanujianskripsi/" + str(suket.id)
                layanan.save()                  
                messages.success(request, 'Berhasil Mengupdate Layanan')
            
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:usulanujianskripsi_edit', nim=nim)

    else:
        # GET request, tidak ada suket
        form = formSuketUsulanUjianSkripsi(instance=datasuket)
    
    layanan = Layanan.objects.filter(mhs=mhs, layanan_jenis__nama_layanan='Suket Usulan Ujian Skripsi') .order_by('-date_in').first()
    ujian = Ujian.objects.filter(mhs_judul__mhs=mhs).order_by('-date_in').first()

    context = {
        'title': 'Suket Usulan Ujian Skripsi',
        'heading': 'Edit Surat Usulan Ujian Skripsi',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'mhs' : mhs,
        'form': form,
        'layanan': layanan,
        'ujian': ujian,
        'skpbb': skPembimbing.objects.filter(mhs=mhs).order_by('-date_in'),
        'bebasplagiasi': SuketBebasPlagiasi.objects.filter(mhs=mhs).first(),
        'bebaspustaka': SuketBebasPustaka.objects.filter(mhs=mhs).first(),
        'berkelakuanbaik': SuketBerkelakuanBaik.objects.filter(mhs=mhs).order_by('-date_in').first(),
        "layanan_isi_parsed": json.loads(layanan.layanan_isi) if layanan else {},
        'proposal': Proposal.objects.get(mhs_judul__mhs=mhs),
        'hasil': Hasil.objects.get(mhs_judul__mhs=mhs),
    }
    return render(request, 'prodi/suket_usulanujianskripsi_edit.html', context)


@check_userprodi
@admin_prodi_required
def usulanujianskripsi_del(request, id):
    data = get_object_or_404(SuketUsulanUjianSkripsi, id=id)
    data.delete()
    messages.info(request, 'Berhasil Menghapus Surat')
    return redirect('acd:usulanujianskripsi')