from django import forms
from django.utils import timezone

tgl_now = timezone.now()

from .models import (Layanan, 
                     User, 
                     UserProdi, 
                     UserDosen, 
                     Prodi, 
                     NoSurat, 
                     TTDProdi, 
                     SkripsiJudul,
                     Proposal,
                     Hasil,
                     Ujian,
                     Pejabat,
                     SuketBebasKuliah,
                     SuketBebasPlagiasi
                    )

class formProfile(forms.ModelForm):
    class Meta:
        model = UserProdi
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


class formNosuratAdd(forms.ModelForm):
    class Meta:
        model = NoSurat
        fields = [    
            'perihal',
            'tujuan',
        ]
        widgets = {
            'perihal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh : Undangan Rapat'}),
            'tujuan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh : Seluruh Dosen Prodi'}),
        }
        labels = {
            'perihal': 'Perihal',
            'tujuan': 'Tujuan',
        }

class formTTD(forms.ModelForm):
    ttd_user = forms.ModelChoiceField(
        queryset=UserDosen.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"  # Optional placeholder text
        )
    
    class Meta:
        model = TTDProdi      
        fields = [    
            'perihal',
            'tujuan',
            'ttd_jabatan',
            'ttd_user',
        ]
        widgets = {
            'perihal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh : Undangan Rapat'}),
            'tujuan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh : Seluruh Dosen Prodi'}),
            'ttd_jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh : Ketua Jurusan'}),
        }
        labels = {
            'perihal': 'Perihal',
            'tujuan': 'Tujuan',
            'ttd_jabatan': 'Nama Jabatan',
        }

        
class formUserEdit(forms.ModelForm):
    class Meta:
        model = UserProdi
        fields = [
            'prodi',
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

    # Form field for 'prodi' using ModelChoiceField
    prodi = forms.ModelChoiceField(
        queryset=Prodi.objects.all(),  # This gets the available 'Prodi' options
        empty_label="Pilih Prodi",  # This is the placeholder option in the dropdown
        widget=forms.Select(attrs={'class': 'form-control'}),  # Using the same form-control class for consistency
        label="Program Studi"
    )



class formLayananEdit(forms.ModelForm):
    class Meta:
        model = Layanan
        fields = [    
            'status',
            'adminp',
            'hasil_test',
            'hasil_file',
            'hasil_link',
        ]
        widgets = {
            'status': forms.Select(
                choices=[
                    ('Waiting', 'Waiting'),
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



class formSkripsiJudulEdit(forms.ModelForm):
    pembimbing1 = forms.ModelChoiceField(
        queryset=UserDosen.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    pembimbing2 = forms.ModelChoiceField(
        queryset=UserDosen.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SkripsiJudul
        fields = [    
            'judul',
            'pembimbing1',
            'pembimbing2',
        ]
        widgets = {
            'judul': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '...'}),
        }



class formProposal(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )
    penguji1 = forms.ModelChoiceField(
        queryset=UserDosen.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Dosen"
    )
    
    class Meta:
        model = Proposal
        fields = [    
            'no_surat',
            'seminar_tgl',
            'seminar_jam',
            'seminar_tempat',
            'seminar_link',
            'penguji1',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*kosongkan jika ambil nomor dari sistem'}),
            'seminar_tgl': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'seminar_jam': forms.TimeInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'time'}),
            'seminar_tempat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zoom Meeting ID : 00000000 Passcode: xxxxx', 'required': 'required'}),
            'seminar_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'link zoom jika ada'}),
            'penguji1': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'ttd_status': forms.Select(
                                choices=[
                                    ('QRcode', 'QRcode'),
                                    ('Manual', 'Manual'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'ttd': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


class formHasil(forms.ModelForm):
    ttd = forms.ModelChoiceField(
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
        model = Hasil
        fields = [    
            'no_surat',
            'seminar_tgl',
            'seminar_jam',
            'seminar_tempat',
            'seminar_link',
            'penguji1',
            'penguji2',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*kosongkan jika ambil nomor dari sistem'}),
            'seminar_tgl': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'seminar_jam': forms.TimeInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'time'}),
            'seminar_tempat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zoom Meeting ID : 00000000 Passcode: xxxxx', 'required': 'required'}),
            'seminar_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'link zoom jika ada'}),
            'penguji1': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'penguji2': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'ttd_status': forms.Select(
                                choices=[
                                    ('QRcode', 'QRcode'),
                                    ('Manual', 'Manual'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'ttd': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


class formUjian(forms.ModelForm):
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
            'ujian_tgl',
            'ujian_jam',
            'ujian_tempat',
            'ujian_link',
            'penguji1',
            'penguji2',
        ]
        widgets = {
            'ujian_tgl': forms.DateInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'date'}),
            'ujian_jam': forms.TimeInput(attrs={'class': 'form-control', 'required': 'required', 'type': 'time'}),
            'ujian_tempat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zoom Meeting ID : 00000000 Passcode: xxxxx', 'required': 'required'}),
            'ujian_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'link zoom jika ada'}),
            'penguji1': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'penguji2': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


class formSuketBebasKuliah(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )
    
    class Meta:
        model = SuketBebasKuliah
        fields = [    
            'no_surat',
            'sks_lulus',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*kosongkan jika ambil nomor dari sistem'}),
            'sks_lulus': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'ttd_status': forms.Select(
                                choices=[
                                    ('QRcode', 'QRcode'),
                                    ('Manual', 'Manual'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'ttd': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }



class formSuketBebasPlagiasi(forms.ModelForm):
    ttd = forms.ModelChoiceField(
        queryset=Pejabat.objects.filter(tgl_selesai__gte=tgl_now),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Pejabat"
    )
    
    class Meta:
        model = SuketBebasPlagiasi
        fields = [    
            'no_surat',
            'nilai_plagiasi',
            'ttd_status',
            'ttd',
        ]
        widgets = {
            'no_surat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '*kosongkan jika ambil nomor dari sistem'}),
            'nilai_plagiasi': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'ttd_status': forms.Select(
                                choices=[
                                    ('QRcode', 'QRcode'),
                                    ('Manual', 'Manual'),
                                ],
                                attrs={'class': 'form-control'}
                            ),
            'ttd': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        }

