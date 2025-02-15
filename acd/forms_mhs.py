from django import forms
from .models import Layanan
from .models import LayananJenis
from .models import UserMhs
from .models import SkripsiJudul
from django.contrib.auth.models import User

class formProfile(forms.ModelForm):
    penasehat_akademik = forms.ModelChoiceField(
        queryset=User.objects.filter(last_name="Dosen"),  # Query only users who are staff (penasehat akademik)
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Penasehat Akademik"  # Optional placeholder text
        )
    
    class Meta:     
        model = UserMhs
        fields = [   
            'telp',
            'gender',
            'photo',
            'tempat_lahir',
            'tgl_lahir',
            'penasehat_akademik',
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
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'tgl_lahir': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'penasehat_akademik': forms.Select(attrs={'class': 'form-control'}),  
        }

        



class formAddLayanan(forms.ModelForm):
    class Meta:
        model = Layanan
        exclude = ['status','nama', 'nim','prodi',] 
        fields = [    
            'layanan_jenis',
            'layanan_isi',
            'layanan_file',
        ]
        widgets = {
            'layanan_isi': forms.Textarea(attrs={'class': 'form-control','rows': 4, 'placeholder': 'Deskripsikan layanan Anda...'}),
            'layanan_jenis': forms.TextInput(attrs={'class': 'form-control'}),
            'layanan_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'layanan_jenis': 'Jenis Layanan',
            'layanan_isi': 'Isi Layanan',
            'layanan_file': 'File Pendukung',
        }

        # Override layanan_jenis dengan ChoiceField
    layanan_jenis = forms.ModelChoiceField(
        queryset=LayananJenis.objects.all(),
        empty_label="Pilih Jenis Layanan",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Jenis Layanan"
    )



class formSkripsiJudul(forms.ModelForm):
    class Meta:
        model = SkripsiJudul
        fields = [
            'judul_1', 
            'deskripsi_judul_1', 
            'judul_2', 
            'deskripsi_judul_2', 
            'judul_3', 
            'deskripsi_judul_3'
        ]
        widgets = {
            'judul_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul 1'}),
            'deskripsi_judul_1': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Masukkan Deskripsi Judul 1', 'rows': 3}),
            'judul_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul 2'}),
            'deskripsi_judul_2': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Masukkan Deskripsi Judul 2', 'rows': 3}),
            'judul_3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul 3'}),
            'deskripsi_judul_3': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Masukkan Deskripsi Judul 3', 'rows': 3}),
            
        }
        labels = {
            'judul_1': 'Judul 1',
            'deskripsi_judul_1': 'Deskripsi Judul 1',
            'judul_2': 'Judul 2',
            'deskripsi_judul_2': 'Deskripsi Judul 2',
            'judul_3': 'Judul 3',
            'deskripsi_judul_3': 'Deskripsi Judul 3',
        }


    

