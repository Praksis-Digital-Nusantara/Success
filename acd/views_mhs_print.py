from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from .decorators_mhs import check_usermhs
from .decorators_mhs import mahasiswa_required

from aam.context_processors import web_name

from .print_utils import tanggal_indo, draw_kop_surat, dl

from .models import SkripsiJudul, JurusanPejabat, ProdiPejabat

import textwrap


@mahasiswa_required
@check_usermhs
def print_pengajuanjudul(request):
    context = web_name(request)  
    usermhs = request.usermhs  
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="kop_surat.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat(p, context, usermhs)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5
    p.drawCentredString(text_x, pos_y, "USULAN JUDUL TUGAS AKHIR")


    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset
        canvas.drawString(posd_x, pos_y, label)  
        canvas.drawString(180, pos_y, ":")  
        canvas.drawString(200, pos_y, value)        
        return pos_y

    pos_y = draw_aligned_text(p, "Nama Mahasiswa", request.user.first_name, 25)
    pos_y = draw_aligned_text(p, "NIM", request.user.username, 12)
    pos_y = draw_aligned_text(p, "Jurusan", usermhs.prodi.jurusan.nama_jurusan, 12)
    pos_y = draw_aligned_text(p, "Program Studi", usermhs.prodi.nama_prodi, 12)
    pos_y = draw_aligned_text(p, "Tempat/ Tgl. Lahir", usermhs.tempat_lahir + ", "+tanggal_indo(usermhs.tgl_lahir), 12)


    pos_y -= dl(p, posd_x, pos_y, 25, "Judul yang diajukan", True, 'L')

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x, pos_y, label)
        wrapped_text = textwrap.wrap(value, width=100)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 20, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 20, pos_y, line)
        return pos_y  
    
    judul = SkripsiJudul.objects.get(user=request.user)
    print (judul)

    pos_y = draw_aligned_text(p, "1.", judul.judul_1,  15)   
    pos_y = draw_aligned_text(p, "2.", judul.judul_2,  15)   
    pos_y = draw_aligned_text(p, "3.", judul.judul_3,  15)

    # TEMPAT TANDA TANGAN
    pos_y -= dl(p, A4[0] - 250, pos_y, 20, "Makassar, ....................", False, 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "Disetujui Oleh", False, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "Diajukan Oleh", False, 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "Penasehat Akademik,", False, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "Mahasiswa Ybs,", False, 'L')

    pos_y -= dl(p, posd_x, pos_y, 60, usermhs.penasehat_akademik.first_name, False, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, request.user.first_name, False, 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "NIP." + usermhs.penasehat_akademik.username, False, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "NIM." + request.user.username, False, 'L')

    
    ################################### BATAS #########################
    pos_y -= dl(p, A4[0] / 2, pos_y, 30, "PERSETUJUAN PIMPINAN PROGRAM STUDI DAN JURUSAN", True, 'C')
    pos_y -= dl(p, posd_x, pos_y, 20, "Judul yang disetujui:", True, 'L')
    
    pos_y -= 15
    p.setFont("Times-Roman", 12)
    for _ in range(4):
        p.drawString(posd_x, pos_y, "......................................................................................................................................................")
        pos_y -= 15

    pos_y -= dl(p, posd_x, pos_y, 20, "Pembimbing yang ditunjuk:", True, 'L')
    pos_y -= dl(p, posd_x, pos_y, 20, "1. .............................", False, 'L')
    pos_y -= dl(p, posd_x, pos_y, 20, "2. .............................", False, 'L')

    pos_y -= dl(p, posd_x, pos_y, 20, "Mengetahui,", False, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "Ketua Program Studi", False, 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "Ketua Jurusan " + usermhs.prodi.jurusan.nama_jurusan, False, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, usermhs.prodi.nama_prodi, False, 'L')

    jurusanP = JurusanPejabat.objects.get(jurusan=usermhs.prodi.jurusan)
    prodiP = ProdiPejabat.objects.get(prodi=usermhs.prodi)

    pos_y -= dl(p, posd_x, pos_y, 60, jurusanP.pejabat.first_name, True, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, prodiP.pejabat.first_name, True, 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "NIP."+jurusanP.pejabat.username, True, 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "NIP."+prodiP.pejabat.username, True, 'L')




    # Menutup halaman dan menyimpan PDF
    p.setTitle("Cetak Usulan Judul "+request.user.username)
    p.showPage()
    p.save()

    return response