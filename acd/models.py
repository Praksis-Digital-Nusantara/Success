from django.db import models
from django.contrib.auth.models import User

########################### TABEL USER MASTER #####################################
User.add_to_class("__str__", lambda self: f"{self.username} - {self.first_name}")


########################### JURUSAN #####################################



class Jurusan(models.Model):
    nama_jurusan = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(max_length=10, default='Aktif', choices=[
        ('Aktif', 'Aktif'),
        ('NonAktif', 'NonAktif'), 
        ])
    kode_surat = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nama_jurusan}"

class JurusanPejabat(models.Model):
    jabatan = models.CharField(max_length=15, choices=[
        ('Ketua', 'Ketua'),
        ('Sekretaris', 'Sekretaris'), 
        ])
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)
    pejabat = models.ForeignKey(User, on_delete=models.CASCADE)
    tgl_mulai = models.DateField(blank=False, null=False)
    tgl_selesai = models.DateField(blank=False, null=False)
    label = models.CharField(max_length=255, blank=True, null=True)
    plt = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.jurusan} - {self.pejabat}"


########################### PROGRAM STUDI #####################################

    
class Prodi(models.Model):
    strata = models.CharField(max_length=5, blank=False, null=False)
    nama_prodi = models.CharField(max_length=255, blank=False, null=False)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.SET_NULL, null=True, blank=True)
    gelar = models.CharField(max_length=10, blank=False, null=False)
    kode_mk = models.CharField(max_length=20, blank=False, null=False)
    nama_mk = models.CharField(max_length=50, blank=False, null=False)
    status = models.CharField(max_length=10, default='Aktif', choices=[
        ('Aktif', 'Aktif'),
        ('NonAktif', 'NonAktif'), 
        ])
    
    def __str__(self):
        return f"{self.nama_prodi} - {self.strata}"

    
class ProdiPejabat(models.Model):
    jabatan = models.CharField(max_length=15, choices=[
        ('Ketua', 'Ketua'), 
        ('Sekretaris', 'Sekretaris'), 
        ])
    prodi = models.ForeignKey(Prodi, on_delete=models.CASCADE)
    pejabat = models.ForeignKey(User, on_delete=models.CASCADE)
    tgl_mulai = models.DateField(blank=False, null=False)
    tgl_selesai = models.DateField(blank=False, null=False)
    label = models.CharField(max_length=255, blank=True, null=True)
    plt = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.prodi} - {self.pejabat}"
    

########################### MANAGE USERS #####################################


class UserMhs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    telp = models.CharField(max_length=15)
    photo = models.FileField(upload_to='static/img_profile/mhs/', null=True, blank=True)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    def __str__(self):
        return f"{self.user.username}"
    
class UserDosen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    telp = models.CharField(max_length=15)
    photo = models.FileField(upload_to='static/img_profile/dosen/', null=True, blank=True)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    def __str__(self):
        return f"{self.user.username}"
    
class UserProdi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    telp = models.CharField(max_length=15)
    photo = models.FileField(upload_to='static/img_profile/prodi/', null=True, blank=True)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    def __str__(self):
        return f"{self.user.username}"
    


class UserFakultas(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telp = models.CharField(max_length=15)
    photo = models.FileField(upload_to='static/img_profile/fakultas/', null=True, blank=True)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    def __str__(self):
        return f"{self.user.username}"
    


#########################  NOMOR SURAT #####################################

class NoSurat(models.Model):
    date_in = models.DateField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adminp_surat")
    jurusan = models.ForeignKey(Jurusan, on_delete=models.SET_NULL, null=True, blank=True)
    tahun = models.CharField(max_length=5, blank=False, null=False)
    # nomor = models.IntegerField(max_length=5, blank=False, null=False)
    nomor = models.CharField(max_length=10) #IZIN UBAH TYPEDATANYA, NDAK BISA JALAN DB SQLITE, SEMENTARA SAYA PAKAI DB SQLITE
    perihal = models.CharField(max_length=255, blank=False, null=False)
    tujuan = models.CharField(max_length=255, blank=False, null=False)


######################## LAYANAN ########################################
    
class LayananJenis(models.Model):
    nama_layanan = models.CharField(max_length=255)
    prasyarat_layanan = models.TextField()
    def __str__(self):
        return f"{self.nama_layanan}"
    
    
class Layanan(models.Model):
    date_in = models.DateTimeField(auto_now_add=True)
    mhs = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='layanan_mhs')
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    layanan_jenis = models.ForeignKey(LayananJenis, on_delete=models.SET_NULL, null=True, blank=True)
    layanan_isi = models.TextField()
    layanan_file = models.FileField(upload_to='static/layanan_files/', null=True, blank=True)
    status = models.CharField(max_length=50, default='Waiting', choices=[
        ('Waiting', 'Waiting'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'), 
        ])
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='layanan_adminp')
    hasil_test = models.TextField(null=True, blank=True)
    hasil_file = models.FileField(upload_to='static/layanan_hasil_files/', null=True, blank=True)
    hasil_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.mhs} - {self.layanan_jenis}"
    

######################## SKRIPSI  ########################################


class SkripsiJudul(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skripsi_judul")
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    date_in = models.DateTimeField(auto_now_add=True)
    judul_1 = models.CharField(max_length=255, verbose_name="Judul 1")
    deskripsi_judul_1 = models.TextField(verbose_name="Deskripsi Judul 1", blank=True, null=True)
    judul_2 = models.CharField(max_length=255, verbose_name="Judul 2", blank=True, null=True)
    deskripsi_judul_2 = models.TextField(verbose_name="Deskripsi Judul 2", blank=True, null=True)
    judul_3 = models.CharField(max_length=255, verbose_name="Judul 3", blank=True, null=True)
    deskripsi_judul_3 = models.TextField(verbose_name="Deskripsi Judul 3", blank=True, null=True)
    penasehat_akademik = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  
    status = models.CharField(max_length=10,  default='Waiting', choices=[
        ('Waiting', 'Waiting'),
        ('Revision', 'Revision'), 
        ('Approved', 'Approved'), 
        ])
    status_ket = models.CharField(max_length=255, verbose_name="status_ket", blank=True, null=True)


######################## PROPOSAL  ########################################

# class SkripsiProposal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_user")
#     tgl_surat = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
#     no_surat = models.ForeignKey(NoSurat, on_delete=models.CASCADE, related_name="proposal_nosurat")
#     mhs1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_mhs1")
#     mhs2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_mhs2")
#     mhs3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_mhs3")
#     mhs4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_mhs4")
#     mhs5 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_mhs5")
#     prodi = models.ForeignKey(Prodi, on_delete=models.CASCADE, related_name="proposal_prodi")
#     judul = models.TextField(verbose_name="Judul", blank=False, null=False)
#     seminar_waktu = models.DateTimeField(blank=False, null=False)
#     seminar_tempat = models.CharField(max_length=255, blank=False, null=False)
#     seminar_link = models.CharField(max_length=255, blank=False, null=False)
#     pbb1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_pbb1")
#     pbb1_nama = models.CharField(max_length=255, blank=False, null=False)
#     pbb2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_pbb2", blank=True, null=True)
#     pbb2_nama = models.CharField(max_length=255, blank=True, null=True)
#     pgj1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_pgj1", blank=True, null=True)
#     pgj1_nama = models.CharField(max_length=255, blank=True, null=True)
#     pgj2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_pgj2", blank=True, null=True)
#     pgj2_nama = models.CharField(max_length=255, blank=True, null=True)
#     pgj2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposal_pgj2", blank=True, null=True)
#     pgj2_nama = models.CharField(max_length=255, blank=True, null=True)
#     ttd_status = models.BooleanField()