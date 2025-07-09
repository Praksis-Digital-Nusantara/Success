from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from uuid import UUID

from . import views
from . import views_fakultas
from . import views_prodi
from . import views_prodi_set
from . import views_mhs
from .view_print import print_pengajuanjudul
from . import views_dosen
from .view_print import (print_skpbb, 
                        print_pengesahan,
                        print_undangan,
                        print_penelitian,
                        print_suket
                        )


urlpatterns = [

    ###### ADMIN FAKULTAS ######   
    path('profile_fakultas', views_fakultas.profile_fakultas, name='profile_fakultas'),
    path('nosurat_fakultas', views_fakultas.nosurat_fakultas, name='nosurat_fakultas'),    
    path('nosurat_fakultas_del', views_fakultas.nosurat_fakultas_del, name='nosurat_fakultas_del'),    
    path('skpbb_pengajuan', views_fakultas.skpbb_pengajuan, name='skpbb_pengajuan'),    
    path('skpbb_list', views_fakultas.skpbb_list, name='skpbb_list'),    
    path('izinpenelitian_pengajuan', views_fakultas.izinpenelitian_pengajuan, name='izinpenelitian_pengajuan'),    
    path('izinpenelitian_list', views_fakultas.izinpenelitian_list, name='izinpenelitian_list'),    
    path('ujian_list/<str:filter>', views_fakultas.ujian_list, name='ujian_list'),    
    path('ujian_proses/<str:id>', views_fakultas.ujian_proses, name='ujian_proses'),     
    path('layanan_fakultas/<str:filter>', views_fakultas.layanan_fakultas, name='layanan_fakultas'), # saya tambahkan filter untuk layanan fakultas - ndx


    ###### ADMIN PRODI ######   
    path('notif_prodi', views_prodi.notif_prodi, name='notif_prodi'),
    path('profile_prodi', views_prodi_set.profile_prodi, name='profile_prodi'),
    path('user_list', views_prodi_set.user_list, name='user_list'),      
    path('user_edit/<str:id>/<str:role>/', views_prodi_set.user_edit, name='user_edit'),
    path('nosurat', views_prodi.nosurat, name='nosurat'),      
    path('nosurat_del', views_prodi.nosurat_del, name='nosurat_del'),      
    path('ttd', views_prodi.ttd, name='ttd'),      
    path('ttd_edit/<str:id>', views_prodi.ttd_edit, name='ttd_edit'),         
    path('ttd_del/<str:id>', views_prodi.ttd_del, name='ttd_del'),         
    path('layanan/<str:filter>', views_prodi.layanan, name='layanan'),  
    path('layanan_edit/<uuid:id>/<str:filter>', views_prodi.layanan_edit, name='layanan_edit'),  
    path('skripsi_sjudul', views_prodi.skripsi_sjudul, name='skripsi_sjudul'),      
    path('skripsi_djudul', views_prodi.skripsi_djudul, name='skripsi_djudul'),      
    path('skripsi_ejudul/<str:nim>/', views_prodi.skripsi_ejudul, name='skripsi_ejudul'),     
    path('proposal', views_prodi.proposal, name='proposal'),   
    path('proposal_edit/<str:nim>', views_prodi.proposal_edit, name='proposal_edit'),   
    path('hasil', views_prodi.hasil, name='hasil'),   
    path('hasil_edit/<str:nim>', views_prodi.hasil_edit, name='hasil_edit'),   
    path('ujian', views_prodi.ujian, name='ujian'),   
    path('ujian_edit/<str:nim>', views_prodi.ujian_edit, name='ujian_edit'),   
    path('suket_bebaskuliah', views_prodi.suket_bebaskuliah, name='suket_bebaskuliah'),   
    path('suket_bebaskuliah_edit/<str:nim>', views_prodi.suket_bebaskuliah_edit, name='suket_bebaskuliah_edit'),   
    path('suket_bebaskuliah_del/<str:id>', views_prodi.suket_bebaskuliah_del, name='suket_bebaskuliah_del'),   
    path('suket_bebasplagiasi', views_prodi.suket_bebasplagiasi, name='suket_bebasplagiasi'),   
    path('suket_bebasplagiasi_edit/<str:nim>', views_prodi.suket_bebasplagiasi_edit, name='suket_bebasplagiasi_edit'),   
    path('suket_bebasplagiasi_del/<str:id>', views_prodi.suket_bebasplagiasi_del, name='suket_bebasplagiasi_del'),   



    ###### MAHASISWA ######
    path('profile_mhs', views_mhs.profile_mhs, name='profile_mhs'),     
    path('layanan_me', views_mhs.layananMe, name='layanan_me'),  
    path('layanan_add', views_mhs.layananAdd, name='layanan_add'),
    path('get-prasyarat-layanan/', views_mhs.get_prasyarat_layanan, name='get_prasyarat_layanan'),
    path('skripsi', views_mhs.skripsi, name='skripsi'),
    path('proposal_reg', views_mhs.proposal_reg, name='proposal_reg'),
    path('proposal_reg_up', views_mhs.proposal_reg_up, name='proposal_reg_up'),
    path('ujian_reg', views_mhs.ujian_reg, name='ujian_reg'),
    path('ujian_reg_up', views_mhs.ujian_reg_up, name='ujian_reg_up'),
    path('skripsi_pjudul', views_mhs.skripsi_pjudul, name='skripsi_pjudul'),
    path('print_pengajuanjudul/', print_pengajuanjudul.print_pengajuanjudul, name='print_pengajuanjudul'),


    ###### DOSEN ######   
    path('profile_dosen', views_dosen.profile_dosen, name='profile_dosen'),
    path('judul_seleksi', views_dosen.judul_seleksi, name='judul_seleksi'),
    path('pbb2_persetujuan', views_dosen.pbb2_persetujuan, name='pbb2_persetujuan'),
    path('proposal_dsn/<str:filter>', views_dosen.proposal_dsn, name='proposal_dsn'),
    path('proposal_dsn_nilai/<str:id>', views_dosen.proposal_dsn_nilai, name='proposal_dsn_nilai'),
    path('hasil_dsn/<str:filter>', views_dosen.hasil_dsn, name='hasil_dsn'),
    path('hasil_dsn_nilai/<str:id>', views_dosen.hasil_dsn_nilai, name='hasil_dsn_nilai'),
    path('ujian_dsn/<str:filter>', views_dosen.ujian_dsn, name='ujian_dsn'),
    path('ujian_dsn_nilai/<str:id>', views_dosen.ujian_dsn_nilai, name='ujian_dsn_nilai'),
    path('judul_seleksi_detail/<uuid:id>', views_dosen.judul_seleksi_detail, name='judul_seleksi_detail'),

    ###### PRINT ######   
    path('print_skpbb/<uuid:id>', print_skpbb.print_skpbb, name='print_skpbb'),
    path('print_pengesahan/<str:jn>/<uuid:id>', print_pengesahan.print_pengesahan, name='print_pengesahan'),
    path('print_undangan/<str:jn>/<uuid:id>', print_undangan.print_undangan, name='print_undangan'),
    path('print_undangan_ujian/<uuid:id>', print_undangan.print_undangan_ujian, name='print_undangan_ujian'),
    path('print_persetujuan_penelitian/<uuid:id>', print_pengesahan.print_persetujuan_penelitian, name='print_persetujuan_penelitian'),
    path('print_izinpenelitian/<uuid:id>', print_penelitian.print_izinpenelitian, name='print_izinpenelitian'),
    path('print_suket_bebaskuliah/<uuid:id>', print_suket.print_suket_bebaskuliah, name='print_suket_bebaskuliah'),
    path('print_suket_bebasplagiasi/<uuid:id>', print_suket.print_suket_bebasplagiasi, name='print_suket_bebasplagiasi'),


    ###### ALL ######
    path('changepass', views.changepass, name='changepass'),     
    path('dashboard', views.index, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),      
    path('', views.index, name='index'),      

    
]
