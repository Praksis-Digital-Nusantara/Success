from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import UserMhs, UserDosen
from .models import Layanan, LayananJenis
from .models import SuketBebasPlagiasi, SuketBebasKuliah, SuketBerkelakuanBaik, SuketBebasPustaka, SuketUsulanUjianSkripsi
from .models import SkripsiJudul, chatPA, skPembimbing, Proposal, Hasil, IzinPenelitian, Ujian, skPenguji

from .forms_mhs import formAddLayanan
from .forms_mhs import formProfile
from .forms_mhs import formSkripsiJudul, formProposalReg, formHasilReg, formUjianReg
from .forms_mhs import formChatPA

from .decorators_mhs import check_usermhs
from .decorators_mhs import mahasiswa_required


@mahasiswa_required
def profile_mhs(request):
    usermhs = UserMhs.objects.get(nim=request.user)   
    if request.method == 'POST':
        form = formProfile(request.POST, request.FILES, instance=usermhs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_mhs')
        else:
            messages.error(request, 'Gagal Memproses, pastikan semua isian sesuai format')
            return redirect('/acd/profile_mhs')
    else:
        form = formProfile(instance=usermhs)

    context = {
        'title' : 'Profile',
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
    layanan_data = Layanan.objects.filter(mhs=usermhs).order_by('-date_in')
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
            layanan_jenis = form.cleaned_data.get('layanan_jenis')
            
            # Cek apakah ada layanan dengan jenis yang sama dan status "Waiting" atau "Processing"
            layanan_exists = Layanan.objects.filter(
                mhs=usermhs, 
                layanan_jenis=layanan_jenis, 
                status__in=["Waiting", "Processing"]
            ).exists()
            
            if layanan_exists:
                messages.error(request, 'Anda masih memiliki layanan dengan jenis ini yang sedang diproses.')
                return redirect('/acd/layanan_me') 
            else:
                layanan = form.save(commit=False)  
                layanan.mhs = usermhs 
                layanan.prodi = usermhs.prodi
                if layanan_jenis.level_proses == 'Fakultas':
                    layanan.status = 'Processing'
                    layanan.hasil_test = 'menunggu diproses oleh admin Falultas'
                else:
                    layanan.status = 'Waiting' 
                layanan.save()  
                messages.success(request, 'Layanan berhasil ditambahkan!')
                return redirect('/acd/layanan_me') 
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan periksa input Anda.')
    else:
        form = formAddLayanan()

    context = {
        'title': 'Layanan Baru',
        'heading': 'Layanan Baru',
        'usermhs': usermhs,
        'photo': usermhs.photo,
        'form': form,
    }
    return render(request, 'mhs/layanan_add.html', context)




#################### SKRIPSI

@mahasiswa_required
@check_usermhs
def skripsi(request):
    usermhs = request.usermhs       

    try:
        skripsi = SkripsiJudul.objects.get(mhs=usermhs)
    except SkripsiJudul.DoesNotExist:
        skripsi = None 
    try:
        skpbb = skPembimbing.objects.filter(mhs=usermhs).order_by('date_in')
    except skPembimbing.DoesNotExist:
        skpbb = None 

    try:
        proposal = Proposal.objects.get(mhs_judul__mhs=usermhs)
    except Proposal.DoesNotExist:
        proposal = None 

    try:
        izinpenelitian = IzinPenelitian.objects.filter(mhs_judul__mhs=usermhs).order_by('-date_in')
    except IzinPenelitian.DoesNotExist:
        izinpenelitian = None 

    try:
        hasil = Hasil.objects.get(mhs_judul__mhs=usermhs)
    except Hasil.DoesNotExist:
        hasil = None 

    try:
        ujian = Ujian.objects.get(mhs_judul__mhs=usermhs)
    except Ujian.DoesNotExist:
        ujian = None 

    context = {
        'title' : 'Skripsi',
        'heading' : 'Skripsi',
        'usermhs' : usermhs,
        'skripsi' : skripsi,
        'skpbb' : skpbb,
        'proposal' : proposal,
        'izinpenelitian' : izinpenelitian,
        'hasil' : hasil,
        'ujian' : ujian,
        'photo' : usermhs.photo,
    }
    return render(request, 'mhs/skripsi.html', context)



@mahasiswa_required
@check_usermhs
def skripsi_pjudul(request):
    usermhs = request.usermhs
    
    # Ambil data skripsi jika sudah ada
    try:
        skripsi_judul = SkripsiJudul.objects.get(mhs=usermhs)
    except ObjectDoesNotExist:
        skripsi_judul = None

    # Ambil semua chat yang sesuai
    chatpa_list = chatPA.objects.filter(dsn=usermhs.penasehat_akademik, mhs=usermhs).order_by('date_in')

    form_skripsi = formSkripsiJudul(instance=skripsi_judul)
    form_chatpa = formChatPA()

    if request.method == 'POST':
        if 'submit_skripsi' in request.POST:  # Submit form skripsi
            form_skripsi = formSkripsiJudul(request.POST, instance=skripsi_judul)
            if form_skripsi.is_valid():
                skripsi_judul = form_skripsi.save(commit=False)
                if skripsi_judul.status in ['', 'Revision']:
                    skripsi_judul.status = 'Waiting'
                skripsi_judul.prodi = usermhs.prodi
                skripsi_judul.mhs = usermhs
                skripsi_judul.save()
                messages.success(request, 'Judul berhasil disimpan.', extra_tags='skripsi')
                return redirect('/acd/skripsi_pjudul')
            else:
                messages.error(request, 'Periksa kembali isian form skripsi.', extra_tags='skripsi')

        elif 'submit_chatpa' in request.POST:  # Submit form chatPA
            form_chatpa = formChatPA(request.POST)
            if form_chatpa.is_valid():
                chatpa = form_chatpa.save(commit=False)
                chatpa.dsn = usermhs.penasehat_akademik
                chatpa.mhs = usermhs
                chatpa.prodi = usermhs.prodi
                chatpa.sender = 'Mahasiswa'
                chatpa.save()
                messages.success(request, 'Pesan ke pembimbing berhasil dikirim.', extra_tags='chatpa')
                return redirect('/acd/skripsi_pjudul')
            else:
                messages.error(request, 'Periksa kembali isi pesan.', extra_tags='chatpa')       

    # Ambil data pembimbing akademik
    # nip_pa = usermhs.penasehat_akademik
    # pa = UserDosen.objects.get(nip=nip_pa)
    pa = usermhs.penasehat_akademik #untuk saya tampilkan foto di chat

    context = {
        'title': 'Pengajuan Judul',
        'heading': 'Pengajuan Judul',
        'usermhs': usermhs,
        'photo': usermhs.photo,
        'form': form_skripsi,
        'form_chatpa': form_chatpa,
        'chatpa': chatpa_list,  # Kirim semua chat ke template
        'pa': pa,
    }
    return render(request, 'mhs/skripsi_pjudul.html', context)



###################### REGISTRASI PROPOSAL #######################################################


@mahasiswa_required
@check_usermhs
def proposal_reg(request):
    usermhs = request.usermhs
    judul = SkripsiJudul.objects.get(mhs=usermhs)

    # Mencoba mengambil Proposal yang ada, jika tidak ada, buat yang baru
    try:
        proposal = Proposal.objects.get(mhs_judul__mhs=usermhs)
    except Proposal.DoesNotExist:
        proposal = Proposal(mhs_judul=judul)  # Membuat proposal baru jika tidak ditemukan
        proposal.save()

    if request.method == 'POST':
        form = formProposalReg(request.POST, request.FILES, instance=proposal)
        if form.is_valid():
            proposal_obj = form.save(commit=False)
            proposal_obj.mhs_judul = judul  # Pastikan judul tetap terikat
            proposal_obj.save()  # Simpan perubahan atau data baru
            messages.success(request, 'Data berhasil disimpan!')
        else:
            messages.error(request, 'Periksa kembali isian form.')
    else:
        form = formProposalReg(instance=proposal)

    context = {
        'title': 'Proposal',
        'heading': 'Proposal Registrasi',
        'usermhs': usermhs,
        'photo': usermhs.photo,
        'judul': judul,
        'proposal': proposal,
        'form': form,
    }
    return render(request, 'mhs/proposal_reg.html', context)


@mahasiswa_required
@check_usermhs
def proposal_reg_up(request):
    usermhs = request.usermhs
    proposal = Proposal.objects.get(mhs_judul__mhs=usermhs)
    if request.method == 'POST':
        if proposal.krs == "" or proposal.krs == "" or proposal.persetujuan_proposal == "" or proposal.kartu_seminar == "" or proposal.konsultasi_skripsi == "":
            messages.error(request, 'Berkas persyaratan belum lengkap, silakan lengkapi terlebih dahulu.')
            return redirect('/acd/proposal_reg')
        else:
            ceklayanan = Layanan.objects.filter(mhs=usermhs, layanan_jenis__nama_layanan='Undangan Seminar Proposal',status__in=['Waiting', 'Processing']).exists()
            if ceklayanan:
                messages.info(request, 'Anda masih memiliki layanan dengan jenis ini yang sedang diproses.')
                return redirect('/acd/proposal_reg')
            else:
                layanan = Layanan(
                    mhs=usermhs,
                    layanan_jenis=LayananJenis.objects.get(nama_layanan='Undangan Seminar Proposal'),
                    status='Waiting',
                    layanan_isi=request.POST.get('layanan_isi'),
                )  # Menambahkan layanan baru
                layanan.save()
                messages.success(request, 'Pendaftar Proposal berhasil!, cek status di menu layanan')
                return redirect('/acd/layanan_me')


###################### SEMINAR HASIL #######################################################
@mahasiswa_required
@check_usermhs
def hasil_reg(request):
    usermhs = request.usermhs
    judul = SkripsiJudul.objects.get(mhs=usermhs)
    # Mencoba mengambil Hasil yang ada, jika tidak ada, buat yang baru
    try:
        hasil = Hasil.objects.get(mhs_judul__mhs=usermhs)
    except Hasil.DoesNotExist:
        hasil = Hasil(mhs_judul=judul)  # Membuat hasil baru jika tidak ditemukan
        hasil.save()
    
    if request.method == 'POST':
        form = formHasilReg(request.POST, request.FILES, instance=hasil)
        if form.is_valid():
            hasil_obj = form.save(commit=False)
            hasil_obj.mhs_judul = judul  # Pastikan judul tetap terikat
            hasil_obj.save()  # Simpan perubahan atau data baru
            messages.success(request, 'Data berhasil disimpan!')
        else:
            messages.error(request, 'Periksa kembali isian form.')
    else:
        form = formHasilReg(instance=hasil)

    context = {
        'title': 'Hasil',
        'heading': 'Hasil Registrasi',
        'usermhs': usermhs,
        'photo': usermhs.photo,
        'judul': judul,
        'hasil': hasil,
        'form': form,
    }
    return render(request, 'mhs/hasil_reg.html', context)

@mahasiswa_required
@check_usermhs
def hasil_reg_up(request):
    usermhs = request.usermhs
    hasil = Hasil.objects.get(mhs_judul__mhs=usermhs)
    if request.method == 'POST':
        if hasil.krs == "" or hasil.ksm == "" or hasil.kartu_kontrol_seminar == "" or hasil.buku_konsultasi == "" or hasil.persetujuan_hasil == "" or hasil.transkrip == "" or hasil.suket_selesai_meneliti == "": 
            messages.error(request, 'Berkas persyaratan belum lengkap, silakan lengkapi terlebih dahulu.')
            return redirect('/acd/hasil_reg')
        else:
            ceklayanan = Layanan.objects.filter(mhs=usermhs, layanan_jenis__nama_layanan='Undangan Seminar Hasil',status__in=['Waiting', 'Processing']).exists()
            if ceklayanan:
                messages.info(request, 'Anda masih memiliki layanan dengan jenis ini yang sedang diproses.')
                return redirect('/acd/hasil_reg')
            else:
                layanan = Layanan(
                    mhs=usermhs,
                    layanan_jenis=LayananJenis.objects.get(nama_layanan='Undangan Seminar Hasil'),
                    status='Waiting',
                    layanan_isi=request.POST.get('layanan_isi'),
                )  # Menambahkan layanan baru
                layanan.save()
                messages.success(request, 'Pendaftar Hasil berhasil!, cek status di menu layanan')
                return redirect('/acd/layanan_me')
###################### REGISTRASI UJIAN #######################################################

@mahasiswa_required
@check_usermhs
def ujian_reg(request):
    usermhs = request.usermhs
    judul = SkripsiJudul.objects.get(mhs=usermhs)

    try:
        ujian = Ujian.objects.get(mhs_judul__mhs=usermhs)
    except Ujian.DoesNotExist:
        ujian = Ujian(mhs_judul=judul)  # Membuat ujian baru jika tidak ditemukan
        ujian.save()

    if request.method == 'POST':
        form = formUjianReg(request.POST, request.FILES, instance=ujian)
        if form.is_valid():
            ujian_obj = form.save(commit=False)
            ujian_obj.mhs_judul = judul  # Pastikan judul tetap terikat
            ujian_obj.save()  # Simpan perubahan atau data baru
            messages.success(request, 'Data berhasil disimpan!')
        else:
            messages.error(request, 'Periksa kembali isian form.')
    else:
        form = formUjianReg(instance=ujian)

    context = {
        'title': 'Ujian',
        'heading': 'Ujian Registrasi',
        'usermhs': usermhs,
        'photo': usermhs.photo,
        'judul': judul,
        'ujian': ujian,
        'berkelakuanbaik': SuketBerkelakuanBaik.objects.filter(mhs=usermhs).order_by('-date_in').first(),
        'bebasbebankuliah': SuketBebasKuliah.objects.filter(mhs=usermhs).order_by('-date_in').first(),
        'bebasplagiasi': SuketBebasPlagiasi.objects.filter(mhs=usermhs).order_by('-date_in').first(),
        'bebaspustaka': SuketBebasPustaka.objects.filter(mhs=usermhs).order_by('-date_in').first(),
        'skpbb': skPembimbing.objects.filter(mhs=usermhs).order_by('-date_in').first(),
        'skpgj': skPenguji.objects.filter(usulan__mhs_judul__mhs=usermhs).order_by('-date_in').first(),
        'proposal': Proposal.objects.get(mhs_judul__mhs=usermhs),
        'usulanujianskripsi': SuketUsulanUjianSkripsi.objects.filter(mhs_judul__mhs=usermhs).order_by('-date_in').first(),
        'hasil': Hasil.objects.get(mhs_judul__mhs=usermhs),
        'form': form,
    }
    return render(request, 'mhs/ujian_reg.html', context)


@mahasiswa_required
@check_usermhs
def ujian_reg_up(request):
    usermhs = request.usermhs
    ujian = Ujian.objects.get(mhs_judul__mhs=usermhs)

    # Cek apakah semua berkas sudah diupload
    # bebaskuliah = SuketBebasKuliah.objects.filter(mhs=usermhs).order_by('-date_in').first()
    bebasplagiasi = SuketBebasPlagiasi.objects.filter(mhs=usermhs).order_by('-date_in').first()
    skpbb = skPembimbing.objects.filter(mhs=usermhs).order_by('-date_in').first()
    skpgj = skPenguji.objects.filter(usulan__mhs_judul__mhs=usermhs).order_by('-date_in').first()
    berkelakuanbaik = SuketBerkelakuanBaik.objects.filter(mhs=usermhs).order_by('-date_in').first()
    bebaspustaka = SuketBebasPustaka.objects.filter(mhs=usermhs).order_by('-date_in').first()
    usulanujianskripsi = SuketUsulanUjianSkripsi.objects.filter(mhs_judul__mhs=usermhs).order_by('-date_in').first()
    proposal = Proposal.objects.get(mhs_judul__mhs=usermhs)
    hasil = Hasil.objects.get(mhs_judul__mhs=usermhs)
    if request.method == 'POST':
        if (
                not bebasplagiasi or
                not skpbb or
                not berkelakuanbaik or
                not bebaspustaka or
                not usulanujianskripsi or
                not skpgj or
                not proposal or
                not hasil or
                not ujian.persetujuan_ujian or
                not ujian.matriks_perbaikan or
                not ujian.transkrip or
                not ujian.ijaza_terakhir or
                not ujian.ukt_terakhir or
                not ujian.bebas_pustaka_univ or
                not ujian.ktp or
                not ujian.krs_berjalan or
                not ujian.usulan_baak or
                not ujian.persetujuan_waktu or
                not ujian.foto_latar_biru
            ):
            messages.error(request, 'Berkas persyaratan belum lengkap, silakan lengkapi terlebih dahulu.')
            return redirect('/acd/ujian_reg')
        else:
            ceklayanan = Layanan.objects.filter(mhs=usermhs, layanan_jenis__nama_layanan='Undangan Ujian Tutup',status__in=['Waiting', 'Processing']).exists()
            if ceklayanan:
                messages.info(request, 'Anda masih memiliki layanan dengan jenis ini yang sedang diproses.')
                return redirect('/acd/ujian_reg')
            else:
                # Jika tidak ada layanan yang sedang diproses, lanjutkan
                layanan = Layanan(
                    mhs=usermhs,
                    layanan_jenis=LayananJenis.objects.get(nama_layanan='Undangan Ujian Tutup'),
                    status='Waiting',
                    layanan_isi=request.POST.get('layanan_isi'),
                    )  # Menambahkan layanan baru
                layanan.save()            
                messages.success(request, 'Pendaftar Ujian berhasil!, cek status di menu layanan')
                return redirect('/acd/layanan_me')

            


