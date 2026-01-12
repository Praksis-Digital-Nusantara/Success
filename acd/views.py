from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout, login, authenticate

from .models import UserMhs, UserProdi, UserFakultas, UserDosen, Layanan, Pejabat
from .models import SkripsiJudul, Proposal, Hasil, Ujian, SkripsiJudul, skUjian

from .forms import RoleChangeForm, CustomPasswordChangeForm

from django.utils import timezone

from datetime import date
from django.db.models import Count


now = timezone.now()



@login_required
def index(request):

    userC = None # izin menambahkan userC = None
    if request.user.last_name == 'Mahasiswa':
        try:
            userC = UserMhs.objects.get(nim=request.user)
            tgl_masuk = userC.tgl_masuk
            tgl_sekarang = date.today()
            selisih_hari_total = (tgl_sekarang - tgl_masuk).days
            ms_tahun = selisih_hari_total // 365
            sisa_hari_setelah_tahun = selisih_hari_total % 365
            ms_bulan = sisa_hari_setelah_tahun // 30
            ms_hari = sisa_hari_setelah_tahun % 30
            data = {
                    'layanan_waiting': Layanan.objects.filter(mhs=userC, status='Waiting').count() or 0,
                    'layanan_processing': Layanan.objects.filter(mhs=userC, status='Processing').count() or 0,
                    'layanan_completed': Layanan.objects.filter(mhs=userC, status='Completed').count() or 0,
                    'layanan_rejected': Layanan.objects.filter(mhs=userC, status='Rejected').count() or 0,
                    'layanan_month': Layanan.objects.filter(mhs=userC, date_in__month=now.month or 0, date_in__year=now.year).count() or 0,
                    'layanan_year': Layanan.objects.filter(mhs=userC, date_in__year=now.year).count() or 0,
                    'layanan_all': Layanan.objects.filter(mhs=userC).count() or 0,
                    'ms_tahun': ms_tahun,
                    'ms_bulan': ms_bulan,
                    'ms_hari': ms_hari,
                }
        except UserMhs.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_mhs')
    elif request.user.last_name == 'Dosen':  
        try:
            userC = UserDosen.objects.get(nip=request.user)
            data = {
                    'seleksi_judul': SkripsiJudul.objects.filter(mhs__penasehat_akademik=userC, judul__isnull=True).count() or 0,
                    'pbb2_persetujuan': SkripsiJudul.objects.filter(pembimbing2=userC, pembimbing2_persetujuan='Waiting').count() or 0,
                    'proposal': Proposal.objects.filter(Q(pembimbing1=userC) | Q(pembimbing2=userC) | Q(penguji1=userC) | Q(penguji2=userC)).count() or 0,
                    'hasil': Hasil.objects.filter(Q(pembimbing1=userC) | Q(pembimbing2=userC) | Q(penguji1=userC) | Q(penguji2=userC)).count() or 0,
                    'ujian': Ujian.objects.filter(Q(pembimbing1=userC) | Q(pembimbing2=userC) | Q(penguji1=userC) | Q(penguji2=userC)).count() or 0,
                }
            is_pejabat_aktif = Pejabat.objects.filter(
                        pejabat=userC,
                        tgl_mulai__lte=now,
                        tgl_selesai__gte=now
            ).exists()
            request.is_pejabat_aktif = is_pejabat_aktif  # bisa dipakai di view & template
        except UserDosen.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_dosen')
    elif request.user.last_name == 'Admin Prodi':  
        try:
            userC = UserProdi.objects.get(username=request.user)
            for layanan in Layanan.objects.filter(status='Rejected'):
                print(layanan.date_in)
            data = {
                    'layanan_waiting': Layanan.objects.filter(status='Waiting', mhs__prodi=userC.prodi).count() or 0,
                    'layanan_processing': Layanan.objects.filter(status='Processing', mhs__prodi=userC.prodi).count() or 0,
                    'layanan_completed': Layanan.objects.filter(status='Completed', mhs__prodi=userC.prodi).count() or 0,
                    'layanan_rejected': Layanan.objects.filter(status='Rejected', mhs__prodi=userC.prodi).count() or 0,
                    'layanan_month': Layanan.objects.filter(date_in__month=now.month or 0, date_in__year=now.year, mhs__prodi=userC.prodi).count() or 0,
                    'layanan_year': Layanan.objects.filter(date_in__year=now.year, mhs__prodi=userC.prodi).count() or 0,
                    'layanan_all': Layanan.objects.filter(mhs__prodi=userC.prodi).count() or 0,
                    'pengajuan_judul': SkripsiJudul.objects.filter(Q(status_sk='-') | Q(status_sk='')).exclude(status='Waiting').count() or 0,
                }
        except UserProdi.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_prodi')
    elif request.user.last_name == 'Admin Fakultas':  
        try:
            userC = UserFakultas.objects.get(username=request.user)
            total_dosen = UserDosen.objects.count() or 0
            total_profesor = UserDosen.objects.filter(jafung='Guru Besar').count() or 0
            total_lektor_kepala = UserDosen.objects.filter(jafung='Lektor Kepala').count() or 0
            total_lektor = UserDosen.objects.filter(jafung='Lektor').count() or 0
            total_asisten_ahli = UserDosen.objects.filter(jafung='Asisten Ahli').count() or 0
            
            persen_profesor = 0
            persen_asisten_ahli = 0
            persen_lektor_kepala = 0
            persen_lektor = 0
            if total_dosen > 0:
                persen_profesor = round((total_profesor / total_dosen) * 100, 1)
                persen_lektor_kepala = round((total_lektor_kepala / total_dosen) * 100, 1)
                persen_asisten_ahli = round((total_asisten_ahli / total_dosen) * 100, 1)
                persen_lektor = round((total_lektor / total_dosen) * 100, 1)

            
            total_mahasiswa = UserMhs.objects.count() or 0
            mhs_per_prodi_query = UserMhs.objects.values('prodi__nama_prodi') \
                                         .annotate(jumlah=Count('nim')) \
                                         .order_by('-jumlah')
            
            list_mhs_prodi = []
            for item in mhs_per_prodi_query:
                nama_prodi = item['prodi__nama_prodi'] if item['prodi__nama_prodi'] else "Tanpa Prodi"
                jumlah = item['jumlah']
                persen = 0
                if total_mahasiswa > 0:
                    persen = round((jumlah / total_mahasiswa) * 100, 1)
                
                list_mhs_prodi.append({
                    'nama': nama_prodi,
                    'jumlah': jumlah,
                    'persen': persen
                })

            data = {
                    'dosen': UserDosen.objects.count() or 0,
                    'profesor': total_profesor,
                    'lektor_kepala': total_lektor_kepala,
                    'asisten_ahli': total_asisten_ahli,
                    'lektor': total_lektor,

                    'persen_profesor': persen_profesor,
                    'persen_asisten_ahli': persen_asisten_ahli,
                    'persen_lektor_kepala': persen_lektor_kepala,
                    'persen_lektor': persen_lektor,

                    'mahasiswa': total_mahasiswa,
                    'list_mhs_prodi': list_mhs_prodi,


                    'skpbb': SkripsiJudul.objects.filter(status_sk='Pengajuan').count() or 0,
                    'skujian': skUjian.objects.filter(nosurat__isnull=True).count() or 0,
                    'izinpenelitian': Layanan.objects.filter(status__in=['Processing','Waiting'], layanan_jenis__nama_layanan='Izin Penelitian').count() or 0,
                    'ujian': Layanan.objects.filter(status__in=['Processing','Waiting'], layanan_jenis__nama_layanan='Undangan Ujian Tutup').count() or 0,
                    'layanan_rejected': Layanan.objects.filter(status='Rejected').count() or 0,
                    'suket_berkelakuanbaik': Layanan.objects.filter(status__in=['Completed'], layanan_jenis__nama_layanan='Surat Keterangan Berkelakuan Baik').count() or 0,
                    'suket_aktifkuliah': Layanan.objects.filter(status__in=['Completed'], layanan_jenis__nama_layanan='Surat Keterangan Aktif Kuliah').count() or 0,
                    'suket_cuti_akademik':Layanan.objects.filter(status__in=['Completed'], layanan_jenis__nama_layanan='Surat Keterangan Cuti Akademik').count() or 0,
                }
        except UserFakultas.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_fakultas')  
        
    context = {
        'title' : 'Dashboard',
        'heading' : 'Dashboard',
        'data' : data,
        'photo' : userC.photo if userC else None,
        'userdetail' : userC if userC else None,
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
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update session auth hash untuk mencegah logout setelah ganti password
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Anda berhasil diubah!')
            return redirect('/acd/changepass')
        else:
            messages.error(request, 'Harap periksa kembali isian formulir.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = {
        'title' : 'Change Password',
        'heading' : 'Change Password',
        'form': form,
    }
    return render(request, 'changepass.html', context)

@login_required
def changerole(request):
    if request.session.get('su', '0') != '557799':
        messages.error(request, 'Anda tidak memiliki izin untuk mengubah role.')
        return redirect('/acd/')
    else:
        if request.method == 'POST':
            form = RoleChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                # Simpan perubahan role
                user_target = form.cleaned_data['user_target']
                logout(request)
                user_target.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user_target)
                request.session['su'] = '557799'
                messages.success(request, 'Berhasil Pindah Role!')
                return redirect('/acd/')
            else:
                messages.error(request, 'Harap periksa kembali isian formulir.')
        else:
            form = RoleChangeForm(user=request.user)

        context = {
            'title' : 'Change Role',
            'heading' : 'Change Role',
            'form': form,
        }
        return render(request, 'changerole.html', context)

