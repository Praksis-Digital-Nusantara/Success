import os
from django.conf import settings


# myapp/context_processors.py
def web_name(request):
    return {
        'baseurl': 'http://127.0.0.1:8000/',
        'web_name': 'FEB - One Click Universal Service',
        'webname': 'E-SUCCESS',
        'ministry_name': 'Kementerian Pendidikan Tinggi, Sains dan Teknologi',
        'university_name': 'Universitas Negeri Makassar',
        'faculty_name': 'Fakultas Ekonomi dan Bisnis',
        'faculty_short_name': 'FEB',
        'address': 'Gedung Laboratorium Terpadu Padhang-Padhang, Sulawesi Barat',
        'address_ttd': 'Majene',
        'telp': '(0422) 22559',
        'fax': '(0422) 22559',
        'website': 'http://feb.unm.ac.id/',
        'email': 'fe@unm.ac.id',
        'api_qrcode' : 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=',
    }

# Izin adding versi static kak, (proble browsing chace css)
def versioned_static(request):
    version = 'v1.0.4d'  # You can update this version number when needed
    return {
        'STATIC_VERSION': version,
    }

