from django import forms
from .models import Layanan
from .models import LayananJenis
from .models import UserMhs, UserDosen
from .models import SkripsiJudul, Proposal, Hasil, Ujian
from .models import chatPA
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from django.core.files.base import ContentFile

class formProfile(forms.ModelForm):
    penasehat_akademik = forms.ModelChoiceField(
        queryset=UserDosen.objects.all(),  # Query only users who are staff (penasehat akademik)
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
            'alamat',
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
            'alamat': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'tgl_lahir': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
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

    layanan_jenis = forms.ModelChoiceField(
        queryset=LayananJenis.objects.all().order_by('nama_layanan'),
        empty_label="Pilih Jenis Layanan",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Jenis Layanan"
    )

    # Perhatikan ini:
    def clean_layanan_file(self):
        file = self.cleaned_data.get('layanan_file')
        if file:
            ext = file.name.split('.')[-1].lower()
            if ext != 'pdf':
                raise forms.ValidationError('Hanya file PDF yang diperbolehkan.')
        return file




class formSkripsiJudul(forms.ModelForm):
    class Meta:
        model = SkripsiJudul
        fields = [
            'judul1', 
            'judul1_masalah', 
            'judul1_solusi', 
            'judul1_j1', 
            'judul1_j1l', 
            'judul1_j2', 
            'judul1_j2l', 
            'judul1_j3', 
            'judul1_j3l', 
            'judul2', 
            'judul2_masalah',
            'judul2_solusi', 
            'judul2_j1', 
            'judul2_j1l', 
            'judul2_j2', 
            'judul2_j2l', 
            'judul2_j3', 
            'judul2_j3l',  
            'judul3', 
            'judul3_masalah',
            'judul3_solusi', 
            'judul3_j1', 
            'judul3_j1l', 
            'judul3_j2', 
            'judul3_j2l', 
            'judul3_j3', 
            'judul3_j3l',             
        ]
        widgets = {
            'judul1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul 1', 'required': 'required'}),
            'judul1_masalah': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Permasalahan', 'rows': 12}),
            'judul1_solusi': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Solusi', 'rows': 12}),
            'judul1_j1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 1'}),
            'judul1_j1l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 1'}),
            'judul1_j2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 2'}),
            'judul1_j2l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 2'}),
            'judul1_j3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 3'}),
            'judul1_j3l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 3'}),

            'judul2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul 2', 'required': 'required'}),
            'judul2_masalah': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Permasalahan', 'rows': 12}),
            'judul2_solusi': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Solusi', 'rows': 12}),
            'judul2_j1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 1'}),
            'judul2_j1l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 1'}),
            'judul2_j2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 2'}),
            'judul2_j2l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 2'}),
            'judul2_j3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 3'}),
            'judul2_j3l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 3'}),

            'judul3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Judul 3', 'required': 'required'}),
            'judul3_masalah': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Permasalahan', 'rows': 12}),
            'judul3_solusi': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Solusi', 'rows': 12}),
            'judul3_j1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 1'}),
            'judul3_j1l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 1'}),
            'judul3_j2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 2'}),
            'judul3_j2l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 2'}),
            'judul3_j3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Jurnal 3'}),
            'judul3_j3l': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Jurnal 3'}),
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





class formProposalReg(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['krs', 'ksm', 'khs', 'persetujuan_proposal', 'kartu_seminar', 'konsultasi_skripsi']
        widgets = {
            'krs': forms.FileInput(attrs={'class': 'form-control'}),
            'ksm': forms.FileInput(attrs={'class': 'form-control'}),
            'khs': forms.FileInput(attrs={'class': 'form-control'}),
            'persetujuan_proposal': forms.FileInput(attrs={'class': 'form-control'}),
            'kartu_seminar': forms.FileInput(attrs={'class': 'form-control'}),
            'konsultasi_skripsi': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all fields to not required
        for field in self.fields.values():
            field.required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Cek jika instance sudah ada di database (update)
        if instance.pk:
            old_instance = Proposal.objects.get(pk=instance.pk)
            # Jika ada file baru diupload pada field krs
            if self.cleaned_data.get('krs') and old_instance.krs and old_instance.krs != self.cleaned_data['krs']:
                # Hapus file lama
                if old_instance.krs and hasattr(old_instance.krs, 'path') and os.path.isfile(old_instance.krs.path):
                    os.remove(old_instance.krs.path)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
 
class formHasilReg(forms.ModelForm):
    class Meta:
        model = Hasil
        fields = ['krs', 'ksm', 'kartu_kontrol_seminar', 'buku_konsultasi', 'persetujuan_hasil', 'transkrip', 'suket_selesai_meneliti']
        widgets = {
            'krs': forms.FileInput(attrs={'class': 'form-control'}),
            'ksm': forms.FileInput(attrs={'class': 'form-control'}),
            'kartu_kontrol_seminar': forms.FileInput(attrs={'class': 'form-control'}),
            'buku_konsultasi': forms.FileInput(attrs={'class': 'form-control'}),
            'persetujuan_hasil': forms.FileInput(attrs={'class': 'form-control'}),
            'transkrip': forms.FileInput(attrs={'class': 'form-control'}),
            'suket_selesai_meneliti': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all fields to not required
        for field in self.fields.values():
            field.required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Cek jika instance sudah ada di database (update)
        if instance.pk:
            old_instance = Hasil.objects.get(pk=instance.pk)
            # Jika ada file baru diupload pada field krs
            if self.cleaned_data.get('krs') and old_instance.krs and old_instance.krs != self.cleaned_data['krs']:
                # Hapus file lama
                if old_instance.krs and hasattr(old_instance.krs, 'path') and os.path.isfile(old_instance.krs.path):
                    os.remove(old_instance.krs.path)
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class formUjianReg(forms.ModelForm):
    class Meta:
        model = Ujian
        fields = ['persetujuan_ujian', 'transkrip', 'ijaza_terakhir', 'krs_berjalan', 'rekomendasi_akademik']
        widgets = {
            'persetujuan_ujian': forms.FileInput(attrs={'class': 'form-control'}),
            'transkrip': forms.FileInput(attrs={'class': 'form-control'}),
            'ijaza_terakhir': forms.FileInput(attrs={'class': 'form-control'}),
            'krs_berjalan': forms.FileInput(attrs={'class': 'form-control'}),
            'rekomendasi_akademik': forms.FileInput(attrs={'class': 'form-control'}),
        }
