from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
import uuid
from uuid import UUID

from .utils import cek_kemiripan_judul  

from .models import UserMhs, SkripsiJudul, chatPA, Proposal, ProposalNilai,  Hasil, HasilNilai,  Ujian, UjianNilai, UserDosen

from .forms_dosen import formProfile, formChatPA, formProposalNilai, formHasilNilai, formUjianNilai

from .decorators_dosen import check_userdosen
from .decorators_dosen import dosen_required



@dosen_required
def profile_dosen(request):
    userdosen = UserDosen.objects.get(nip=request.user)     
    if request.method == 'POST':
        form = formProfile(request.POST, request.FILES, instance=userdosen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_dosen')
    else:
        form = formProfile(instance=userdosen)

    context = {
        'title' : 'Profile',
        'heading' : 'Edit Profile',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'form': form,
    }
    return render(request, 'dosen/set/profile.html', context)

################################### SELEKSI JUDUL ##################################################

@dosen_required
@check_userdosen
def judul_seleksi(request):      
    userdosen = request.userdosen  
    data_mhs = UserMhs.objects.filter(penasehat_akademik=userdosen)

    # Ambil daftar NIM mahasiswa bimbingan
    nim_list = data_mhs.values_list('nim', flat=True)
    # Ambil judul skripsi berdasarkan NIM
    data = SkripsiJudul.objects.filter(mhs__in=nim_list, status__in=['ACC Judul 1', 'ACC Judul 2', 'ACC Judul 3', 'Waiting']).order_by('-date_in')

    context = {
        'title': 'Seleksi Judul',
        'heading': 'Seleksi Judul',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'data_mhs': data_mhs,
        'data': data,
    }
    return render(request, 'dosen/judul_seleksi.html', context)


@dosen_required
@check_userdosen
def judul_seleksi_detail(request, id):
    userdosen = request.userdosen  
    try:
        # Pastikan id adalah UUID yang valid
        uuid_obj = UUID(str(id), version=4)
    except ValueError:
        return render(request, "404.html")  
         
    data = get_object_or_404(SkripsiJudul, id=uuid_obj)

    # Cek kemiripan judul 1, 2, dan 3
    kemiripan_judul1 = cek_kemiripan_judul(data.id, data.judul1) if data.judul1 else []
    kemiripan_judul2 = cek_kemiripan_judul(data.id, data.judul2) if data.judul2 else []
    kemiripan_judul3 = cek_kemiripan_judul(data.id, data.judul3) if data.judul3 else []

    # CHAT MAHASISWA DAN DOSEN

    chatpa_list = chatPA.objects.filter(dsn=userdosen, mhs=data.mhs).order_by('date_in')
    form_chatpa = formChatPA()

    if request.method == 'POST':
        if 'submit_chatpa' in request.POST: 
            form_chatpa = formChatPA(request.POST)
            if form_chatpa.is_valid():
                chatpa = form_chatpa.save(commit=False)
                chatpa.dsn = userdosen
                chatpa.mhs = data.mhs
                chatpa.prodi = data.mhs.prodi
                chatpa.sender = 'Dosen'
                chatpa.save()
                messages.success(request, 'Pesan ke mahasiswa berhasil dikirim.', extra_tags='chatpa')
            else:
                messages.error(request, 'Periksa kembali isi pesan.', extra_tags='chatpa')       
        elif 'judul1_acc' in request.POST:
            data.status = "ACC Judul 1"
            data.judul = data.judul1
            data.pembimbing1= userdosen
            data.save()
            messages.success(request, 'Judul 1 di ACC', extra_tags='acc_judul')
        elif 'judul2_acc' in request.POST:
            data.status = "ACC Judul 2"
            data.judul = data.judul2
            data.pembimbing1= userdosen
            data.save()
            messages.success(request, 'Judul 2 di ACC', extra_tags='acc_judul')
        elif 'judul3_acc' in request.POST:
            data.status = "ACC Judul 3"
            data.judul = data.judul3
            data.pembimbing1= userdosen
            data.save()
            messages.success(request, 'Judul 3 di ACC', extra_tags='acc_judul')



    context = {
        'title': 'Seleksi Judul',
        'heading': 'Seleksi Judul Detail',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'data': data,
        'form_chatpa': form_chatpa,
        'chatpa': chatpa_list,  # Kirim semua chat ke template
        'kemiripan_judul1': kemiripan_judul1,
        'kemiripan_judul2': kemiripan_judul2,
        'kemiripan_judul3': kemiripan_judul3,
    }
    return render(request, 'dosen/judul_seleksi_detail.html', context)



################################### PERSETUJUAN MENJADI PEMBIMBIN 2 ##################################################

@dosen_required
@check_userdosen
def pbb2_persetujuan(request):      
    userdosen = request.userdosen  
    data = SkripsiJudul.objects.filter(pembimbing2=userdosen, pembimbing2_persetujuan='Waiting').order_by('-date_in')

    if request.method == 'POST':
        skripsi_id = request.POST.get('skripsi_id')
        judul = SkripsiJudul.objects.get(id=skripsi_id)
        judul.pembimbing2_persetujuan = request.POST.get('status')
        judul.pembimbing2_komentar = request.POST.get('status_ket')
        judul.save()
        messages.success(request, 'Persetujuan Pembimbing 2 berhasil disimpan!')

    context = {
        'title': 'Persetujuan Pembimbing 2',
        'heading': 'Persetujuan Pembimbing 2',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'data': data,
    }
    return render(request, 'dosen/pbb2_persetujuan.html', context)


################################ PORPOSAL ####################################

@dosen_required
@check_userdosen
def proposal_dsn(request, filter):      
    userdosen = request.userdosen 
    if filter == 'Pembimbing1' : 
        data = Proposal.objects.filter(pembimbing1 = userdosen)
    elif filter == 'Pembimbing2' : 
        data = Proposal.objects.filter(pembimbing2 = userdosen)
    elif filter == 'Penguji1' : 
        data = Proposal.objects.filter(penguji1 = userdosen)
    elif filter == 'Penguji2' : 
        data = Proposal.objects.filter(penguji2 = userdosen)
    else : 
        data = Proposal.objects.filter(
            Q(pembimbing1=userdosen) |
            Q(pembimbing2=userdosen) |
            Q(penguji1=userdosen) |
            Q(penguji2=userdosen)
        )

    context = {
        'title': 'Proposal Mahasiswa',
        'heading': 'Proposal Mahasiswa',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'data': data,
        'filter': filter,
    }
    return render(request, 'dosen/proposal_dsn.html', context)


@dosen_required
@check_userdosen
def proposal_dsn_nilai(request, id):      
    userdosen = request.userdosen 
    data = Proposal.objects.get(id=id)

    nilai = None
    create = False

    # Cek dan buat ProposalNilai jika belum ada
    if data.pembimbing1.nip == userdosen.nip:
        if data.nilai1 is None:
            nilai = ProposalNilai.objects.create()
            data.nilai1 = nilai
            data.save()
        else:
            nilai = data.nilai1
    elif data.pembimbing2.nip == userdosen.nip:
        if data.nilai2 is None:
            nilai = ProposalNilai.objects.create()
            data.nilai2 = nilai
            data.save()
        else:
            nilai = data.nilai2
    elif data.penguji1.nip == userdosen.nip:
        if data.nilai3 is None:
            nilai = ProposalNilai.objects.create()
            data.nilai3 = nilai
            data.save()
        else:
            nilai = data.nilai3
    elif data.penguji2.nip == userdosen.nip:
        if data.nilai4 is None:
            nilai = ProposalNilai.objects.create()
            data.nilai4 = nilai
            data.save()
        else:
            nilai = data.nilai4
    else:
        messages.error(request, 'Anda tidak memiliki akses untuk menilai proposal ini.')
        return redirect('/acd/proposal_dsn/Semua') 

    # Form processing
    if request.method == 'POST':
        form = formProposalNilai(request.POST, instance=nilai)
        if form.is_valid():
            tosave = form.save(commit=False)
            # Hitung rata-rata dari nilai yang tidak kosong
            nilai_list = tosave.aspek1 + tosave.aspek2 + tosave.aspek3 + tosave.aspek4 + tosave.aspek5 + tosave.aspek6
            mean = nilai_list/6
            if mean >= 85 :
                nilaiHuruf = 'A'  
            elif mean >= 80 :
                nilaiHuruf = 'A-'  
            elif mean >= 75 :
                nilaiHuruf = 'B+'  
            elif mean >= 70 :
                nilaiHuruf = 'B'  
            elif mean >= 65 :
                nilaiHuruf = 'B-'  
            elif mean >= 50 :
                nilaiHuruf = 'C'  
            elif mean >= 40 :
                nilaiHuruf = 'D'  
            else :
                nilaiHuruf = 'E' 

            tosave.nilai_angka = mean
            tosave.nilai_huruf = nilaiHuruf
            tosave.save()
            messages.success(request, 'Nilai berhasil disimpan!')
    else:
        form = formProposalNilai(instance=nilai)

     


    context = {
        'title': 'Proposal Mahasiswa',
        'heading': 'Proposal Nilai',
        'userdosen': userdosen,
        'photo': userdosen.photo,
        'data': data,
        'form': form,
        'nilai': nilai,
    }
    return render(request, 'dosen/proposal_dsn_nilai.html', context)





################################ HASIL ####################################

@dosen_required
@check_userdosen
def hasil_dsn(request, filter):    
    userdosen = request.userdosen 
    if filter == 'Pembimbing1' : 
        data = Hasil.objects.filter(pembimbing1 = userdosen)
    elif filter == 'Pembimbing2' : 
        data = Hasil.objects.filter(pembimbing2 = userdosen)
    elif filter == 'Penguji1' : 
        data = Hasil.objects.filter(penguji1 = userdosen)
    elif filter == 'Penguji2' : 
        data = Hasil.objects.filter(penguji2 = userdosen)
    else : 
        data = Hasil.objects.filter(
            Q(pembimbing1=userdosen) |
            Q(pembimbing2=userdosen) |
            Q(penguji1=userdosen) |
            Q(penguji2=userdosen)
        )

    context = {
        'title': 'Hasil Mahasiswa',
        'heading': 'Hasil Mahasiswa',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'data': data,
        'filter': filter,
    }
    return render(request, 'dosen/hasil_dsn.html', context)


@dosen_required
@check_userdosen
def hasil_dsn_nilai(request, id):      
    userdosen = request.userdosen 
    data = Hasil.objects.get(id=id)

    nilai = None
    create = False

    if data.pembimbing1.nip == userdosen.nip:
        if data.nilai1 is None:
            nilai = HasilNilai.objects.create()
            data.nilai1 = nilai
            data.save()
        else:
            nilai = data.nilai1
    elif data.pembimbing2.nip == userdosen.nip:
        if data.nilai2 is None:
            nilai = HasilNilai.objects.create()
            data.nilai2 = nilai
            data.save()
        else:
            nilai = data.nilai2
    elif data.penguji1.nip == userdosen.nip:
        if data.nilai3 is None:
            nilai = HasilNilai.objects.create()
            data.nilai3 = nilai
            data.save()
        else:
            nilai = data.nilai3
    elif data.penguji2.nip == userdosen.nip:
        if data.nilai4 is None:
            nilai = HasilNilai.objects.create()
            data.nilai4 = nilai
            data.save()
        else:
            nilai = data.nilai4
    else:
        messages.error(request, 'Anda tidak memiliki akses untuk menilai hasil ini.')
        return redirect('/acd/hasil_dsn/Semua') 

    # Form processing
    if request.method == 'POST':
        form = formHasilNilai(request.POST, instance=nilai)
        if form.is_valid():
            tosave = form.save(commit=False)
            # Hitung rata-rata dari nilai yang tidak kosong
            nilai_list = tosave.aspek1 + tosave.aspek2 + tosave.aspek3 + tosave.aspek4 + tosave.aspek5 + tosave.aspek6
            mean = nilai_list/6
            if mean >= 85 :
                nilaiHuruf = 'A'  
            elif mean >= 80 :
                nilaiHuruf = 'A-'  
            elif mean >= 75 :
                nilaiHuruf = 'B+'  
            elif mean >= 70 :
                nilaiHuruf = 'B'  
            elif mean >= 65 :
                nilaiHuruf = 'B-'  
            elif mean >= 50 :
                nilaiHuruf = 'C'  
            elif mean >= 40 :
                nilaiHuruf = 'D'  
            else :
                nilaiHuruf = 'E' 

            tosave.nilai_angka = mean
            tosave.nilai_huruf = nilaiHuruf
            tosave.save()
            messages.success(request, 'Nilai berhasil disimpan!')
    else:
        form = formHasilNilai(instance=nilai)

     


    context = {
        'title': 'Hasil Mahasiswa',
        'heading': 'Hasil Nilai',
        'userdosen': userdosen,
        'photo': userdosen.photo,
        'data': data,
        'form': form,
        'nilai': nilai,
    }
    return render(request, 'dosen/proposal_dsn_nilai.html', context)




################################ UJIAN ####################################

@dosen_required
@check_userdosen
def ujian_dsn(request, filter):    
    userdosen = request.userdosen 
    if filter == 'Pembimbing1' : 
        data = Ujian.objects.filter(pembimbing1 = userdosen)
    elif filter == 'Pembimbing2' : 
        data = Ujian.objects.filter(pembimbing2 = userdosen)
    elif filter == 'Penguji1' : 
        data = Ujian.objects.filter(penguji1 = userdosen)
    elif filter == 'Penguji2' : 
        data = Ujian.objects.filter(penguji2 = userdosen)
    elif filter == 'PimpinanSidang' : 
        data = Ujian.objects.filter(wd__pejabat = userdosen)
    elif filter == 'SekretarisSidang' : 
        data = Ujian.objects.filter(kaprodi__pejabat = userdosen)
    else : 
        data = Ujian.objects.filter(
            Q(pembimbing1=userdosen) |
            Q(pembimbing2=userdosen) |
            Q(penguji1=userdosen) |
            Q(penguji2=userdosen)
        )

    context = {
        'title': 'Ujian Mahasiswa',
        'heading': 'Ujian Mahasiswa',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'data': data,
        'filter': filter,
    }
    return render(request, 'dosen/ujian_dsn.html', context)


@dosen_required
@check_userdosen
def ujian_dsn_nilai(request, id):      
    userdosen = request.userdosen 
    data = Ujian.objects.get(id=id)

    nilai = None
    create = False

    if data.pembimbing1.nip == userdosen.nip:
        if data.nilai1 is None:
            nilai = UjianNilai.objects.create()
            data.nilai1 = nilai     
        else:
            nilai = data.nilai1
        if data.pembimbing1 == data.wd.pejabat :
                data.nilai5 = nilai
        if data.pembimbing1 == data.kaprodi.pejabat :
                data.nilai6 = nilai
        data.save()
    elif data.pembimbing2.nip == userdosen.nip:
        if data.nilai2 is None:
            nilai = UjianNilai.objects.create()
            data.nilai2 = nilai
        else:
            nilai = data.nilai2        
        if data.pembimbing2 == data.wd.pejabat :
            data.nilai5 = nilai
        if data.pembimbing2 == data.kaprodi.pejabat :
            data.nilai6 = nilai
        data.save()
    elif data.penguji1.nip == userdosen.nip:
        if data.nilai3 is None:
            nilai = UjianNilai.objects.create()
            data.nilai3 = nilai     
        else:
            nilai = data.nilai3
        if data.penguji1 == data.wd.pejabat :
                data.nilai5 = nilai
        if data.penguji1 == data.kaprodi.pejabat :
                data.nilai6 = nilai
        data.save()
    elif data.penguji2.nip == userdosen.nip:
        if data.nilai4 is None:
            nilai = UjianNilai.objects.create()
            data.nilai4 = nilai
        else:
            nilai = data.nilai4        
        if data.penguji2 == data.wd.pejabat :
            data.nilai5 = nilai
        if data.penguji2 == data.kaprodi.pejabat :
            data.nilai6 = nilai
        data.save()
    elif data.wd.pejabat == userdosen:
        if data.nilai5 is None:
            nilai = UjianNilai.objects.create()
            data.nilai5 = nilai
        else:
            nilai = data.nilai5
        data.save()
    elif data.kaprodi.pejabat == userdosen:
        if data.nilai6 is None:
            nilai = UjianNilai.objects.create()
            data.nilai6 = nilai            
        else:
            nilai = data.nilai6
        data.save()
    else:
        messages.error(request, 'Anda tidak memiliki akses untuk menilai ujian skripsi ini.')
        return redirect('/acd/ujian_dsn/Semua') 

    # Form processing
    if request.method == 'POST':
        form = formUjianNilai(request.POST, instance=nilai)
        if form.is_valid():
            tosave = form.save(commit=False)
            # Hitung rata-rata dari nilai yang tidak kosong
            nilai_list = tosave.aspek1 + tosave.aspek2 + tosave.aspek3 + tosave.aspek4 + tosave.aspek5 + tosave.aspek6
            mean = nilai_list/6
            if mean >= 85 :
                nilaiHuruf = 'A'  
            elif mean >= 80 :
                nilaiHuruf = 'A-'  
            elif mean >= 75 :
                nilaiHuruf = 'B+'  
            elif mean >= 70 :
                nilaiHuruf = 'B'  
            elif mean >= 65 :
                nilaiHuruf = 'B-'  
            elif mean >= 50 :
                nilaiHuruf = 'C'  
            elif mean >= 40 :
                nilaiHuruf = 'D'  
            else :
                nilaiHuruf = 'E' 

            tosave.nilai_angka = mean
            tosave.nilai_huruf = nilaiHuruf
            tosave.save()
            messages.success(request, 'Nilai berhasil disimpan!')
    else:
        form = formUjianNilai(instance=nilai)

     


    context = {
        'title': 'Ujian Mahasiswa',
        'heading': 'Ujian Nilai',
        'userdosen': userdosen,
        'photo': userdosen.photo,
        'data': data,
        'form': form,
        'nilai': nilai,
    }
    return render(request, 'dosen/ujian_dsn_nilai.html', context)


