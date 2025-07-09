import difflib
from .models import SkripsiJudul

def cek_kemiripan_judul(id, input_judul, threshold=0.01):
    judul_eksisting = []

    data_skripsi = SkripsiJudul.objects.filter(id=id).first()

    for skripsi in SkripsiJudul.objects.exclude(id=id).exclude(date_in__gte=data_skripsi.date_in):
        judul_eksisting.extend([
            {'judul': skripsi.judul1, 'mhs': skripsi.mhs} if skripsi.judul1 else None,
            {'judul': skripsi.judul2, 'mhs': skripsi.mhs} if skripsi.judul2 else None,
            {'judul': skripsi.judul3, 'mhs': skripsi.mhs} if skripsi.judul3 else None,
        ])

    hasil = []
    for item in filter(None, judul_eksisting):  # abaikan yang kosong/null
        similarity = difflib.SequenceMatcher(None, input_judul.lower(), item['judul'].lower()).ratio()
        if similarity >= threshold:
            hasil.append({
                'judul': item['judul'],
                'kemiripan': round(similarity * 100, 2),
                'mhs': item['mhs']
            })

    hasil.sort(key=lambda x: x['kemiripan'], reverse=True)
    return hasil

