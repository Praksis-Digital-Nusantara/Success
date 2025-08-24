from .models import Pejabat, UserDosen
from django.utils import timezone

def pejabat_aktif(request):
    if not request.user.is_authenticated:
        return {}

    if request.user.last_name == 'Dosen':
        try:
            userC = UserDosen.objects.get(nip=request.user)
            is_pejabat_aktif = Pejabat.objects.filter(
                pejabat=userC,
                tgl_mulai__lte=timezone.now(),
                tgl_selesai__gte=timezone.now()
            ).exists()
            return {'is_pejabat_aktif': is_pejabat_aktif}
        except UserDosen.DoesNotExist:
            return {}
    
    return {}
