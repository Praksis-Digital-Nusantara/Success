import os
from django.conf import settings


# myapp/context_processors.py
def web_name(request):
    return {
        'web_name': 'Sistem Informasi Fakultas Ekonomi dan Bisnis UNM',
        'webname': 'SUCCESS'
    }

# Izin adding versi static kak, (proble browsing chace css)
def versioned_static(request):
    version = 'v1.0.0'  # You can update this version number when needed
    return {
        'STATIC_VERSION': version,
    }

