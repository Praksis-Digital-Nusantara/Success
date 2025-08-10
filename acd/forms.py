from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Custom Password Change Form anto
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class RoleChangeForm(forms.Form):
    user_target = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Pilih Username"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Ambil user jika ada
        super().__init__(*args, **kwargs)

