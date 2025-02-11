import os
from django.conf import settings


# myapp/context_processors.py
def web_name(request):
    return {
        'web_name': 'Sistem Informasi Fakultas Ekonomi dan Bisnis UNM',
        'webname': 'SUCCESS',
        'ministry_name': 'Kementerian Pendidikan Tinggi, Sains dan Teknologi',
        'university_name': 'Universitas Negeri Makassar  (UNM)',
        'faculty_name': 'Fakultas Ekonomi dan Bisnis',
    }

# Izin adding versi static kak, (proble browsing chace css)
def versioned_static(request):
    version = 'v1.0.3'  # You can update this version number when needed
    return {
        'STATIC_VERSION': version,
    }

