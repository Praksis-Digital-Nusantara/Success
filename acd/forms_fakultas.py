from django import forms
from .models import Prodi, Pejabat
from .models import UserFakultas, UserDosen
from .models import NoSuratFakultas, KodeSurat
from .models import Ujian
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



class formPejabatEdit(forms.ModelForm):
    class Meta:
        model = Pejabat
        fields = [
            'jabatan', 
            'prodi',  
            'pejabat', 
            'tgl_mulai', 
            'tgl_selesai', 
            'label', 
            'plt', 
        ]
        widgets = {
            'jabatan': forms.Select(attrs={'class': 'form-control'}),
            'prodi': forms.Select(attrs={'class': 'form-control'}),
            'pejabat': forms.Select(attrs={'class': 'form-control'}),
            'tgl_mulai': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'tgl_selesai': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'plt': forms.NullBooleanSelect(attrs={'class': 'form-control'}),

        }
        labels = {
            'jabatan': 'Jabatan',
            'nama_prodi': 'Nama Program Studi',
            'pejabat': 'Nama Pejabat',
            'tgl_mulai': 'Tanggal Mulai',
            'tgl_selesai': 'Tanggal Selesai',
            'label': 'Label Jabatan',
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


