from django import forms
from .models import Layanan, UserProdi, Prodi, NoSurat, TTDProdi, User, SkripsiJudul

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
        queryset=User.objects.filter(last_name="Dosen"), 
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
        queryset=User.objects.filter(last_name="Dosen"), 
        to_field_name="username",  # Tambahkan ini
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    pembimbing2 = forms.ModelChoiceField(
        queryset=User.objects.filter(last_name="Dosen"), 
        to_field_name="username",  # Tambahkan ini
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

