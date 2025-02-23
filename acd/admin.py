from django.contrib import admin
from .models import UserMhs, UserProdi, UserDosen, UserFakultas
from .models import LayananJenis, Layanan
from .models import Prodi, Jurusan, ProdiPejabat, JurusanPejabat
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

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

admin.site.register(UserMhs)


admin.site.register(Prodi)
admin.site.register(Jurusan)
admin.site.register(ProdiPejabat)
admin.site.register(JurusanPejabat)
admin.site.register(LayananJenis)