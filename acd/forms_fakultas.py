from django import forms
from .models import Prodi, ProdiPejabat
from .models import UserFakultas
from django.contrib.auth.models import User

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



class formProdiPejabatEdit(forms.ModelForm):
    class Meta:
        model = ProdiPejabat
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
            'tgl_mulai': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'tgl_selesai': forms.SelectDateWidget(attrs={'class': 'form-control'}),
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


