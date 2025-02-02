from django import forms
from django.contrib.auth.models import User

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


