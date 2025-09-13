from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils import timezone

from .models import Prodi, Pejabat, UserFakultas
from .models import NoSuratFakultas, Layanan, KodeSurat
from .models import SkripsiJudul, Proposal, skPembimbing, skPenguji, IzinPenelitian, Ujian, Yudisium, Hasil
from .models import SuketBebasKuliah, SuketBebasPlagiasi, SuketBerkelakuanBaik, SuketBebasPustaka


from .forms_fakultas import formLayananFakultasEdit
from .forms_fakultas import formProfile, formProdiEdit
from .forms_fakultas import formNoSurat, formUjian, formYudisium

from .decorators_fakultas import check_userfakultas
from .decorators_fakultas import fakultas_required

from aam.context_processors import web_name

tgl_now = timezone.now()


@fakultas_required
def profile_fakultas(request):
    userfakultas = UserFakultas.objects.get(username=request.user)     
    if request.method == 'POST':
        form = formProfile(request.POST, request.FILES, instance=userfakultas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_fakultas')
    else:
        form = formProfile(instance=userfakultas)

    context = {
        'title' : 'Edit Profile',
        'heading' : 'Edit Profile',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'form': form,
    }
    return render(request, 'fakultas/set/profile.html', context)


##########################  LAYANAN ######################################
# saya tambahkan filter untuk layanan fakultas - ndx
@fakultas_required
@check_userfakultas
def layanan_fakultas(request, filter):           
    userfakultas = request.userfakultas
    
    if filter != 'All':
        layanan_data = Layanan.objects.filter(layanan_jenis__level_proses='Fakultas',status=filter).order_by('-date_in')
    else:
        layanan_data = Layanan.objects.filter(layanan_jenis__level_proses='Fakultas').order_by('-date_in')
    
    context = {
        'title': 'Layanan',
        'heading': 'List Layanan',
        'userfakultas' : userfakultas,
        'filter' : filter,
        'photo' : userfakultas.photo,
        'layanan_data': layanan_data,
    }
    return render(request, 'fakultas/layanan_fakultas.html', context)


@fakultas_required
@check_userfakultas
def layanan_fakultas_edit(request, id, filter):
    userfakultas = request.userfakultas  
    layanan = get_object_or_404(Layanan, id=id)
    if request.method == 'POST':
        form = formLayananFakultasEdit(request.POST, request.FILES, instance=layanan)
        if form.is_valid():
            layanan = form.save(commit=False)  
            layanan.adminp = request.user   
            layanan.save()  
            messages.success(request, 'Berhasil')
            return redirect('acd:layanan_fakultas_edit', id=layanan.id, filter=filter)
        else:
            messages.error(request, 'periksa kembali isian data anda!')
            return redirect('acd:layanan_fakultas_edit', id=layanan.id, filter=filter)
    else:
        form = formLayananFakultasEdit(instance=layanan)

    context = {
        'title' : 'Kelolah Layanan',
        'heading' : 'Kelolah Layanan',
        'userfakultas' : userfakultas,
        'filter' : filter,
        'photo' : userfakultas.photo,
        'form': form,
    }
    return render(request, 'fakultas/layanan_fakultas_edit.html', context)


########### NOMOR SURAT #####################################################
@fakultas_required
@check_userfakultas
def nosurat_fakultas(request):           
    userfakultas = request.userfakultas   
    tahun = datetime.now().year
    nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
    if nosurat_cek:
        nosurat_baru = nosurat_cek.nomor + 1
    else:
        nosurat_baru = 1  

    if request.method == 'POST':
        form = formNoSurat(request.POST)
        if form.is_valid():
            nosurat = form.save(commit=False)  
            nosurat.adminp = request.user   
            nosurat.tahun = tahun
            nosurat.nomor = nosurat_baru 
            nosurat.save()  
            messages.success(request, 'No Surat Berhasil Ditambahkan')
        else:
            messages.error(request, 'periksa kembali isian data anda!')
        return redirect('acd:nosurat_fakultas')
    else:
        form = formNoSurat(request.POST)

    data = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-date_in')
    context = {
        'title': 'Nomor Surat',
        'heading': 'Nomor Surat',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
        'form' : form
    }
    return render(request, 'fakultas/nosurat.html', context)


@fakultas_required
@check_userfakultas
def nosurat_fakultas_del(request):
    userfakultas = request.userfakultas
    tahun = datetime.now().year
    data = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-date_in').first()
    if data:
        data.delete()
        messages.success(request, 'Berhasil Membatalkan Nomor Surat Terakhir')
    else:
        messages.warning(request, 'Tidak ada nomor surat untuk dibatalkan')
    return redirect('acd:nosurat_fakultas')


########### SK PEMBIMBING #####################################################
@fakultas_required
@check_userfakultas
def skpbb_list(request):           
    userfakultas = request.userfakultas
    data = skPembimbing.objects.all().order_by('-date_in')
    context = {
        'title': 'SK Pembimbing - List',
        'heading': 'Daftar SK Pembimbing',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
    }
    return render(request, 'fakultas/skpbb_list.html', context)


@fakultas_required
@check_userfakultas
def skpbb_pengajuan(request):           
    userfakultas = request.userfakultas
    data = SkripsiJudul.objects.filter(status_sk='Pengajuan')

    if request.method == "POST":
        skripsi_id = request.POST.get("skripsi_id")
        data_skripsi = SkripsiJudul.objects.get(id=skripsi_id)

        # Ambil nosurat, jika kosong ambil di sistem
        nosurat = request.POST.get("nosurat")
        if nosurat == "" :
            tahun = datetime.now().year
            nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
            if nosurat_cek:
                nosurat_baru = nosurat_cek.nomor + 1
            else:
                nosurat_baru = 1  
            kodesurat = KodeSurat.objects.get(jenis='SK Pembimbing')

            addnosurat = NoSuratFakultas.objects.create(
                adminp = request.user,
                tahun = tahun,
                nomor = nosurat_baru, 
                perihal = 'SK Pembimbing ' + str(data_skripsi.mhs),
                tujuan = 'Dosen Pembimbing Skripsi',
                kode = kodesurat.kode
            )
            nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun)            

        
        # Buat instance SK Pembimbing
        skpembimbing = skPembimbing.objects.create(
            nosurat=nosurat,
            mhs=data_skripsi.mhs,
            prodi=data_skripsi.prodi,  # Pastikan mhs memiliki relasi ke Prodi
            pembimbing1=data_skripsi.pembimbing1,
            pembimbing2=data_skripsi.pembimbing2,
            judul=data_skripsi.judul,
            ttd = Pejabat.objects.get(jabatan='Dekan', tgl_selesai__gte=tgl_now),
        )

        # Update status skripsi jika diperlukan
        data_skripsi.status_sk = 'Terbit'
        data_skripsi.save()

        #update layanan agar status DIPROSES
        context_pro = web_name(request)
        try:
            layanan = Layanan.objects.get(mhs=data_skripsi.mhs, layanan_jenis__nama_layanan__in = ['Penerbitan SK Pembimbing', 'Perpanjangan SK Pembimbing', 'Revisi SK Pembimbing'], status='Processing')
            layanan.status = 'Completed'
            layanan.hasil_test = 'SK Pembimbing anda telah diterbitkan, unduh di tautan berikut:'
            layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_skpbb/" + str(skpembimbing.id)
            layanan.save() 
            messages.success(request, f"Layanan Mahasiswa {data_skripsi.mhs} Berhasil diperbaharui ")
        except Layanan.DoesNotExist:
            messages.info(request, f"Tidak ada layanan yang ditemukan untuk mahasiswa {data_skripsi.mhs} ")

        # tambahkan program untuk skpbb     
        messages.success(request, f"SK Pembimbing {data_skripsi.mhs} berhasil diterbitkan ")

    context = {
        'title': 'SK Pembimbing - Pengajuan',
        'heading': 'Daftar Pengajuan SK Pembimbing',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
    }
    return render(request, 'fakultas/skpbb_pengajuan.html', context)



########### SK PENGUJI #####################################################
@fakultas_required
@check_userfakultas
def skpgj_list(request):           
    userfakultas = request.userfakultas
    data = skPenguji.objects.filter(nosurat__isnull=False).order_by('-date_in')
    context = {
        'title': 'SK Penguji - List',
        'heading': 'Daftar SK Penguji',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
    }
    return render(request, 'fakultas/skpgj_list.html', context)


@fakultas_required
@check_userfakultas
def skpgj_pengajuan(request):           
    userfakultas = request.userfakultas

    if request.method == "POST":
        id = request.POST.get("id")
        skpgj = skPenguji.objects.filter(id=id).first()
        # Ambil nosurat, jika kosong ambil di sistem
        nosurat = request.POST.get("nosurat")
        if nosurat == "" :
            tahun = datetime.now().year
            nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
            if nosurat_cek:
                nosurat_baru = nosurat_cek.nomor + 1
            else:
                nosurat_baru = 1  
            kodesurat = KodeSurat.objects.get(jenis='SK Penguji')

            addnosurat = NoSuratFakultas.objects.create(
                adminp = request.user,
                tahun = tahun,
                nomor = nosurat_baru, 
                perihal = 'SK Penguji ' + str(skpgj.usulan.mhs_judul.mhs),
                tujuan = 'Dosen Penguji Skripsi',
                kode = kodesurat.kode
            )
            nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 
        
        if skpgj:
            skpgj.nosurat = nosurat
            skpgj.date_in = tgl_now
            skpgj.ttd = Pejabat.objects.get(jabatan='Dekan', tgl_selesai__gte=tgl_now)
            skpgj.save()
            messages.success(request, f"SK Penguji berhasil diterbitkan ")


    data = skPenguji.objects.filter(nosurat__isnull=True).order_by('-date_in')
    context = {
        'title': 'SK Penguji - Pengajuan',
        'heading': 'Pengajuan SK Penguji',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
    }
    return render(request, 'fakultas/skpgj_pengajuan.html', context)




##########################  IZIN PENELITIAN ######################################
@fakultas_required
@check_userfakultas
def izinpenelitian_list(request):           
    userfakultas = request.userfakultas
    data = IzinPenelitian.objects.all().order_by('-date_in')
    context = {
        'title': 'Izin Penelitian - List',
        'heading': 'Daftar Izin Penelitian',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
    }
    return render(request, 'fakultas/izinpenelitian_list.html', context)


@fakultas_required
@check_userfakultas
def izinpenelitian_pengajuan(request):           
    userfakultas = request.userfakultas
    data = Layanan.objects.filter(status__in = ['Waiting', 'Processing'], layanan_jenis__nama_layanan = 'Izin Penelitian')

    if request.method == "POST":
        layanan_id = request.POST.get("id")
        layanan = Layanan.objects.get(id=layanan_id)
        action = request.POST.get('action')
        if action == 'tolak':
            #update layanan agar status DITOLAK
            layanan.status = 'Rejected'
            layanan.hasil_test = request.POST.get("alasan")
            layanan.adminp = request.user
            layanan.save() 
            messages.warning(request, f"Izin Penelitian {layanan.mhs} ditolak ")
        else :
            data_skripsi = SkripsiJudul.objects.get(mhs=layanan.mhs)
            # Buat instance Izin Penelitian
            nosurat= request.POST.get("nosurat")
            if nosurat == "" :
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Izin Penelitian')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    perihal = 'Izin Penelitian ' + str(data_skripsi.mhs),
                    tujuan = 'Pimpinan ' + request.POST.get("pimpinan"),
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun) 

            izinpenelitian = IzinPenelitian.objects.create(
                no_surat= nosurat,
                adminp = request.userfakultas,
                mhs_judul = data_skripsi,
                lokasi = request.POST.get("lokasi"),
                pimpinan = request.POST.get("pimpinan"),
                pimpinancq = request.POST.get("pimpinancq"),
                ttd = Pejabat.objects.get(jabatan='Wakil Dekan I', tgl_selesai__gte=tgl_now)  
            )

            #update layanan agar status DIPROSES
            context_pro = web_name(request)
            layanan.status = 'Completed'
            layanan.adminp = request.user
            layanan.hasil_test = 'Izin Penelitian anda telah terbit, download di tautan berikut:'
            layanan.hasil_link = context_pro.get("baseurl", "") + "acd/print_izinpenelitian/" + str(izinpenelitian.id)
            layanan.save() 

            # tambahkan program untuk izin penelitian     
            messages.success(request, f"Izin Penelitian {data_skripsi.mhs} berhasil diterbitkan ")  # Updated message to reflect Izin Penelitian
        

    context = {
        'title': 'Izin Penelitian - Pengajuan',
        'heading': 'Daftar Pengajuan Izin Penelitian',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
    }
    return render(request, 'fakultas/izinpenelitian_pengajuan.html', context)




##########################  UJIAN TUTUP SKRIPSI ######################################
@fakultas_required
@check_userfakultas
def ujian_list(request, filter):           
    userfakultas = request.userfakultas
    if filter == 'pengajuan':
        title = 'Ujian Tutup - Pengajuan'
        data = Ujian.objects.filter(ujian_tgl__isnull=False, no_surat__isnull=True).order_by('-date_in')
    elif filter == 'terbit':
        title = 'Ujian Tutup - Terbit'
        data = Ujian.objects.filter(ujian_tgl__isnull=False, no_surat__isnull=False).order_by('-date_in')
    else:
        title = 'Ujian Tutup'
        data = Ujian.objects.all().order_by('-date_in')

    
    context = {
        'title': title,
        'heading': title,
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'data' : data,
    }
    return render(request, 'fakultas/ujian_list.html', context)


@fakultas_required
@check_userfakultas
def ujian_proses(request, id):     
    userfakultas = request.userfakultas
    ujian = Ujian.objects.get(id=id)

    if request.method == "POST":
        form = formUjian(request.POST, instance=ujian)
        if form.is_valid():
            # Ambil nosurat, jika kosong ambil di sistem
            nosurat = request.POST.get("no_surat")
            if not nosurat :
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                if nosurat_cek:
                    nosurat_baru = nosurat_cek.nomor + 1
                else:
                    nosurat_baru = 1  
                kodesurat = KodeSurat.objects.get(jenis='Undangan Ujian')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp = request.user,
                    tahun = tahun,
                    nomor = nosurat_baru, 
                    perihal = 'Undangan Ujian ' + str(ujian.mhs_judul.mhs),
                    tujuan = 'Dosen Pimpinan Sidang, Pembimbing dan Penguji Skripsi',
                    kode = kodesurat.kode
                )
                nosurat =  str(nosurat_baru) + str(kodesurat.kode) + str(tahun)  
                messages.info(request, 'Nosurat diambil dari sistem') 

            ujian = form.save(commit=False)
            ujian.adminp = request.userfakultas
            ujian.no_surat = nosurat
            ujian.save()
            messages.success(request, 'Data Ujian berhasil diperbarui!')

            try:
                layanan = Layanan.objects.get(
                    mhs=ujian.mhs_judul.mhs,
                    layanan_jenis__nama_layanan='Undangan Ujian Tutup',
                    status__in=['Processing', 'Waiting']
                )
                layanan.status = 'Completed'
                layanan.hasil_test = 'Undangan Ujian anda telah diterbitkan, unduh di tautan berikut:'
                layanan.hasil_link = "/acd/print_undangan_ujian/" + str(ujian.id)
                layanan.adminp = request.user
                layanan.save()
                messages.info(request, f"Layanan Mahasiswa {ujian.mhs_judul.mhs} Berhasil diperbaharui ")
            except Layanan.DoesNotExist:
                messages.info(request, f"Tidak ada layanan yang ditemukan untuk mahasiswa {ujian.mhs_judul.mhs} ")


        else:
            messages.error(request, 'Periksa kembali isian data anda!')
    else:
        form = formUjian(instance=ujian)

    context = {
        'title': "Ujian Tutup - Proses",
        'heading': "Ujian Tutup - Proses",
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'ujian' : ujian,
        'bebaskuliah' : SuketBebasKuliah.objects.filter(mhs=ujian.mhs_judul.mhs).first(),
        'bebasplagiasi' : SuketBebasPlagiasi.objects.filter(mhs=ujian.mhs_judul.mhs).first(),
        'berkelakuanbaik': SuketBerkelakuanBaik.objects.filter(mhs=ujian.mhs_judul.mhs).first(),
        'bebaspustaka': SuketBebasPustaka.objects.filter(mhs=ujian.mhs_judul.mhs).first(),
        'skpbb' : skPembimbing.objects.filter(mhs=ujian.mhs_judul.mhs).order_by('-date_in').first(),
        'skpgj' : skPenguji.objects.filter(usulan__mhs_judul__mhs=ujian.mhs_judul.mhs).order_by('-date_in').first(),
        'proposal': Proposal.objects.get(mhs_judul__mhs=ujian.mhs_judul.mhs),
        'hasil': Hasil.objects.get(mhs_judul__mhs=ujian.mhs_judul.mhs),
        'form' : form,
    }
    return render(request, 'fakultas/ujian_proses.html', context)

@fakultas_required
@check_userfakultas
def ujian_yudisium(request, id):
    userfakultas = request.userfakultas  
    data = get_object_or_404(Ujian, id=id)
    yudisium, created = Yudisium.objects.get_or_create(ujian=data)
    
    if request.method == "POST":
        form = formYudisium(request.POST, instance=yudisium)
        if form.is_valid():
            # Ambil nosurat, jika kosong ambil dari sistem
            nosurat = request.POST.get("no_surat")
            if not nosurat:
                tahun = datetime.now().year
                nosurat_cek = NoSuratFakultas.objects.filter(tahun=tahun).order_by('-nomor').first()
                nosurat_baru = nosurat_cek.nomor + 1 if nosurat_cek else 1
                kodesurat = KodeSurat.objects.get(jenis='Berita Acara Yudisium')

                addnosurat = NoSuratFakultas.objects.create(
                    adminp=request.user,
                    tahun=tahun,
                    nomor=nosurat_baru, 
                    perihal='Yudisium Mahasiswa',
                    tujuan=str(data.mhs_judul.mhs),
                    kode=kodesurat.kode
                )
                nosurat = f"{nosurat_baru}{kodesurat.kode}{tahun}"
                messages.info(request, 'Nosurat diambil dari sistem') 

            update = form.save(commit=False)
            update.no_surat = nosurat
            update.ujian = data
            update.save()
            messages.success(request, 'Data Yudisium berhasil diperbarui!')
            return redirect('acd:ujian_yudisium', id=id)            
        else:
            messages.error(request, 'Periksa kembali isian data anda!')
    else:
        form = formYudisium(instance=yudisium)

    context = {
        'title': 'Ujian',
        'heading': 'Nilai Ujian',
        'form': form,  # Perbaikan di sini, sebelumnya salah
        'userfakultas': userfakultas,
        'photo': userfakultas.photo,
        'data': data,
    }
    return render(request, 'fakultas/ujian_yudisium.html', context)












