from django.contrib import admin
from .models import UserMhs, UserProdi, UserDosen, UserFakultas
from .models import LayananJenis, Layanan
from .models import Prodi, Jurusan, Pejabat
from .models import KodeSurat, SkripsiJudul
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin
from .admin_resources import UserMhsResource, UserDsnResource

class UserMhsImport(ImportExportModelAdmin):
    resource_class = UserMhsResource  # Import User Mahasiswa

class UserDsnImport(ImportExportModelAdmin):
    resource_class = UserDsnResource  # Import User DOSEN


admin.site.register(UserMhs, UserMhsImport)
admin.site.register(UserDosen, UserDsnImport)


@admin.register(Layanan)
class LayananAdmin(admin.ModelAdmin):
    list_display = ('date_in', 'mhs', 'prodi', 'layanan_jenis', 'status', 'adminp')  # Kolom yang ditampilkan
    list_filter = ('prodi', 'layanan_jenis', 'status')  # Filter berdasarkan kolom
    search_fields = ('mhs', 'layanan_jenis')  # Pencarian
    ordering = ('-date_in',)  # Urutan data


class MhsInline(admin.StackedInline):
    model = UserMhs
    fk_name = 'nim'
    can_delete = False
    verbose_name_plural = 'AccountsMhs'

class DosenInline(admin.StackedInline):
    model = UserDosen
    can_delete = False
    verbose_name_plural = 'AccountsDosen'

class ProdiInline(admin.StackedInline):
    model = UserProdi
    can_delete = False
    verbose_name_plural = 'AccountsProdi'

class FakultasInline(admin.StackedInline):
    model = UserFakultas
    can_delete = False
    verbose_name_plural = 'AccountsFakultas'

class CustomUserAdmin(UserAdmin):
    inlines = (MhsInline, DosenInline, ProdiInline, FakultasInline)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(KodeSurat)
admin.site.register(Prodi)
admin.site.register(Jurusan)
admin.site.register(Pejabat)
admin.site.register(LayananJenis)
admin.site.register(SkripsiJudul)