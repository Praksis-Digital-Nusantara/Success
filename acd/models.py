from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from django.db import models
from django.conf import settings
from django.utils import timezone

########################### TABEL USER MASTER #####################################
User.add_to_class("__str__", lambda self: f"{self.username} - {self.first_name}")


########################### JURUSAN #####################################

class Jurusan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_jurusan = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(max_length=10, default='Aktif', choices=[
        ('Aktif', 'Aktif'),
        ('NonAktif', 'NonAktif'), 
        ])
    kode_surat = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nama_jurusan}"



########################### PROGRAM STUDI #####################################

    
class Prodi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

   

########################### MANAGE USERS #####################################

def rename_photo_dsn(instance, filename):
    ext = filename.split('.')[-1]
    nip = instance.nip
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')  # format waktu: 20250427153520
    new_filename = f"{nip}_{timestamp}.{ext}"
    return os.path.join('img_profile/dsn/', new_filename)

   
class UserDosen(models.Model):
    nip = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username", primary_key=True)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    status_kepegawaian = models.CharField(max_length=15, choices=[
                    ('PNS', 'PNS'),
                    ('CPNS', 'CPNS'),
                    ('PPPK', 'PPPK'),
                    ('NON-ASN', 'NON-ASN'),
                ],null=True, blank=True)
    telp = models.CharField(max_length=15)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    tempat_lahir = models.CharField(max_length=50, null=True, blank=True)
    tgl_lahir = models.DateField(null=True, blank=True)
    nidn = models.CharField(max_length=20, null=True, blank=True)
    pangkat = models.CharField(max_length=30, choices=[
                    ('Penata Muda Tingkat I', 'Penata Muda Tingkat I'),
                    ('Penata', 'Penata'),
                    ('Penata Tingkat I', 'Penata Tingkat I'),
                    ('Pembina', 'Pembina'),
                    ('Pembina Utama Muda', 'Pembina Utama Muda'),
                    ('Pembina Utama Madya', 'Pembina Utama Madya'),
                    ('Pembina Utama', 'Pembina Utama'),
                ],null=True, blank=True)
    golongan = models.CharField(max_length=10, choices=[
                    ('III/b', 'III/b'),
                    ('III/c', 'III/c'),
                    ('III/d', 'III/d'),
                    ('IV/a', 'IV/a'),
                    ('IV/b', 'IV/b'),
                    ('IV/c', 'IV/c'),
                    ('IV/d', 'IV/d'),
                    ('IV/e', 'IV/e'),
                ],null=True, blank=True)
    jafung = models.CharField(max_length=15, choices=[
                    ('Asisten Ahli', 'Asisten Ahli'),
                    ('Lektor', 'Lektor'),
                    ('Lektor Kepala', 'Lektor Kepala'),
                    ('Guru Besar', 'Guru Besar'),
                ],null=True, blank=True)
    bidang_keahlian = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to=rename_photo_dsn)

    def save(self, *args, **kwargs):
        try:
            old_instance = UserDosen.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, old_instance.photo.name)
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)
        except UserDosen.DoesNotExist:
            pass  # ini data baru, jadi tidak perlu hapus apa-apa

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nip}"
    


def rename_photo_mhs(instance, filename):
    ext = filename.split('.')[-1]
    nim = instance.nim
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')  # format waktu: 20250427153520
    new_filename = f"{nim}_{timestamp}.{ext}"
    return os.path.join('img_profile/mhs/', new_filename)  

class UserMhs(models.Model):
    nim = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username", primary_key=True)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True, related_name="usermhs_prodi")
    telp = models.CharField(max_length=15)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    tempat_lahir = models.CharField(max_length=50, null=True, blank=True)
    tgl_lahir = models.DateField(null=True, blank=True)
    tgl_masuk = models.DateField(null=True, blank=True)
    alamat = models.CharField(max_length=255, null=True, blank=True)
    penasehat_akademik = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, null=True, blank=True, related_name="usermhs_pa") 
    photo = models.ImageField(upload_to=rename_photo_mhs)

    def save(self, *args, **kwargs):
        try:
            old_instance = UserMhs.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, old_instance.photo.name)
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)
        except UserMhs.DoesNotExist:
            pass  # ini data baru, jadi tidak perlu hapus apa-apa

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nim}"
    

def rename_photo_admin(instance, filename):
    ext = filename.split('.')[-1]
    username = instance.username
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')  # format waktu: 20250427153520
    new_filename = f"{username}_{timestamp}.{ext}"
    return os.path.join('img_profile/admin/', new_filename)  


class UserProdi(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username", primary_key=True)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    telp = models.CharField(max_length=15)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    photo = models.ImageField(upload_to=rename_photo_admin)

    def save(self, *args, **kwargs):
        try:
            old_instance = UserProdi.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, old_instance.photo.name)
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)
        except UserProdi.DoesNotExist:
            pass  # ini data baru, jadi tidak perlu hapus apa-apa

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"
    


class UserFakultas(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username", primary_key=True)
    telp = models.CharField(max_length=15)
    gender = models.CharField(max_length=15, choices=[
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ])
    photo = models.ImageField(upload_to=rename_photo_admin)
    def save(self, *args, **kwargs):
        try:
            old_instance = UserProdi.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, old_instance.photo.name)
                if os.path.isfile(old_photo_path):
                    os.remove(old_photo_path)
        except UserProdi.DoesNotExist:
            pass  # ini data baru, jadi tidak perlu hapus apa-apa

        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.username}"
    


########################## SET PEJABAT  #####################################

class Pejabat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jabatan = models.CharField(max_length=30, choices=[
                    ('Dekan', 'Dekan'),
                    ('Wakil Dekan I', 'Wakil Dekan I'),
                    ('Wakil Dekan II', 'Wakil Dekan II'),
                    ('Wakil Dekan III', 'Wakil Dekan III'),
                    ('Wakil Dekan IV', 'Wakil Dekan IV'),
                    ('Penjaminan Mutu', 'Penjaminan Mutu'),
                    ('Kepala Bagian Umum', 'Kepala Bagian Umum'),
                    ('Ketua Jurusan', 'Ketua Jurusan'),
                    ('Sekretaris Jurusan', 'Sekretaris Jurusan'),
                    ('Ketua Prodi', 'Ketua Prodi'),
                    ('Sekretaris Prodi', 'Sekretaris Prodi'),
                ])
    jabatan_level = models.CharField(max_length=15, choices=[
                    ('Fakultas', 'Fakultas'),
                    ('Jurusan', 'Jurusan'),
                    ('Prodi', 'Prodi'),
                ])
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True, related_name="pejabat_prodi")
    jurusan = models.ForeignKey(Jurusan, on_delete=models.SET_NULL, null=True, blank=True, related_name="pejabat_jurusan")
    pejabat = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, null=True, related_name="pejabat_pejabat")
    tgl_mulai = models.DateField(blank=False, null=False)
    tgl_selesai = models.DateField(blank=False, null=False)
    label = models.CharField(max_length=255, blank=True, null=True)
    plt = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.jabatan} - {self.pejabat}"
   


#########################  NOMOR SURAT #####################################

class NoSurat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="adminp_surat")
    jurusan = models.ForeignKey(Jurusan, on_delete=models.SET_NULL, null=True, blank=True)
    tahun = models.CharField(max_length=5, blank=False, null=False)
    nomor = models.IntegerField(blank=False, null=False)
    perihal = models.CharField(max_length=255, blank=False, null=False)
    tujuan = models.CharField(max_length=255, blank=False, null=False)

class NoSuratFakultas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="nosuratf_admin")
    tahun = models.CharField(max_length=5, blank=False, null=False)
    nomor = models.IntegerField(blank=False, null=False)
    perihal = models.CharField(max_length=255, blank=False, null=False)
    tujuan = models.CharField(max_length=255, blank=False, null=False)
    kode = models.CharField(max_length=50, blank=False, null=False)

class KodeSurat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jenis = models.CharField(max_length=100, blank=False, null=False)
    kode = models.CharField(max_length=50, blank=False, null=False)
    def __str__(self):
        return f"{self.jenis} - {self.kode}"

#########################  TTD QRCODE #####################################

class TTDProdi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="ttdqr_admin")
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    perihal = models.CharField(max_length=255, blank=True, null=True)
    tujuan = models.CharField(max_length=255, blank=True, null=True)
    ttd_jabatan = models.CharField(max_length=255, blank=True, null=True)
    ttd_user = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, null=True, blank=True, related_name="ttdqr_ttduser")


######################## LAYANAN ########################################
    
class LayananJenis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    nama_layanan = models.CharField(max_length=255)
    prasyarat_layanan = models.TextField()
    level_proses = models.CharField(max_length=15, choices=[
                    ('Fakultas', 'Fakultas'),
                    ('Jurusan', 'Jurusan'),
                    ('Prodi', 'Prodi'),
                ])
    def __str__(self):
        return f"{self.nama_layanan}"


def rename_layanan_file(instance, filename):
    ext = filename.split('.')[-1]
    mhs = instance.mhs
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')  # format waktu: 20250427153520
    new_filename = f"{mhs}_{timestamp}.{ext}"
    return os.path.join('layanan/masuk/', new_filename)
def rename_layanan_file_balas(instance, filename):
    ext = filename.split('.')[-1]
    mhs = instance.mhs
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')  # format waktu: 20250427153520
    new_filename = f"B_{mhs}_{timestamp}.{ext}"
    return os.path.join('layanan/balas/', new_filename)
    
class Layanan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, null=True, blank=True)
    layanan_jenis = models.ForeignKey(LayananJenis, on_delete=models.SET_NULL, null=True, blank=True)
    layanan_isi = models.TextField()
    layanan_file = models.FileField(upload_to=rename_layanan_file, null=True, blank=True)
    status = models.CharField(max_length=50, default='Waiting')
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='layanan_adminp')
    hasil_test = models.TextField(null=True, blank=True)
    hasil_file = models.FileField(upload_to=rename_layanan_file_balas, null=True, blank=True)
    hasil_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.mhs} - {self.layanan_jenis}"
    

######################## SKRIPSI  ########################################


class SkripsiJudul(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mhs = models.ForeignKey(UserMhs, on_delete=models.CASCADE, related_name="skripsi_judul")
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    date_in = models.DateTimeField(auto_now_add=True)
    judul1 = models.CharField(max_length=255, blank=True, null=True)
    judul1_masalah = models.TextField(blank=True, null=True)
    judul1_solusi = models.TextField(blank=True, null=True)
    judul1_j1 = models.CharField(max_length=255, blank=True, null=True)
    judul1_j1l = models.CharField(max_length=255, blank=True, null=True)
    judul1_j2 = models.CharField(max_length=255, blank=True, null=True)
    judul1_j2l = models.CharField(max_length=255, blank=True, null=True)
    judul1_j3 = models.CharField(max_length=255, blank=True, null=True)
    judul1_j3l = models.CharField(max_length=255, blank=True, null=True)
    judul2 = models.CharField(max_length=255, blank=True, null=True)
    judul2_masalah = models.TextField(blank=True, null=True)
    judul2_solusi = models.TextField(blank=True, null=True)
    judul2_j1 = models.CharField(max_length=255, blank=True, null=True)
    judul2_j1l = models.CharField(max_length=255, blank=True, null=True)
    judul2_j2 = models.CharField(max_length=255, blank=True, null=True)
    judul2_j2l = models.CharField(max_length=255, blank=True, null=True)
    judul2_j3 = models.CharField(max_length=255, blank=True, null=True)
    judul2_j3l = models.CharField(max_length=255, blank=True, null=True)
    judul3 = models.CharField(max_length=255, blank=True, null=True)
    judul3_masalah = models.TextField(blank=True, null=True)     
    judul3_solusi = models.TextField(blank=True, null=True)
    judul3_j1 = models.CharField(max_length=255, blank=True, null=True)
    judul3_j1l = models.CharField(max_length=255, blank=True, null=True)
    judul3_j2 = models.CharField(max_length=255, blank=True, null=True)
    judul3_j2l = models.CharField(max_length=255, blank=True, null=True)
    judul3_j3 = models.CharField(max_length=255, blank=True, null=True)
    judul3_j3l = models.CharField(max_length=255, blank=True, null=True)     
    status = models.CharField(max_length=15,  default='Waiting', choices=[
        ('Waiting', 'Waiting'),
        ('Revision', 'Revision'), 
        ('Approved', 'Approved'), 
        ])
    status_ket = models.CharField(max_length=255, verbose_name="status_ket", blank=True, null=True)
    judul = models.CharField(max_length=255, blank=True, null=True)     
    pembimbing1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, to_field="nip", related_name="skripsi_pbb1", blank=True, null=True)    
    pembimbing2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, to_field="nip", related_name="skripsi_pbb2", blank=True, null=True)   
    pembimbing2_persetujuan = models.CharField(max_length=50, blank=True, null=True)     
    pembimbing2_komentar = models.CharField(max_length=255, blank=True, null=True)     
    status_sk = models.CharField(max_length=15,  default='-', choices=[
        ('-', '-'),
        ('Pengajuan', 'Pengajuan'), 
        ('Pembaharuan', 'Pembaharuan'), 
        ('Terbit', 'Terbit'), 
        ])
    
    def __str__(self):
        return f"{self.judul}"
    
class chatPA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, to_field="nim", related_name="chatpa_mhs", null=True)
    dsn = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, to_field="nip", related_name="chatpa_dsn", null=True)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)


class skPembimbing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    nosurat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="skpbb_mhs", null=True)
    prodi = models.ForeignKey(Prodi, on_delete=models.SET_NULL, null=True, blank=True)
    pembimbing1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, to_field="nip", related_name="skpbb_pbb1", null=True)
    pembimbing2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, to_field="nip", related_name="skpbb_pbb2", null=True)
    judul = models.CharField(max_length=255, blank=True, null=True)    
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="skpbb_pejabatttd", null=True)



###################### PROPOSAL  ########################################


class ProposalNilai(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    aspek1 = models.FloatField(blank=True, null=True)
    aspek2 = models.FloatField(blank=True, null=True)
    aspek3 = models.FloatField(blank=True, null=True)
    aspek4 = models.FloatField(blank=True, null=True)
    aspek5 = models.FloatField(blank=True, null=True)
    aspek6 = models.FloatField(blank=True, null=True)
    nilai_angka = models.FloatField(blank=True, null=True)
    nilai_huruf = models.CharField(max_length=20, blank=True, null=True)
    komentar = models.TextField(blank=True, null=True)


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(UserProdi, on_delete=models.SET_NULL, related_name="proposal_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs_judul = models.ForeignKey(SkripsiJudul, on_delete=models.SET_NULL, related_name="proposal_mhs", blank=True, null=True)
    seminar_tgl = models.DateField(blank=True, null=True)
    seminar_jam = models.TimeField(blank=True, null=True)
    seminar_tempat = models.CharField(max_length=255, blank=True, null=True)
    seminar_link = models.CharField(max_length=255, blank=True, null=True)
    pembimbing1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="proposal_pbb1", blank=True, null=True)
    pembimbing2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="proposal_pbb2", blank=True, null=True)
    penguji1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="proposal_pgj1", blank=True, null=True)
    penguji2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="proposal_pgj2", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, blank=True, null=True)
    nilai1 = models.ForeignKey(ProposalNilai, on_delete=models.SET_NULL, related_name="proposal_nilai1", blank=True, null=True)
    nilai2 = models.ForeignKey(ProposalNilai, on_delete=models.SET_NULL, related_name="proposal_nilai2", blank=True, null=True)
    nilai3 = models.ForeignKey(ProposalNilai, on_delete=models.SET_NULL, related_name="proposal_nilai3", blank=True, null=True)
    nilai4 = models.ForeignKey(ProposalNilai, on_delete=models.SET_NULL, related_name="proposal_nilai4", blank=True, null=True)
    nilai5 = models.ForeignKey(ProposalNilai, on_delete=models.SET_NULL, related_name="proposal_nilai5", blank=True, null=True)
    # syarat untuk proposal
    krs = models.FileField(upload_to='layanan/syaratproposal/', null=True, blank=True)
    khs = models.FileField(upload_to='layanan/syaratproposal/', null=True, blank=True)
    ksm = models.FileField(upload_to='layanan/syaratproposal/', null=True, blank=True)
    persetujuan_proposal = models.FileField(upload_to='layanan/syaratproposal/', null=True, blank=True)
    kartu_seminar = models.FileField(upload_to='layanan/syaratproposal/', null=True, blank=True)
    konsultasi_skripsi = models.FileField(upload_to='layanan/syaratproposal/', null=True, blank=True)


##########################  SK PENGUJI  ########################################
class skPenguji(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    nosurat = models.CharField(max_length=50, blank=True, null=True)
    proposal = models.ForeignKey(Proposal, on_delete=models.SET_NULL, related_name="skpgj_proposal", null=True) 
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="skpgj_pejabatttd", null=True)



##########################  PENELITIAN  ########################################
class IzinPenelitian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(UserFakultas, on_delete=models.SET_NULL, related_name="izinpenelitian_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs_judul = models.ForeignKey(SkripsiJudul, on_delete=models.SET_NULL, related_name="izinpenelitian_mhsjudul", blank=True, null=True)
    lokasi = models.CharField(max_length=255, blank=True, null=True)
    pimpinan = models.CharField(max_length=255, blank=True, null=True)
    pimpinancq = models.CharField(max_length=255, blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, blank=True, null=True)



##########################  HASIL  ########################################

class HasilNilai(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    aspek1 = models.FloatField(blank=True, null=True)
    aspek2 = models.FloatField(blank=True, null=True)
    aspek3 = models.FloatField(blank=True, null=True)
    aspek4 = models.FloatField(blank=True, null=True)
    aspek5 = models.FloatField(blank=True, null=True)
    aspek6 = models.FloatField(blank=True, null=True)
    nilai_angka = models.FloatField(blank=True, null=True)
    nilai_huruf = models.CharField(max_length=20, blank=True, null=True)
    komentar = models.TextField(blank=True, null=True)



class Hasil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(UserProdi, on_delete=models.SET_NULL, related_name="hasil_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs_judul = models.ForeignKey(SkripsiJudul, on_delete=models.SET_NULL, related_name="hasil_mhs", blank=True, null=True)
    seminar_tgl = models.DateField(blank=True, null=True)
    seminar_jam = models.TimeField(blank=True, null=True)
    seminar_tempat = models.CharField(max_length=255, blank=False, null=False)
    seminar_link = models.CharField(max_length=255, blank=True, null=True)
    pembimbing1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="hasil_pbb1", blank=True, null=True)
    pembimbing2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="hasil_pbb2", blank=True, null=True)
    penguji1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="hasil_pgj1", blank=True, null=True)
    penguji2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="hasil_pgj2", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, blank=True, null=True)
    nilai1 = models.ForeignKey(HasilNilai, on_delete=models.SET_NULL, related_name="hasil_nilai1", blank=True, null=True)
    nilai2 = models.ForeignKey(HasilNilai, on_delete=models.SET_NULL, related_name="hasil_nilai2", blank=True, null=True)
    nilai3 = models.ForeignKey(HasilNilai, on_delete=models.SET_NULL, related_name="hasil_nilai3", blank=True, null=True)
    nilai4 = models.ForeignKey(HasilNilai, on_delete=models.SET_NULL, related_name="hasil_nilai4", blank=True, null=True)
    nilai5 = models.ForeignKey(HasilNilai, on_delete=models.SET_NULL, related_name="hasil_nilai5", blank=True, null=True)
    # syarat untuk hasil
    krs = models.FileField(upload_to='layanan/syarathasil/', null=True, blank=True)
    ksm = models.FileField(upload_to='layanan/syarathasil/', null=True, blank=True)
    kartu_kontrol_seminar = models.FileField(upload_to='layanan/syarathasil/', null=True, blank=True)
    buku_konsultasi = models.FileField(upload_to='layanan/syarathasil/', null=True, blank=True)
    persetujuan_hasil = models.FileField(upload_to='layanan/syarathasil/', null=True, blank=True)
    transkrip = models.FileField(upload_to='layanan/syarathasil/', null=True, blank=True)
    suket_selesai_meneliti = models.FileField(upload_to='layanan/syarathasil/', null=True, blank=True)
    
##########################  UJIAN  ########################################

class UjianNilai(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    aspek1 = models.FloatField(blank=True, null=True)
    aspek2 = models.FloatField(blank=True, null=True)
    aspek3 = models.FloatField(blank=True, null=True)
    aspek4 = models.FloatField(blank=True, null=True)
    aspek5 = models.FloatField(blank=True, null=True)
    aspek6 = models.FloatField(blank=True, null=True)
    nilai_angka = models.FloatField(blank=True, null=True)
    nilai_huruf = models.CharField(max_length=20, blank=True, null=True)
    komentar = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nilai_angka}"



class Ujian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(UserFakultas, on_delete=models.SET_NULL, related_name="ujian_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs_judul = models.ForeignKey(SkripsiJudul, on_delete=models.SET_NULL, related_name="ujian_mhs", blank=True, null=True)
    ujian_tgl = models.DateField(blank=True, null=True)
    ujian_jam = models.TimeField(blank=True, null=True)
    ujian_tempat = models.CharField(max_length=255, blank=False, null=False)
    ujian_link = models.CharField(max_length=255, blank=True, null=True)
    pembimbing1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="ujian_pbb1", blank=True, null=True)
    pembimbing2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="ujian_pbb2", blank=True, null=True)
    penguji1 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="ujian_pgj1", blank=True, null=True)
    penguji2 = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="ujian_pgj2", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')
    kaprodi = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, blank=True, null=True)
    dekan = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="ujian_dekan", blank=True, null=True)
    wd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL,  related_name="ujian_wd1", blank=True, null=True)
    nilai1 = models.ForeignKey(UjianNilai, on_delete=models.SET_NULL, related_name="ujian_nilai1", blank=True, null=True)
    nilai2 = models.ForeignKey(UjianNilai, on_delete=models.SET_NULL, related_name="ujian_nilai2", blank=True, null=True)
    nilai3 = models.ForeignKey(UjianNilai, on_delete=models.SET_NULL, related_name="ujian_nilai3", blank=True, null=True)
    nilai4 = models.ForeignKey(UjianNilai, on_delete=models.SET_NULL, related_name="ujian_nilai4", blank=True, null=True)
    nilai5 = models.ForeignKey(UjianNilai, on_delete=models.SET_NULL, related_name="ujian_nilai5", blank=True, null=True)
    nilai6 = models.ForeignKey(UjianNilai, on_delete=models.SET_NULL, related_name="ujian_nilai6", blank=True, null=True)
    # syarat untuk ujian
    persetujuan_ujian = models.FileField(upload_to='layanan/syaratujian/', null=True, blank=True)
    transkrip = models.FileField(upload_to='layanan/syaratujian/', null=True, blank=True)
    ijaza_terakhir = models.FileField(upload_to='layanan/syaratujian/', null=True, blank=True)
    krs_berjalan = models.FileField(upload_to='layanan/syaratujian/', null=True, blank=True)
    rekomendasi_akademik = models.FileField(upload_to='layanan/syaratujian/', null=True, blank=True)


class Yudisium(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    ujian = models.ForeignKey(Ujian, on_delete=models.SET_NULL, related_name="yudisium_ujian", null=True)
    ipk = models.FloatField(blank=True, null=True)
    kualifikasi = models.CharField(max_length=20, blank=True, null=True) 
    catatan = models.TextField(blank=True, null=True) 
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="yudisium_ttd", blank=True, null=True)


#################################### SURAT LAINNYA ####################################

class SuketBebasKuliah(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sbk_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="sbk_mhs", blank=True, null=True)
    sks_lulus = models.IntegerField(blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="sbk_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')

class SuketBebasPlagiasi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sbp_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="sbp_mhs", blank=True, null=True)
    nilai_plagiasi = models.IntegerField(blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="sbp_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')

class SuketAktifKuliah(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sak_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="sak_mhs", blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    tahun_akademik = models.CharField(max_length=20, blank=True, null=True)
    ortu_nama = models.CharField(max_length=50, blank=True, null=True)
    ortu_nip = models.CharField(max_length=30, blank=True, null=True)
    ortu_gol = models.CharField(max_length=30, blank=True, null=True)
    ortu_pekerjaan = models.CharField(max_length=100, blank=True, null=True)
    ortu_instansi = models.CharField(max_length=100, blank=True, null=True)
    ortu_alamat = models.CharField(max_length=255, blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="sak_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')

class SuketBerkelakuanBaik(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="skb_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="skb_mhs", blank=True, null=True)
    tujuan = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    tahun_akademik = models.CharField(max_length=20, blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="skb_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')

class SuketIzinObservasi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sio_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="sio_mhs", blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    tahun_akademik = models.CharField(max_length=20, blank=True, null=True)
    perihal = models.CharField(max_length=255, blank=True, null=True)
    tujuan = models.CharField(max_length=100, blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="sio_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')


class SuketRekomendasi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="srk_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="srk_mhs", blank=True, null=True)
    perihal = models.TextField(blank=True, null=True)
    alasan_rekomendasi = models.TextField(blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="srk_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')

class SuketIzinLab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sil_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="sil_mhs", blank=True, null=True)
    judul = models.ForeignKey(SkripsiJudul, on_delete=models.SET_NULL, related_name="sil_judul", blank=True, null=True)
    lab = models.TextField(blank=True, null=True)
    waktu_mulai = models.DateField(blank=True, null=True)
    waktu_selesai = models.DateField(blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="sil_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')


class SuratTugas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_in = models.DateTimeField(auto_now_add=True)
    adminp = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="st_admin", blank=True, null=True)
    no_surat = models.CharField(max_length=50, blank=True, null=True)
    nama_kegiatan = models.TextField(blank=True, null=True)
    tgl_mulai = models.DateField(blank=True, null=True)
    tgl_selesai = models.DateField(blank=True, null=True)
    jam = models.TimeField(blank=True, null=True)
    tempat = models.CharField(max_length=255, blank=True, null=True)
    ttd = models.ForeignKey(Pejabat, on_delete=models.SET_NULL, related_name="st_ttd", blank=True, null=True)
    ttd_status = models.CharField(max_length=20, default='QRcode')

class SuratTugas_NamaDosen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    urut = models.IntegerField(blank=True, null=True)
    surat = models.ForeignKey(SuratTugas, on_delete=models.SET_NULL, related_name="std_surat", blank=True, null=True) 
    dosen = models.ForeignKey(UserDosen, on_delete=models.SET_NULL, related_name="std_dosen", blank=True, null=True) 
    jabatan = models.CharField(max_length=255, blank=True, null=True)

class SuratTugas_NamaMhs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    urut = models.IntegerField(blank=True, null=True)
    surat = models.ForeignKey(SuratTugas, on_delete=models.SET_NULL, related_name="stm_surat", blank=True, null=True) 
    mhs = models.ForeignKey(UserMhs, on_delete=models.SET_NULL, related_name="stm_mhs", blank=True, null=True) 
    jabatan = models.CharField(max_length=255, blank=True, null=True)