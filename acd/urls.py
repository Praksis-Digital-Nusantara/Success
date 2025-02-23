from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views
from . import views_fakultas
from . import views_prodi
from . import views_prodi_set
from . import views_mhs
from . import views_mhs_print
from . import views_dosen

urlpatterns = [

    ###### ADMIN FAKULTAS ######   
    path('profile_fakultas', views_fakultas.profile_fakultas, name='profile_fakultas'),
    path('prodi_list', views_fakultas.prodi_list, name='prodi_list'),    
    path('prodi_edit/<int:id>', views_fakultas.prodi_edit, name='prodi_edit'),    
    path('prodi_pejabat_list', views_fakultas.prodi_pejabat_list, name='prodi_pejabat_list'),    
    path('prodi_pejabat_edit/<int:id>', views_fakultas.prodi_pejabat_edit, name='prodi_pejabat_edit'),    


    ###### ADMIN PRODI ######   
    path('profile_prodi', views_prodi_set.profile_prodi, name='profile_prodi'),
    path('user_list', views_prodi_set.user_list, name='user_list'),      
    path('user_edit/<str:id>/<str:role>/', views_prodi_set.user_edit, name='user_edit'),
    path('layanan', views_prodi.layanan, name='layanan'),  
    path('layanan_edit/<int:id>/', views_prodi.layanan_edit, name='layanan_edit'),  
    path('skripsi_sjudul', views_prodi.skripsi_sjudul, name='skripsi_sjudul'),      
    path('skripsi_djudul', views_prodi.skripsi_djudul, name='skripsi_djudul'),      
    path('skripsi_ejudul/<int:id>/', views_prodi.skripsi_ejudul, name='skripsi_ejudul'),      
    path('nosurat', views_prodi.nosurat, name='nosurat'),      
    path('ttd', views_prodi.ttd, name='ttd'),      
    path('ttd_edit/<int:id>/', views_prodi.ttd_edit, name='ttd_edit'),      



    ###### MAHASISWA ######
    path('profile_mhs', views_mhs.profile_mhs, name='profile_mhs'),     
    path('layanan_me', views_mhs.layananMe, name='layanan_me'),  
    path('layanan_add', views_mhs.layananAdd, name='layanan_add'),
    path('get-prasyarat-layanan/', views_mhs.get_prasyarat_layanan, name='get_prasyarat_layanan'),
    path('skripsi', views_mhs.skripsi, name='skripsi'),
    path('skripsi_pjudul', views_mhs.skripsi_pjudul, name='skripsi_pjudul'),
    path('print_pengajuanjudul/', views_mhs_print.print_pengajuanjudul, name='print_pengajuanjudul'),


    ###### DOSEN ######   
    path('profile_dosen', views_dosen.profile_dosen, name='profile_dosen'),


    ###### ALL ######
    path('changepass', views.changepass, name='changepass'),     
    path('dashboard', views.index, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),      
    path('', views.index, name='index'),      

    
]
