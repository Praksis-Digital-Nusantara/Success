from django import forms
from django.forms import modelformset_factory
from .models import Prodi, Pejabat, Layanan, LayananJenis
from .models import UserFakultas, UserDosen
from .models import NoSuratFakultas, KodeSurat
from .models import Ujian, Yudisium
from .models import SuketAktifKuliah, SuketIzinObservasi, SuketRekomendasi, SuketIzinLab, SuketBerkelakuanBaik, SuketCutiAkademik
from .models import SuratTugas, SuratTugas_NamaDosen, SuratTugas_NamaMhs
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q



tgl_now = timezone.now()

class formProfile(forms.ModelForm):
    class Meta:
        model = UserFakultas
        fields = [   
            'telp',
            'gender',
            'photo',
        ]
        widgets = {
            'gender': forms.Select(
                choices=[
                    ('Laki-laki', 'Laki-laki'),
                    ('Perempuan', 'Perempuan'),
                ],
                attrs={'class': 'form-control'}
            ),
            'telp': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class formProdiEdit(forms.ModelForm):
    class Meta:
        model = Prodi
        fields = [
            'strata', 
            'nama_prodi',  
            'jurusan', 
            'gelar', 
            'nama_mk', 
            'kode_mk', 
            'status', 
        ]
        widgets = {
            'strata': forms.Select(
                choices=[
                    ('S1', 'S1'),
                    ('S2', 'S2'),
                    ('S3', 'S3'),
                    ('D1', 'D1'),
                    ('D2', 'D2'),
                    ('D3', 'D3'),
                    ('D4', 'D4'),
                    ('Profesi', 'Profesi'),
                ],
                attrs={'class': 'form-control'}
            ),
            'nama_prodi': forms.TextInput(attrs={'class': 'form-control'}),
            'jurusan': forms.Select(attrs={'class': 'form-control'}),
            'gelar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh : S.Pd. '}),
            'nama_mk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skripsi / Tugas Akhir / Tesis '}),
            'kode_mk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kode mk untuk Skripsi / Tugas Akhir / Tesis '}),
            'status': forms.Select(
                choices=[
                    ('Aktif', 'Aktif'),
                    ('Nonaktif', 'Nonaktif'),
                ],
                attrs={'class': 'form-control'}
            ),

        }
        labels = {
            'strata': 'Strata',
            'nama_prodi': 'Nama Program Studi',
            'status': 'Status',
        }


class formLayananFakultasEdit(forms.ModelForm):
    class Meta:
        model = Layanan
        fields = [    
            'status',
            'hasil_test',
            'hasil_file',
            'hasil_link',
        ]
        widgets = {
            'status': forms.Select(
                choices=[
                    ('Processing', 'Processing'),
                    ('Rejected', 'Rejected'),
                    ('Completed', 'Completed'),
                ],
                attrs={'class': 'form-control'}
            ),
            'hasil_test': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '...'}),
            'hasil_link': forms.TextInput(attrs={'class': 'form-control'}),
            'hasil_file': forms.FileInput(attrs={'class': 'form-control'}),
        }



class formNoSurat(forms.ModelForm):
    kode = forms.ModelChoiceField(
        queryset=KodeSurat.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Kode Surat",
        label="Kode Surat"
    )

    class Meta:
        model = NoSuratFakultas
        fields = ['perihal', 'tujuan', 'kode']
        widgets = {
            'perihal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Undangan Rapat'}),
            'tujuan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Seluruh Dosen Prodi'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tampilkan jenis - kode di dropdown
        self.fields['kode'].label_from_instance = lambda obj: f"{obj.jenis} - {obj.kode}"

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_kode_obj = self.cleaned_data['kode']
        instance.kode = selected_kode_obj.kode  # simpan hanya string kode
        if commit:
            instance.save()
        return instance


class formUjian(forms.ModelForm):
    dekan = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(
            tgl_selesai__gte=tgl_now, jabatan__in=['Dekan', 'Wakil Dekan I']
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )
    wd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )
    kaprodi = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )
    penguji1 = forms.ModelChoiceField(
        queryset=UserDosen.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Dosen"
    )
    penguji2 = forms.ModelChoiceField(
        queryset=UserDosen.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Dosen"
    )
    
    class Meta:
        model = Ujian
        fields = [    
            'no_surat',
            'ujian_tgl',
            'ujian_jam',
            'ujian_tempat',
            'ujian_link',
            'penguji1',
            'penguji2',
            'ttd_status',
            'kaprodi',
            'wd',
            'dekan',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*kosongkan jika ambil nomor dari sistem'}),
            'ujian_tgl': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'ujian_jam': forms.TimeInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'time'}),
            'ujian_tempat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zoom Meeting ID : 00000000 Passcode: xxxxx', 'required': 'required'}),
            'ujian_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'link zoom jika ada'}),
            'penguji1': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'penguji2': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'ttd_status': forms.Select(
                                choices=[
                                    ('QRcode', 'QRcode'),
                                    ('Manual', 'Manual'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'kaprodi': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'wd': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'dekan': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


class formYudisium(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(
            tgl_selesai__gte=tgl_now, jabatan__in=['Dekan', 'Wakil Dekan I']
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )

    class Meta:
        model = Yudisium
        fields = [    
            'date_in',
            'no_surat',
            'ipk',
            'kualifikasi',
            'catatan',
            'ttd',
        ]
        widgets = {
            'date_in': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'no_surat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*kosongkan jika ambil nomor dari sistem'}),
            'catatan': forms.TextInput(attrs={'class': 'form-control'}),
            'ipk': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'number', 'step': '0.01'}),
            'kualifikasi': forms.Select(
                                choices=[
                                    ('Pujian', 'Pujian'),
                                    ('Sangat Memuaskan', 'Sangat Memuaskan'),
                                    ('Memuaskan', 'Memuaskan'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'ttd': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


# SUKET AKTIF KULIAH
class formSuketAktifKuliah(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now, jabatan__in=['Wakil Dekan III']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )

    class Meta:
        model = SuketAktifKuliah
        fields = [
            'no_surat',
            'semester',
            'tahun_akademik',
            'ortu_nama',
            'ortu_nip',
            'ortu_gol',
            'ortu_pekerjaan',
            'ortu_instansi',
            'ortu_alamat',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '*kosongkan jika ambil nomor dari sistem'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: II / Dua'
            }),
            'tahun_akademik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 2024/2025'
            }),
            'ortu_nama': forms.TextInput(attrs={'class': 'form-control'}),
            'ortu_nip': forms.TextInput(attrs={'class': 'form-control'}),
            'ortu_gol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: III.a'
            }),
            'ortu_pekerjaan': forms.TextInput(attrs={'class': 'form-control'}),
            'ortu_instansi': forms.TextInput(attrs={'class': 'form-control'}),
            'ortu_alamat': forms.TextInput(attrs={'class': 'form-control'}),
            'ttd_status': forms.Select(
                choices=[
                    ('QRcode', 'QRcode'),
                    ('Manual', 'Manual'),
                ],
                attrs={'class': 'form-control'}
            ),
            # 'ttd' dikustomisasi di luar Meta
        }


# SUKET AKTIF KULIAH
class formSuketIzinObservasi(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now, jabatan__in=['Wakil Dekan I']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )

    class Meta:
        model = SuketIzinObservasi
        fields = [
            'no_surat',
            'semester',
            'tahun_akademik',
            'perihal',
            'tujuan',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '*kosongkan jika ambil nomor dari sistem'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: II / Dua'
            }),
            'tahun_akademik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 2024/2025 Genap'
            }),
            'perihal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'izin melakukan observasi uji coba angket sekolah'
            }),
            'tujuan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kepala SMAN 1 Indonesia'
            }),
            'ttd_status': forms.Select(
                choices=[
                    ('QRcode', 'QRcode'),
                    ('Manual', 'Manual'),
                ],
                attrs={'class': 'form-control'}
            ),
            # 'ttd' dikustomisasi di luar Meta
        }




class formSuketIzinLab(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now, jabatan__in=['Wakil Dekan I']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )

    class Meta:
        model = SuketIzinLab
        fields = [
            'no_surat',
            'lab',
            'waktu_mulai',
            'waktu_selesai',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '*kosongkan jika ambil nomor dari sistem'
            }),
            'lab': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'contoh : Laboratorium Biologi Dasar, Laboratorium Microbiologi'
            }),
            'waktu_mulai': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'waktu_selesai': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'ttd_status': forms.Select(
                choices=[
                    ('QRcode', 'QRcode'),
                    ('Manual', 'Manual'),
                ],
                attrs={'class': 'form-control'}
            ),
            # 'ttd' dikustomisasi di luar Meta
        }


class formSuketRekomendasi(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now, jabatan__in=['Wakil Dekan II']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )

    class Meta:
        model = SuketRekomendasi
        fields = [
            'no_surat',
            'perihal',
            'alasan_rekomendasi',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '*kosongkan jika ambil nomor dari sistem'
            }),
            'perihal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'contoh : Untuk mengikuti program Beasiswa LAZ Hadji Kalla yang diselenggarakan oleh  Asnaf Gharimin'
            }),
            'alasan_rekomendasi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'contoh : karena mahasiswa tersebut tidak mampu dan tidak bisa mengikuti proses ujian skripsi bila belum melunasi seluru biaya UKT/SPP'
            }),
            'ttd_status': forms.Select(
                choices=[
                    ('QRcode', 'QRcode'),
                    ('Manual', 'Manual'),
                ],
                attrs={'class': 'form-control'}
            ),
            # 'ttd' dikustomisasi di luar Meta
        }



class formSuratTugas(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now, jabatan__in=['Dekan','Wakil Dekan II']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )

    class Meta:
        model = SuratTugas
        fields = [
            'no_surat',
            'nama_kegiatan',
            'tgl_mulai',
            'tgl_selesai',
            'jam',
            'tempat',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*Kosongkan jika dari sistem'}),
            'nama_kegiatan': forms.TextInput(attrs={'class': 'form-control'}),
            'tgl_mulai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tgl_selesai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'jam': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'tempat': forms.TextInput(attrs={'class': 'form-control'}),
            'ttd_status': forms.Select(
                choices=[('QRcode', 'QRcode'), ('Manual', 'Manual')],
                attrs={'class': 'form-control'}
            ),
        }

class formSuratTugas_NamaDosen(forms.ModelForm):
    class Meta:
        model = SuratTugas_NamaDosen
        fields = ['dosen', 'jabatan']
        widgets = {
            'dosen': forms.Select(attrs={'class': 'form-control'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Dosen'}),
        }

class formSuratTugas_NamaMhs(forms.ModelForm):
    class Meta:
        model = SuratTugas_NamaMhs
        fields = ['mhs', 'jabatan']
        widgets = {
            'mhs': forms.Select(attrs={'class': 'form-control'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Mahasiswa'}),
        }


class formSuketBerkelakuanBaik(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now, jabatan__in=['Wakil Dekan III']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )

    class Meta:
        model = SuketBerkelakuanBaik
        fields = [
            'no_surat',
            'semester',
            'tahun_akademik',
            'tujuan',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '*kosongkan jika ambil nomor dari sistem'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: II / Dua'
            }),
            'tahun_akademik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 2024/2025 Genap'
            }),
            'tujuan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Misal: Untuk Keperluan Ujian Tutup'
            }),
            'ttd_status': forms.Select(
                choices=[
                    ('QRcode', 'QRcode'),
                    ('Manual', 'Manual'),
                ],
                attrs={'class': 'form-control'}
            ),
            # 'ttd' dikustomisasi di luar Meta
        }

class formSuketCutiAkademik(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now, jabatan__in=['Dekan']),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )
    class Meta:
        model = SuketCutiAkademik
        fields = [
            'no_surat',
            'alasan',
            'terakhir_terdaftar',
            'cuti_semester',
            'terhitung_cuti',
            'tahun_akademik',
            'kembali_aktif',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '*kosongkan jika ambil nomor dari sistem'
            }),
            'alasan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Cuti Akademik'
            }),
            'terakhir_terdaftar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Semester II / Dua'
            }),
            'cuti_semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: II / Dua'
            }),
            'terhitung_cuti': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh:  Mulai bulan Januari 2025 s/d Agustus 2025.'
            }),
            'tahun_akademik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 2024/2025 Genap'
            }),
            'kembali_aktif': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh:  Semester III Tahun Akademik 2024/2025'
            }),
            'ttd_status': forms.Select(
                choices=[
                    ('QRcode', 'QRcode'),
                    ('Manual', 'Manual'),
                ],
                attrs={'class': 'form-control'}
            ),
            # 'ttd' dikustomisasi di luar Meta
        }