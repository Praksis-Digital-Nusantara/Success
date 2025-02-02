from django import forms
from .models import Layanan
from .models import LayananJenis
from .models import UserDosen
from .models import SkripsiJudul
from django.contrib.auth.models import User

class formProfile(forms.ModelForm):
    class Meta:
        model = UserDosen
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


