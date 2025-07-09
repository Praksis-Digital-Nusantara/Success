from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Layanan
from .models import LayananJenis
from .models import UserDosen
from .models import ProposalNilai, HasilNilai, UjianNilai
from .models import chatPA
from django.contrib.auth.models import User

class formProfile(forms.ModelForm):
    class Meta:
        model = UserDosen
        fields = [   
            'telp',
            'gender',
            'photo',
            'status_kepegawaian',
            'tempat_lahir',
            'tgl_lahir',
            'nidn',
            'pangkat',
            'golongan',
            'jafung',
            'bidang_keahlian',
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
            'status_kepegawaian': forms.Select(
                                choices=[
                                    ('PNS', 'PNS'),
                                    ('CPNS', 'CPNS'),
                                    ('PPPK', 'PPPK'),
                                    ('NON-ASN', 'NON-ASN'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'tgl_lahir': forms.DateInput(attrs={'class': 'form-control'}),
            'nidn': forms.TextInput(attrs={'class': 'form-control'}),
            'pangkat': forms.Select(
                                choices=[
                                    ('Penata Muda Tingkat I', 'Penata Muda Tingkat I'),
                                    ('Penata', 'Penata'),
                                    ('Penata Tingkat I', 'Penata Tingkat I'),
                                    ('Pembina', 'Pembina'),
                                    ('Pembina Utama Muda', 'Pembina Utama Muda'),
                                    ('Pembina Utama Madya', 'Pembina Utama Madya'),
                                    ('Pembina Utama', 'Pembina Utama'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'golongan': forms.Select(
                                choices=[
                                    ('III/b', 'III/b'),
                                    ('III/c', 'III/c'),
                                    ('III/d', 'III/d'),
                                    ('IV/a', 'IV/a'),
                                    ('IV/b', 'IV/b'),
                                    ('IV/c', 'IV/c'),
                                    ('IV/d', 'IV/d'),
                                    ('IV/e', 'IV/e'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'jafung': forms.Select(
                                choices=[
                                    ('Asisten Ahli', 'Asisten Ahli'),
                                    ('Lektor', 'Lektor'),
                                    ('Lektor Kepala', 'Lektor Kepala'),
                                    ('Guru Besar', 'Guru Besar'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'bidang_keahlian': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

class formChatPA(forms.ModelForm):
    class Meta:
        model = chatPA
        fields = [
            'message', 
        ]
        widgets = {
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tulis Pesan ke PA ...'}),
        }

class formProposalNilai(forms.ModelForm):
    class Meta:
        model = ProposalNilai
        fields = ['aspek1', 'aspek2', 'aspek3', 'aspek4', 'aspek5', 'aspek6', 'komentar']
        widgets = {
            'aspek1': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek2': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek3': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek4': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek5': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek6': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'komentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Berikan komentar kepada mahasiswa'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for aspek in ['aspek1', 'aspek2', 'aspek3', 'aspek4', 'aspek5', 'aspek6']:
            nilai = cleaned_data.get(aspek)
            if nilai is None:
                self.add_error(aspek, "Nilai wajib diisi.")
            elif not (0 <= nilai <= 100):
                self.add_error(aspek, "Nilai harus antara 0 dan 100.")




class formHasilNilai(forms.ModelForm):
    class Meta:
        model = HasilNilai
        fields = ['aspek1', 'aspek2', 'aspek3', 'aspek4', 'aspek5', 'aspek6', 'komentar']
        widgets = {
            'aspek1': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek2': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek3': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek4': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek5': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek6': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'komentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Berikan komentar kepada mahasiswa'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for aspek in ['aspek1', 'aspek2', 'aspek3', 'aspek4', 'aspek5', 'aspek6']:
            nilai = cleaned_data.get(aspek)
            if nilai is None:
                self.add_error(aspek, "Nilai wajib diisi.")
            elif not (0 <= nilai <= 100):
                self.add_error(aspek, "Nilai harus antara 0 dan 100.")



class formUjianNilai(forms.ModelForm):
    class Meta:
        model = UjianNilai
        fields = ['aspek1', 'aspek2', 'aspek3', 'aspek4', 'aspek5', 'aspek6', 'komentar']
        widgets = {
            'aspek1': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek2': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek3': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek4': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek5': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'aspek6': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'komentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Berikan komentar kepada mahasiswa'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for aspek in ['aspek1', 'aspek2', 'aspek3', 'aspek4', 'aspek5', 'aspek6']:
            nilai = cleaned_data.get(aspek)
            if nilai is None:
                self.add_error(aspek, "Nilai wajib diisi.")
            elif not (0 <= nilai <= 100):
                self.add_error(aspek, "Nilai harus antara 0 dan 100.")


