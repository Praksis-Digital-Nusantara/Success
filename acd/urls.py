from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from uuid import UUID

from . import views
from . import views_fakultas
from . import views_fakultas_suket
from . import views_prodi
from . import views_prodi_set
from . import views_mhs
from .view_print import print_pengajuanjudul
from . import views_dosen
from .view_print import (print_skpbb, 
                        print_skpgj,
                        print_pengesahan,
                        print_undangan,
                        print_penelitian,
                        print_yudisium,
                        print_yudisium_nilai,
                        print_suket_aktifkuliah,
                        print_suket_bebaskuliah,
                        print_suket_bebasplagiasi,
                        print_suket_izinobservasi,
                        print_suket_rekomendasi,
                        print_suket_izinlab,
                        print_surat_tugas,
                        print_suket_berkelakuanbaik,
                        print_suket_cutiakademik
                        )


urlpatterns = [

    ###### ADMIN FAKULTAS ######   
    path('profile_fakultas', views_fakultas.profile_fakultas, name='profile_fakultas'),
    path('nosurat_fakultas', views_fakultas.nosurat_fakultas, name='nosurat_fakultas'),    
    path('nosurat_fakultas_del', views_fakultas.nosurat_fakultas_del, name='nosurat_fakultas_del'),    
    path('skpbb_pengajuan', views_fakultas.skpbb_pengajuan, name='skpbb_pengajuan'),    
    path('skpbb_list', views_fakultas.skpbb_list, name='skpbb_list'),    
    path('skpgj_pengajuan', views_fakultas.skpgj_pengajuan, name='skpgj_pengajuan'),    
    path('skpgj_list', views_fakultas.skpgj_list, name='skpgj_list'),    
    path('izinpenelitian_pengajuan', views_fakultas.izinpenelitian_pengajuan, name='izinpenelitian_pengajuan'),    
    path('izinpenelitian_list', views_fakultas.izinpenelitian_list, name='izinpenelitian_list'),    
    path('ujian_list/<str:filter>', views_fakultas.ujian_list, name='ujian_list'),    
    path('ujian_proses/<str:id>', views_fakultas.ujian_proses, name='ujian_proses'),     
    path('ujian_yudisium/<str:id>', views_fakultas.ujian_yudisium, name='ujian_yudisium'),     
    path('layanan_fakultas/<str:filter>', views_fakultas.layanan_fakultas, name='layanan_fakultas'),
    path('layanan_fakultas_edit/<uuid:id>/<str:filter>', views_fakultas.layanan_fakultas_edit, name='layanan_fakultas_edit'), 
    path('suket_aktifkuliah', views_fakultas_suket.suket_aktifkuliah, name='suket_aktifkuliah'),   
    path('suket_aktifkuliah_edit/<str:nim>', views_fakultas_suket.suket_aktifkuliah_edit, name='suket_aktifkuliah_edit'),   
    path('suket_aktifkuliah_del/<str:id>', views_fakultas_suket.suket_aktifkuliah_del, name='suket_aktifkuliah_del'), 
    path('suket_izinobservasi', views_fakultas_suket.suket_izinobservasi, name='suket_izinobservasi'),   
    path('suket_izinobservasi_edit/<str:nim>', views_fakultas_suket.suket_izinobservasi_edit, name='suket_izinobservasi_edit'),   
    path('suket_izinobservasi_del/<str:id>', views_fakultas_suket.suket_izinobservasi_del, name='suket_izinobservasi_del'), 
    path('suket_izinlab', views_fakultas_suket.suket_izinlab, name='suket_izinlab'),   
    path('suket_izinlab_edit/<str:nim>', views_fakultas_suket.suket_izinlab_edit, name='suket_izinlab_edit'),   
    path('suket_izinlab_del/<str:id>', views_fakultas_suket.suket_izinlab_del, name='suket_izinlab_del'), 
    path('suket_rekomendasi', views_fakultas_suket.suket_rekomendasi, name='suket_rekomendasi'),   
    path('suket_rekomendasi_edit/<str:nim>', views_fakultas_suket.suket_rekomendasi_edit, name='suket_rekomendasi_edit'),   
    path('suket_rekomendasi_del/<str:id>', views_fakultas_suket.suket_rekomendasi_del, name='suket_rekomendasi_del'), 
    path('surat_tugas', views_fakultas_suket.surat_tugas, name='surat_tugas'),   
    path('surat_tugas_edit/<str:id>', views_fakultas_suket.surat_tugas_edit, name='surat_tugas_edit'),   
    path('surat_tugas_del/<str:id>', views_fakultas_suket.surat_tugas_del, name='surat_tugas_del'), 
    path('surat_tugas_delnamadosen/<str:id>/<str:surat>', views_fakultas_suket.surat_tugas_delnamadosen, name='surat_tugas_delnamadosen'), 
    path('surat_tugas_delnamamhs/<str:id>/<str:surat>', views_fakultas_suket.surat_tugas_delnamamhs, name='surat_tugas_delnamamhs'), 
    path('suket_berkelakuanbaik', views_fakultas_suket.suket_berkelakuanbaik, name='suket_berkelakuanbaik'),  
    path('suket_berkelakuanbaik_edit/<str:nim>', views_fakultas_suket.suket_berkelakuanbaik_edit, name='suket_berkelakuanbaik_edit'),  
    path('suket_berkelakuanbaik_del/<str:id>', views_fakultas_suket.suket_berkelakuanbaik_del, name='suket_berkelakuanbaik_del'), 
    path('suket_cutiakademik', views_fakultas_suket.suket_cutiakademik, name='suket_cutiakademik'),  
    path('suket_cutiakademik_edit/<str:nim>', views_fakultas_suket.suket_cutiakademik_edit, name='suket_cutiakademik_edit'),  
    path('suket_cutiakademik_del/<str:id>', views_fakultas_suket.suket_cutiakademik_del, name='suket_cutiakademik_del'), 

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
    path('proposal_nilai/<str:id>', views_prodi.proposal_nilai, name='proposal_nilai'),   
    path('proposal_del/<str:id>', views_prodi.proposal_del, name='proposal_del'),   
    path('hasil', views_prodi.hasil, name='hasil'),   
    path('hasil_edit/<str:nim>', views_prodi.hasil_edit, name='hasil_edit'),   
    path('hasil_nilai/<str:id>', views_prodi.hasil_nilai, name='hasil_nilai'),   
    path('ujian', views_prodi.ujian, name='ujian'),   
    path('ujian_edit/<str:nim>', views_prodi.ujian_edit, name='ujian_edit'),   
    path('ujian_nilai/<str:id>', views_prodi.ujian_nilai, name='ujian_nilai'),   
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
    path('hasil_reg', views_mhs.hasil_reg, name='hasil_reg'),
    path('hasil_reg_up', views_mhs.hasil_reg_up, name='hasil_reg_up'),
    path('ujian_reg', views_mhs.ujian_reg, name='ujian_reg'),
    path('ujian_reg_up', views_mhs.ujian_reg_up, name='ujian_reg_up'),
    path('skripsi_pjudul', views_mhs.skripsi_pjudul, name='skripsi_pjudul'),
    path('print_pengajuanjudul/', print_pengajuanjudul.print_pengajuanjudul, name='print_pengajuanjudul'),


    ###### DOSEN ######   
    path('profile_dosen', views_dosen.profile_dosen, name='profile_dosen'),
    path('judul_seleksi', views_dosen.judul_seleksi, name='judul_seleksi'),
    path('pbb2_persetujuan', views_dosen.pbb2_persetujuan, name='pbb2_persetujuan'),
    path('dsn_skpbb', views_dosen.dsn_skpbb, name='dsn_skpbb'),
    path('dsn_skpgj', views_dosen.dsn_skpgj, name='dsn_skpgj'),
    path('proposal_dsn/<str:filter>', views_dosen.proposal_dsn, name='proposal_dsn'),
    path('proposal_dsn_nilai/<str:id>', views_dosen.proposal_dsn_nilai, name='proposal_dsn_nilai'),
    path('hasil_dsn/<str:filter>', views_dosen.hasil_dsn, name='hasil_dsn'),
    path('hasil_dsn_nilai/<str:id>', views_dosen.hasil_dsn_nilai, name='hasil_dsn_nilai'),
    path('ujian_dsn/<str:filter>', views_dosen.ujian_dsn, name='ujian_dsn'),
    path('ujian_dsn_nilai/<str:id>', views_dosen.ujian_dsn_nilai, name='ujian_dsn_nilai'),
    path('judul_seleksi_detail/<uuid:id>', views_dosen.judul_seleksi_detail, name='judul_seleksi_detail'),
    path('list_ttd_pejabat', views_dosen.list_ttd_pejabat, name='list_ttd_pejabat'),
    path('kelola_ttd/<str:model_name>/<uuid:id>/<str:action>/',views_dosen.kelola_ttd,name='kelola_ttd'),
    ###### PRINT ######   
    path('print_skpbb/<uuid:id>', print_skpbb.print_skpbb, name='print_skpbb'),
    path('print_skpgj/<uuid:id>', print_skpgj.print_skpgj, name='print_skpgj'),
    path('print_pengesahan/<str:jn>/<uuid:id>', print_pengesahan.print_pengesahan, name='print_pengesahan'),
    path('print_undangan/<str:jn>/<uuid:id>', print_undangan.print_undangan, name='print_undangan'),
    path('print_undangan_ujian/<uuid:id>', print_undangan.print_undangan_ujian, name='print_undangan_ujian'),
    path('print_persetujuan_penelitian/<uuid:id>', print_pengesahan.print_persetujuan_penelitian, name='print_persetujuan_penelitian'),
    path('print_izinpenelitian/<uuid:id>', print_penelitian.print_izinpenelitian, name='print_izinpenelitian'),
    path('print_permohonan_penerbitan_sip/<uuid:id>', print_pengesahan.print_permohonan_penerbitan_sip, name='print_permohonan_penerbitan_sip'),
    path('print_suket_bebaskuliah/<uuid:id>', print_suket_bebaskuliah.print_suket_bebaskuliah, name='print_suket_bebaskuliah'),
    path('print_suket_bebasplagiasi/<uuid:id>', print_suket_bebasplagiasi.print_suket_bebasplagiasi, name='print_suket_bebasplagiasi'),
    path('print_suket_aktifkuliah/<uuid:id>', print_suket_aktifkuliah.print_suket_aktifkuliah, name='print_suket_aktifkuliah'),
    path('print_suket_izinobservasi/<uuid:id>', print_suket_izinobservasi.print_suket_izinobservasi, name='print_suket_izinobservasi'),
    path('print_suket_izinlab/<uuid:id>', print_suket_izinlab.print_suket_izinlab, name='print_suket_izinlab'),
    path('print_suket_rekomendasi/<uuid:id>', print_suket_rekomendasi.print_suket_rekomendasi, name='print_suket_rekomendasi'),
    path('print_yudisium/<uuid:id>', print_yudisium.print_yudisium, name='print_yudisium'),
    path('print_yudisium_nilai/<uuid:id>', print_yudisium_nilai.print_yudisium_nilai, name='print_yudisium_nilai'),
    path('print_surat_tugas/<uuid:id>', print_surat_tugas.print_surat_tugas, name='print_surat_tugas'),
    path('print_suket_berkelakuanbaik/<uuid:id>', print_suket_berkelakuanbaik.print_suket_berkelakuanbaik, name='print_suket_berkelakuanbaik'),
    path('print_suket_cutiakademik/<uuid:id>', print_suket_cutiakademik.print_suket_cutiakademik, name='print_suket_cutiakademik'),

    ###### ALL ######
    path('changepass', views.changepass, name='changepass'),     
    path('changerole', views.changerole, name='changerole'),     
    path('dashboard', views.index, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),      
    path('', views.index, name='index'),      

    
]
